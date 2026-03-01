import { motion } from "framer-motion";
import { Shield, Lock, Eye, Database, Trash2, Mail } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import GlassCard from "@/components/GlassCard";

const Privacy = () => {
  const sections = [
    {
      icon: Shield,
      title: "Data Protection Commitment",
      content: "AccessAI is committed to protecting your personal health information. We use industry-standard encryption and security measures to ensure your data remains safe and confidential. Your trust is our top priority."
    },
    {
      icon: Lock,
      title: "Secure Data Transmission",
      content: "All data transmitted between your device and our servers is encrypted using TLS (Transport Layer Security) protocol. We never transmit unencrypted personal health information over the internet."
    },
    {
      icon: Eye,
      title: "Information We Collect",
      content: "We collect only the information necessary to provide our services: medical reports you upload (for analysis), basic profile information for scheme matching, and usage data to improve our services. We do not collect unnecessary personal data."
    },
    {
      icon: Database,
      title: "How We Use Your Data",
      content: "Your data is used exclusively to: analyze your medical reports and provide explanations, generate relevant questions for doctor consultations, match you with eligible government healthcare schemes, and improve our AI models (anonymized data only)."
    },
    {
      icon: Trash2,
      title: "Data Retention & Deletion",
      content: "You have full control over your data. You can request deletion of your medical reports and associated analysis at any time. By default, uploaded documents are automatically deleted after 30 days of inactivity. You can also delete your account and all associated data instantly."
    },
    {
      icon: Mail,
      title: "Your Rights",
      content: "You have the right to: access your personal data, request corrections to inaccurate data, request deletion of your data, object to processing of your data, and export your data in a portable format. To exercise these rights, contact us at privacy@accessai.health"
    }
  ];

  return (
    <div className="min-h-screen relative">
      <div className="animated-gradient-bg" />
      <Navbar />

      {/* Hero Section */}
      <section className="pt-28 pb-16 px-4">
        <div className="container mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-3xl mx-auto"
          >
            <div className="w-20 h-20 rounded-2xl gradient-bg flex items-center justify-center mx-auto mb-6">
              <Shield className="w-10 h-10 text-primary-foreground" />
            </div>
            <h1 className="font-display font-bold text-3xl sm:text-5xl lg:text-6xl leading-tight mb-6">
              Privacy <span className="gradient-text">Policy</span>
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground leading-relaxed">
              Your privacy is fundamental to our mission. This policy explains how we collect, 
              use, protect, and respect your personal health information.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Last Updated */}
      <section className="py-8 px-4">
        <div className="container mx-auto text-center">
          <p className="text-muted-foreground">
            <span className="font-semibold text-foreground">Last Updated:</span> March 2026
          </p>
        </div>
      </section>

      {/* Privacy Sections */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-4xl">
          {sections.map((section, i) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="mb-8"
            >
              <GlassCard className="p-6 sm:p-8">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl gradient-bg-subtle flex items-center justify-center flex-shrink-0">
                    <section.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="font-display text-xl font-semibold mb-3">{section.title}</h2>
                    <p className="text-muted-foreground leading-relaxed">{section.content}</p>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Data Sharing */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <GlassCard className="p-6 sm:p-8">
              <h2 className="font-display text-xl font-semibold mb-4">Data Sharing</h2>
              <p className="text-muted-foreground leading-relaxed mb-4">
                AccessAI does <span className="font-semibold text-foreground">NOT</span> sell, trade, or rent your personal health information to third parties. Your data is never shared with:
              </p>
              <ul className="list-disc list-inside text-muted-foreground space-y-2 ml-2">
                <li>Insurance companies</li>
                <li>Employers or potential employers</li>
                <li>Advertising networks</li>
                <li>Third-party marketing companies</li>
              </ul>
              <p className="text-muted-foreground leading-relaxed mt-4">
                We may only share anonymized, aggregated data for research and public health purposes, which cannot be traced back to any individual.
              </p>
            </GlassCard>
          </motion.div>
        </div>
      </section>

      {/* Compliance */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <GlassCard className="p-6 sm:p-8">
              <h2 className="font-display text-xl font-semibold mb-4">Regulatory Compliance</h2>
              <p className="text-muted-foreground leading-relaxed mb-4">
                AccessAI is committed to complying with applicable data protection laws and regulations, including:
              </p>
              <ul className="list-disc list-inside text-muted-foreground space-y-2 ml-2">
                <li>Digital Personal Data Protection Act (DPDPA) - India</li>
                <li>General Data Protection Regulation (GDPR) - European Union</li>
                <li>Health Insurance Portability and Accountability Act (HIPAA) - United States</li>
              </ul>
              <p className="text-muted-foreground leading-relaxed mt-4">
                Our infrastructure and processes are designed to meet or exceed the requirements of these regulations.
              </p>
            </GlassCard>
          </motion.div>
        </div>
      </section>

      {/* Contact */}
      <section className="py-16 px-4">
        <div className="container mx-auto text-center max-w-2xl">
          <GlassCard className="p-8">
            <h2 className="font-display text-xl font-semibold mb-4">Questions or Concerns?</h2>
            <p className="text-muted-foreground mb-6">
              If you have any questions about this Privacy Policy or want to exercise your data rights, 
              please contact our Data Protection Officer.
            </p>
            <a 
              href="mailto:privacy@accessai.health"
              className="btn-primary-gradient inline-flex items-center gap-2 px-6 py-3 font-semibold"
            >
              <Mail className="w-4 h-4" />
              privacy@accessai.health
            </a>
          </GlassCard>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Privacy;
