'use client';

import { motion } from 'framer-motion';
import BentoGrid, { BentoItem } from '../components/BentoGrid';
import Journey from '../components/Journey';
import {
    Braces,
    Database,
    LineChart,
    Binary,
    BarChart3,
    Sigma,
    Table2,
    Code2,
    Palette,
    FileCode2,
    Cloud,
    Terminal
} from 'lucide-react';

const techStack = [
    { icon: Braces, label: 'Python', color: '#3776ab' },
    { icon: Database, label: 'SQL (Postgres/MySQL)', color: '#f29111' },
    { icon: BarChart3, label: 'Power BI', color: '#f2c811' },
    { icon: Cloud, label: 'AWS', color: '#ff9900' },
    { icon: Database, label: 'Google BigQuery', color: '#4285f4' },
    { icon: FileCode2, label: 'PHP', color: '#777BB4' },
    { icon: Binary, label: 'TypeScript', color: '#3178c6' },
    { icon: Binary, label: 'React / Next.js', color: '#00D8FF' },
    { icon: Code2, label: 'Google Apps Script', color: '#34a853' },
    { icon: Sigma, label: 'Pandas & NumPy', color: '#150458' },
    { icon: Table2, label: 'Excel', color: '#217346' },
    { icon: Palette, label: 'HTML & CSS', color: '#E34F26' },
];

export default function About() {
    return (
        <section id="about" className="py-24 px-6 bg-background-secondary/50">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
                <motion.div
                    className="text-center mb-16"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                >
                    <span className="text-accent font-mono text-sm uppercase tracking-widest">
                        The Person
                    </span>
                    <h2 className="section-title mt-4">
                        About <span className="gradient-text">Me</span>
                    </h2>
                </motion.div>

                <div className="grid lg:grid-cols-2 gap-12 items-start">
                    {/* Left Column - Story */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        {/* Profile Card */}
                        <div className="glass-card p-8 mb-8">
                            <div className="flex items-start gap-6 mb-6">
                                <motion.div
                                    className="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent to-accent-secondary flex items-center justify-center text-3xl font-bold text-background shrink-0"
                                    whileHover={{ rotate: 5, scale: 1.05 }}
                                >
                                    W
                                </motion.div>
                                <div>
                                    <h3 className="text-2xl font-bold mb-1">M. Wildan Nuril Akmal</h3>
                                    <p className="text-accent font-mono text-sm">
                                        Data Analyst & Machine Learning Engineer
                                    </p>
                                    <p className="text-foreground-muted text-sm mt-1">
                                        Jakarta • Mathematics Background
                                    </p>
                                </div>
                            </div>

                            {/* The Story */}
                            <div className="space-y-4 text-foreground-muted leading-relaxed">
                                <p>
                                    <span className="text-foreground font-semibold">The Hybrid Journey:</span>{' '}
                                    I didn&apos;t start in tech, I started in pure <span className="text-accent">Mathematics</span>.
                                    I fell in love with logic and patterns, which naturally pulled me toward Data.
                                    For me, it&apos;s not just about using libraries it&apos;s about seeing the math come to life to solve actual problems.
                                </p>
                                <p>
                                    <span className="text-foreground font-semibold">The Edge:</span>{' '}
                                    I don&apos;t just trust the &quot;black box&quot;. Because I understand the math underneath from
                                    eigenvalues to gradient descent I can fix broken models and optimize messy pipelines
                                    when the standard tools fail.
                                </p>

                            </div>
                        </div>

                        {/* Quick Facts */}
                        <div className="grid grid-cols-2 gap-4">
                            <motion.div
                                className="glass-card p-4 text-center"
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="text-3xl mb-2"></div>
                                <div className="text-sm font-medium">Mathematics</div>
                                <div className="text-xs text-foreground-muted">Degree</div>
                            </motion.div>

                            <motion.div
                                className="glass-card p-4 text-center"
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="text-3xl mb-2"></div>
                                <div className="text-sm font-medium">ML Models</div>
                                <div className="text-xs text-foreground-muted">Built 15+</div>
                            </motion.div>
                            <motion.div
                                className="glass-card p-4 text-center"
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="text-3xl mb-2"></div>
                                <div className="text-sm font-medium">Impact Driven</div>
                                <div className="text-xs text-foreground-muted">Always</div>
                            </motion.div>
                        </div>
                    </motion.div>

                    {/* Right Column - Tech Stack & Widget */}
                    <motion.div
                        initial={{ opacity: 0, x: 30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="space-y-8"
                    >
                        {/* Tech Stack Bento */}
                        <div>
                            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                <span className="text-accent"></span>
                                Tools & Technologies
                            </h3>
                            <BentoGrid>
                                {techStack.map((tech, i) => (
                                    <BentoItem
                                        key={tech.label}
                                        icon={tech.icon}
                                        label={tech.label}
                                        color={tech.color}
                                        size={i === 0 || i === 2 ? 'large' : 'normal'}
                                    />
                                ))}
                            </BentoGrid>
                        </div>

                        {/* Journey Timeline */}
                        <div>
                            <Journey />
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
