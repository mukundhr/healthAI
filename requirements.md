# AccessAI - Requirements Document

**Version:** 1.0  
**Last Updated:** February 10, 2026  
**Status:** Final  
**Reviewed By:** Project Team

---

## Executive Summary

**AccessAI** is a voice-first, multilingual healthcare access platform that converts complex medical reports into simple, regional-language audio guidance and connects users with government healthcare schemes.

### Problem Statement
Rural patients cannot understand their medical reports due to medical jargon, language barriers, and limited access to healthcare professionals.

### Solution
AI-powered platform that provides instant medical report interpretation through voice-based explanations in regional languages, optimized for low-bandwidth environments and low-literacy users.

### Key Innovation
RAG-powered medical interpretation combined with government scheme matching, delivered through optimized voice interfaces specifically designed for rural India.

### Target Impact
- Reduce treatment delays caused by medical literacy gaps
- Increase awareness and utilization of government healthcare schemes  
- Provide accessible healthcare guidance to underserved communities

---

## 1. Functional Requirements

### 1.1 User Interface Layer

#### **Language Selection**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-1.1.1 | System SHALL provide language selection interface at startup | **High** |
| FR-1.1.2 | System SHALL support Telugu, Hindi, Tamil, Kannada, Bengali, and English | **High** |
| FR-1.1.3 | System SHALL remember user's language preference across sessions | Medium |
| FR-1.1.4 | System SHALL allow language switching at any time | Medium |

#### **Document Upload**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-1.2.1 | System SHALL accept medical reports in JPG, PNG, and PDF formats | **High** |
| FR-1.2.2 | System SHALL support document sizes up to 10MB | **High** |
| FR-1.2.3 | System SHALL provide camera capture functionality for mobile users | **High** |
| FR-1.2.4 | System SHALL show upload progress indicator | Medium |
| FR-1.2.5 | System SHALL validate file format and size before upload | Medium |

#### **Voice Input** *(Future Enhancement)*

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-1.3.1 | System SHALL accept voice queries in supported regional languages | Low |
| FR-1.3.2 | System SHALL handle audio input up to 60 seconds | Low |
| FR-1.3.3 | System SHALL provide visual feedback during voice recording | Low |

---

### 1.2 Document Processing Layer

#### **OCR & Text Extraction**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-2.1.1 | System SHALL extract text from scanned medical reports using Amazon Textract | **High** |
| FR-2.1.2 | System SHALL handle low-quality and noisy document images | **High** |
| FR-2.1.3 | System SHALL identify and extract key medical parameters (Hb, MCV, BP, glucose, etc.) | **High** |
| FR-2.1.4 | System SHALL classify document type (blood test, X-ray report, prescription, etc.) | Medium |
| FR-2.1.5 | System SHALL complete OCR processing within 5 seconds for standard documents | **High** |

#### **PII Protection**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-2.2.1 | System SHALL detect and anonymize patient name, phone number, address before AI processing | **CRITICAL** |
| FR-2.2.2 | System SHALL remove hospital IDs, ABHA numbers, and other identifiers | **CRITICAL** |
| FR-2.2.3 | System SHALL tokenize sensitive data for session tracking without exposing PII | **CRITICAL** |
| FR-2.2.4 | System SHALL log PII removal actions for audit purposes | **High** |

---

### 1.3 AI Processing Layer

#### **Medical Interpretation**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-3.1.1 | System SHALL use Amazon Bedrock (Claude 4.5 Haiku) for medical text interpretation | **High** |
| FR-3.1.2 | System SHALL convert medical jargon into plain language explanations | **High** |
| FR-3.1.3 | System SHALL identify abnormal values based on standard medical ranges | **High** |
| FR-3.1.4 | System SHALL provide context-appropriate explanations based on age and gender | Medium |
| FR-3.1.5 | System SHALL avoid making diagnostic statements | **CRITICAL** |

