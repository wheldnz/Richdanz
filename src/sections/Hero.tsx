'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowDown, Download, Github, Linkedin, Printer } from 'lucide-react';
import LiveStats from '../components/LiveStats';

const words = ["AI Engineer", "Data Analytics", "Full Stack Developer"];

export default function Hero() {
    const [text, setText] = useState('');
    const [isDeleting, setIsDeleting] = useState(false);
    const [loopNum, setLoopNum] = useState(0);
    const [typingSpeed, setTypingSpeed] = useState(150);

    useEffect(() => {
        const handleType = () => {
            const i = loopNum % words.length;
            const fullText = words[i];

            setText(isDeleting
                ? fullText.substring(0, text.length - 1)
                : fullText.substring(0, text.length + 1)
            );

            // Dynamic speed
            let typeSpeed = isDeleting ? 40 : 100;

            if (!isDeleting && text === fullText) {
                // Done typing, wait before deleting
                typeSpeed = 2000;
                setIsDeleting(true);
            } else if (isDeleting && text === '') {
                // Done deleting, switch to next word
                setIsDeleting(false);
                setLoopNum(loopNum + 1);
                typeSpeed = 500;
            }

            setTypingSpeed(typeSpeed);
        };

        const timer = setTimeout(handleType, typingSpeed);
        return () => clearTimeout(timer);
    }, [text, isDeleting, loopNum, typingSpeed]);

    return (
        <section className="relative min-h-screen flex flex-col items-center justify-center px-6 pt-32 overflow-hidden">


            {/* Main Content */}
            <div className="relative z-10 max-w-5xl mx-auto text-center">
                {/* Tagline */}
                <motion.div
                    className="mb-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card text-sm font-mono">
                        <span className="w-2 h-2 bg-accent rounded-full animate-pulse" />
                        Open to opportunities
                    </span>
                </motion.div>

                {/* Main Headline */}
                <motion.h1
                    className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 min-h-[160px] md:min-h-[200px]"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                >
                    <span className="block mb-2">Mathematics</span>
                    <span className="flex flex-wrap items-baseline justify-center gap-x-3 gap-y-1">
                        <span>×</span>
                        <span className="gradient-text inline-block">
                            {text}
                            <span className="animate-pulse ml-1 text-accent">|</span>
                        </span>
                    </span>
                </motion.h1>

                {/* Subheadline */}
                <motion.p
                    className="text-lg md:text-xl text-foreground-muted max-w-2xl mx-auto mb-8 leading-relaxed"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                >
                    From proofs to predictions — bridging rigorous logic with real-world impact.
                    <span className="block mt-2 text-accent font-mono text-base">
                        Data Analyst | BI &amp; Analytics Engineer
                    </span>
                </motion.p>

                {/* CTA Buttons */}
                <motion.div
                    className="flex flex-wrap justify-center gap-4 mb-12"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.3 }}
                >
                    <motion.a
                        href="#projects"
                        className="btn-primary flex items-center gap-2"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        View Projects
                        <ArrowDown className="w-4 h-4" />
                    </motion.a>

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
                </motion.div>

                {/* Social Links */}
                <motion.div
                    className="flex justify-center gap-4 mb-12"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                >
                    <motion.a
                        href="https://github.com/wheldnz"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="glass-card p-3 hover:bg-accent/10 transition-colors"
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        whileTap={{ scale: 0.9 }}
                    >
                        <Github className="w-5 h-5" />
                    </motion.a>
                    <motion.a
                        href="https://www.linkedin.com/in/wildan-nuril/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="glass-card p-3 hover:bg-accent/10 transition-colors"
                        whileHover={{ scale: 1.1, rotate: -5 }}
                        whileTap={{ scale: 0.9 }}
                    >
                        <Linkedin className="w-5 h-5" />
                    </motion.a>
                </motion.div>

                {/* Live Stats */}
                <LiveStats />
            </div>


        </section>
    );
}
