from flask import Flask, request, render_template, jsonify
from math import sqrt

app = Flask(__name__)

# ✅ Fonction de calcul de distance
def calculate_distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


# ✅ Route HTML
@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template('index.html', result=None)

    if request.method == 'POST':
        try:
            start_point = list(map(int, request.form['apoint'].split(',')[0:2]))
            end_point = list(map(int, request.form['bpoint'].split(',')[0:2]))

            if not start_point or not end_point:
                return render_template('index.html', result="Erreur dans les coordonnées")

            result = calculate_distance(start_point, end_point)

            return render_template('index.html', result=result)

        except Exception:
            return render_template('index.html', result="Erreur de saisie")


# ✅ API
@app.route('/api/distance', methods=['POST'])
def api_distance():
    try:
        start_point = list(map(int, request.json['start_point'].split(',')[0:2]))
        end_point = list(map(int, request.json['end_point'].split(',')[0:2]))

        if not start_point or not end_point:
            return jsonify({"error": "Coordonnées invalides"}), 400

        result = calculate_distance(start_point, end_point)

        return jsonify({
            "distance": result
        })

    except Exception:
        return jsonify({"error": "Erreur de requête"}), 400


if __name__ == '__main__':
    app.run(debug=True)
