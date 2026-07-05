'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Download, CheckCircle, Github, Linkedin, Mail, Instagram, Printer } from 'lucide-react';

const contactReasons = [
    { value: 'hire', label: 'Hire you', emoji: '' },
    { value: 'collaborate', label: 'Collaborate', emoji: '' },
    { value: 'ihsg', label: 'Discuss IHSG strategies', emoji: '' },
    { value: 'hello', label: 'Just say hi', emoji: '' },
];

const socialLinks = [
    { icon: Github, label: 'GitHub', href: 'https://github.com/wheldnz', color: '#333' },
    { icon: Linkedin, label: 'LinkedIn', href: 'https://www.linkedin.com/in/wildan-nuril/', color: '#0077b5' },
    { icon: Instagram, label: 'Instagram', href: 'https://instagram.com/wheldnz', color: '#E1306C' },
    { icon: Mail, label: 'Email', href: 'mailto:wildanuril99@gmail.com', color: '#ea4335' },
];

export default function Contact() {
    const [formState, setFormState] = useState({
        name: '',
        email: '',
        reason: '',
        message: '',
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const res = await fetch('https://formspree.io/f/mbdkkbod', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formState),
            });

            if (res.ok) {
                setIsSubmitted(true);
                setTimeout(() => {
                    setIsSubmitted(false);
                    setFormState({ name: '', email: '', reason: '', message: '' });
                }, 3000);
            } else {
                alert('Something went wrong. Please try again later.');
            }
        } catch (error) {
            console.error(error);
            alert('Failed to send message.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <section id="contact" className="py-24 px-6">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
                <motion.div
                    className="text-center mb-16"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                >
                    <span className="text-accent font-mono text-sm uppercase tracking-widest">
                        The Vault
                    </span>
                    <h2 className="section-title mt-4">
                        Let&apos;s <span className="gradient-text">Connect</span>
                    </h2>
                    <p className="text-foreground-muted mt-4 max-w-xl mx-auto">
                        Whether you want to collaborate, hire, or just chat about IHSG strategies—
                        I&apos;d love to hear from you.
                    </p>
                </motion.div>

                <div className="grid lg:grid-cols-2 gap-12">
                    {/* Left Column - Contact Form */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        <div className="glass-card p-8">
                            <AnimatePresence mode="wait">
                                {isSubmitted ? (
                                    <motion.div
                                        key="success"
                                        className="flex flex-col items-center justify-center py-12 text-center"
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.8 }}
                                    >
                                        <motion.div
                                            initial={{ scale: 0 }}
                                            animate={{ scale: 1 }}
                                            transition={{ type: 'spring', stiffness: 200 }}
                                        >
                                            <CheckCircle className="w-16 h-16 text-accent mb-4" />
                                        </motion.div>
                                        <h3 className="text-xl font-bold mb-2">Message Sent!</h3>
                                        <p className="text-foreground-muted">
                                            I&apos;ll get back to you as soon as possible.
                                        </p>
                                    </motion.div>
                                ) : (
                                    <motion.form
                                        key="form"
                                        onSubmit={handleSubmit}
                                        className="space-y-6"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        exit={{ opacity: 0 }}
                                    >
                                        {/* Name */}
                                        <div>
                                            <label className="text-sm font-medium block mb-2">
                                                Name
                                            </label>
                                            <input
                                                type="text"
                                                required
                                                value={formState.name}
                                                onChange={(e) => setFormState({ ...formState, name: e.target.value })}
                                                className="w-full px-4 py-3 rounded-xl bg-background border border-card-border focus:border-accent focus:outline-none transition-colors"
                                                placeholder="Your name"
                                            />
                                        </div>

                                        {/* Email */}
                                        <div>
                                            <label className="text-sm font-medium block mb-2">
                                                Email
                                            </label>
                                            <input
                                                type="email"
                                                required
                                                value={formState.email}
                                                onChange={(e) => setFormState({ ...formState, email: e.target.value })}
                                                className="w-full px-4 py-3 rounded-xl bg-background border border-card-border focus:border-accent focus:outline-none transition-colors"
                                                placeholder="you@example.com"
                                            />
                                        </div>

                                        {/* Reason Dropdown */}
                                        <div>
                                            <label className="text-sm font-medium block mb-2">
                                                I want to...
                                            </label>
                                            <select
                                                required
                                                value={formState.reason}
                                                onChange={(e) => setFormState({ ...formState, reason: e.target.value })}
                                                className="w-full px-4 py-3 rounded-xl bg-background border border-card-border focus:border-accent focus:outline-none transition-colors cursor-pointer"
                                            >
                                                <option value="">Select a reason</option>
                                                {contactReasons.map((reason) => (
                                                    <option key={reason.value} value={reason.value}>
                                                        {reason.label}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>

                                        {/* Message */}
                                        <div>
                                            <label className="text-sm font-medium block mb-2">
                                                Message
                                            </label>
                                            <textarea
                                                required
                                                rows={4}
                                                value={formState.message}
                                                onChange={(e) => setFormState({ ...formState, message: e.target.value })}
                                                className="w-full px-4 py-3 rounded-xl bg-background border border-card-border focus:border-accent focus:outline-none transition-colors resize-none"
                                                placeholder="Your message..."
                                            />
                                        </div>

                                        {/* Submit Button */}
                                        <motion.button
                                            type="submit"
                                            disabled={isSubmitting}
                                            className="btn-primary w-full flex items-center justify-center gap-2"
                                            whileHover={{ scale: 1.02 }}
                                            whileTap={{ scale: 0.98 }}
                                        >
                                            {isSubmitting ? (
                                                <>
                                                    <motion.div
                                                        className="w-5 h-5 border-2 border-background border-t-transparent rounded-full"
                                                        animate={{ rotate: 360 }}
                                                        transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                                                    />
                                                    Sending...
                                                </>
                                            ) : (
                                                <>
                                                    <Send className="w-4 h-4" />
                                                    Send Message
                                                </>
                                            )}
                                        </motion.button>
                                    </motion.form>
                                )}
                            </AnimatePresence>
                        </div>
                    </motion.div>

                    {/* Right Column - Resume & Social */}
                    <motion.div
                        initial={{ opacity: 0, x: 30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="space-y-8"
                    >
                        {/* Resume Download */}
                        <div className="glass-card p-8">
                            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                                <span className="text-accent"></span>
                                Resume
                            </h3>
                            <p className="text-foreground-muted mb-6">
                                Download my ATS-friendly resume for a detailed look at my experience,
                                skills, and education.
                            </p>
                            <div className="flex flex-wrap gap-4">
                                <motion.a
                                    href="/resume.pdf"
                                    download
                                    className="btn-primary inline-flex items-center gap-2"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                >
                                    <Download className="w-4 h-4" />
                                    Download PDF
                                </motion.a>
                                <motion.a
                                    href="/print-portfolio"
                                    className="btn-secondary inline-flex items-center gap-2"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                >
                                    <Printer className="w-4 h-4" />
                                    Print CV/Portfolio
                                </motion.a>
                            </div>
                        </div>

                        {/* Social Links */}
                        <div className="glass-card p-8">
                            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                                <span className="text-accent"></span>
                                Connect Elsewhere
                            </h3>
                            <div className="grid grid-cols-2 gap-4">
                                {socialLinks.map((social) => (
                                    <motion.a
                                        key={social.label}
                                        href={social.href}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="glass-card p-4 flex items-center gap-3 hover:bg-accent/10 transition-colors"
                                        whileHover={{ scale: 1.05, x: 5 }}
                                        whileTap={{ scale: 0.95 }}
                                    >
                                        <social.icon
                                            className="w-5 h-5"
                                            style={{ color: social.color }}
                                        />
                                        <span className="font-medium text-sm">{social.label}</span>
                                    </motion.a>
                                ))}
                            </div>
                        </div>

                        {/* Fun Fact */}
                        <motion.div
                            className="glass-card p-6 text-center"
                            whileHover={{ scale: 1.02 }}
                        >
                            <p className="text-sm text-foreground-muted">
                                <span className="text-2xl block mb-2"></span>
                                Probability of me replying: <span className="text-accent font-mono font-bold">0.98</span>
                                <br />
                                <span className="text-xs">(The other 0.02 is when I&apos;m debugging)</span>
                            </p>
                        </motion.div>
                    </motion.div>
                </div>

                {/* Footer */}
                <motion.footer
                    className="mt-24 pt-8 border-t border-card-border text-center text-foreground-muted text-sm"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                >
                    <p>
                        Built with <span className="text-accent">Next.js</span> & <span className="text-accent">Framer Motion</span>
                    </p>
                    <p className="mt-2 font-mono text-xs">
                        © 2026 • Made with ∑ rigor and caffeine
                    </p>
                </motion.footer>
            </div>
        </section>
    );
}
