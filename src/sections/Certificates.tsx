'use client';

import { motion } from 'framer-motion';
import { Award, ExternalLink, Calendar, CheckCircle2 } from 'lucide-react';

// Mock Certificates Data - User can edit this later
const certificates = [
    {
        title: 'TensorFlow Developer Certificate',
        issuer: 'Google',
        date: '2024',
        id: 'Credential ID: 12345678',
        link: '#',
        image: 'https://placehold.co/600x400/1a1a2e/00ff88?text=TensorFlow+Cert',
        skills: ['Deep Learning', 'Computer Vision', 'NLP']
    },
    {
        title: 'Professional Data Engineer',
        issuer: 'Google Cloud',
        date: '2023',
        id: 'Credential ID: 87654321',
        link: '#',
        image: 'https://placehold.co/600x400/1a1a2e/3b82f6?text=GCP+Data+Engineer',
        skills: ['BigQuery', 'Dataflow', 'Cloud SQL']
    },
    {
        title: 'IBM Data Science Professional',
        issuer: 'Coursera',
        date: '2023',
        id: 'Credential ID: ABCDEFGH',
        link: '#',
        image: 'https://placehold.co/600x400/1a1a2e/007aff?text=IBM+Data+Science',
        skills: ['Python', 'SQL', 'Data Visualization']
    },
    {
        title: 'Deep Learning Specialization',
        issuer: 'DeepLearning.AI',
        date: '2022',
        id: 'Credential ID: XYZ12345',
        link: '#',
        image: 'https://placehold.co/600x400/1a1a2e/ff0055?text=DeepLearning.AI',
        skills: ['Neural Networks', 'Hyperparameter Tuning']
    }
];

export default function Certificates() {
    return (
        <section id="certificates" className="py-24 px-6 relative overflow-hidden">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <motion.div
                    className="text-center mb-16"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                >
                    <motion.span
                        className="text-accent font-mono text-sm uppercase tracking-widest"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        Credentials
                    </motion.span>
                    <h2 className="section-title mt-4">
                        Licenses & <span className="gradient-text">Certifications</span>
                    </h2>
                </motion.div>

                {/* Grid */}
                <div className="grid md:grid-cols-2 gap-6">
                    {certificates.map((cert, index) => (
                        <motion.div
                            key={index}
                            className="glass-card p-6 group relative overflow-hidden"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ y: -5 }}
                        >
                            {/* Certificate Image Preview */}
                            <div className="relative h-40 mb-6 rounded-lg overflow-hidden group-hover:shadow-lg transition-all">
                                <img
                                    src={cert.image}
                                    alt={cert.title}
                                    className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                            </div>

                            <div className="flex items-start justify-between mb-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center text-accent">
                                        <Award className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-lg group-hover:text-accent transition-colors">
                                            {cert.title}
                                        </h3>
                                        <p className="text-sm text-foreground-muted">{cert.issuer}</p>
                                    </div>
                                </div>
                                <span className="text-xs font-mono text-foreground-muted bg-foreground/5 px-2 py-1 rounded">
                                    {cert.date}
                                </span>
                            </div>

                            <p className="text-xs text-foreground-muted mb-4 font-mono">
                                {cert.id}
                            </p>

                            {/* Skills */}
                            <div className="flex flex-wrap gap-2 mb-4">
                                {cert.skills.map((skill) => (
                                    <span
                                        key={skill}
                                        className="text-xs px-2 py-0.5 rounded-full border border-white/10 text-foreground-muted group-hover:border-accent/30 transition-colors"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>

                            {/* Link */}
                            <a
                                href={cert.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 text-sm font-medium text-accent hover:underline"
                            >
                                Show Credential <ExternalLink className="w-3 h-3" />
                            </a>

                            {/* Decorative Gradient on Hover */}
                            <div
                                className="absolute inset-0 opacity-0 group-hover:opacity-10 pointer-events-none transition-opacity duration-500"
                                style={{
                                    background: 'linear-gradient(45deg, transparent, var(--accent), transparent)'
                                }}
                            />
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
