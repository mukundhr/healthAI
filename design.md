# HealthAccess AI - System Design Document

## Executive Summary

HealthAccess AI is a low-bandwidth, multilingual, voice-first healthcare access assistant designed to bridge the gap between complex medical information and underserved communities. The system simplifies medical reports, matches users with government healthcare schemes, and provides audio-based guidance for low-literacy users in rural and semi-urban areas.

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Mobile Web   │    │  WhatsApp    │    │   SMS        │      │
│  │  Interface   │    │  Integration │    │  Fallback    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      API GATEWAY LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  • Authentication  • Rate Limiting  • Request Routing            │
│  • Compression     • Caching        • Load Balancing             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                   DOCUMENT PROCESSING LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Image/PDF    │───▶│  OCR Engine  │───▶│ Text         │      │
│  │ Upload       │    │ (AWS Textract│    │ Extraction   │      │
│  │ Handler      │    │  /Tesseract) │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ Voice Input  │───▶│ Speech-to-   │                           │
│  │ (Optional)   │    │ Text (STT)   │                           │
│  └──────────────┘    └──────────────┘                           │
│                                                                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      AI PROCESSING LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │         Document Classification & Analysis            │       │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐      │       │
│  │  │ Report Type│  │ Key Value  │  │ Medical    │      │       │
│  │  │ Classifier │  │ Extraction │  │ Entity NER │      │       │
│  │  └────────────┘  └────────────┘  └────────────┘      │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              LLM Reasoning Engine                     │       │
│  │         (AWS Bedrock / Claude / Llama)                │       │
│  │  • Medical jargon simplification                       │       │
│  │  • Context-aware explanations                         │       │
│  │  • Personalized guidance generation                   │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │         Retrieval-Augmented Generation (RAG)          │       │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐      │       │
│  │  │ Medical KB │  │ Scheme DB  │  │ Vector     │      │       │
│  │  │ Retrieval  │  │ Matching   │  │ Search     │      │       │
│  │  └────────────┘  └────────────┘  └────────────┘      │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    OUTPUT GENERATION LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Text         │───▶│ Text-to-     │───▶│ Audio        │      │
│  │ Formatter    │    │ Speech (TTS) │    │ Compression  │      │
│  │              │    │ (AWS Polly)  │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │         Multilingual Translation Layer                │       │
│  │  (Telugu, Hindi, Tamil, Kannada, Bengali, etc.)       │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    DATA & STORAGE LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Medical      │    │ Government   │    │ User Profile │      │
│  │ Knowledge    │    │ Scheme       │    │ Database     │      │
│  │ Base         │    │ Database     │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Document     │    │ Audio Cache  │    │ Analytics &  │      │
│  │ Storage (S3) │    │ (Redis)      │    │ Logs         │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Upload → OCR/STT → Document Classification → 
Knowledge Retrieval → LLM Reasoning → Simplification → 
Translation → TTS → Compressed Audio → User
```

### Technology Stack

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

## Key Design Principles

- **Voice-First**: Multilingual audio output for accessibility
- **Low-Bandwidth**: Optimized for poor connectivity areas
- **Privacy-First**: No persistent storage of sensitive medical data
- **Non-Diagnostic**: Provides information, not medical advice
