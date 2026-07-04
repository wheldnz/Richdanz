'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutGrid, BarChart3, Sigma, Layers } from 'lucide-react';
import ProjectCard from '../components/ProjectCard';

type Category = 'all' | 'data' | 'math' | 'fullstack';

const projects = [
    {
        title: 'Analisis Sentimen RUU TNI',
        description: 'Analisis sentimen publik di platform X (Twitter) terhadap revisi Undang-Undang TNI menggunakan Natural Language Processing dan klasifikasi Naive Bayes.',
        category: 'data' as const,
        metric: '84.6%',
        metricLabel: 'Model Akurasi',
        image: '/images/projects/analisis-sentimen-ruu-tni.png',
        tags: ['Python', 'NLP', 'Jupyter', 'TF-IDF'],
        link: '/projects/analisis-sentimen-ruu-tni',
    },
    {
        title: 'E-Commerce Toko Online PHP',
        description: 'Aplikasi e-commerce toko online lengkap dengan database relational MySQL, fitur keranjang belanja, proses checkout, dan panel administrasi.',
        category: 'fullstack' as const,
        metric: '100ms',
        metricLabel: 'Waktu Respons',
        image: '/images/projects/toko-online.png',
        tags: ['PHP', 'MySQL', 'Bootstrap', 'E-Commerce'],
        link: '/projects/toko-online',
    },
    {
        title: 'Klasifikasi Diabetes Sekuens DNA',
        description: 'Deteksi dini risiko diabetes melitus berdasarkan pola sekuens DNA manusia menggunakan ekstraksi fitur K-mers dan klasifikasi K-Nearest Neighbors.',
        category: 'math' as const,
        metric: '93.2%',
        metricLabel: 'Akurasi KNN',
        image: '/images/projects/klasifikasi-diabetes-dna.png',
        tags: ['Python', 'Bioinformatics', 'KNN', 'K-mers'],
        link: '/projects/klasifikasi-diabetes-dna',
    },
    {
        title: 'CS-AI-Agent Customer Service',
        description: 'Agen Customer Service otonom berbasis LLM yang dibekali kemampuan menggunakan peralatan (tool-use) untuk melacak paket dan refund otomatis.',
        category: 'fullstack' as const,
        metric: '88%',
        metricLabel: 'Resolusi Otomatis',
        image: '/images/projects/cs-ai-agent.png',
        tags: ['Python', 'LangChain', 'OpenAI', 'AI Agent'],
        link: '/projects/cs-ai-agent',
    },
    {
        title: 'Kalkulator Average Down Saham IDX',
        description: 'Kalkulator investasi interaktif untuk mensimulasikan perhitungan rata-rata beli bawah (average down) saham di Bursa Efek Indonesia (IDX).',
        category: 'fullstack' as const,
        metric: '0.02s',
        metricLabel: 'Kalkulasi Latensi',
        image: '/images/projects/avg-down-idx.png',
        tags: ['TypeScript', 'Next.js', 'React', 'Finance'],
        link: '/projects/avg-down-idx',
    },
    {
        title: 'Data Pipeline Saham Indonesia',
        description: 'Pipeline data otonom untuk melakukan scraping, pembersihan, dan analisis fundamental saham-saham di Bursa Efek Indonesia (IDX).',
        category: 'data' as const,
        metric: '500+',
        metricLabel: 'Emiten Tersaring',
        image: '/images/projects/data-saham-indonesia.png',
        tags: ['Python', 'Pandas', 'Scraping', 'Finance'],
        link: '/projects/data-saham-indonesia',
    },
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
