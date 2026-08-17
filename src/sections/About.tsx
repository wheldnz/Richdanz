'use client';

import { motion } from 'framer-motion';
import BentoGrid, { BentoItem } from '../components/BentoGrid';
import Journey from '../components/Journey';
import {
    Braces,
    Database,
    LineChart,
    Binary,
    BarChart3,
    Sigma,
    Table2,
    Code2,
    Palette,
    FileCode2,
    Cloud,
    Terminal,
    Sparkles
} from 'lucide-react';

const techStack = [
    { icon: Braces, label: 'Python', color: '#3776ab' },
    { icon: Database, label: 'SQL (BigQuery, MySQL, Postgres)', color: '#f29111' },
    { icon: BarChart3, label: 'Power BI & DAX', color: '#f2c811' },
    { icon: Cloud, label: 'Google Cloud Platform', color: '#4285f4' },
    { icon: Table2, label: 'Advanced Excel', color: '#217346' },
    { icon: Sigma, label: 'Pandas & NumPy', color: '#150458' },
    { icon: Binary, label: 'Scikit-Learn', color: '#f7931e' },
    { icon: Sparkles, label: 'TensorFlow / Keras', color: '#ff6f00' },
    { icon: Code2, label: 'Google Apps Script', color: '#34a853' },
    { icon: BarChart3, label: 'Tableau', color: '#e97627' },
    { icon: Database, label: 'Apache Airflow & dbt', color: '#017cee' },
    { icon: FileCode2, label: 'Git & GitHub', color: '#181717' },
];

export default function About() {
    return (
        <section id="about" className="py-8 md:py-12 px-6 bg-background-secondary/50">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
                <motion.div
                    className="text-center mb-16"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                >
                    <span className="text-accent font-mono text-sm uppercase tracking-widest">
                        The Person
                    </span>
                    <h2 className="section-title mt-4">
                        About <span className="gradient-text">Me</span>
                    </h2>
                </motion.div>

                <div className="grid lg:grid-cols-2 gap-12 items-start">
                    {/* Left Column - Story */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        {/* Profile Card */}
                        <div className="glass-card p-8 mb-8">
                            <div className="flex items-start gap-6 mb-6">
                                <motion.div
                                    className="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent to-accent-secondary flex items-center justify-center text-3xl font-bold text-background shrink-0"
                                    whileHover={{ rotate: 5, scale: 1.05 }}
                                >
                                    W
                                </motion.div>
                                <div>
                                    <h3 className="text-2xl font-bold mb-1">M. Wildan Nuril Akmal</h3>
                                    <p className="text-accent font-mono text-sm">
                                        Data Analyst | Power BI Engineer | ML Engineer
                                    </p>
                                    <p className="text-foreground-muted text-sm mt-1">
                                        Jakarta • Mathematics Background
                                    </p>
                                </div>
                            </div>

                            {/* The Story */}
                            <div className="space-y-4 text-foreground-muted leading-relaxed">
                                <p>
                                    <span className="text-foreground font-semibold">The Data Journey:</span>{' '}
                                    I started with a strong foundation in <span className="text-accent">Mathematics</span>,
                                    which naturally evolved into a passion for turning raw data into business impact.
                                    From building Power BI dashboards to deploying machine learning models, I bridge the gap between data and decision-making.
                                </p>
                                <p>
                                    <span className="text-foreground font-semibold">The Edge:</span>{' '}
                                    With a math background, I don&apos;t just build dashboards or train models — I understand the
                                    statistics underneath. From hypothesis testing to gradient descent, I optimize pipelines
                                    and validate insights with rigor.
                                </p>

                            </div>
                        </div>

                        {/* Quick Facts */}
                        <div className="grid grid-cols-2 gap-4">
                            <motion.div
                                className="glass-card p-4 text-center"
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="text-3xl mb-2"></div>
                                <div className="text-sm font-medium">Dashboards</div>
                                <div className="text-xs text-foreground-muted">Built 20+</div>
                            </motion.div>

                            <motion.div
                                className="glass-card p-4 text-center"
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="text-3xl mb-2"></div>
                                <div className="text-sm font-medium">ML Models</div>
                                <div className="text-xs text-foreground-muted">Deployed 15+</div>
                            </motion.div>
                            <motion.div
                                className="glass-card p-4 text-center"
                                whileHover={{ scale: 1.02 }}
                            >
                                <div className="text-3xl mb-2"></div>
                                <div className="text-sm font-medium">Data Pipelines</div>
                                <div className="text-xs text-foreground-muted">Automated 10+</div>
                            </motion.div>
                        </div>
                    </motion.div>

                    {/* Right Column - Tech Stack & Widget */}
                    <motion.div
                        initial={{ opacity: 0, x: 30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="space-y-8"
                    >
                        {/* Tech Stack Bento */}
                        <div>
                            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                <span className="text-accent"></span>
                                Tools & Technologies
                            </h3>
                            <BentoGrid>
                                {techStack.map((tech, i) => (
                                    <BentoItem
                                        key={tech.label}
                                        icon={tech.icon}
                                        label={tech.label}
                                        color={tech.color}
                                        size={i === 0 || i === 2 ? 'large' : 'normal'}
                                    />
                                ))}
                            </BentoGrid>
                        </div>

                        {/* Journey Timeline */}
                        <div>
                            <Journey />
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