#### **Knowledge Retrieval (RAG)**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-3.2.1 | System SHALL use Amazon OpenSearch for vector-based knowledge retrieval | **High** |
| FR-3.2.2 | System SHALL retrieve top 5 most relevant medical reference documents | **High** |
| FR-3.2.3 | System SHALL cross-reference extracted data with verified medical knowledge base | **High** |
| FR-3.2.4 | System SHALL match medical conditions to relevant government schemes | **High** |
| FR-3.2.5 | System SHALL provide confidence scores for retrieved information | Medium |

#### **Risk-Aware Guidance**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-3.3.1 | System SHALL flag critically abnormal values prominently | **CRITICAL** |
| FR-3.3.2 | System SHALL recommend immediate medical attention when appropriate | **CRITICAL** |
| FR-3.3.3 | System SHALL express uncertainty when confidence is low | **High** |
| FR-3.3.4 | System SHALL include disclaimer that output is informational, not diagnostic | **CRITICAL** |

---

### 1.4 Output Generation Layer

#### **Text Summaries**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-4.1.1 | System SHALL generate simplified health summary in user's selected language | **High** |
| FR-4.1.2 | System SHALL highlight key findings and abnormal values | **High** |
| FR-4.1.3 | System SHALL provide actionable next steps | **High** |
| FR-4.1.4 | System SHALL format text for readability on small screens | Medium |

#### **Audio Generation**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-4.2.1 | System SHALL use Amazon Polly Neural TTS for audio generation | **High** |
| FR-4.2.2 | System SHALL generate audio in user's selected regional language | **High** |
| FR-4.2.3 | System SHALL use natural, conversational voice synthesis | **High** |
| FR-4.2.4 | System SHALL compress audio to <200KB per minute (32kbps Opus) | **High** |
| FR-4.2.5 | System SHALL provide audio playback controls (play, pause, replay) | Medium |
| FR-4.2.6 | System SHALL support adjustable playback speed (0.75x, 1x, 1.25x, 1.5x) | Low |

#### **Government Scheme Matching**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-4.3.1 | System SHALL identify applicable government healthcare schemes | **High** |
| FR-4.3.2 | System SHALL display scheme eligibility criteria | **High** |
| FR-4.3.3 | System SHALL provide scheme contact information and next steps | **High** |
| FR-4.3.4 | System SHALL support Ayushman Bharat and state-level programs | **High** |

---

### 1.5 Data Storage Layer

#### **Temporary Storage**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-5.1.1 | System SHALL store uploaded documents in Amazon S3 with 24-hour retention | **High** |
| FR-5.1.2 | System SHALL automatically delete expired documents | **CRITICAL** |
| FR-5.1.3 | System SHALL encrypt all stored documents at rest | **CRITICAL** |

#### **Caching**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-5.2.1 | System SHALL cache generated audio files in ElastiCache (Redis) for 7 days | Medium |
| FR-5.2.2 | System SHALL serve cached audio for identical requests | Medium |
| FR-5.2.3 | System SHALL invalidate cache when knowledge base is updated | Low |

#### **Knowledge Database**

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| FR-5.3.1 | System SHALL maintain medical knowledge base in Amazon RDS PostgreSQL | **High** |
| FR-5.3.2 | System SHALL store government scheme database with eligibility criteria | **High** |
| FR-5.3.3 | System SHALL update scheme information monthly | Medium |
| FR-5.3.4 | System SHALL support storing 1 million+ scheme records | Low |

---

## 2. Non-Functional Requirements

### 2.1 Performance Requirements

| **Requirement ID** | **Metric** | **Target** | **Priority** |
|:-------------------|:-----------|:-----------|:-------------|
| NFR-2.1.1 | OCR processing time | ≤ 5 seconds | **High** |
| NFR-2.1.2 | AI interpretation time | ≤ 8 seconds | **High** |
| NFR-2.1.3 | Audio generation time | ≤ 5 seconds | **High** |
| NFR-2.1.4 | End-to-end processing time | ≤ 15 seconds | **High** |
| NFR-2.1.5 | API response time | ≤ 2 seconds | Medium |
| NFR-2.1.6 | System uptime | 99.5% | **CRITICAL** |

