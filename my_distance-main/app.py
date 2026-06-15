from flask import Flask, request, render_template, jsonify
from math import sqrt
from datetime import datetime

app = Flask('my_distance')

distances = []

# ✅ Fonction propre pour calculer la distance
def calculate_distance(p1, p2):
    return sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

# ✅ Fonction pour parser les entrées utilisateur
def parse_point(point_str):
    try:
        x, y = map(int, point_str.split(','))
        return (x, y)
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template('index.html', result=None)

    if request.method == 'POST':
        start_point = parse_point(request.form['bpoint'])
        end_point = parse_point(request.form['apoint'])

        if not start_point or not end_point:
            return render_template('index.html', result="Erreur de saisie")

        result_tmp = calculate_distance(start_point, end_point)

        result = {
            'requested_at': datetime.now(),
            'result_distance': result_tmp,
            'start_point': start_point,
            'end_point': end_point
        }

        distances.append(result)

        return render_template('index.html', result=result)

# ✅ API liste
@app.route('/api/distances', methods=['GET'])
def get_distances():
    return jsonify(distances)

# ✅ API calcul
@app.route('/api/distance', methods=['POST'])
def calculate_api():
    if not request.json:
        return {"error": "Invalid input"}, 400

    start_point = parse_point(request.json.get('start_point', ''))
    end_point = parse_point(request.json.get('end_point', ''))

    if not start_point or not end_point:
        return {"error": "Invalid format"}, 400

    result_tmp = calculate_distance(start_point, end_point)

    result = {
        'requested_at': datetime.now(),
        'result_distance': result_tmp,
        'start_point': start_point,
        'end_point': end_point
    }

    return jsonify(result)
