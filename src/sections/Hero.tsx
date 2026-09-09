'use client';

import { motion } from 'framer-motion';
import { ArrowDown, Download, Github, Linkedin, Printer } from 'lucide-react';
import { TabId } from '../components/Navigation';
import { projects } from './Projects';
import { certificates } from './Certificates';

interface HeroProps {
    onSelectTab?: (tab: TabId) => void;
}

// Real, countable facts - the same source Projects and Certificates render from,
// so the ticket can never drift out of sync with what's actually on the page.
const ticketRows = [
    { n: projects.length, l: 'Projects Shipped' },
    { n: certificates.length, l: 'Certifications Verified' },
    { n: '2025', l: 'Working Since' },
];

export default function Hero({ onSelectTab }: HeroProps) {
    return (
        <section className="relative px-6 pt-4 md:pt-8 pb-12 overflow-hidden">
            <div className="relative z-10 max-w-5xl mx-auto">
                <div className="grid md:grid-cols-[1.3fr_0.9fr] gap-10 md:gap-12 items-center">
                    {/* Lead: name, role, bio, actions */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full surface-card text-sm font-mono">
                            <span className="w-2 h-2 bg-accent rounded-full animate-pulse" />
                            Open to opportunities
                        </span>

                        <h1 className="font-serif text-4xl md:text-6xl leading-[0.98] tracking-tight mt-5 mb-4">
                            <span className="block">M. Wildan</span>
                            <span className="block mark-swipe">Nuril Akmal</span>
                        </h1>

                        <svg className="underline-doodle w-52 h-3 mb-5" viewBox="0 0 210 12" aria-hidden="true">
                            <path d="M2 8 Q 40 2, 80 7 T 160 6 T 208 8" />
                        </svg>

                        <p className="text-lg text-foreground-muted max-w-xl leading-relaxed">
                            Transforming raw data into actionable business insights through analytics, dashboards, and machine learning.
                            <span className="block mt-2 text-accent font-mono text-sm">
                                Data Analyst · Power BI Engineer · Machine Learning Engineer
                            </span>
                        </p>

                        <div className="flex flex-wrap gap-4 mt-8">
                            <motion.button
                                onClick={() => onSelectTab && onSelectTab('projects')}
                                className="btn-primary flex items-center gap-2 cursor-pointer"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                View Projects
                                <ArrowDown className="w-4 h-4" />
                            </motion.button>

                            <motion.a
                                href="/resume.pdf"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="btn-secondary flex items-center gap-2"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <Download className="w-4 h-4" />
                                Resume (ATS)
                            </motion.a>

                            <motion.a
                                href="/print-portfolio"
                                className="btn-secondary flex items-center gap-2"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <Printer className="w-4 h-4" />
                                Print CV / Portfolio
                            </motion.a>
                        </div>

                        <div className="flex gap-4 mt-6">
                            <motion.a
                                href="https://github.com/wheldnz"
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label="GitHub profile"
                                className="surface-card p-3 hover:bg-accent/10 transition-colors"
                                whileHover={{ scale: 1.1, rotate: 5 }}
                                whileTap={{ scale: 0.9 }}
                            >
                                <Github className="w-5 h-5" />
                            </motion.a>
                            <motion.a
                                href="https://www.linkedin.com/in/wildan-nuril/"
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label="LinkedIn profile"
                                className="surface-card p-3 hover:bg-accent/10 transition-colors"
                                whileHover={{ scale: 1.1, rotate: -5 }}
                                whileTap={{ scale: 0.9 }}
                            >
                                <Linkedin className="w-5 h-5" />
                            </motion.a>
                        </div>
                    </motion.div>

                    {/* Ticket: credibility at a glance, torn-stub style */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, rotate: 4 }}
                        animate={{ opacity: 1, scale: 1, rotate: 2.5 }}
                        transition={{ duration: 0.6, delay: 0.15 }}
                        className="ticket font-mono"
                    >
                        {ticketRows.map((row, i) => (
                            <div
                                key={row.l}
                                className={`flex justify-between items-baseline gap-4 py-2.5 ${i < ticketRows.length - 1 ? 'border-b border-dashed border-card-border' : ''
                                    }`}
                            >
                                <span className="text-2xl md:text-3xl">{row.n}</span>
                                <span className="text-[10px] md:text-[11px] text-foreground-muted uppercase text-right max-w-[110px]">{row.l}</span>
                            </div>
                        ))}
                        <div className="text-center text-[10px] tracking-widest text-foreground-muted uppercase mt-3">
                            ✂ credibility ticket, not a claim
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