### 2.2 Scalability Requirements

| **Requirement ID** | **Metric** | **Target** | **Priority** |
|:-------------------|:-----------|:-----------|:-------------|
| NFR-2.2.1 | Concurrent users supported | 1,000 users | **High** |
| NFR-2.2.2 | Peak requests per hour | 10,000 requests | **High** |
| NFR-2.2.3 | Auto-scaling trigger threshold | 70% CPU utilization | Medium |
| NFR-2.2.4 | Maximum scale-out time | 2 minutes | Medium |

### 2.3 Bandwidth Optimization

| **Requirement ID** | **Metric** | **Target** | **Priority** |
|:-------------------|:-----------|:-----------|:-------------|
| NFR-2.3.1 | Page load time on 2G network | ≤ 5 seconds | **CRITICAL** |
| NFR-2.3.2 | Total page size | ≤ 500KB | **High** |
| NFR-2.3.3 | Audio file size | ≤ 200KB per minute | **High** |
| NFR-2.3.4 | Image compression ratio | 70-80% | Medium |
| NFR-2.3.5 | Progressive Web App caching | Enabled | **High** |

### 2.4 Usability Requirements

| **Requirement ID** | **Metric** | **Target** | **Priority** |
|:-------------------|:-----------|:-----------|:-------------|
| NFR-2.4.1 | Maximum steps to complete task | 4 steps | **High** |
| NFR-2.4.2 | Minimum font size | 16px | **High** |
| NFR-2.4.3 | Touch target minimum size | 48x48 pixels | **High** |
| NFR-2.4.4 | Color contrast ratio | 4.5:1 minimum | **High** |
| NFR-2.4.5 | Minimum screen size supported | 4.5 inches | Medium |

### 2.5 Accessibility Requirements

| **Requirement ID** | **Metric** | **Standard** | **Priority** |
|:-------------------|:-----------|:-------------|:-------------|
| NFR-2.5.1 | WCAG compliance level | 2.1 Level AA | **High** |
| NFR-2.5.2 | Screen reader compatibility | Full support | **High** |
| NFR-2.5.3 | Keyboard navigation | Complete | Medium |
| NFR-2.5.4 | Voice-only navigation | Supported | **High** |

---

## 3. Security Requirements

### 3.1 Data Privacy & Protection

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| SR-3.1.1 | System SHALL anonymize all PII before sending to AI services | **CRITICAL** |
| SR-3.1.2 | System SHALL NOT store medical documents persistently | **CRITICAL** |
| SR-3.1.3 | System SHALL comply with India's Digital Personal Data Protection Act, 2023 | **CRITICAL** |
| SR-3.1.4 | System SHALL delete all session data after 24 hours | **CRITICAL** |
| SR-3.1.5 | System SHALL implement data minimization principles | **High** |

### 3.2 Encryption & Transmission

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| SR-3.2.1 | System SHALL use TLS 1.3 for all data in transit | **CRITICAL** |
| SR-3.2.2 | System SHALL encrypt all data at rest using AES-256 | **CRITICAL** |
| SR-3.2.3 | System SHALL use HTTPS exclusively for all API calls | **CRITICAL** |
| SR-3.2.4 | System SHALL implement secure WebSocket connections for real-time features | **High** |

### 3.3 Authentication & Authorization

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| SR-3.3.1 | API endpoints SHALL require authentication tokens | **High** |
| SR-3.3.2 | System SHALL implement rate limiting (100 requests/hour per user) | **High** |
| SR-3.3.3 | Admin panel SHALL require multi-factor authentication | **CRITICAL** |
| SR-3.3.4 | System SHALL enforce role-based access control (RBAC) | **High** |

