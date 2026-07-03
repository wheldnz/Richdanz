'use client';

import { motion } from 'framer-motion';
import { Briefcase, GraduationCap, Code2, LineChart } from 'lucide-react';

const journeyItems = [
    {
        year: '2024 - Present',
        title: 'Full Stack Data Engineer',
        company: 'Freelance / Open Source',
        description: 'Building end-to-end data systems. merging Data Engineering with modern Web Development (Next.js).',
        icon: Code2,
        color: '#00ff88',
    },
    {
        year: '2022 - 2023',
        title: 'Machine Learning Engineer',
        company: 'Independent Projects',
        description: 'Developed algorithmic trading models (IHSG) and engaged in deep learning research (Computer Vision & NLP).',
        icon: LineChart,
        color: '#3b82f6',
    },
    {
        year: '2018 - 2022',
        title: 'Bachelor of Mathematics',
        company: 'University Graduate',
        description: 'Specialized in pure mathematics, logic, and statistical modeling. The foundation of my data science career.',
        icon: GraduationCap,
        color: '#f29111',
    },
];

export default function Journey() {
    return (
        <div className="glass-card p-6 md:p-8">
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                <span className="text-accent"></span>
                My Journey
            </h3>

            <div className="relative border-l-2 border-white/10 ml-3 space-y-8">
                {journeyItems.map((item, index) => (
                    <motion.div
                        key={index}
                        className="relative pl-8"
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 }}
                    >
                        {/* Timeline Dot */}
                        <div
                            className="absolute -left-[9px] top-0 w-4 h-4 rounded-full border-2 border-background"
                            style={{ backgroundColor: item.color }}
                        />

                        {/* Content */}
                        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-1">
                            <h4 className="font-bold text-foreground">{item.title}</h4>
                            <span className="text-xs font-mono text-accent/80 bg-accent/5 px-2 py-0.5 rounded w-fit mt-1 sm:mt-0">
                                {item.year}
                            </span>
                        </div>

                        <p className="text-sm text-foreground-muted font-medium mb-1">
                            {item.company}
                        </p>

                        <p className="text-sm text-foreground-muted/80 leading-relaxed">
                            {item.description}
                        </p>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
