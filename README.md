<div align="center">

# AccessAI

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![AWS](https://img.shields.io/badge/AWS-Bedrock%20%7C%20Polly%20%7C%20Textract-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5%2B-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A low-bandwidth, multilingual, voice-first system that helps underserved communities understand medical information and navigate public healthcare schemes.**

> AccessAI is not a diagnostic system. It is an information and navigation layer.

</div>

---

## The Problem

Millions of people in rural and semi-urban settings receive medical reports they cannot understand, in a healthcare landscape that is hard to navigate without help.

| Challenge | Impact |
|-----------|--------|
| **Unexplained medical terms** | Reports use clinical shorthand (e.g., Hb 8.2, MCV low) with no plain-language context |
| **Lost-in-translation** | Existing translation tools convert words, not meaning |
| **Limited doctor access** | Consultations carry long wait times and out-of-pocket costs |
| **Fragmented policy information** | Government healthcare schemes are buried across large, poorly structured PDF portals |

The result: patients delay treatment not because care is unavailable, but because they cannot understand what they need or where to go.

---

## What AccessAI Does

AccessAI sits between the patient and the healthcare system. It takes a medical report or a plain question, and returns a simple, voice-based explanation in the user's regional language — along with matched government schemes and clear next steps.

```
User uploads report or asks a question
        ↓
PII is stripped before AI processing
        ↓
AI extracts, interprets, and simplifies medical content
        ↓
Relevant government schemes are matched
        ↓
Regional-language audio explanation + action steps delivered
```

### Design Principles

| Principle | Description |
|-----------|-------------|
| **Voice-first** | Designed for low-literacy and accessibility-constrained users |
| **Low-bandwidth** | Optimized for unstable or limited connectivity |
| **Privacy-aware** | Minimal retention of sensitive medical data |
| **Non-diagnostic** | Provides information and guidance, not medical advice |
| **India-contextual** | Supports regional languages and government healthcare programs |

---

## User Journey

**Step 1 — Input**
The user selects their preferred language, then either uploads a medical report (image or PDF) or types a question.

**Step 2 — Processing**
The system extracts text from the document, anonymizes PII, and passes the content to the AI layer. The AI interprets the medical and policy context, retrieves verified references, and evaluates scheme eligibility.

**Step 3 — Output**
The user receives a regional-language audio explanation, a simplified health summary, matched government schemes with eligibility hints, and actionable next steps — where to go, when, and why.

---

## Architecture

| Layer | Components |
|-------|------------|
| **Input** | Medical reports (image / PDF), text queries, voice queries |
| **Processing** | OCR (Textract), speech-to-text, AI reasoning via Amazon Bedrock |
| **Knowledge** | RAG over verified medical references and government scheme database |
| **Output** | Regional-language audio (Polly), text summaries, SMS-based action plans |

---

## Technology Stack

### Frontend

| Component | Technology |
|-----------|------------|
| Framework | React 18 + Vite |
| Routing | React Router DOM |
| Styling | Tailwind CSS |
| UI Components | Radix UI primitives |
| Language | TypeScript |

### Backend

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| Server | Uvicorn |
| AWS SDK | boto3 |
| Data Validation | Pydantic |

### AI & Cloud Services

| Component | Technology |
|-----------|------------|
| LLM | Amazon Bedrock (Claude) |
| OCR | Amazon Textract |
| Text-to-Speech | Amazon Polly |
| Storage | Amazon S3 |
| Vector Search | FAISS / OpenSearch |

---

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- AWS account with access to Bedrock, Textract, Polly, and S3

### 1. Clone the repository

```bash
git clone https://github.com/your-username/accessai.git
cd accessai
```

### 2. Configure environment variables

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

Open both `.env` files and fill in your AWS credentials and service configuration.

### 3. Start the frontend

```bash
npm install
npm run dev
```

### 4. Start the backend

```bash
cd backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

The frontend will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

---

## Core Features

### Medical Document Understanding
Supports scanned images and PDFs, extracts key health parameters, and handles noisy or low-quality scans gracefully.

### Voice-First Interaction
Delivers regional-language audio output and accepts hands-free voice input, specifically designed for low-literacy users.

### AI-Driven Simplification
Converts medical jargon into plain language with context-aware summaries. Confidence-aware responses reduce the risk of misinformation.

### Government Scheme Matching
Identifies relevant national and state healthcare schemes, provides eligibility hints, and delivers next-step guidance via audio and SMS.

### Low-Bandwidth Optimization
Compressed audio delivery, PWA support for intermittent connectivity, and a lightweight UI optimized for low-end devices.

---

## Security & Privacy

AccessAI is designed to minimize exposure of sensitive medical and personal data at every stage.

**PII anonymization before AI processing** — Names, ages, phone numbers, addresses, and hospital IDs are detected and redacted or tokenized before any content is sent to the LLM. The model never receives raw user-identifying information.

**Ephemeral session-based handling** — Medical documents and extracted text are processed in-memory within short-lived sessions and are not stored persistently.

**Separated processing boundaries** — PII handling, medical interpretation, and response generation are isolated into distinct stages to prevent unintended data leakage.

**Encrypted communication** — All data in transit between services is encrypted using secure transport protocols.

**Non-diagnostic safeguards** — All outputs are framed as informational guidance to reduce the risk of harm from misinterpretation.

---

## Scope & Limitations

AccessAI is a guidance and navigation tool, not a clinical system.

- It does not diagnose conditions or prescribe treatment
- OCR and speech recognition errors are possible; outputs include cautionary framing
- It is designed to complement healthcare systems, not replace them
- Scheme eligibility information is indicative and should be verified with the relevant authority

---

## Why AccessAI

AccessAI addresses the first barrier to healthcare access: **understanding**.

Most digital health tools are built for the already-connected — people with smartphones, literacy, and time. AccessAI is built for everyone else. By converting medical and policy information into clear, localized, voice-based guidance, it gives underserved communities the clarity they need to take the right action, faster.

---

## License

MIT — see [LICENSE](LICENSE) for details.
