/**
 * AccessAI API Client
 * Connects the frontend to the backend API with full type safety.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// ==================== Types ====================

export type ProcessingStatus =
  | 'pending'
  | 'uploading'
  | 'preprocessing'
  | 'extracting'
  | 'analyzing'
  | 'processing'
  | 'completed'
  | 'failed';

export type Language = 'en' | 'hi' | 'kn';

export interface DocumentUploadResponse {
  session_id: string;
  document_id: string;
  file_name: string;
  file_size: number;
  status: ProcessingStatus;
  message: string;
}

export interface QualityInfo {
  blur_score: number;
  contrast_score: number;
  quality_rating: 'good' | 'fair' | 'poor';
  issues: string[];
  is_acceptable: boolean;
}

export interface DocumentStatus {
  session_id: string;
  document_id: string;
  status: ProcessingStatus;
  status_message: string;
  file_name: string;
  ocr_confidence?: number;
  quality?: QualityInfo;
  engine_used?: string;
  fallback_used: boolean;
  created_at: string;
  updated_at: string;
}

export interface DocumentResult {
  session_id: string;
  document_id: string;
  text: string;
  confidence: number;
  blocks_count: number;
  tables: string[][][];
  key_value_pairs: { key: string; value: string }[];
  engine: string;
  fallback_used: boolean;
  quality?: QualityInfo;
}

export interface KeyFinding {
  test_name: string;
  value: string;
  normal_range: string;
  status: 'normal' | 'high' | 'low' | 'critical';
  explanation: string;
}

export interface AbnormalValue {
  test_name: string;
  value: string;
  normal_range: string;
  severity: 'mild' | 'moderate' | 'severe';
  explanation: string;
}

export interface SourceGroundingItem {
  test_name: string;
  extracted_value: number;
  reference_range: string;
  status: 'normal' | 'high' | 'low';
}

export interface AnalysisResponse {
  session_id: string;
  document_id: string;
  summary: string;
  key_findings: KeyFinding[];
  abnormal_values: AbnormalValue[];
  things_to_note: string[];
  questions_for_doctor: string[];
  confidence: number;
  confidence_notes: string;
  ocr_confidence: number;
  source_grounding: SourceGroundingItem[];
  language: Language;
  model: string;
  processing_time_ms: number;
}

export interface FollowUpResponse {
  answer: string;
  related_values: string[];
  should_ask_doctor: boolean;
  confidence: 'high' | 'medium' | 'low';
}

export interface SchemeInfo {
  id: string;
  name: string;
  type: string;
  coverage: string;
  eligibility: string[];
  documents_required: string[];
  benefits: string[];
  state: string;
  match_reason: string;
  apply_link?: string;
  helpline: string;
  relevance_score: number;
  action_steps: string[];
  conditions_covered: string[];
}

export interface SchemeMatchResponse {
  schemes: SchemeInfo[];
  count: number;
  summary: string;
  rag_used: boolean;
}

export interface AudioResponse {
  audio_url: string;
  audio_key: string;
  voice_id: string;
  language: Language;
  duration_estimate_seconds?: number;
  expires_at: string;
}

// ==================== API Client ====================

class AccessAIApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Document endpoints
  async uploadDocument(file: File): Promise<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/documents/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(error.detail);
    }

    return response.json();
  }

  async getDocumentStatus(sessionId: string): Promise<DocumentStatus> {
    return this.request<DocumentStatus>(`/documents/status/${sessionId}`);
  }

  async getDocumentResult(sessionId: string): Promise<DocumentResult> {
    return this.request<DocumentResult>(`/documents/result/${sessionId}`);
  }

  async deleteDocument(sessionId: string): Promise<void> {
    await this.request(`/documents/${sessionId}`, { method: 'DELETE' });
  }

  // Analysis endpoints
  async analyzeDocument(
    sessionId: string,
    documentId: string,
    language: Language = 'en'
  ): Promise<AnalysisResponse> {
    return this.request<AnalysisResponse>('/analysis/explain', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        document_id: documentId,
        language,
      }),
    });
  }

  async getAnalysisResult(sessionId: string): Promise<AnalysisResponse> {
    return this.request<AnalysisResponse>(`/analysis/result/${sessionId}`);
  }

  async askFollowUp(
    sessionId: string,
    question: string,
    language: Language = 'en'
  ): Promise<FollowUpResponse> {
    return this.request<FollowUpResponse>('/analysis/followup', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        question,
        language,
      }),
    });
  }

  // Scheme endpoints
  async matchSchemes(
    state: string,
    incomeRange: string,
    age: number,
    isBpl: boolean,
    conditions?: string[],
    sessionId?: string,
    language?: Language
  ): Promise<SchemeMatchResponse> {
    return this.request<SchemeMatchResponse>('/schemes/match', {
      method: 'POST',
      body: JSON.stringify({
        state,
        income_range: incomeRange,
        age,
        is_bpl: isBpl,
        conditions,
        session_id: sessionId,
        language: language || 'english',
      }),
    });
  }

  async searchSchemes(
    state?: string,
    query?: string,
    schemeType?: string
  ): Promise<{ schemes: SchemeInfo[]; count: number }> {
    const params = new URLSearchParams();
    if (state) params.append('state', state);
    if (query) params.append('query', query);
    if (schemeType) params.append('scheme_type', schemeType);
    return this.request(`/schemes/search?${params.toString()}`);
  }

  async getSchemeDetails(schemeId: string): Promise<SchemeInfo> {
    return this.request<SchemeInfo>(`/schemes/${schemeId}`);
  }

  // Audio endpoints
  async synthesizeSpeech(text: string, language: Language = 'hi'): Promise<AudioResponse> {
    return this.request<AudioResponse>('/audio/synthesize', {
      method: 'POST',
      body: JSON.stringify({ text, language }),
    });
  }

  async synthesizeExplanation(
    explanation: string,
    language: Language = 'hi'
  ): Promise<{ audio_url: string; voice_id: string; language: string; expires_at: string }> {
    return this.request('/audio/synthesize-explanation', {
      method: 'POST',
      body: JSON.stringify({ explanation, language }),
    });
  }
}

// Export singleton
export const apiClient = new AccessAIApiClient();
export { AccessAIApiClient };
