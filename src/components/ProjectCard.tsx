'use client';

import { motion } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';

interface ProjectCardProps {
    title: string;
    description: string;
    category: 'data' | 'ml' | 'other';
    metric: string;
    metricLabel: string;
    image?: string;
    link?: string;
    tags: string[];
}

const categoryLabels = {
    data: 'Data & BI',
    ml: 'Machine Learning',
    other: 'Other',
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
            className="group relative block surface-card p-6 overflow-hidden"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            whileHover={{ y: -6 }}
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

            {/* Category + headline metric: always visible, not hidden behind hover
                so keyboard and touch users see it too, not just mouse hover */}
            <div className="flex items-start justify-between gap-3">
                <span className={`category-badge ${category}`}>
                    {categoryLabels[category]}
                </span>
                <div className="text-right shrink-0">
                    <div className="text-lg font-mono font-bold text-accent leading-none">{metric}</div>
                    <div className="text-[11px] text-foreground-muted mt-1">{metricLabel}</div>
                </div>
            </div>

            {/* Content */}
            <h3 className="mt-4 font-serif text-xl font-normal tracking-tight group-hover:text-accent transition-colors duration-300">
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

            {/* Arrow Icon: signals the card is a real link to the case study.
                Also revealed on keyboard focus, not hover alone, so keyboard
                users get the same affordance as mouse users. */}
            <motion.div
                className="absolute bottom-4 right-4 w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center opacity-0 group-hover:opacity-100 group-focus-visible:opacity-100 transition-all duration-300"
                whileHover={{ scale: 1.1 }}
            >
                <ArrowUpRight className="w-5 h-5 text-accent" />
            </motion.div>
        </motion.a>
    );
}
