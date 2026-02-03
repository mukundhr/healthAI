# Generative AI for Demystifying Legal & Healthcare Documents

An AI-powered assistant designed to simplify and analyze complex legal and healthcare documents such as contract agreements, legal notices, insurance policies, medical reports, and prescriptions. Built with Google Gemini API and an interactive Streamlit interface, it helps individuals, legal professionals, patients, and caregivers better understand critical documents by extracting key details, identifying potential risks, and providing plain-language explanations.

## Features

### Document Upload
- **Multiple Format Support**: PDF, JPEG, PNG, TXT
- **Document Types**: Contracts, legal notices, insurance policies, medical reports, prescriptions, and more
- **Batch Processing**: Upload multiple documents simultaneously

### Advanced OCR Technology
- **Google Cloud Vision API** for accurate text extraction from images
- **Intelligent Fallback**: Pillow + Gemini for maximum reliability
- **Handles Complex Layouts**: Preserves document structure and formatting

### PII Protection
Automatically detects and anonymizes 7 types of Personally Identifiable Information:
- Emails
- Phone numbers
- ID/Aadhaar numbers
- Dates
- Names
- Organizations
- Locations

Privacy-first approach: Real data is restored in outputs after AI processing.

### AI-Powered Document Analysis
- **Automatic Document Type Detection**: Identifies legal vs. healthcare documents
- **Smart Extraction**: Focuses on:
  - Legal clauses and contract terms
  - Medical parameters and health metrics
  - Insurance details and coverage
  - Patient information
- **Context-Aware Analysis**: Uses Gemini for deep understanding

### Contextual Q&A
- **Natural Language Questions**: Ask questions in plain English
- **RAG-Powered Responses**: Retrieval-Augmented Generation for accurate, context-aware answers
- **Semantic Search**: FAISS vector storage for relevant information retrieval

### Simplification & Summarization
- **Plain Language Conversion**: Transforms legal/medical jargon into understandable terms
- **Concise Summaries**: Extracts key points from lengthy documents
- **Structured Outputs**: Organized information presentation

### Risk & Compliance Insights
- **Insurance Analysis**: Identifies coverage gaps
- **Legal Risk Assessment**: Flags potential contractual issues
- **Medical Alerts**: Highlights critical health indicators
- **Deadline Tracking**: Reminds about important dates
- **Compliance Checks**: Ensures regulatory adherence

### Multilingual Support
Translate results into:
- English
- Hindi
- Kannada

### Interactive Web UI
- **Streamlit-based Interface**: User-friendly and responsive
- **Drag & Drop Upload**: Easy document handling
- **Real-time Processing**: Instant analysis results
- **Side-by-Pide Comparison**: Compare document sections

## Technology Stack

- **Google Gemini API**: Core AI model for document analysis
- **Google Cloud Vision API**: OCR for image documents
- **Streamlit**: Web interface framework
- **FAISS**: Vector storage for semantic search
- **Hugging Face CrossEncoder**: Reranking for accurate retrieval
- **Python**: Primary programming language

## Getting Started

### Prerequisites
- Python 3.8+
- Google Cloud account (for Vision API)
- Gemini API key

## Usage Guide

### Uploading Documents
1. Navigate to the upload section
2. Drag and drop or select files (PDF, JPEG, PNG, TXT)
3. Click "Analyze" to process

### Asking Questions
1. Use the chat interface to ask questions
2. Get instant AI-generated answers based on document context
3. Follow-up questions for deeper understanding

### Viewing Analysis
- **Summary Tab**: High-level document overview
- **Detailed View**: Clause-by-clause analysis
- **Risks Tab**: Identified issues and concerns
- **Q&A History**: Previous questions and answers

## Security & Privacy

- **Local Processing**: Documents are processed locally when possible
- **PII Anonymization**: Sensitive information is protected before AI processing
- **No Data Retention**: Uploaded documents are not stored permanently
- **Encrypted Communication**: All API communications are secure

## Acknowledgments

- Google Gemini API for powerful AI capabilities
- Google Cloud Vision for OCR
- Streamlit for the web interface
- Hugging Face for transformer models

---

**Built with for making legal and healthcare documents accessible to everyone**
