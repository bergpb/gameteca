from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'teste'

# sem os padrões da oo, pelo menos a maioria deles
class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console
        
game_1 = Game('Super Mario', 'Action', 'SNES')
game_2 = Game('Pokemon Gold', 'RPG', 'GBA')
game_3 = Game('Mortal Kombat', 'Fight', 'SNES')
lista = [game_1, game_2, game_3]

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', tab_name="Login",
                            next=next)
    
    
@app.route('/logout', methods=['GET'])
def logout():
    session['user_logged'] = None
    flash('Please login again.', 'is-warning')
    # in url_for pass a name of method to redirect into your route
    return redirect(url_for('login'))
    
    
@app.route('/auth', methods=['POST'])
def auth():
    if 'senha' == request.form['password']:
        session['user_logged'] = request.form['username']
        # pass a class inside a flash message
        flash(request.form['username'] + ' logged.', 'is-success')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('Username or password invalid', 'is-danger')
        return redirect(url_for('login'))
        

@app.route('/')
def index():
    return render_template('list_games.html', title='Games',
                            tab_name="Listing Games", games=lista)


@app.route('/new')
def new():
    if 'user_logged' not in session or session['user_logged'] == None:
        flash('Please login.', 'is-warning')
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
    game = Game(name, category, console)
    lista.append(game)
    return redirect(url_for('index'))
    


app.run(host='0.0.0.0', port=3000, debug=True)