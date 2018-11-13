from flask import Flask, render_template, request, redirect, session, flash, url_for
from model import User, Game, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

app.secret_key = 'teste'

db.init_app(app)

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', tab_name="Login",
                            next=next)
    
    
@app.route('/logout', methods=['GET'])
def logout():
    session['user_logged'] = None
    flash('Please login again.', 'red')
    # in url_for pass a name of method to redirect into your route
    return redirect(url_for('login'))
    
    
@app.route('/auth', methods=['POST'])
def auth():
    if 'senha' == request.form['password']:
        session['user_logged'] = request.form['username']
        # pass a class inside a flash message
        flash(request.form['username'] + ' logged.', 'green')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('Username or password invalid', 'red')
        return redirect(url_for('login'))
        

@app.route('/')
def index():
    lista = Game.query.all()
    return render_template('list_games.html', title='Games',
                            tab_name="Listing Games", games=lista)


@app.route('/new')
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
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)