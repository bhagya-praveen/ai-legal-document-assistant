from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pypdf import PdfReader
from google import genai

from config import Config
from database.db import db
from models.document import Document


documents_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/api/documents"
)


@documents_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_document():

    # Get logged-in user's ID
    user_id = get_jwt_identity()

    # Check whether a file was uploaded
    if "file" not in request.files:
        return {
            "message": "No file uploaded"
        }, 400

    file = request.files["file"]

    if file.filename == "":
        return {
            "message": "No file selected"
        }, 400

    # Only allow PDF files
    if not file.filename.lower().endswith(".pdf"):
        return {
            "message": "Only PDF files are allowed"
        }, 400

    try:

        # Read PDF
        reader = PdfReader(file)

        extracted_text = ""

        for page in reader.pages:
            extracted_text += page.extract_text() or ""

        # Make sure PDF contains text
        if not extracted_text.strip():
            return {
                "message": "Could not extract text from this PDF"
            }, 400

        # Save document information to database
        document = Document(
            user_id=int(user_id),
            filename=file.filename,
            extracted_text=extracted_text
        )

        db.session.add(document)
        db.session.commit()

        return {
            "message": "Document uploaded successfully",
            "document": {
                "id": document.id,
                "filename": document.filename,
                "text_length": len(extracted_text)
            }
        }, 201

    except Exception as e:

        db.session.rollback()

        return {
            "message": "Error processing PDF",
            "error": str(e)
        }, 500


@documents_bp.route("/<int:document_id>/ask", methods=["POST"])
@jwt_required()
def ask_question(document_id):

    user_id = get_jwt_identity()

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    question = data.get("question")

    if not question:
        return {
            "message": "Question is required"
        }, 400

    # Find the document belonging to the logged-in user
    document = Document.query.filter_by(
        id=document_id,
        user_id=int(user_id)
    ).first()

    if not document:
        return {
            "message": "Document not found"
        }, 404

    try:

        # Create Gemini client
        client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

        prompt = f"""
You are an AI legal document assistant.

Answer the user's question using ONLY the information
contained in the legal document below.

If the answer cannot be found in the document,
say that the information is not available in the document.

Do not invent facts or legal information.

LEGAL DOCUMENT:
{document.extracted_text}

USER QUESTION:
{question}

Provide a clear and concise answer.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        answer = response.text

        return {
            "message": "Answer generated successfully",
            "document_id": document.id,
            "question": question,
            "answer": answer
        }, 200

    except Exception as e:

        print("AI ERROR:", repr(e))

        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return {
                "message": "The AI service is temporarily unavailable. Please try again in a moment."
            }, 503

        return {
            "message": "AI processing failed. Please try again."
        }, 500