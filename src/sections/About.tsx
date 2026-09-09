'use client';

import { motion } from 'framer-motion';
import BentoGrid, { BentoItem } from '../components/BentoGrid';
import { projects } from './Projects';
import { certificates } from './Certificates';
import {
    Braces,
    Database,
    LineChart,
    Binary,
    BarChart3,
    Sigma,
    Table2,
    Code2,
    FileCode2,
    Cloud,
    Award,
    Sparkles
} from 'lucide-react';

// Brand colors, each nudged in lightness (hue and saturation kept intact) so the
// icon still reads as its real-world brand mark while clearing 3:1 non-text
// contrast against both the light "paper" and dark "ink" card backgrounds -
// several original brand hexes (a pale Power BI yellow, GitHub's near-black,
// Pandas' navy) were invisible in one theme or the other. Verified with the
// antislop-human contrast checker.
const techStack = [
    { icon: Braces, label: 'Python', color: '#3776ab' },
    { icon: Database, label: 'SQL (BigQuery, MySQL, Postgres)', color: '#c6750b' },
    { icon: BarChart3, label: 'Power BI & DAX', color: '#a08309' },
    { icon: Cloud, label: 'Google Cloud Platform', color: '#4285f4' },
    { icon: Table2, label: 'Advanced Excel', color: '#268350' },
    { icon: Sigma, label: 'Pandas & NumPy', color: '#7554f7' },
    { icon: Binary, label: 'Scikit-Learn', color: '#ca7007' },
    { icon: Sparkles, label: 'TensorFlow / Keras', color: '#e06200' },
    { icon: Code2, label: 'Google Apps Script', color: '#309c4d' },
    { icon: BarChart3, label: 'Tableau', color: '#da6616' },
    { icon: Database, label: 'Apache Airflow & dbt', color: '#017cee' },
    { icon: FileCode2, label: 'Git & GitHub', color: '#757070' },
];

// Real, countable facts sourced straight from this site's own content
// (Projects and Certificates sections) rather than invented round numbers.
const quickFacts = [
    { label: 'Projects Shipped', value: projects.length, icon: LineChart },
    { label: 'Certifications Earned', value: certificates.length, icon: Award },
];

export default function About() {
    return (
        <section id="about" className="relative overflow-hidden py-8 md:py-12 px-6 bg-background-secondary/50">
            <div className="ghost-num" aria-hidden="true">02</div>
            <div className="relative max-w-6xl mx-auto">
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
                        About <span className="mark-swipe">Me</span>
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
                        <div className="surface-card p-8 mb-8">
                            <div className="flex items-start gap-6 mb-6">
                                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent to-accent-secondary flex items-center justify-center text-3xl font-bold text-background shrink-0">
                                    W
                                </div>
                                <div>
                                    <h3 className="text-2xl font-bold mb-1">M. Wildan Nuril Akmal</h3>
                                    <p className="text-accent font-mono text-sm">
                                        Data Analyst | Power BI Engineer | ML Engineer
                                    </p>
                                    <p className="text-foreground-muted text-sm mt-1">
                                        Currently at PT. Sukses Multi Servis • Jakarta
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
                                    With a math background, I don&apos;t just build dashboards or train models, I understand the
                                    statistics underneath. From hypothesis testing to gradient descent, I optimize pipelines
                                    and validate insights with rigor.
                                </p>
                            </div>
                        </div>

                        {/* Real facts, counted from the Projects and Certificates sections on this site */}
                        <div className="grid grid-cols-2 gap-4">
                            {quickFacts.map((fact) => (
                                <div key={fact.label} className="surface-card p-5 flex items-center gap-4">
                                    <fact.icon className="w-6 h-6 text-accent shrink-0" />
                                    <div>
                                        <div className="text-2xl font-bold font-mono">{fact.value}</div>
                                        <div className="text-xs text-foreground-muted">{fact.label}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </motion.div>

                    {/* Right Column - Tech Stack */}
                    <motion.div
                        initial={{ opacity: 0, x: 30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        <h3 className="text-lg font-bold mb-4">
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
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
