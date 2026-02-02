'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import ThemeToggle from './ThemeToggle';
import { Menu, X } from 'lucide-react';

const navItems = [
    { label: 'Projects', href: '#projects' },
    { label: 'About', href: '#about' },
    { label: 'Contact', href: '#contact' },
];

export default function Navigation() {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <motion.nav
            className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${isScrolled ? 'py-3' : 'py-6'
                }`}
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
        >
            <div className="max-w-6xl mx-auto px-6">
                <div
                    className={`flex items-center justify-between ${isScrolled ? 'glass-card px-6 py-3' : ''
                        }`}
                >
                    {/* Logo */}
                    <motion.a
                        href="#"
                        className="flex items-center gap-2 font-bold text-lg"
                        whileHover={{ scale: 1.05 }}
                    >
                        <span className="text-3xl">∭</span>
                    </motion.a>

                    {/* Desktop Nav */}
                    <div className="hidden md:flex items-center gap-12">
                        {navItems.map((item, index) => (
                            <motion.a
                                key={item.label}
                                href={item.href}
                                className="relative text-sm font-medium text-foreground-muted hover:text-foreground transition-colors group"
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 * index }}
                                whileHover={{ y: -2 }}
                            >
                                {item.label}
                                <motion.span
                                    className="absolute -bottom-1 left-0 w-0 h-0.5 bg-accent group-hover:w-full transition-all duration-300"
                                />
                            </motion.a>
                        ))}
                    </div>

                    {/* Right Side */}
                    <div className="flex items-center gap-4">
                        <ThemeToggle />

                        {/* Mobile Menu Button */}
                        <motion.button
                            className="md:hidden glass-card p-2"
                            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                            whileTap={{ scale: 0.9 }}
                        >
                            {isMobileMenuOpen ? (
                                <X className="w-5 h-5" />
                            ) : (
                                <Menu className="w-5 h-5" />
                            )}
                        </motion.button>
                    </div>
                </div>

                {/* Mobile Menu */}
                <motion.div
                    className={`md:hidden mt-4 glass-card overflow-hidden ${isMobileMenuOpen ? 'block' : 'hidden'
                        }`}
                    initial={{ height: 0, opacity: 0 }}
                    animate={{
                        height: isMobileMenuOpen ? 'auto' : 0,
                        opacity: isMobileMenuOpen ? 1 : 0,
                    }}
                    transition={{ duration: 0.3 }}
                >
                    <div className="p-4 space-y-4">
                        {navItems.map((item) => (
                            <a
                                key={item.label}
                                href={item.href}
                                className="block text-foreground-muted hover:text-foreground transition-colors py-2"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                {item.label}
                            </a>
                        ))}
                    </div>
                </motion.div>
            </div>
        </motion.nav>
    );
}
