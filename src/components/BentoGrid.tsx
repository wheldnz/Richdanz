'use client';

import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';

interface BentoItemProps {
    icon: LucideIcon;
    label: string;
    color: string;
    size?: 'normal' | 'large';
}

export function BentoItem({ icon: Icon, label, color, size = 'normal' }: BentoItemProps) {
    return (
        <motion.div
            className={`glass-card flex flex-col items-center justify-center gap-2 p-4 ${size === 'large' ? 'col-span-2 row-span-2' : ''
                }`}
            whileHover={{
                scale: 1.05,
                rotateY: 5,
                rotateX: 5,
            }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            style={{ transformStyle: 'preserve-3d' }}
        >
            <motion.div
                className="relative"
                whileHover={{ rotate: 360, scale: 1.2 }}
                transition={{ duration: 0.6, type: 'spring' }}
            >
                <Icon
                    className={`${size === 'large' ? 'w-12 h-12' : 'w-8 h-8'}`}
                    style={{ color }}
                />
                {/* Glow effect */}
                <motion.div
                    className="absolute inset-0 blur-xl opacity-50"
                    style={{ backgroundColor: color }}
                />
            </motion.div>
            <span className={`font-mono ${size === 'large' ? 'text-sm' : 'text-xs'} text-foreground-muted`}>
                {label}
            </span>
        </motion.div>
    );
}

interface BentoGridProps {
    children: React.ReactNode;
}

export default function BentoGrid({ children }: BentoGridProps) {
    return (
        <motion.div
            className="grid grid-cols-4 md:grid-cols-6 gap-3"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ staggerChildren: 0.1 }}
        >
            {children}
        </motion.div>
    );
}
