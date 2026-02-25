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

type Step = "upload" | "processing" | "results";

const UploadPage = () => {
  const [step, setStep] = useState<Step>("upload");
  const [lowBandwidth, setLowBandwidth] = useState(false);
  const [playingLang, setPlayingLang] = useState<string | null>(null);
  const [audioSpeed, setAudioSpeed] = useState<"1x" | "1.5x">("1x");
  const [dragOver, setDragOver] = useState(false);

  // Scheme matching state
  const [schemeState, setSchemeState] = useState("Karnataka");
  const [schemeIncome, setSchemeIncome] = useState("below-1l");
  const [schemeAge, setSchemeAge] = useState("30");
  const [schemeBpl, setSchemeBpl] = useState(true);
  const [showSchemes, setShowSchemes] = useState(false);

  const simulateUpload = () => {
    setStep("processing");
    setTimeout(() => setStep("results"), 2500);
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
                    onDrop={(e) => { e.preventDefault(); setDragOver(false); simulateUpload(); }}
                    className={`border-2 border-dashed rounded-2xl p-10 text-center transition-colors cursor-pointer ${
                      dragOver ? "border-primary bg-primary/5" : "border-border hover:border-primary/40"
                    }`}
                    onClick={simulateUpload}
                  >
                    <Upload className="w-10 h-10 mx-auto mb-3 text-muted-foreground" />
                    <p className="text-foreground font-medium mb-1">
                      Drag & drop your report here
                    </p>
                    <p className="text-sm text-muted-foreground">
                      or click to browse · PDF, JPG, PNG
                    </p>
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
                    <p className="text-xs text-muted-foreground">OCR Confidence: 94%</p>
                  </div>
                  <button
                    onClick={() => setStep("upload")}
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
                </h3>
                <div className="space-y-3 text-sm leading-relaxed text-secondary-foreground">
                  <p>
                    Your blood test results are mostly within normal range. Your <span className="text-primary font-medium">hemoglobin level is 12.8 g/dL</span>, which is within healthy limits.
                  </p>
                  <p>
                    Your <span className="text-primary font-medium">blood sugar (fasting)</span> is at 110 mg/dL — slightly above the standard 100 mg/dL threshold. This is considered <span className="text-accent font-medium">pre-diabetic range</span> and worth discussing with your doctor.
                  </p>
                  <p>
                    All other values including liver function and kidney function markers appear normal.
                  </p>
                </div>

                {/* Confidence Panel */}
                <div className="mt-6 grid grid-cols-3 gap-3">
                  {[
                    { label: "AI Confidence", value: 87 },
                    { label: "OCR Accuracy", value: 94 },
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
              </GlassCard>

              {/* Questions for Doctor */}
              <GlassCard delay={0.2}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-display font-bold text-lg text-foreground flex items-center gap-2">
                    <MessageSquareText className="w-5 h-5 text-primary" />
                    Questions for Your Doctor
                  </h3>
                  <div className="flex gap-2">
                    <button className="glass-card p-2 hover:text-foreground text-muted-foreground transition-colors">
                      <Copy className="w-4 h-4" />
                    </button>
                    <button className="glass-card p-2 hover:text-foreground text-muted-foreground transition-colors">
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <ol className="space-y-3 text-sm text-secondary-foreground">
                  {[
                    "My fasting blood sugar is 110 mg/dL. Should I be concerned about pre-diabetes?",
                    "What lifestyle changes would you recommend to bring my blood sugar within range?",
                    "Should I get an HbA1c test to confirm my average blood sugar levels?",
                    "Are there any dietary restrictions I should follow based on these results?",
                    "How soon should I get my blood tested again for follow-up?",
                  ].map((q, i) => (
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

              {/* Audio Output */}
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
                        onClick={() => setPlayingLang(isPlaying ? null : lang)}
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
                  onClick={() => setShowSchemes(true)}
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
                      {[
                        {
                          name: "Ayushman Bharat (PM-JAY)",
                          reason: "BPL household with income below ₹1,00,000",
                          docs: "Aadhaar Card, BPL Certificate, Income Certificate",
                          link: "https://pmjay.gov.in",
                        },
                        {
                          name: "Vajpayee Arogyashree",
                          reason: "Karnataka resident with BPL card",
                          docs: "BPL Card, Aadhaar, State Domicile",
                          link: "https://arogya.karnataka.gov.in",
                        },
                      ].map((scheme, i) => (
                        <motion.div
                          key={scheme.name}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="glass-card p-4 space-y-2"
                        >
                          <h4 className="font-display font-semibold text-foreground">{scheme.name}</h4>
                          <p className="text-xs text-accent"><span className="font-medium">Eligible because:</span> {scheme.reason}</p>
                          <p className="text-xs text-muted-foreground"><span className="font-medium text-secondary-foreground">Documents needed:</span> {scheme.docs}</p>
                          <a
                            href={scheme.link}
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
