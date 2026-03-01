import { motion } from "framer-motion";
import { Mail, Phone, MapPin, MessageSquare, Clock, HeadphonesIcon } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import GlassCard from "@/components/GlassCard";

const Contact = () => {
  const contactMethods = [
    {
      icon: Mail,
      title: "Email Us",
      description: "Send us an email anytime",
      value: "support@accessai.health",
      action: "mailto:support@accessai.health",
      available: "24/7"
    },
    {
      icon: Phone,
      title: "Call Us",
      description: "Speak with our support team",
      value: "+91 1800-XXX-XXXX",
      action: "tel:+911800XXXXXXX",
      available: "Mon-Fri: 9AM-6PM IST"
    },
    {
      icon: MessageSquare,
      title: "Live Chat",
      description: "Chat with us in real-time",
      value: "Start Chat",
      action: "#",
      available: "Mon-Fri: 9AM-9PM IST"
    }
  ];

  const officeLocations = [
    {
      city: "Bangalore",
      address: "AccessAI Technologies Pvt. Ltd.",
      details: "Innovation Hub, Tech Park\nBangalore, Karnataka 560001"
    },
    {
      city: "Hyderabad",
      address: "AccessAI Research Center",
      details: "Health Tech Incubator\nHyderabad, Telangana 500081"
    }
  ];

  const faqs = [
    {
      question: "What are your support hours?",
      answer: "Our support team is available Monday through Friday, 9 AM to 6 PM IST. For urgent matters outside these hours, you can email us and we'll respond within 24 hours."
    },
    {
      question: "How quickly will I get a response?",
      answer: "We aim to respond to all inquiries within 24 hours. During business hours, most emails are answered within 4-6 hours."
    },
    {
      question: "Can I get help in my local language?",
      answer: "Yes! Our support team can assist you in Hindi, Kannada, English, and several other regional languages. Just let us know your preferred language."
    },
    {
      question: "How do I report a technical issue?",
      answer: "Please email support@accessai.health with details about the issue, including any error messages, your device type, and steps to reproduce the problem. Attach screenshots if possible."
    },
    {
      question: "Is there a community forum?",
      answer: "Yes! Join our community forum to connect with other users, share experiences, and get peer support. Access it through our website."
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
              <HeadphonesIcon className="w-10 h-10 text-primary-foreground" />
            </div>
            <h1 className="font-display font-bold text-3xl sm:text-5xl lg:text-6xl leading-tight mb-6">
              Get in <span className="gradient-text">Touch</span>
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground leading-relaxed">
              Have questions? We'd love to hear from you. Our team is here to help 
              and support you on your healthcare journey.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-5xl">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {contactMethods.map((method, i) => (
              <motion.div
                key={method.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <GlassCard hover className="p-6 text-center h-full">
                  <div className="w-14 h-14 rounded-xl gradient-bg flex items-center justify-center mx-auto mb-4">
                    <method.icon className="w-7 h-7 text-primary-foreground" />
                  </div>
                  <h3 className="font-display font-semibold text-lg mb-2">{method.title}</h3>
                  <p className="text-sm text-muted-foreground mb-3">{method.description}</p>
                  <a
                    href={method.action}
                    className="text-primary font-semibold hover:underline"
                  >
                    {method.value}
                  </a>
                  <p className="text-xs text-muted-foreground mt-3 flex items-center justify-center gap-1">
                    <Clock className="w-3 h-3" />
                    {method.available}
                  </p>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Office Locations */}
      <section className="py-16 px-4 bg-card/30">
        <div className="container mx-auto max-w-4xl">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-display text-2xl sm:text-3xl font-bold text-center mb-12"
          >
            Our <span className="gradient-text">Offices</span>
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {officeLocations.map((office, i) => (
              <motion.div
                key={office.city}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <GlassCard className="p-6">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl gradient-bg-subtle flex items-center justify-center flex-shrink-0">
                      <MapPin className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-display font-semibold text-lg mb-2">{office.city}</h3>
                      <p className="font-semibold text-foreground mb-1">{office.address}</p>
                      <p className="text-muted-foreground text-sm whitespace-pre-line">{office.details}</p>
                    </div>
                  </div>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-4xl">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="font-display text-2xl sm:text-3xl font-bold text-center mb-12"
          >
            Frequently Asked <span className="gradient-text">Questions</span>
          </motion.h2>

          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <motion.div
                key={faq.question}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
              >
                <GlassCard className="p-5">
                  <h3 className="font-display font-semibold mb-2">{faq.question}</h3>
                  <p className="text-muted-foreground text-sm">{faq.answer}</p>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feedback */}
      <section className="py-16 px-4">
        <div className="container mx-auto text-center max-w-2xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <GlassCard className="p-8">
              <h2 className="font-display text-xl font-semibold mb-4">We Value Your Feedback</h2>
              <p className="text-muted-foreground mb-6">
                Help us improve AccessAI! Share your feedback, suggestions, or report any issues 
                to help us serve you better.
              </p>
              <a
                href="mailto:feedback@accessai.health"
                className="btn-primary-gradient inline-flex items-center gap-2 px-6 py-3 font-semibold"
              >
                <Mail className="w-4 h-4" />
                Send Feedback
              </a>
            </GlassCard>
          </motion.div>
        </div>
      </section>

      {/* Emergency Notice */}
      <section className="pb-16 px-4">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <GlassCard className="p-6 border-l-4 border-l-red-500 bg-red-500/5">
              <h3 className="font-display font-semibold text-red-500 mb-2">Medical Emergency?</h3>
              <p className="text-muted-foreground text-sm">
                If you're experiencing a medical emergency, please call your local emergency number 
                immediately. AccessAI support cannot assist with medical emergencies.
              </p>
            </GlassCard>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Contact;
