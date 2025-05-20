from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import json, os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'segredo_seguro_aqui'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

USERS_FILE = 'users.json'
DATA_FILE = 'habits.json'


# Modelo de usuário
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    if user_id in get_users():
        return User(user_id)
    return None


def get_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}  # retorna dicionário vazio se for inválido
        except json.JSONDecodeError:
            return {}



def save_user(username, password):
    users = get_users()
    users[username] = password
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)


def load_habits():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_habits(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_user_habits():
    data = load_habits()
    return data.get(current_user.id, [])

def save_user_habits(habits):
    data = load_habits()
    data[current_user.id] = habits
    save_habits(data)



def get_last_days(n=7):
    today = datetime.today()
    return [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in reversed(range(n))]


@app.route('/')
@login_required
def index():
    habits = get_user_habits()
    days = get_last_days()

    for habit in habits:
        habit['progress'] = sum(1 for day in days if day in habit['days'])

    return render_template('index.html', habits=habits, days=days)


@app.route('/add', methods=['POST'])
@login_required
def add():
    habit_name = request.form.get('Habit')
    habits = get_user_habits()
    if habit_name:
        habits.append({"name": habit_name, "days": []})
        save_user_habits(habits)
    return redirect('/')


@app.route('/toggle', methods=['POST'])
@login_required
def toggle():
    habit_name = request.form['habit_name']
    date = request.form['date']
    habits = get_user_habits()

    for habit in habits:
        if habit['name'] == habit_name:
            if date in habit['days']:
                habit['days'].remove(date)
            else:
                habit['days'].append(date)
            break

    save_user_habits(habits)
    return redirect('/')


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    habit_name = request.form['habit_name']
    data = load_habits()
    habits = get_user_habits()
    habits = [h for h in habits if h['name'] != habit_name]
    save_user_habits(habits)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if users.get(username) == password:
            login_user(User(username))
            return redirect('/')
        return "Usuário ou senha inválidos"
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username in users:
            return "Usuário já existe!"
        save_user(username, password)
        login_user(User(username))
        return redirect('/')
    return render_template('register.html')


@app.route('/api/habits')
@login_required
def api_habits():
    habits = get_user_habits()
    return {"habits": habits}



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