### 3.4 Audit & Monitoring

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| SR-3.4.1 | System SHALL log all user actions with timestamps | **High** |
| SR-3.4.2 | System SHALL monitor for suspicious activity | **High** |
| SR-3.4.3 | System SHALL alert administrators on security incidents | **CRITICAL** |
| SR-3.4.4 | Audit logs SHALL be retained for 90 days | Medium |
| SR-3.4.5 | Logs SHALL NOT contain PII or sensitive medical data | **CRITICAL** |

---

## 4. Technical Requirements

### 4.1 AWS Services Stack

| **Component** | **Technology** | **Purpose** |
|:--------------|:---------------|:------------|
| **OCR** | Amazon Textract | Extract text from medical reports (images/PDFs) |
| **AI Reasoning** | Amazon Bedrock<br/>(Claude 4.5 Haiku) | Medical interpretation and simplification |
| **Voice Output** | Amazon Polly<br/>(Neural TTS) | Regional language audio generation |
| **Knowledge Base** | Amazon OpenSearch | Vector database for RAG-based retrieval |
| **Speech Input** | Amazon Transcribe | Voice-to-text conversion *(future)* |
| **Backend** | AWS Lambda | Serverless orchestration and processing |
| **API Gateway** | Amazon API Gateway | Request routing and rate limiting |
| **Storage** | Amazon S3 | Temporary document storage (24h retention) |
| **Cache** | Amazon ElastiCache<br/>(Redis) | Audio file caching |
| **Database** | Amazon RDS<br/>(PostgreSQL) | Medical knowledge and government schemes |

### 4.2 Frontend Requirements

| **Requirement ID** | **Component** | **Technology** | **Priority** |
|:-------------------|:--------------|:---------------|:-------------|
| TR-4.2.1 | Framework | Next.js 14+ | **High** |
| TR-4.2.2 | UI Library | React 18+ | **High** |
| TR-4.2.3 | Styling | Tailwind CSS | **High** |
| TR-4.2.4 | PWA Support | Service Workers | **High** |
| TR-4.2.5 | State Management | React Context / Zustand | Medium |

### 4.3 Backend Requirements

| **Requirement ID** | **Component** | **Technology** | **Priority** |
|:-------------------|:--------------|:---------------|:-------------|
| TR-4.3.1 | Serverless Functions | AWS Lambda (Node.js/Python) | **High** |
| TR-4.3.2 | API Design | RESTful + GraphQL *(optional)* | **High** |
| TR-4.3.3 | API Documentation | OpenAPI/Swagger | Medium |
| TR-4.3.4 | Error Handling | Structured error responses | **High** |

### 4.4 Database Requirements

| **Requirement ID** | **Component** | **Technology** | **Priority** |
|:-------------------|:--------------|:---------------|:-------------|
| TR-4.4.1 | Relational Database | Amazon RDS PostgreSQL | **High** |
| TR-4.4.2 | Vector Search | Amazon OpenSearch | **High** |
| TR-4.4.3 | Cache Layer | Amazon ElastiCache (Redis) | Medium |
| TR-4.4.4 | Backup Strategy | Automated daily backups | **High** |

### 4.5 AI/ML Requirements

| **Requirement ID** | **Component** | **Specification** | **Priority** |
|:-------------------|:--------------|:------------------|:-------------|
| TR-4.5.1 | LLM Model | Claude 4.5 Haiku (fast, cost-effective) | **High** |
| TR-4.5.2 | Embedding Model | Amazon Titan Embeddings G1 | **High** |
| TR-4.5.3 | Vector Dimensions | 1024 dimensions | Medium |
| TR-4.5.4 | RAG Top-K Retrieval | 5 documents | Medium |
| TR-4.5.5 | Prompt Templates | Medical safety guidelines included | **CRITICAL** |

