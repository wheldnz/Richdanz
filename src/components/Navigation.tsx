'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import ThemeToggle from './ThemeToggle';
import { Menu, X } from 'lucide-react';

export type TabId = 'hero' | 'projects' | 'about' | 'certificates' | 'contact';

interface NavigationProps {
    activeTab: TabId;
    onSelectTab: (tab: TabId) => void;
}

const navItems: { label: string; tab: TabId }[] = [
    { label: 'Home', tab: 'hero' },
    { label: 'Projects', tab: 'projects' },
    { label: 'About', tab: 'about' },
    { label: 'Credentials', tab: 'certificates' },
    { label: 'Contact', tab: 'contact' },
];

export default function Navigation({ activeTab, onSelectTab }: NavigationProps) {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 30);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleNavClick = (tab: TabId) => {
        onSelectTab(tab);
        setIsMobileMenuOpen(false);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

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
                    className={`grid grid-cols-3 items-center ${isScrolled ? 'glass-card px-6 py-3' : ''
                        }`}
                >
                    {/* Logo (Left) */}
                    <div className="flex justify-start">
                        <button
                            onClick={() => handleNavClick('hero')}
                            className="flex items-center gap-2 font-bold text-lg focus:outline-none"
                        >
                            <span className="text-3xl font-extrabold text-foreground hover:text-accent transition-colors">W</span>
                        </button>
                    </div>

                    {/* Desktop Nav (Center) */}
                    <div className="hidden md:flex justify-center items-center gap-8">
                        {navItems.map((item, index) => {
                            const isActive = activeTab === item.tab;
                            return (
                                <button
                                    key={item.label}
                                    onClick={() => handleNavClick(item.tab)}
                                    className={`relative text-sm font-medium transition-colors cursor-pointer py-1 ${
                                        isActive ? 'text-accent font-semibold' : 'text-foreground-muted hover:text-foreground'
                                    }`}
                                >
                                    {item.label}
                                    {isActive ? (
                                        <motion.span
                                            layoutId="activeTabIndicator"
                                            className="absolute -bottom-1 left-0 right-0 h-0.5 bg-accent rounded-full"
                                            transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                                        />
                                    ) : null}
                                </button>
                            );
                        })}
                    </div>

                    {/* Right Side (Right) */}
                    <div className="flex justify-end items-center gap-4">
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
                    <div className="p-4 space-y-3">
                        {navItems.map((item) => (
                            <button
                                key={item.label}
                                onClick={() => handleNavClick(item.tab)}
                                className={`block w-full text-left transition-colors py-2 px-3 rounded-lg text-sm font-medium ${
                                    activeTab === item.tab
                                        ? 'bg-accent/10 text-accent font-semibold'
                                        : 'text-foreground-muted hover:text-foreground'
                                }`}
                            >
                                {item.label}
                            </button>
                        ))}
                    </div>
                </motion.div>
            </div>
        </motion.nav>
    );
}
