# AccessAI

**AccessAI** is a low-bandwidth, multilingual, voice-first healthcare access system designed to help underserved communities understand medical information and navigate public healthcare schemes.

It converts complex medical reports and policy documents into simple, localized, audio-based guidance, reducing delays caused by confusion, literacy barriers, and fragmented information.

AccessAI is **not a diagnostic system**. It is an information and navigation layer.

---

## Problem

In rural and semi-urban settings:

- Medical reports contain unexplained clinical terms (e.g., Hb 8.2, MCV low)
- Translation tools convert text but not meaning
- Doctor consultations involve long wait times and costs
- Government healthcare information exists across large, hard-to-navigate PDF portals

As a result, patients delay treatment due to lack of clarity and guidance.

---

## Solution Overview

AccessAI provides instant, voice-based explanations of medical reports and connects users to relevant government healthcare schemes.

The system focuses on:
- Understanding medical content
- Simplifying it into actionable language
- Delivering guidance through regional-language audio
- Reducing dependency on intermediaries

---

## User Journey

### 1. Input
- User selects preferred language
- Uploads a medical report or asks a question (text or voice)

### 2. Processing
- Medical text is extracted from documents
- AI interprets medical and policy context
- Verified medical and government data is retrieved
- Scheme eligibility is evaluated

### 3. Output
- Regional-language audio explanation
- Simplified health summary
- Matched government healthcare scheme
- Actionable next steps (where to go, when, and why)

---

## System Design Principles

- **Voice-First**  
  Designed for low-literacy and accessibility-constrained users

- **Low-Bandwidth**  
  Optimized for unstable or limited connectivity environments

- **Privacy-Aware**  
  Minimal retention of sensitive medical data

- **Non-Diagnostic**  
  Provides information and guidance, not medical advice

- **India-Contextual**  
  Supports regional languages and government healthcare programs

---

## Architecture Overview

**Input Layer**
- Medical reports (image / PDF)
- Text queries
- Voice queries

**Processing Layer**
- OCR for medical document extraction
- Speech-to-text for voice input
- AI reasoning for medical and policy interpretation

**Knowledge Layer**
- Retrieval-augmented generation (RAG)
- Verified medical references
- Government healthcare scheme database

**Output Layer**
- Regional-language text summaries
- Voice explanations
- SMS-based action plans

---

## Technology Stack

### Input & Ingestion
- OCR: Amazon Textract  
- Speech-to-Text: Amazon Transcribe  
- Frontend: React / Next.js (Progressive Web App)

### AI & Reasoning
- LLM: Amazon Bedrock (Claude)  
- Prompted for medical simplification and risk-aware summaries

### Knowledge Retrieval
- Vector Search: FAISS / OpenSearch  
- Data Sources: Curated medical references and government policy data

### Output
- Text-to-Speech: Amazon Polly  
- Channels: Web audio, SMS fallback

### Backend & Infrastructure
- API Layer: FastAPI / AWS Lambda  
- Storage: Amazon S3 (temporary, session-based)  
- Security: AWS IAM, encrypted APIs

---

## Core Features

### Medical Document Understanding
- Supports scanned images and PDFs
- Extracts key health parameters
- Handles noisy and low-quality reports

### Voice-First Interaction
- Regional-language audio output
- Hands-free voice input
- Designed for low-literacy users

### AI-Driven Simplification
- Converts medical jargon into plain language
- Context-aware summaries
- Confidence-aware responses to reduce misinformation risk

### Government Scheme Matching
- Identifies relevant healthcare schemes
- Provides eligibility hints
- Delivers next-step guidance via audio and SMS

### Low-Bandwidth Optimization
- Compressed audio delivery
- PWA support for intermittent connectivity
- Lightweight UI for low-end devices

---

## Security & Privacy

AccessAI is designed to minimize exposure of sensitive medical and personal data at every stage of processing.

- **PII Anonymization Before AI Processing**  
  Personally identifiable information (name, age, phone number, address, hospital ID, etc.) is detected and redacted or tokenized before any data is sent to the LLM.  
  The language model never receives raw user-identifying information.

- **Ephemeral, Session-Based Data Handling**  
  Medical documents and extracted text are processed in-memory or within short-lived sessions and are not stored persistently.

- **Separated Processing Boundaries**  
  PII handling, medical interpretation, and response generation are isolated into separate stages to prevent unintended data leakage.

- **Encrypted Communication**  
  All data in transit between services is encrypted using secure transport protocols.

- **Healthcare-Aware Design**  
  The system is designed with medical data sensitivity in mind and avoids unnecessary data retention or reuse.

- **Non-Diagnostic Safeguards**  
  Outputs are framed as informational guidance, reducing the risk of harm from misinterpretation.
---

## Scope & Limitations

- AccessAI does not diagnose conditions or prescribe treatment
- Outputs are informational and supportive in nature
- OCR and speech recognition errors are possible; guidance includes cautionary framing
- Designed to complement healthcare systems, not replace them
---

## Why AccessAI

AccessAI addresses the first barrier to healthcare access: understanding.

By transforming medical and policy information into clear, localized, voice-based guidance, it enables faster and more informed decisions for communities that are often excluded from digital healthcare tools.

---
