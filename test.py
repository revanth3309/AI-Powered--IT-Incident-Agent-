from flask import Flask, request, jsonify
from vector_store.vector_search import search_similar_cases
from models.summarizer import generate_summary
app = Flask(__name__)

@app.route('/search', methods=['POST'])
def vector_search_only():
    data = request.get_json()

    # ✅ Validate input
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

if __name__ == "__main__":
    app.run(debug=True)
