'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutGrid, BarChart3, Sigma, Layers } from 'lucide-react';
import ProjectCard from '../components/ProjectCard';

type Category = 'all' | 'data' | 'math' | 'fullstack';

const projects = [
    {
        title: 'Enterprise Sales Analytics',
        description: 'End-to-end sales analysis pipeline, processing over 1.2 million rows of transaction data to deliver actionable insights on profit margins and regional store performance.',
        category: 'data' as const,
        metric: '1.2M Rows',
        metricLabel: 'Sales Orders',
        image: '/images/projects/enterprise-sales.png',
        tags: ['SQL', 'Power BI', 'ETL', 'Python'],
        link: '/projects/enterprise-sales-analytics',
    },
    {
        title: 'Customer Churn Analytics',
        description: 'Churn forecasting and cohort retention dashboard tracking customer lifetime value (CLV) and feature usage patterns for a 1-million-customer subscription platform.',
        category: 'data' as const,
        metric: '92%',
        metricLabel: 'Prediction Accuracy',
        image: '/images/projects/customer-churn.png',
        tags: ['SQL', 'Power BI', 'Cohort', 'Retention'],
        link: '/projects/customer-churn-analytics',
    },
    {
        title: 'Supply Chain Analytics',
        description: 'Inventory optimization and supply chain logistics dashboard monitoring stock turnover, warehouse capacity, and supplier SLA performance across global operations.',
        category: 'data' as const,
        metric: '96%',
        metricLabel: 'OTIF Rate',
        image: '/images/projects/supply-chain.png',
        tags: ['SQL', 'Power BI', 'Inventory', 'Logistics'],
        link: '/projects/supply-chain-analytics',
    },
    {
        title: 'HR Analytics',
        description: 'Workforce demographics and employee attrition dashboard, utilizing historical career paths and attendance metrics to pinpoint turnover drivers.',
        category: 'data' as const,
        metric: '8%',
        metricLabel: 'Attrition Goal',
        image: '/images/projects/hr-analytics.png',
        tags: ['SQL', 'Power BI', 'HR', 'Retention'],
        link: '/projects/hr-analytics',
    },
    {
        title: 'Repair Service Analytics',
        description: 'Hardware maintenance operations dashboard monitoring Mean Time to Repair (MTTR), technician SLA achievement rates, and device breakdown patterns.',
        category: 'data' as const,
        metric: '3.2 Hours',
        metricLabel: 'Average MTTR',
        image: '/images/projects/repair-service.png',
        tags: ['SQL', 'Power BI', 'SLA', 'Operations'],
        link: '/projects/repair-service-analytics',
    },
    {
        title: 'Insurance Underwriting Analytics',
        description: 'Portfolio analysis dashboard for insurance underwriting, monitoring premium growth, claim loss ratios, and operational approval SLA metrics across branches.',
        category: 'data' as const,
        metric: '64%',
        metricLabel: 'Loss Ratio',
        image: '/images/projects/insurance-analytics.png',
        tags: ['SQL', 'Power BI', 'Finance', 'Actuarial'],
        link: '/projects/insurance-analytics',
    },
    {
        title: 'Neural Network From Scratch',
        description: 'Deep dive into the linear algebra behind neural networks. Built a full NN using only NumPy to understand backpropagation.',
        category: 'math' as const,
        metric: '∇',
        metricLabel: 'Gradient Descent',
        tags: ['NumPy', 'Calculus', 'Linear Algebra'],
        link: '#',
    },
    {
        title: 'Calculus Behind CNNs',
        description: 'Visual blog post explaining convolution as a mathematical operation and how gradients flow through pooling layers.',
        category: 'math' as const,
        metric: '5K+',
        metricLabel: 'Views',
        tags: ['Matplotlib', 'LaTeX', 'D3.js'],
        link: '#',
    },
    {
        title: 'Company Profile Business',
        description: 'Full stack dashboard for SaaS metrics. Built with Next.js for SSR, Node.js backend, and a custom component library.',
        category: 'fullstack' as const,
        metric: '99%',
        metricLabel: 'Lighthouse Score',
        tags: ['Next.js', 'Node.js', 'PostgreSQL'],
        link: '#',
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
