from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from model import User, Game, db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# get absolute path from current file and concat
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

app.secret_key = 'teste'

db.init_app(app)

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', tab_name="Login",
                            next=next)
                            
                            
@app.route('/auth', methods=['POST',])
def auth():
    usuario = User.query.filter_by(username = request.form['username']).first()
    print(usuario)
    if usuario:
        if usuario.password == request.form['password']:
            # save username in session
            session['user_logged'] = request.form['username']
            # pass a class inside a flash message
            flash(request.form['username'] + ' logged.', 'green')
            next_page = request.form['next']
            return redirect(next_page)
        else:
            flash('Password invalid', 'red')
            return redirect(url_for('login'))
    else:
        flash('Username invalid', 'red')
        return redirect(url_for('login'))


@app.route('/')
def index():
    lista = Game.query.all()
    return render_template('list_games.html', title='Games',
                            tab_name="Listing Games", games=lista)


@app.route('/new', methods=['GET',])
def new():
    if 'user_logged' not in session or session['user_logged'] == None:
        flash('Please login.', 'red')
        # Save try in user access to redirect to here again after login
        return redirect(url_for('login', next=url_for('new')))
    else:
        
        return render_template('new_game.html', title='New Game',
                                tab_name="New Game")
                                

@app.route('/create', methods=['POST',])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game(name=name, category=category, console=console)
    db.session.add(game)
    db.session.commit()
    # uploading image to server
    image = request.files['image']
    load_path = app.config['UPLOAD_PATH']
    image.save('{}/capa_{}.jpg'.format(load_path, game.id))
    return redirect(url_for('index'))
                                

@app.route('/edit/<int:game_id>', methods=['GET',])
def edit(game_id):
    if 'user_logged' not in session or session['user_logged'] == None:
        flash('Please login.', 'red')
        # Save try in user access to redirect to here again after login
        return redirect(url_for('login', next=url_for('edit')))
    else:
        game = Game.query.filter_by(id = game_id).first()
        return render_template('edit.html', title='Edit Game',
                                tab_name="Edit Game", game = game, cover_game = 'capa_{}.jpg'.format(game.id))
                                
@app.route('/update', methods=['POST',])
def update():
    # update values in bd, retrieve by id and get form values passing into a object
    # or you can pass value into url and update value too (make this???)
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game.query.get(request.form['game_id'])
    game.name = name
    game.category = category
    game.console = console
    db.session.commit()
    return redirect(url_for('index'))
    
    
@app.route('/delete/<int:game_id>', methods=['GET',])
def delete(game_id):
    game = Game.query.get(game_id)
    db.session.delete(game)
    db.session.commit()
    flash('Game removed.', 'orange')
    return redirect(url_for('index'))


@app.route('/logout', methods=['GET',])
def logout():
    session['user_logged'] = None
    flash('Please login again.', 'red')
    # in url_for pass a name of method to redirect into your route
    return redirect(url_for('login'))
    
    
@app.route('/uploads/<filename>', methods=['GET',])
def image(filename):
    return send_from_directory('uploads', filename)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)