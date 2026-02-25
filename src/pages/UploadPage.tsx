import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload, FileText, Brain, MessageSquareText, Volume2, Landmark,
  Copy, Download, Play, Pause, ChevronDown, Wifi, WifiOff, Loader2, CheckCircle2
} from "lucide-react";
import Navbar from "@/components/Navbar";
import DisclaimerBar from "@/components/DisclaimerBar";
import GlassCard from "@/components/GlassCard";
import WaveformVisualizer from "@/components/WaveformVisualizer";
import { apiClient } from "@/lib/api";
import { AnalysisResponse, DocumentStatus, DocumentUploadResponse, SchemeMatchResponse } from "@/lib/api";

type Step = "upload" | "processing" | "results";

const UploadPage = () => {
  const [step, setStep] = useState<Step>("upload");
  const [lowBandwidth, setLowBandwidth] = useState(false);
  const [playingLang, setPlayingLang] = useState<string | null>(null);
  const [audioSpeed, setAudioSpeed] = useState<"1x" | "1.5x">("1x");
  const [dragOver, setDragOver] = useState(false);

  // API related state
  const [uploadResponse, setUploadResponse] = useState<DocumentUploadResponse | null>(null);
  const [documentStatus, setDocumentStatus] = useState<DocumentStatus | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [schemeResult, setSchemeResult] = useState<SchemeMatchResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Scheme matching state
  const [schemeState, setSchemeState] = useState("Karnataka");
  const [schemeIncome, setSchemeIncome] = useState("below-1l");
  const [schemeAge, setSchemeAge] = useState("30");
  const [schemeBpl, setSchemeBpl] = useState(true);
  const [showSchemes, setShowSchemes] = useState(false);

  // Audio state
  const [hindiAudioUrl, setHindiAudioUrl] = useState<string | null>(null);
  const [kannadaAudioUrl, setKannadaAudioUrl] = useState<string | null>(null);

  // Handle document upload
  const handleUpload = async (file: File) => {
    try {
      setStep("processing");
      
      const response = await apiClient.uploadDocument(file);
      setUploadResponse(response);
      
      // Poll for processing status
      const pollInterval = setInterval(async () => {
        const status = await apiClient.getDocumentStatus(response.session_id);
        setDocumentStatus(status);
        
        if (status.status === "completed") {
          clearInterval(pollInterval);
          setStep("results");
          // Automatically analyze
          await analyzeDocument(response.session_id, response.document_id);
        } else if (status.status === "failed") {
          clearInterval(pollInterval);
          setStep("upload");
          alert("Processing failed. Please try again.");
        }
      }, 2000);
      
    } catch (error) {
      console.error("Upload error:", error);
      setStep("upload");
      alert("Upload failed. Please try again.");
    }
  };

  // Handle drag and drop
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleUpload(e.dataTransfer.files[0]);
    }
  };

  // Handle file input
  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleUpload(e.target.files[0]);
    }
  };

  // Analyze document
  const analyzeDocument = async (sessionId: string, documentId: string) => {
    try {
      setIsAnalyzing(true);
      
      const analysis = await apiClient.analyzeDocument(sessionId, documentId, "en");
      setAnalysisResult(analysis);
      
      // Generate audio
      await generateAudio(analysis.explanation);
      
    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Generate audio
  const generateAudio = async (text: string) => {
    try {
      const hindiResponse = await apiClient.synthesizeSpeech(text, "hi");
      const kannadaResponse = await apiClient.synthesizeSpeech(text, "kn");
      
      setHindiAudioUrl(hindiResponse.audio_url);
      setKannadaAudioUrl(kannadaResponse.audio_url);
    } catch (error) {
      console.error("Audio synthesis error:", error);
    }
  };

  // Find eligible schemes
  const findEligibleSchemes = async () => {
    try {
      const response = await apiClient.matchSchemes(
        schemeState,
        schemeIncome,
        parseInt(schemeAge),
        schemeBpl
      );
      setSchemeResult(response);
      setShowSchemes(true);
    } catch (error) {
      console.error("Scheme matching error:", error);
    }
  };

  // Play audio
  const playAudio = async (lang: string) => {
    if (playingLang === lang) {
      setPlayingLang(null);
      return;
    }

    setPlayingLang(lang);
    
    try {
      let audioUrl = lang === "Hindi" ? hindiAudioUrl : kannadaAudioUrl;
      
      if (!audioUrl && analysisResult) {
        const response = await apiClient.synthesizeSpeech(
          analysisResult.explanation,
          lang === "Hindi" ? "hi" : "kn"
        );
        
        audioUrl = response.audio_url;
        if (lang === "Hindi") {
          setHindiAudioUrl(audioUrl);
        } else {
          setKannadaAudioUrl(audioUrl);
        }
      }

      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.playbackRate = audioSpeed === "1x" ? 1 : 1.5;
        audio.play();
        
        audio.onended = () => {
          setPlayingLang(null);
        };
      }
    } catch (error) {
      console.error("Audio playback error:", error);
      setPlayingLang(null);
    }
  };

  return (
    <div className="min-h-screen relative">
      <div className="animated-gradient-bg" />
      <Navbar />

      <main className="pt-20 pb-20 px-4">
        <div className="container mx-auto max-w-3xl space-y-6">

          {/* Upload Section */}
          <GlassCard className="mt-4">
            <div className="flex items-center justify-between mb-5">
              <h2 className="font-display font-bold text-xl text-foreground flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary" />
                Upload Your Medical Report
              </h2>
              <button
                onClick={() => setLowBandwidth(!lowBandwidth)}
                className="glass-card flex items-center gap-1.5 px-3 py-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
              >
                {lowBandwidth ? <WifiOff className="w-3.5 h-3.5" /> : <Wifi className="w-3.5 h-3.5" />}
                {lowBandwidth ? "Low BW" : "Normal"}
              </button>
            </div>

            <AnimatePresence mode="wait">
              {step === "upload" && (
                <motion.div
                  key="upload"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div
                    onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                    onDragLeave={() => setDragOver(false)}
                    onDrop={handleDrop}
                    className={`border-2 border-dashed rounded-2xl p-10 text-center transition-colors cursor-pointer ${
                      dragOver ? "border-primary bg-primary/5" : "border-border hover:border-primary/40"
                    }`}
                  >
                    <input
                      type="file"
                      accept=".pdf,.jpg,.jpeg,.png"
                      onChange={handleFileInput}
                      className="hidden"
                      id="file-upload"
                    />
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <Upload className="w-10 h-10 mx-auto mb-3 text-muted-foreground" />
                      <p className="text-foreground font-medium mb-1">
                        Drag & drop your report here
                      </p>
                      <p className="text-sm text-muted-foreground">
                        or click to browse · PDF, JPG, PNG
                      </p>
                    </label>
                  </div>
                </motion.div>
              )}

              {step === "processing" && (
                <motion.div
                  key="processing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center py-12 gap-4"
                >
                  <Loader2 className="w-10 h-10 text-primary animate-spin" />
                  <p className="text-foreground font-medium">Processing your report…</p>
                  <p className="text-xs text-muted-foreground">Extracting text with OCR</p>
                  <div className="w-48 h-1.5 rounded-full bg-muted overflow-hidden">
                    <motion.div
                      className="h-full gradient-bg rounded-full"
                      initial={{ width: "0%" }}
                      animate={{ width: "100%" }}
                      transition={{ duration: 2.2, ease: "easeInOut" }}
                    />
                  </div>
                </motion.div>
              )}

              {step === "results" && (
                <motion.div
                  key="results-upload"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-3 p-4 rounded-xl bg-accent/10"
                >
                  <CheckCircle2 className="w-5 h-5 text-accent" />
                  <div>
                    <p className="text-sm font-medium text-foreground">Report processed successfully</p>
                    <p className="text-xs text-muted-foreground">
                      OCR Confidence: {documentStatus?.ocr_confidence?.toFixed(0) || 'Processing...'}%
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      setStep("upload");
                      setUploadResponse(null);
                      setDocumentStatus(null);
                      setAnalysisResult(null);
                      setSchemeResult(null);
                      setShowSchemes(false);
                    }}
                    className="ml-auto text-xs text-primary hover:underline"
                  >
                    Upload another
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </GlassCard>

          {/* Results — only show after processing */}
          {step === "results" && (
            <>
              {/* AI Explanation */}
              <GlassCard delay={0.1}>
                <h3 className="font-display font-bold text-lg mb-4 text-foreground flex items-center gap-2">
                  <Brain className="w-5 h-5 text-primary" />
                  Simplified Explanation
                  {isAnalyzing && <Loader2 className="w-4 h-4 animate-spin ml-2" />}
                </h3>
                {analysisResult ? (
                  <div className="space-y-3 text-sm leading-relaxed text-secondary-foreground">
                    {analysisResult.explanation.split('\n\n').map((paragraph, i) => (
                      <p key={i}>{paragraph}</p>
                    ))}
                  </div>
                ) : (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="w-6 h-6 animate-spin text-primary" />
                    <span className="ml-2 text-sm text-muted-foreground">Analyzing your report...</span>
                  </div>
                )}

                {/* Confidence Panel */}
                {analysisResult && (
                  <div className="mt-6 grid grid-cols-3 gap-3">
                    {[
                      { label: "AI Confidence", value: analysisResult.confidence },
                      { label: "OCR Accuracy", value: Math.round(analysisResult.ocr_confidence) },
                      { label: "Clarity", value: 72, text: "Medium" },
                    ].map((m) => (
                      <div key={m.label} className="text-center">
                        <p className="text-xs text-muted-foreground mb-1.5">{m.label}</p>
                        <div className="h-2 rounded-full bg-muted overflow-hidden">
                          <motion.div
                            className="h-full gradient-bg rounded-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${m.value}%` }}
                            transition={{ duration: 0.8, delay: 0.3 }}
                          />
                        </div>
                        <p className="text-xs text-foreground mt-1 font-medium">
                          {m.text || `${m.value}%`}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </GlassCard>

              {/* Questions for Doctor */}
              {analysisResult && (
                <GlassCard delay={0.2}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-display font-bold text-lg text-foreground flex items-center gap-2">
                      <MessageSquareText className="w-5 h-5 text-primary" />
                      Questions for Your Doctor
                    </h3>
                    <div className="flex gap-2">
                      <button 
                        onClick={() => {
                          navigator.clipboard.writeText(analysisResult.questions.join('\n'));
                        }}
                        className="glass-card p-2 hover:text-foreground text-muted-foreground transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                      <button className="glass-card p-2 hover:text-foreground text-muted-foreground transition-colors">
                        <Download className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  <ol className="space-y-3 text-sm text-secondary-foreground">
                    {analysisResult.questions.map((q, i) => (
                      <motion.li
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.4 + i * 0.08 }}
                        className="flex gap-3"
                      >
                        <span className="text-primary font-display font-bold">{i + 1}.</span>
                        <span>{q}</span>
                      </motion.li>
                    ))}
                  </ol>
                </GlassCard>
              )}

              {/* Audio Output */}
              {analysisResult && (
              <GlassCard delay={0.3}>
                <h3 className="font-display font-bold text-lg mb-5 text-foreground flex items-center gap-2">
                  <Volume2 className="w-5 h-5 text-primary" />
                  Listen in Your Language
                </h3>

                <div className="flex flex-col sm:flex-row gap-4">
                  {["Hindi", "Kannada"].map((lang) => {
                    const isPlaying = playingLang === lang;
                    return (
                      <button
                        key={lang}
                        onClick={() => playAudio(lang)}
                        className="flex-1 glass-card flex items-center gap-4 p-4 hover:border-primary/30 transition-all group"
                      >
                        <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center flex-shrink-0">
                          {isPlaying ? (
                            <Pause className="w-5 h-5 text-primary-foreground" />
                          ) : (
                            <Play className="w-5 h-5 text-primary-foreground ml-0.5" />
                          )}
                        </div>
                        <div className="flex-1 text-left">
                          <p className="text-sm font-medium text-foreground">Play in {lang}</p>
                          <WaveformVisualizer playing={isPlaying} />
                        </div>
                      </button>
                    );
                  })}
                </div>

                <div className="flex items-center gap-2 mt-4">
                  <span className="text-xs text-muted-foreground">Speed:</span>
                  {(["1x", "1.5x"] as const).map((s) => (
                    <button
                      key={s}
                      onClick={() => setAudioSpeed(s)}
                      className={`text-xs px-3 py-1 rounded-full transition-colors ${
                        audioSpeed === s
                          ? "gradient-bg text-primary-foreground font-medium"
                          : "glass-card text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </GlassCard>
              )}

              {/* Scheme Matching */}
              <GlassCard delay={0.4}>
                <h3 className="font-display font-bold text-lg mb-5 text-foreground flex items-center gap-2">
                  <Landmark className="w-5 h-5 text-primary" />
                  Government Scheme Matching
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
                  <div>
                    <label className="text-xs text-muted-foreground mb-1.5 block">State</label>
                    <select
                      value={schemeState}
                      onChange={(e) => setSchemeState(e.target.value)}
                      className="w-full glass-card bg-secondary p-3 rounded-xl text-sm text-foreground border-none outline-none"
                    >
                      <option>Karnataka</option>
                      <option>Maharashtra</option>
                      <option>Tamil Nadu</option>
                      <option>Uttar Pradesh</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1.5 block">Income Range</label>
                    <select
                      value={schemeIncome}
                      onChange={(e) => setSchemeIncome(e.target.value)}
                      className="w-full glass-card bg-secondary p-3 rounded-xl text-sm text-foreground border-none outline-none"
                    >
                      <option value="below-1l">Below ₹1,00,000</option>
                      <option value="1l-3l">₹1,00,000 – ₹3,00,000</option>
                      <option value="3l-5l">₹3,00,000 – ₹5,00,000</option>
                      <option value="above-5l">Above ₹5,00,000</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1.5 block">Age</label>
                    <input
                      type="number"
                      value={schemeAge}
                      onChange={(e) => setSchemeAge(e.target.value)}
                      className="w-full glass-card bg-secondary p-3 rounded-xl text-sm text-foreground border-none outline-none"
                      placeholder="Enter age"
                    />
                  </div>
                  <div className="flex items-end">
                    <button
                      onClick={() => setSchemeBpl(!schemeBpl)}
                      className={`w-full p-3 rounded-xl text-sm font-medium transition-colors ${
                        schemeBpl
                          ? "gradient-bg text-primary-foreground"
                          : "glass-card text-muted-foreground"
                      }`}
                    >
                      {schemeBpl ? "BPL Card Holder ✓" : "APL (No BPL Card)"}
                    </button>
                  </div>
                </div>

                <button
                  onClick={findEligibleSchemes}
                  className="btn-primary-gradient w-full py-3 text-sm font-semibold"
                >
                  Find Eligible Schemes
                </button>

                <AnimatePresence>
                  {showSchemes && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-5 space-y-4 overflow-hidden"
                    >
                      {schemeResult?.schemes.map((scheme, i) => (
                        <motion.div
                          key={scheme.id}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="glass-card p-4 space-y-2"
                        >
                          <h4 className="font-display font-semibold text-foreground">{scheme.name}</h4>
                          <p className="text-xs text-accent"><span className="font-medium">Eligible because:</span> {scheme.match_reason}</p>
                          <p className="text-xs text-muted-foreground"><span className="font-medium text-secondary-foreground">Documents needed:</span> {scheme.documents_required.join(', ')}</p>
                          <a
                            href={scheme.apply_link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block text-xs text-primary hover:underline mt-1"
                          >
                            Apply Now →
                          </a>
                        </motion.div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </GlassCard>
            </>
          )}
        </div>
      </main>

      <DisclaimerBar />
    </div>
  );
};

export default UploadPage;