### 4.6 Infrastructure Requirements

| **Requirement ID** | **Component** | **Technology** | **Priority** |
|:-------------------|:--------------|:---------------|:-------------|
| TR-4.6.1 | Cloud Provider | AWS | **High** |
| TR-4.6.2 | Infrastructure as Code | Terraform / CloudFormation | **High** |
| TR-4.6.3 | CI/CD Pipeline | GitHub Actions / AWS CodePipeline | **High** |
| TR-4.6.4 | Monitoring | Amazon CloudWatch + Alerts | **High** |
| TR-4.6.5 | Primary Region | ap-south-1 (Mumbai, India) | **High** |

---

## 5. Data Requirements

### 5.1 Medical Knowledge Base

| **Requirement ID** | **Data Type** | **Specification** | **Priority** |
|:-------------------|:--------------|:------------------|:-------------|
| DR-5.1.1 | Medical Terms Dictionary | 10,000+ common terms with simplified explanations | **High** |
| DR-5.1.2 | Normal Value Ranges | Standard ranges for 50+ medical parameters | **High** |
| DR-5.1.3 | Disease Information | 500+ common conditions with explanations | Medium |
| DR-5.1.4 | Update Frequency | Quarterly review and updates | Medium |

### 5.2 Government Scheme Database

| **Requirement ID** | **Data Type** | **Specification** | **Priority** |
|:-------------------|:--------------|:------------------|:-------------|
| DR-5.2.1 | Central Schemes | Ayushman Bharat, PM-JAY, etc. | **High** |
| DR-5.2.2 | State Schemes | 28 states + 8 UTs covered | **High** |
| DR-5.2.3 | Eligibility Criteria | Structured data for automated matching | **High** |
| DR-5.2.4 | Update Frequency | Monthly verification and updates | **High** |

### 5.3 Language Resources

| **Requirement ID** | **Resource Type** | **Specification** | **Priority** |
|:-------------------|:------------------|:------------------|:-------------|
| DR-5.3.1 | Supported Languages | Telugu, Hindi, Tamil, Kannada, Bengali, English | **High** |
| DR-5.3.2 | Medical Term Translations | 5,000+ terms per language | **High** |
| DR-5.3.3 | Voice Models | Neural TTS for all supported languages | **High** |
| DR-5.3.4 | Cultural Appropriateness | Reviewed by native speakers | **High** |

---

## 6. Compliance Requirements

### 6.1 Legal Compliance

| **Requirement ID** | **Compliance Area** | **Standard** | **Priority** |
|:-------------------|:-------------------|:-------------|:-------------|
| CR-6.1.1 | Data Protection | India's DPDP Act, 2023 | **CRITICAL** |
| CR-6.1.2 | User Consent | Explicit consent before processing | **CRITICAL** |
| CR-6.1.3 | Terms of Service | Clear, accessible ToS document | **High** |
| CR-6.1.4 | Privacy Policy | Comprehensive privacy disclosure | **High** |

### 6.2 Medical Compliance

| **Requirement ID** | **Requirement** | **Priority** |
|:-------------------|:----------------|:-------------|
| CR-6.2.1 | System SHALL NOT provide medical diagnoses | **CRITICAL** |
| CR-6.2.2 | System SHALL NOT prescribe treatments or medications | **CRITICAL** |
| CR-6.2.3 | System SHALL display prominent "Not a Diagnostic Tool" disclaimer | **CRITICAL** |
| CR-6.2.4 | System SHALL recommend consulting healthcare professionals | **CRITICAL** |
| CR-6.2.5 | All outputs SHALL be framed as informational guidance only | **CRITICAL** |

---

## 7. Testing Requirements

### 7.1 Testing Coverage Standards

