'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutGrid, BarChart3, Sigma, Layers } from 'lucide-react';
import ProjectCard from '../components/ProjectCard';

type Category = 'all' | 'data' | 'math' | 'fullstack';

const projects = [
    {
        title: 'P&L Analysis Dashboard',
        description: 'Comprehensive profit and loss analysis tool for financial decision-making. Reduced reporting time by 60% and improved forecast accuracy.',
        category: 'data' as const,
        metric: '+15%',
        metricLabel: 'Efficiency Gain',
        tags: ['Python', 'Tableau', 'SQL'],
    },
    {
        title: 'Bidding Optimization Engine',
        description: 'ML-powered system for optimizing auction bids. Analyzes historical data to predict optimal bid prices in real-time.',
        category: 'data' as const,
        metric: '23%',
        metricLabel: 'Win Rate Increase',
        tags: ['PyTorch', 'XGBoost', 'FastAPI'],
    },
    {
        title: 'Stock Scalping Strategy',
        description: 'High-win-rate trading strategy for Indonesian stocks (IHSG). Uses technical indicators and ML for entry/exit signals.',
        category: 'data' as const,
        metric: '68%',
        metricLabel: 'Win Rate',
        tags: ['Python', 'TA-Lib', 'Backtesting'],
    },
    {
        title: 'Neural Network From Scratch',
        description: 'Deep dive into the linear algebra behind neural networks. Built a full NN using only NumPy to understand backpropagation.',
        category: 'math' as const,
        metric: '∇',
        metricLabel: 'Gradient Descent',
        tags: ['NumPy', 'Calculus', 'Linear Algebra'],
    },
    {
        title: 'Revenue Forecasting Model',
        description: 'Time series forecasting for quarterly revenue predictions. Integrated with Streamlit dashboard for stakeholder presentations.',
        category: 'data' as const,
        metric: '94%',
        metricLabel: 'Accuracy (MAPE)',
        tags: ['Prophet', 'Streamlit', 'Pandas'],
    },
    {
        title: 'Calculus Behind CNNs',
        description: 'Visual blog post explaining convolution as a mathematical operation and how gradients flow through pooling layers.',
        category: 'math' as const,
        metric: '5K+',
        metricLabel: 'Views',
        tags: ['Matplotlib', 'LaTeX', 'D3.js'],
    },
    {
        title: 'Company Profile Business',
        description: 'Full stack dashboard for SaaS metrics. Built with Next.js for SSR, Node.js backend, and a custom component library.',
        category: 'fullstack' as const,
        metric: '99%',
        metricLabel: 'Lighthouse Score',
        tags: ['Next.js', 'Node.js', 'PostgreSQL'],
    },
];

const categories = [
    { id: 'all', label: 'General', icon: LayoutGrid },
    { id: 'data', label: 'Data', icon: BarChart3 },
    { id: 'math', label: 'Math', icon: Sigma },
    { id: 'fullstack', label: 'Full Stack', icon: Layers },
];

export default function Projects() {
    const [activeCategory, setActiveCategory] = useState<Category>('all');

    const filteredProjects = activeCategory === 'all'
        ? projects
        : projects.filter(p => p.category === activeCategory);

    return (
        <section id="projects" className="py-24 px-6">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
                <motion.div
                    className="text-center mb-16"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                >
                    <motion.span
                        className="text-accent font-mono text-sm uppercase tracking-widest"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        The Lab
                    </motion.span>
                    <h2 className="section-title mt-4">
                        Featured <span className="gradient-text">Projects</span>
                    </h2>
                    <p className="text-foreground-muted mt-4 max-w-xl mx-auto">
                        Explore my work across data analysis, machine learning, and mathematical foundations.
                        Each project tells a story of problem-solving and impact.
                    </p>
                </motion.div>

                {/* Category Filter */}
                <motion.div
                    className="flex flex-wrap justify-center gap-3 mb-12"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.2 }}
                >
                    {categories.map((cat) => (
                        <motion.button
                            key={cat.id}
                            onClick={() => setActiveCategory(cat.id as Category)}
                            className={`px-5 py-2.5 rounded-full font-medium text-sm transition-all cursor-pointer ${activeCategory === cat.id
                                ? 'bg-accent text-background'
                                : 'glass-card hover:bg-accent/10'
                                }`}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <span className="mr-2">
                                <cat.icon className="w-4 h-4 inline-block" />
                            </span>
                            {cat.label}
                        </motion.button>
                    ))}
                </motion.div>

                {/* Projects Grid */}
                <motion.div
                    className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
                    layout
                >
                    {filteredProjects.map((project, index) => (
                        <motion.div
                            key={project.title}
                            layout
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <ProjectCard {...project} />
                        </motion.div>
                    ))}
                </motion.div>

                {/* View All CTA */}
                <motion.div
                    className="text-center mt-12"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                >
                    <motion.a
                        href="https://github.com/wheldnz"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-secondary inline-flex items-center gap-2"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        View All on GitHub
                        <span className="text-accent">→</span>
                    </motion.a>
                </motion.div>
            </div>
        </section>
    );
}
