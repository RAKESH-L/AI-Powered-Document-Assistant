from flask import Blueprint, request, jsonify
from app.service.documentservicesecureapi import process_file_and_answer_question

documentcontroller = Blueprint('documentcontroller', __name__)

@documentcontroller.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and question submission.
    """

    if 'question' not in request.form:
        return jsonify({"error": " question are required"}), 400
    
    if 'file' not in request.files :
        return jsonify({"error": "File  are required"}), 400

    file = request.files['file']
    question = request.form['question']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Process the file and get the answer
        answer = process_file_and_answer_question(file, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
