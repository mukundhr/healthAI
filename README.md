# AccessAI

**AccessAI** is a low-bandwidth, multilingual, voice-first healthcare access system designed to help underserved communities understand medical information and navigate public healthcare schemes.

It converts complex medical reports and policy documents into simple, localized, audio-based guidance, reducing delays caused by confusion, literacy barriers, and fragmented information.

> **AccessAI is not a diagnostic system. It is an information and navigation layer.**

---

## Problem

### Challenges in Rural and Semi-Urban Settings

| Challenge | Description |
|-----------|-------------|
| **Unexplained Medical Terms** | Medical reports contain clinical terms (e.g., Hb 8.2, MCV low) without explanation |
| **Lost-in-Translation** | Translation tools convert text but not meaning |
| **Limited Doctor Access** | Consultations involve long wait times and costs |
| **Fragmented Information** | Government healthcare information exists across large, hard-to-navigate PDF portals |

**Result:** Patients delay treatment due to lack of clarity and guidance.

---

## Solution Overview

AccessAI provides instant, voice-based explanations of medical reports and connects users to relevant government healthcare schemes.

### System Focus

| Focus Area | Description |
|------------|-------------|
| **Understanding** | Medical content extraction and interpretation |
| **Simplification** | Converting medical jargon into actionable language |
| **Delivery** | Guidance through regional-language audio |
| **Independence** | Reducing dependency on intermediaries |

---

## User Journey

### 1. Input

| Step | Actions |
|------|---------|
| **Language Selection** | User selects preferred language |
| **Upload/Query** | Uploads a medical report or asks a question (text or voice) |

### 2. Processing

| Process | Description |
|---------|-------------|
| **Text Extraction** | Medical text is extracted from documents |
| **AI Interpretation** | AI interprets medical and policy context |
| **Data Retrieval** | Verified medical and government data is retrieved |
| **Eligibility Evaluation** | Scheme eligibility is evaluated |

### 3. Output

| Output | Description |
|--------|-------------|
| **Audio Explanation** | Regional-language audio explanation |
| **Health Summary** | Simplified health summary |
| **Scheme Match** | Matched government healthcare scheme |
| **Action Steps** | Actionable next steps (where to go, when, and why) |

---

## System Design Principles

| Principle | Description |
|-----------|-------------|
| **Voice-First** | Designed for low-literacy and accessibility-constrained users |
| **Low-Bandwidth** | Optimized for unstable or limited connectivity environments |
| **Privacy-Aware** | Minimal retention of sensitive medical data |
| **Non-Diagnostic** | Provides information and guidance, not medical advice |
| **India-Contextual** | Supports regional languages and government healthcare programs |

---

## Architecture Overview

### System Layers

| Layer | Components |
|-------|------------|
| **Input Layer** | Medical reports (image / PDF), Text queries, Voice queries |
| **Processing Layer** | OCR for medical document extraction, Speech-to-text for voice input, AI reasoning for medical and policy interpretation |
| **Knowledge Layer** | Retrieval-augmented generation (RAG), Verified medical references, Government healthcare scheme database |
| **Output Layer** | Regional-language text summaries, Voice explanations, SMS-based action plans |

---

## Technology Stack

### Frontend

| Component | Technology |
|-----------|------------|
| **Framework** | React 18 + Vite |
| **Routing** | React Router DOM |
| **Styling** | Tailwind CSS |
| **UI Components** | Radix UI primitives |
| **Language** | TypeScript |
| **Build Tool** | Vite |

### Backend

| Component | Technology |
|-----------|------------|
| **API Framework** | FastAPI |
| **Server** | Uvicorn |
| **AWS SDK** | boto3 |
| **Data Validation** | Pydantic |

### AI & Cloud Services

| Component | Technology |
|-----------|------------|
| **LLM** | Amazon Bedrock (Claude) |
| **OCR** | Amazon Textract |
| **Text-to-Speech** | Amazon Polly |
| **Storage** | Amazon S3 |

### Knowledge Retrieval

| Component | Technology |
|-----------|------------|
| **Vector Search** | FAISS / OpenSearch |
| **Data Sources** | Curated medical references and government policy data |

---

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- AWS Account (for cloud services)

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

### Environment Variables

Copy the example environment files and configure them:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

---

## Core Features

### Medical Document Understanding

| Feature | Description |
|---------|-------------|
| **Format Support** | Supports scanned images and PDFs |
| **Parameter Extraction** | Extracts key health parameters |
| **Quality Handling** | Handles noisy and low-quality reports |

### Voice-First Interaction

| Feature | Description |
|---------|-------------|
| **Audio Output** | Regional-language audio output |
| **Voice Input** | Hands-free voice input |
| **Target Users** | Designed for low-literacy users |

### AI-Driven Simplification

| Feature | Description |
|---------|-------------|
| **Plain Language** | Converts medical jargon into plain language |
| **Context-Aware** | Context-aware summaries |
| **Confidence Handling** | Confidence-aware responses to reduce misinformation risk |

### Government Scheme Matching

| Feature | Description |
|---------|-------------|
| **Scheme Identification** | Identifies relevant healthcare schemes |
| **Eligibility Hints** | Provides eligibility hints |
| **Next Steps** | Delivers next-step guidance via audio and SMS |

### Low-Bandwidth Optimization

| Feature | Description |
|---------|-------------|
| **Audio Compression** | Compressed audio delivery |
| **Offline Support** | PWA support for intermittent connectivity |
| **Lightweight Design** | Lightweight UI for low-end devices |

---

## Security & Privacy

AccessAI is designed to minimize exposure of sensitive medical and personal data at every stage of processing.

### Privacy Measures

| Measure | Description |
|---------|-------------|
| **PII Anonymization Before AI Processing** | Personally identifiable information (name, age, phone number, address, hospital ID, etc.) is detected and redacted or tokenized before any data is sent to the LLM. The language model never receives raw user-identifying information. |
| **Ephemeral, Session-Based Data Handling** | Medical documents and extracted text are processed in-memory or within short-lived sessions and are not stored persistently. |
| **Separated Processing Boundaries** | PII handling, medical interpretation, and response generation are isolated into separate stages to prevent unintended data leakage. |
| **Encrypted Communication** | All data in transit between services is encrypted using secure transport protocols. |
| **Healthcare-Aware Design** | The system is designed with medical data sensitivity in mind and avoids unnecessary data retention or reuse. |
| **Non-Diagnostic Safeguards** | Outputs are framed as informational guidance, reducing the risk of harm from misinterpretation. |

---

## Scope & Limitations

### What AccessAI Does NOT Do

| Limitation | Description |
|------------|-------------|
| **No Diagnosis** | Does not diagnose conditions or prescribe treatment |
| **Informational Only** | Outputs are informational and supportive in nature |
| **Potential Errors** | OCR and speech recognition errors are possible; guidance includes cautionary framing |
| **Complementary Tool** | Designed to complement healthcare systems, not replace them |

---

## Why AccessAI

AccessAI addresses the first barrier to healthcare access: **understanding**.

By transforming medical and policy information into clear, localized, voice-based guidance, it enables faster and more informed decisions for communities that are often excluded from digital healthcare tools.

---
