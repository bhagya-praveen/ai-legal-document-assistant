# AI Legal Document Assistant

An AI-powered web application that allows users to upload legal PDF documents and ask questions about their contents. The application extracts text from uploaded documents and uses Google's Gemini AI to generate answers based only on the information available in the document.

## Features

* User registration and login
* JWT-based authentication
* Secure password hashing
* PDF document upload
* Text extraction from PDF documents
* Document storage using SQLite
* AI-powered question answering using Google Gemini
* User-specific document access
* Simple web-based frontend
* Error handling for unavailable AI services

## Tech Stack

### Backend

* Python
* Flask
* Flask-JWT-Extended
* Flask-SQLAlchemy
* SQLite

### AI

* Google Gemini API
* Google GenAI Python SDK

### PDF Processing

* pypdf

### Frontend

* HTML
* CSS
* JavaScript

### Configuration

* python-dotenv
* Environment variables for API keys and security secrets

## Project Structure


## Project Structure

* `app.py` — Main Flask application
* `config.py` — Application configuration
* `database/` — Database setup
* `models/` — User and document models
* `routes/` — Authentication and document API routes
* `services/` — AI/document processing services
* `static/` — CSS and JavaScript files
* `templates/` — HTML frontend
* `requirements.txt` — Project dependencies

## How It Works

1. User creates an account and logs in.
2. The user uploads a legal PDF.
3. The application extracts text from the PDF.
4. The user asks a question about the document.
5. The extracted document text and question are sent to Gemini AI.
6. The generated answer is displayed to the user.


## Setup

### 1. Clone the repository


git clone <your-repository-url>
cd ai-legal-document-assistant


### 2. Create a virtual environment


python -m venv venv


Activate it on Windows:


venv\Scripts\activate


### 3. Install dependencies


pip install -r requirements.txt


### 4. Configure environment variables

Create a .env file in the project root:


JWT_SECRET_KEY=your-jwt-secret


GEMINI_API_KEY=your-gemini-api-key


Do not commit the .env file to GitHub.

### 5. Run the application


python app.py


The application will run locally at:


http://127.0.0.1:5000


## Usage

1. Register a new account.
2. Log in using your credentials.
3. Upload a legal PDF document.
4. Enter a question about the document.
5. The application sends the document content and question to Gemini.
6. The generated answer is displayed in the application.

If the requested information cannot be found in the document, the assistant is instructed to indicate that the information is not available rather than inventing an answer.

## Security

* API credentials are stored using environment variables.
* JWT authentication is used to protect API endpoints.
* Passwords are stored using password hashing.
* Users can access only documents associated with their authenticated account.
* .env, database files, test documents, and Python cache files are excluded from version control.

## Limitations

* The application currently processes text-based PDFs.
* Scanned/image-only PDFs may not provide extractable text.
* AI responses depend on the availability and limits of the Gemini API.
* SQLite is used for local development.

## Future Improvements

* Retrieval-Augmented Generation (RAG) with document chunking and embeddings
* Support for larger documents
* Improved document search and retrieval
* PostgreSQL for production deployments
* Docker containerization
* More advanced frontend functionality
* Conversation history
* Deployment to a cloud platform

## Disclaimer

This project is intended for educational and demonstration purposes. It does not provide professional legal advice. AI-generated responses should not be treated as a substitute for advice from a qualified legal professional.
