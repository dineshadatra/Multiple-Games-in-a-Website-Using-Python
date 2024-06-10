from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_game/<game_name>', methods=['POST'])
def run_game(game_name):
    try:
        subprocess.Popen(['python', f'{game_name}.py'])
        return jsonify({'status': 'success', 'message': f'Game {game_name} is running!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
