'use client';

import { useEffect, useState, useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { LucideIcon, LineChart, Award } from 'lucide-react';
import { projects } from '../sections/Projects';
import { certificates } from '../sections/Certificates';

interface StatItem {
    label: string;
    value: number;
    icon: LucideIcon;
}

// Counted directly from the Projects and Certificates sections below,
// not invented round numbers.
const stats: StatItem[] = [
    { label: 'Projects Shipped', value: projects.length, icon: LineChart },
    { label: 'Certifications Earned', value: certificates.length, icon: Award },
];

function AnimatedNumber({ value }: { value: number }) {
    const [displayValue, setDisplayValue] = useState(0);
    const ref = useRef<HTMLSpanElement>(null);
    const isInView = useInView(ref, { once: true });

    useEffect(() => {
        if (!isInView) return;

        const duration = 1200;
        const steps = Math.max(value, 1);
        const stepDuration = duration / steps;
        let current = 0;

        const timer = setInterval(() => {
            current++;
            setDisplayValue(Math.min(current, value));

            if (current >= value) {
                clearInterval(timer);
            }
        }, stepDuration);

        return () => clearInterval(timer);
    }, [value, isInView]);

    return <span ref={ref} className="stat-number">{displayValue}</span>;
}

export default function LiveStats() {
    return (
        <motion.div
            className="flex flex-wrap justify-center gap-4 md:gap-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.6 }}
        >
            {stats.map((stat, index) => (
                <motion.div
                    key={stat.label}
                    className="surface-card px-6 py-4 flex items-center gap-3"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    whileHover={{ scale: 1.03 }}
                >
                    <stat.icon className="w-5 h-5 text-accent shrink-0" />
                    <div className="flex flex-col">
                        <AnimatedNumber value={stat.value} />
                        <span className="text-xs text-foreground-muted font-mono uppercase tracking-wider">
                            {stat.label}
                        </span>
                    </div>
                </motion.div>
            ))}
        </motion.div>
    );
}
