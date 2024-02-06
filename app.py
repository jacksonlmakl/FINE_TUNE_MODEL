from flask import Flask, request, jsonify
from similarity import *
from generate_training_data import *
app = Flask(__name__)

@app.route('/create_training_data', methods=['POST'])
def create_training_data():
    content = request.json
    try:
        text = content['text']
        TrainingData(text).save()  # Assuming this function saves the data and doesn't return anything
        return jsonify({"message": "Training data created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/create_model', methods=['POST'])
def create_fine_tuned_model():
    content = request.json
    try:
        text = content['text']
        job_id = create_model(text)
        return jsonify({"job_id": job_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_model_id', methods=['GET'])
def fetch_model_id():
    job_id = request.args.get('job_id')
    try:
        model_id = get_model_id(job_id)
        return jsonify({"model_id": model_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/use_model', methods=['POST'])
def use_fine_tuned_model():
    content = request.json
    try:
        model_id = content['model_id']
        text = content['text']
        response = use_model(model_id, text)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
