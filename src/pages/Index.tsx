import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  FileUp, Brain, MessageSquareText, Volume2, Landmark, Wifi,
  ShieldCheck, Languages, Zap
} from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import DisclaimerBar from "@/components/DisclaimerBar";
import GlassCard from "@/components/GlassCard";
import VoicePulse from "@/components/VoicePulse";

const features = [
  { icon: FileUp, title: "Upload Medical Reports", desc: "Securely upload PDFs, images of lab results, prescriptions, and more." },
  { icon: Brain, title: "AI Explanation with Confidence", desc: "Get plain-language summaries with transparency on AI certainty levels." },
  { icon: MessageSquareText, title: "Doctor Questions Generator", desc: "Auto-generated questions to help you have better conversations with your doctor." },
  { icon: Volume2, title: "Audio Output", desc: "Listen to explanations in Hindi & Kannada with natural voice synthesis." },
  { icon: Landmark, title: "Government Scheme Matching", desc: "Discover healthcare schemes you're eligible for based on your profile." },
  { icon: Wifi, title: "Low Bandwidth Mode", desc: "Optimized for 2G/3G connections and low-end devices." },
];

const whyItems = [
  { icon: ShieldCheck, title: "Reduces Confusion", desc: "Medical jargon is simplified into everyday language so you always understand what's going on." },
  { icon: Languages, title: "Breaks Language Barriers", desc: "Get information in your preferred language — no more guessing what your reports say." },
  { icon: Zap, title: "Speeds Up Decisions", desc: "Know what to ask, what schemes apply, and what steps to take — faster." },
];

const stagger = { hidden: {}, visible: { transition: { staggerChildren: 0.1 } } };
const fadeUp = { hidden: { opacity: 0, y: 24 }, visible: { opacity: 1, y: 0, transition: { duration: 0.5 } } };

const Index = () => {
  return (
    <div className="min-h-screen relative">
      <div className="animated-gradient-bg" />
      <Navbar />

      {/* Hero */}
      <section className="pt-28 pb-20 sm:pt-36 sm:pb-28 px-4">
        <div className="container mx-auto flex flex-col items-center text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <VoicePulse size={80} />
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="font-display font-bold text-3xl sm:text-5xl lg:text-6xl leading-tight max-w-3xl mb-5"
          >
            Understand Your Medical Reports.{" "}
            <span className="gradient-text">In Your Language. Instantly.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="text-lg sm:text-xl text-muted-foreground max-w-xl mb-10"
          >
            AI-powered report simplification and healthcare scheme guidance for everyone.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.55 }}
          >
            <Link
              to="/upload"
              className="btn-primary-gradient inline-flex items-center gap-2 px-8 py-4 text-lg font-semibold"
            >
              Start Now
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-display text-2xl sm:text-3xl font-bold text-center mb-12"
          >
            Everything You Need
          </motion.h2>

          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-80px" }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5"
          >
            {features.map((f, i) => (
              <motion.div key={f.title} variants={fadeUp}>
                <GlassCard hover delay={0} className="h-full">
                  <div className="w-11 h-11 rounded-xl gradient-bg-subtle flex items-center justify-center mb-4">
                    <f.icon className="w-5 h-5 text-primary" />
                  </div>
                  <h3 className="font-display font-semibold text-lg mb-2 text-foreground">{f.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Why AccessAI */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-display text-2xl sm:text-3xl font-bold text-center mb-12"
          >
            Why <span className="gradient-text">AccessAI</span>?
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {whyItems.map((item, i) => (
              <GlassCard key={item.title} delay={i * 0.15} className="text-center">
                <div className="w-14 h-14 rounded-2xl gradient-bg-subtle flex items-center justify-center mx-auto mb-5">
                  <item.icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="font-display font-semibold text-lg mb-3 text-foreground">{item.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
              </GlassCard>
            ))}
          </div>
        </div>
      </section>

      <Footer />
      <DisclaimerBar />
    </div>
  );
};

export default Index;
