from app import app, db
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory

from app.models.tables import User, Game


@app.route('/')
def index():
    if 'user_id' not in session or session['user_id'] == None:
        flash('Please login.', 'warning')
        return redirect(url_for('login'))
    else:
        list = Game.query.filter_by(user_id = session['user_id']).all()
        return render_template('list.html', title='Games',
                                tab_name="Listing Games", games=list)

@app.route('/login')
def login():
    if 'user_id' in session:
        if session['user_id'] != None:
            return redirect(url_for('index'))
        else:
            next = request.args.get('next')
            return render_template('login.html', tab_name="Login",
                                    next=next)
    else:
        next = request.args.get('next')
        return render_template('login.html', tab_name="Login",
                                next=next)

  
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html', tab_name="Sign Up")

    
@app.route('/signup_data', methods=['POST'])
def signup_data():
    user = User(username=request.form['username'],
                password=request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User signed, please login.', 'success')
    return redirect(url_for('login'))
    
   
@app.route('/auth', methods=['POST'])
def auth():
    user = User.query.filter_by(username = request.form['username']).first()
    if user:
        if user.password == request.form['password']:
            session['user_id'] = user.id
            flash('User {} logged!'.format(user.username), 'success')
            next_page = request.form['next']
            return redirect(next_page)
    else:
        flash('Username or password incorrect.', 'danger')
        return redirect(url_for('login'))
        

@app.route('/admin')
def admin():
    if 'user_id' in session:
        user = User.query.filter_by(id = session['user_id']).first()
        if user.admin == True:
            users = User.query.all()
            return render_template('admin.html', title='Admin',
                                    tab_name="Listing Users", users=users)
    else:
        return render_template('404.html', tab_name="404 error")
        

@app.route('/new', methods=['GET'])
def new():
    if 'user_id' not in session or session['user_id'] == None:
        flash('Please login.', 'warning')
        return redirect(url_for('login', next=url_for('new')))
    else:
        
        return render_template('new.html', title='New Game',
                                tab_name="New Game")
   

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game(name=name, category=category, console=console, user_id=session['user_id'])
    db.session.add(game)
    db.session.commit()
    if 'file' in request.files:
        image = request.files['image']
        load_path = app.config['UPLOAD_PATH']
        image.save('{}/capa_{}.jpg'.format(load_path, game.id))
    return redirect(url_for('index'))
    
    
@app.route('/show/<int:game_id>')
def show(game_id):
    if 'user_id' not in session or session['user_id'] == None:
        flash('Please login.', 'warning')
        return redirect(url_for('login', next=url_for('edit')))
    else:
        game_data = Game.query.filter_by(id = game_id).first()
        if game_data.user_id == session['user_id']:
            return render_template('show.html',  title="Show Game",
                                    tab_name="Show Game", game = game_data)
        else:
            return render_template('404.html', tab_name="404 error")
    

@app.route('/edit/<int:game_id>', methods=['GET'])
def edit(game_id):
    if 'user_id' not in session or session['user_id'] == None:
        flash('Please login.', 'warning')
        return redirect(url_for('login', next=url_for('edit')))
    else:
        game_data = Game.query.filter_by(id = game_id).first()
        if game_data.user_id == session['user_id']:
            return render_template('edit.html', title='Edit Game',
                                    tab_name="Edit Game", game = game_data,
                                    cover_game = 'capa_{}.jpg'.format(game_data.id))
        else:
            return render_template('404.html', tab_name="404 error")


@app.route('/uploads/<filename>', methods=['GET'])
def image(filename):
    return send_from_directory('uploads', filename)


@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game.query.get(request.form['game_id'])
    game.name = name
    game.category = category
    game.console = console
    db.session.commit()
    return redirect(url_for('index'))
    
    
@app.route('/delete/<int:game_id>', methods=['GET'])
def delete(game_id):
    game = Game.query.get(game_id)
    db.session.delete(game)
    db.session.commit()
    flash('Game removed.', 'warning')
    return redirect(url_for('index'))


@app.route('/logout', methods=['GET',])
def logout():
    session['user_id'] = None
    flash('Please login.', 'warning')
    return redirect(url_for('login'))