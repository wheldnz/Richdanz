'use client';

import { useEffect, useState, useRef } from 'react';
import { motion, useInView } from 'framer-motion';

interface StatItem {
    label: string;
    value: number | string;
    suffix: string;
    icon: string;
}

const stats: StatItem[] = [
    { label: 'Projects', value: 15, suffix: '+', icon: '📊' },
    { label: 'Models Trained', value: 42, suffix: '+', icon: '🤖' },
    { label: 'Unlimited', value: '∞', suffix: '', icon: '🚀' },
];

function AnimatedNumber({ value, suffix }: { value: number | string; suffix: string }) {
    const [displayValue, setDisplayValue] = useState<number | string>(0);
    const ref = useRef<HTMLSpanElement>(null);
    const isInView = useInView(ref, { once: true });

    useEffect(() => {
        if (!isInView) return;

        if (typeof value === 'string') {
            setDisplayValue(value);
            return;
        }

        const duration = 2000;
        const steps = 60;
        const stepValue = value / steps;
        let current = 0;
        let step = 0;

        const timer = setInterval(() => {
            step++;
            current = Math.min(Math.round(stepValue * step), value);
            setDisplayValue(current);

            if (step >= steps) {
                clearInterval(timer);
                setDisplayValue(value);
            }
        }, duration / steps);

        return () => clearInterval(timer);
    }, [value, isInView]);

    return (
        <span ref={ref} className="stat-number">
            {displayValue}
            <span className="text-lg">{suffix}</span>
        </span>
    );
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
                    className="glass-card px-6 py-4 flex items-center gap-3"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    whileHover={{ scale: 1.05 }}
                >
                    <span className="text-2xl">{stat.icon}</span>
                    <div className="flex flex-col">
                        <AnimatedNumber value={stat.value} suffix={stat.suffix} />
                        <span className="text-xs text-foreground-muted font-mono uppercase tracking-wider">
                            {stat.label}
                        </span>
                    </div>
                </motion.div>
            ))}
        </motion.div>
    );
}
