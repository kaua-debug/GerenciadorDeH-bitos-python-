from flask import Flask, render_template, request, redirect
import json
import os

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

# Inicia o servidor Flask
if __name__ == '__main__':
    print("🚀 Servidor rodando em http://127.0.0.1:5000")
    app.run(debug=True)
