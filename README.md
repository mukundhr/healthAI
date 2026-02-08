# HealthAccess AI

HealthAccess AI is a low-bandwidth, multilingual, voice-first healthcare access assistant designed to bridge the gap between complex medical information and underserved communities. The system simplifies medical reports, matches users with government healthcare schemes, and provides audio-based guidance for low-literacy users in rural and semi-urban areas.

---
### Data Flow

```
User Upload → OCR/STT → Document Classification → 
Knowledge Retrieval → LLM Reasoning → Simplification → 
Translation → TTS → Compressed Audio → User
```
---

## User Flow

### 1. Home - Input Stage
- **Smartphone / User**
- User Selects Language (Telugu, Hindi, Tamil, Kannada, Bengali, etc.)
- Clicks 'Scan Report' Button

### 2. Processing - Analysis Stage
- **Document Scanning**
- Analyzing Medical Text...
- Checking Govt Schemes...

### 3. Result - Output Stage
- Play Audio Explanation
- Health Summary (e.g., Hb Low)
- Scheme Matched: Ayushman Bharat
- Send SMS Action Plan

---

## Key Design Principles

- **Voice-First**: Multilingual audio output for accessibility
- **Low-Bandwidth**: Optimized for poor connectivity areas
- **Privacy-First**: No persistent storage of sensitive medical data
- **Non-Diagnostic**: Provides information, not medical advice

---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **OCR** | AWS Textract / Google Cloud Vision / Tesseract |
| **LLM** | AWS Bedrock (Claude) / Llama 3 / GPT-4 |
| **TTS** | AWS Polly / Google Cloud TTS |
| **STT** | AWS Transcribe / Whisper |
| **Backend** | FastAPI / Flask (Python), AWS Lambda |
| **Storage** | AWS S3, PostgreSQL, FAISS / Pinecone |
| **Frontend** | React / Next.js (PWA), Twilio |
| **Infrastructure** | AWS / Google Cloud, CloudFront |

---

## Features

### Document Upload
- **Multiple Format Support**: PDF, Image documents
- **Mobile Web Interface**: Accessible via smartphones
- **SMS Fallback**: Alternative access method

### Voice-First Experience
- **Multilingual Support**: Telugu, Hindi, Tamil, Kannada, Bengali, and more
- **Text-to-Speech**: Audio explanations for low-literacy users
- **Speech-to-Text**: Voice input for hands-free interaction

### AI-Powered Analysis
- **Document Classification**: Identifies medical report types
- **Medical Entity Extraction**: Key health metrics and parameters
- **LLM Reasoning**: Context-aware medical jargon simplification
- **RAG-Based Retrieval**: Medical knowledge base and scheme matching

### Government Scheme Matching
- **Automatic Eligibility Check**: Matches users with relevant schemes
- **Scheme Database**: Ayushman Bharat and other government programs
- **Action Plan SMS**: Sends personalized recommendations

### Low-Bandwidth Optimization
- **Compressed Audio**: Efficient delivery in poor connectivity
- **Mobile Web PWA**: Progressive Web App for offline capabilities
- **Smart Caching**: Redis-based audio cache for faster delivery

---

## Security & Privacy

- **No Persistent Storage**: Sensitive medical data is not stored permanently
- **Privacy-First Architecture**: Designed for healthcare data protection
- **Secure API Communications**: All API communications are encrypted

---

## Getting Started

### Prerequisites
- Python 3.8+
- AWS Cloud account (for Textract, Polly, S3) or Google Cloud account
- API keys for LLM services (Claude, Llama, or GPT-4)

---

## Acknowledgments

- AWS for cloud services (Textract, Polly, Bedrock, S3)
- Google Cloud for Vision API and Text-to-Speech
- Meta for Llama 3 language model
- Anthropic for Claude
- OpenAI for GPT-4

---

**Built with for making healthcare accessible to everyone**
