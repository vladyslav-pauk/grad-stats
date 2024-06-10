from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app)

# Load the dataset
with open('../dataset/student_data_v1.pkl', 'rb') as file:
    data = pickle.load(file)

df = pd.DataFrame(data)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    if query:
        matches = df[df['University'].str.lower().str.contains(query)]
    else:
        matches = df
    matches = sorted(set(matches['University'].str.title()))
    return jsonify(matches)

@app.route('/statistics', methods=['GET'])
def statistics():
    query = request.args.get('query', '').lower()
    if query:
        matches = df[df['University'].str.lower().str.contains(query)]
    else:
        matches = df
    # stats = matches.describe().to_dict()
    # return jsonify(stats)
    matches = matches.drop(columns=['URL', 'Snapshots', 'Department'])
    for col in matches.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            matches[col] = pd.to_datetime(matches[col], unit='ms').dt.strftime('%m/%d/%Y')

    return matches.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)