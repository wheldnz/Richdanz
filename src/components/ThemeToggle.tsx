'use client';

import { motion } from 'framer-motion';
import { Moon, Sun, Terminal, FileText } from 'lucide-react';
import { useTheme } from './ThemeProvider';

export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme();

    return (
        <motion.button
            onClick={toggleTheme}
            className="relative flex items-center gap-2 px-4 py-2 rounded-full glass-card cursor-pointer overflow-hidden group"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
            {/* Background slide animation */}
            <motion.div
                className="absolute inset-0 bg-gradient-to-r from-accent/20 to-accent-secondary/20"
                initial={false}
                animate={{
                    x: theme === 'dark' ? '0%' : '100%',
                }}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            />

            {/* Terminal Icon */}
            <motion.div
                className="relative z-10 flex items-center gap-1"
                animate={{
                    opacity: theme === 'dark' ? 1 : 0.5,
                    scale: theme === 'dark' ? 1 : 0.9,
                }}
            >
                <Terminal className="w-4 h-4" />
                <span className="text-xs font-mono hidden sm:inline">Terminal</span>
            </motion.div>

            {/* Divider */}
            <div className="relative z-10 w-px h-4 bg-foreground/20" />

            {/* Paper Icon */}
            <motion.div
                className="relative z-10 flex items-center gap-1"
                animate={{
                    opacity: theme === 'light' ? 1 : 0.5,
                    scale: theme === 'light' ? 1 : 0.9,
                }}
            >
                <FileText className="w-4 h-4" />
                <span className="text-xs font-mono hidden sm:inline">Paper</span>
            </motion.div>

            {/* Floating Icon Animation */}
            <motion.div
                className="absolute -right-1 -top-1"
                animate={{
                    rotate: theme === 'dark' ? 0 : 180,
                }}
                transition={{ type: 'spring', stiffness: 200, damping: 20 }}
            >
                {theme === 'dark' ? (
                    <Moon className="w-3 h-3 text-accent" />
                ) : (
                    <Sun className="w-3 h-3 text-accent" />
                )}
            </motion.div>
        </motion.button>
    );
}
