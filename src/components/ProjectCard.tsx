'use client';

import { motion } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';

interface ProjectCardProps {
    title: string;
    description: string;
    category: 'data' | 'math' | 'fullstack';
    metric: string;
    metricLabel: string;
    image?: string;
    link?: string;
    tags: string[];
}

const categoryLabels = {
    data: 'Data Focus', // Merged Analyst+ML
    math: 'Mathematics',
    fullstack: 'Full Stack',
};

export default function ProjectCard({
    title,
    description,
    category,
    metric,
    metricLabel,
    image,
    tags,
    link = '#',
}: ProjectCardProps) {
    return (
        <motion.a
            href={link}
            className="group relative block glass-card p-6 overflow-hidden"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            whileHover={{ y: -8 }}
            transition={{ duration: 0.4 }}
        >
            {/* Project Image */}
            {image && (
                <div className="relative h-44 -mx-6 -mt-6 mb-4 overflow-hidden border-b border-card-border rounded-t-3xl">
                    <img
                        src={image}
                        alt={title}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-background/20 to-transparent" />
                </div>
            )}

            {/* Hover Metric Popup */}
            <motion.div
                className="absolute top-4 right-4 glass-card px-4 py-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10"
                initial={{ scale: 0.8, opacity: 0 }}
                whileHover={{ scale: 1 }}
            >
                <div className="text-lg font-bold gradient-text">{metric}</div>
                <div className="text-xs text-foreground-muted">{metricLabel}</div>
            </motion.div>

            {/* Category Badge */}
            <span className={`category-badge ${category} mt-2 inline-block`}>
                {categoryLabels[category]}
            </span>

            {/* Content */}
            <h3 className="mt-4 text-xl font-bold tracking-tight group-hover:gradient-text transition-all duration-300">
                {title}
            </h3>

            <p className="mt-2 text-foreground-muted text-sm leading-relaxed">
                {description}
            </p>

            {/* Tags */}
            <div className="mt-4 flex flex-wrap gap-2">
                {tags.map((tag) => (
                    <span
                        key={tag}
                        className="text-xs font-mono px-2 py-1 rounded-md bg-foreground/5 text-foreground-muted"
                    >
                        {tag}
                    </span>
                ))}
            </div>

            {/* Arrow Icon */}
            <motion.div
                className="absolute bottom-4 right-4 w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300"
                whileHover={{ scale: 1.1, rotate: 45 }}
            >
                <ArrowUpRight className="w-5 h-5 text-accent" />
            </motion.div>

            {/* Gradient border on hover */}
            <motion.div
                className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                style={{
                    background: 'linear-gradient(135deg, transparent 0%, var(--glow) 50%, transparent 100%)',
                    padding: '1px',
                    mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
                    maskComposite: 'xor',
                    WebkitMaskComposite: 'xor',
                }}
            />
        </motion.a>
    );
}
