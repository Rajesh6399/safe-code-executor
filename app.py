from flask import Flask, request, jsonify
from runner import run_python_code
 
try:
    # Optional: allow browser UI (index.html) to call API from file://
    from flask_cors import CORS
    use_cors = True
except ImportError:
    use_cors = False
 
app = Flask(__name__)
 
if use_cors:
    CORS(app)  # Safe and convenient for local development
 
MAX_CODE_LENGTH = 5000  # Security: avoid huge input
 
@app.route("/", methods=["GET"])
def home():
    return "<h2>Safe Code Executor API is running</h2><p>Send POST /run with JSON {'code': '...'} </p>"
 
@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json(silent=True)
 
    if not data or "code" not in data:
        return jsonify({
            "output": "",
            "errors": "No code provided"
        }), 400
 
    code = data["code"]
 
    if not isinstance(code, str):
        return jsonify({
            "output": "",
            "errors": "Code must be a string"
        }), 400
 
    if len(code) > MAX_CODE_LENGTH:
        return jsonify({
            "output": "",
            "errors": "Code too long. Limit is 5000 characters."
        }), 400
 
    result = run_python_code(code)
 
    return jsonify({
        "output": result.get("output", ""),
        "errors": result.get("errors", "")
    })
 
if __name__ == "__main__":
    app.run(debug=True)
 