| **Test Type** | **Coverage Requirement** | **Notes** |
|:--------------|:------------------------|:----------|
| **Unit Testing** | Minimum 80% code coverage | All API endpoints: 100% coverage |
| **Integration Testing** | End-to-end user flows | All third-party integrations verified |
| **Performance Testing** | 1,000 concurrent users | Load, stress, and response time testing |
| **Accessibility Testing** | WCAG 2.1 AA compliance | Automated tools + manual verification |
| **Localization Testing** | All 6 languages | Native speaker review required |

### 7.2 Test Scenarios

#### **Functional Testing**
- Document upload and OCR accuracy
- PII anonymization verification
- AI interpretation quality
- Audio generation and compression
- Scheme matching accuracy

#### **Security Testing**
- Penetration testing
- Data encryption verification
- Authentication/authorization testing
- PII leakage prevention

#### **Performance Testing**
- Load testing (1,000 concurrent users)
- Stress testing to breaking point
- Bandwidth optimization verification

---

## 8. Success Metrics

### 8.1 Technical KPIs

| **Metric** | **Target** | **Measurement Method** |
|:-----------|:-----------|:-----------------------|
| System Uptime | **99.5%** | Monthly average monitoring |
| OCR Accuracy | **>90%** | Automated testing against ground truth |
| Average Response Time | **<15 seconds** | End-to-end processing time |
| Audio Compression Ratio | **70-80%** | File size comparison |

### 8.2 User Experience KPIs

| **Metric** | **Target** | **Measurement Method** |
|:-----------|:-----------|:-----------------------|
| User Satisfaction Score | **>4.0/5.0** | Post-interaction survey |
| Task Completion Rate | **>80%** | Analytics tracking |
| Audio Playback Completion | **>75%** | Playback analytics |
| Return User Rate | **>40%** | Monthly active users |

### 8.3 Impact KPIs

| **Metric** | **Target** | **Measurement Method** |
|:-----------|:-----------|:-----------------------|
| Reports Processed | **10,000/month** | System logs |
| Scheme Matches Made | **5,000/month** | Database records |
| Time Saved per Report | **30 minutes** | User survey |
| Users Reached (Year 1) | **50,000** | Cumulative user count |

---

## 9. Supported Languages & Schemes

### 9.1 Supported Languages

| **Language** | **Native Script** | **TTS Support** | **Status** |
|:-------------|:------------------|:----------------|:-----------|
| English | English | Yes | Active |
| Telugu | తెలుగు | Yes | Active |
| Hindi | हिन्दी | Yes | Active |
| Tamil | தமிழ் | Yes | Active |
| Kannada | ಕನ್ನಡ | Yes | Active |
| Bengali | বাংলা | Yes | Active |

### 9.2 Supported Government Healthcare Schemes

| **Scheme Category** | **Examples** | **Coverage** |
|:-------------------|:-------------|:-------------|
| **Central Schemes** | Ayushman Bharat (PM-JAY) | National |
| **State Health Insurance** | 28 states + 8 UTs | State-level |
| **Emergency Healthcare** | Trauma care, disaster relief | National |
| **Maternal & Child Health** | PMSMA, Janani Suraksha Yojana | National |
| **Disease-Specific** | TB, HIV, Cancer assistance programs | National |

### 9.3 Supported Medical Report Types

| **Report Type** | **Examples** | **OCR Accuracy Target** |
|:----------------|:-------------|:------------------------|
| **Blood Tests** | CBC, lipid profile, HbA1c, liver/kidney function | >95% |
| **Radiology Reports** | X-ray, ultrasound summaries | >90% |
| **Prescriptions** | Medication summaries | >85% |
| **Discharge Summaries** | Hospital discharge documents | >90% |
| **Diagnostic Tests** | ECG, spirometry results | >85% |

---

## Document Control

### Version History

| **Version** | **Date** | **Author** | **Changes** |
|:------------|:---------|:-----------|:------------|
| 1.0 | Feb 10, 2026 | Project Team | Initial release |

---

**End of Document**