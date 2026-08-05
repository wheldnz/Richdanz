'use client';

import { motion } from 'framer-motion';
import { Briefcase, GraduationCap, LineChart, Database } from 'lucide-react';

const journeyItems = [
    {
        year: 'June 2025 - Present',
        title: 'Data & Business Analyst',
        company: 'PT. Sukses Multi Servis',
        points: [
            'Claims & SLA Analytics: Tracked ~300 monthly service claims across 9 insurance partners (SQL, Excel), monitoring resolution rate and turnaround time, averaging 5–6 days against a 7-day SLA.',
            'P&L Dashboard: Built Power BI dashboards for daily, monthly, and yearly P&L across 16 brand partners, 9 official service centers, and 50 retail partners.',
            'Retail Marketplace Analytics: Analyzed marketplace retail P&L over 5 months, identifying top-selling products for restocking and dead stock for discount/bundling, lifting net profit margin from ~5% to over 32%.',
            'ETL & Automation: Built SQL/Python ETL pipelines pulling claims, P&L, and service data from 16 brand systems into BigQuery, plus an n8n-based WhatsApp chatbot automating customer data retrieval, cutting reporting time by 50%.',
            'Pricing Model: Built a Python pricing model across 500+ operational units, contributing to a 12% margin gain over a 3-quarter pilot.',
            'Data Modeling: Restructured relational data models for 5,000+ SKUs across brand partners, improving data accuracy to 95%.',
            'Cross-functional Collaboration: Collaborated with Finance, Warehouse, and Insurance partner teams to validate P&L figures, reconcile SKU data against physical stock, and support monthly SLA/claims reporting.'
        ],
        icon: LineChart,
        color: '#00ff88',
    },
    {
        year: 'June - July 2024',
        title: 'Database Management (Intern)',
        company: 'PT. ASABRI (Persero) KC Malang',
        points: [
            'Managed and audited 1,000+ sensitive customer records, ensuring zero-data-loss and 98% accuracy.',
            'Programmed document archiving and scanning automation, reducing daily processing times by 40%.'
        ],
        icon: Database,
        color: '#3b82f6',
    },
    {
        year: 'Aug 2021 - Dec 2024',
        title: 'Bachelor of Science in Mathematics',
        company: 'State Islamic University of Maulana Malik Ibrahim Malang',
        points: [
            'Graduated with a GPA of 3.60 / 4.00.',
            'Specialized in statistical modeling, logic, and pure mathematics.',
            'Built the analytical foundation for engineering models, data pipelines, and quantitative research.'
        ],
        icon: GraduationCap,
        color: '#f29111',
    },
];

export default function Journey() {
    return (
        <div className="glass-card p-6 md:p-8">
            <h3 className="text-lg font-bold mb-8 flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-accent" />
                My Journey
            </h3>

            <div className="relative border-l-2 border-white/10 ml-3 space-y-10">
                {journeyItems.map((item, index) => (
                    <motion.div
                        key={index}
                        className="relative pl-8"
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 }}
                    >
                        {/* Timeline Dot */}
                        <div
                            className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full border-2 border-background flex items-center justify-center"
                            style={{ backgroundColor: item.color }}
                        />

                        {/* Content */}
                        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-1.5 gap-y-1">
                            <div className="flex items-center gap-2">
                                <item.icon className="w-4 h-4 text-foreground-muted" />
                                <h4 className="font-bold text-foreground text-base">{item.title}</h4>
                            </div>
                            <span className="text-xs font-mono text-accent/90 bg-accent/10 px-2.5 py-1 rounded w-fit sm:mt-0">
                                {item.year}
                            </span>
                        </div>

                        <p className="text-sm text-accent font-semibold mb-3">
                            {item.company}
                        </p>

                        <ul className="list-disc list-outside ml-4 space-y-2 text-xs text-foreground-muted/90 leading-relaxed">
                            {item.points.map((point, pIdx) => (
                                <li key={pIdx}>{point}</li>
                            ))}
                        </ul>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
