
# This file contains the main web application logic, setting up the API endpoint where users will send their queries.
# Explanation:
    # The Flask app runs a simple POST API endpoint (/query) that accepts a JSON query.
    # It calls the search() function from utils.py to retrieve relevant documents.
    # Then, it uses generate_answer() to generate a response based on the retrieved documents.

from flask import Flask, request, jsonify
from utils import search, generate_answer

app = Flask(__name__)


@app.route('/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query')
    relevant_documents = search(user_query)
    answer = generate_answer(user_query, " ".join(relevant_documents))
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)

