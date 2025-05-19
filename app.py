from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = 'habits.json'

# Carrega os hábitos do arquivo JSON
def load_habits():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Salva os hábitos no arquivo JSON
def save_habits(habits):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(habits, f, indent=2)

def get_last_days(n=7):
    today = datetime.today()
    return [(today - timedelta(days=1)).strftime('%Y-%m-%d') for i in reversed(range(n))] 

# Página inicial
@app.route('/')
def index():
    habits = load_habits()
    return render_template('index.html', habits=habits)

# Adiciona novo hábito
@app.route('/add', methods=['POST'])
def add():
    habit_name = request.form.get('Habit')
    if habit_name:
        habits = load_habits()
        habits.append({"name": habit_name, "days": []})
        save_habits(habits)
    return redirect('/')

@app.route('/toggle', methods=['POST'])
def toggle():
    habit_name = request.form['habit_name']
    date = request.fprm['date']


    habits = load_habits()
    for habit in habits:
        if habit['name'] == habit_name:
            if date in habit['days']:
                habit['days'].remove(date)
            else:
                habit['days'].append(date)
                break
            save_habits(habits)
            return redirect('/')

# Inicia o servidor Flask
if __name__ == '__main__':
    print("🚀 Servidor rodando em http://127.0.0.1:5000")
    app.run(debug=True)
