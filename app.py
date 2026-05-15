from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.preprocessor import preprocess
from models.root_cause_function import predict_root_cause
from vector_store.vector_search import search_similar_cases   # ✅ FIXED
from models.summarizer import generate_summary
from utils.preprocessor import preprocess
app = Flask(__name__)
CORS(app)

# Alternative: Enable CORS with specific configuration
# CORS(app, resources={
#     r"/*": {
#         "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
#         "methods": ["GET", "POST", "PUT", "DELETE"],
#         "allow_headers": ["Content-Type", "Authorization"]
#     }
# })


@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/preprocess_logs', methods=['POST'])
def preprocess_logs_route():
    """
    Accepts raw logs via POST request and returns structured output.
    JSON format: { "logs": "<your raw log string>" }
    or text/plain body with raw logs directly.
    """
    if request.is_json:
        data = request.get_json()
        raw_logs = data.get("logs", "")
    else:
        raw_logs = request.data.decode("utf-8")

    if not raw_logs.strip():
        return jsonify({"error": "No log data received"}), 400

    cleaned = preprocess(raw_logs)
    return jsonify({"processed_logs": cleaned})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    description = data.get('description')
    # close_notes = data.get('close_notes')
    full_text = description
    # Step 1: Predict root cause using ML
    root_cause = predict_root_cause(full_text)

    # Step 2: Get similar historical tickets
    similar_cases = search_similar_cases(full_text)

    # Step 3: Generate summary using LLM
    summary = generate_summary(full_text, root_cause, similar_cases)

    # Step 4: Return as JSON
    return jsonify({
        'root_cause': root_cause,
        'summary': summary,
        'similar_cases': similar_cases
    })


@app.route('/search', methods=['POST'])
def vector_search_only():
    data = request.get_json()

    
    if not data or 'query' not in data or not data['query']:
        return jsonify({"error": "Missing or empty 'query' field in JSON body"}), 400

    description = data['query']
    similar_cases = search_similar_cases(description)
    return jsonify(similar_cases)

@app.route('/summarize', methods=['POST'])
def summarize_from_cases():
    data = request.json

    if not data or 'query' not in data or 'similar_cases' not in data:
        return jsonify({"error": "Missing 'query' or 'similar_cases' in JSON body"}), 400

    query = data['query']
    similar_cases = data['similar_cases']

    summary = generate_summary(query, root_cause=None, similar_cases=similar_cases)

    return jsonify({
        'summary': summary
    })

@app.route('/feedback', methods=['POST'])
def feedback_update():
    """
    Accepts user feedback on incorrect root cause prediction.
    JSON body should include:
    - description: the full ticket description
    - predicted: the incorrect predicted label
    - true_label: the actual root cause provided by user
    """
    data = request.json
    description = data.get('description')
    predicted = data.get('predicted')
    true_label = data.get('true_label')

    if not description or not predicted or not true_label:
        return jsonify({"error": "Missing one or more required fields: 'description', 'predicted', 'true_label'"}), 400

    try:
        from models.root_cause_function import update_and_verify  # import if not already
        updated_pred, true_class = update_and_verify(description, predicted, true_label)
        return jsonify({
            "message": "Model updated with user feedback",
            "new_prediction": updated_pred,
            "true_label_used": true_class
        })
    except Exception as e:
        return jsonify({"error": f"Model update failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True,port=5001)
