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
            className={`surface-card flex flex-col items-center justify-center gap-2 p-4 ${size === 'large' ? 'col-span-2 row-span-2' : ''
                }`}
            whileHover={{ scale: 1.04, y: -2 }}
            whileTap={{ scale: 0.97 }}
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
        >
            <Icon
                className={`${size === 'large' ? 'w-12 h-12' : 'w-8 h-8'}`}
                style={{ color }}
            />
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
