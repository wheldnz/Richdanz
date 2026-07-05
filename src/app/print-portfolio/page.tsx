'use client';

import Link from 'next/link';
import { Printer, ArrowLeft, Mail, Phone, MapPin, Linkedin, Github, Globe, Award, Briefcase, GraduationCap, Code } from 'lucide-react';

const personalInfo = {
    name: 'M. WILDAN NURIL AKMAL',
    title: 'Data & Business Analyst',
    location: 'North Jakarta, Indonesia',
    email: 'wildanuril99@gmail.com',
    phone: '+6285225990234',
    linkedin: 'https://www.linkedin.com/in/wildan-nuril/',
    github: 'https://github.com/wheldnz',
    portfolio: 'https://portofolio-tau-lemon-87.vercel.app/'
};

const summary = `Data Analyst with 1+ years of experience transforming multi-source operational data into actionable business insights. Skilled in SQL, Python, BigQuery, Advanced Excel, reporting automation, and dashboard development using Power BI and Tableau. Mathematics graduate bringing rigorous logical and statistical frameworks to machine learning pipelines, predictive modeling, and quantitative research.`;

const experiences = [
    {
        role: 'Data & Business Analyst',
        company: 'PT. Sukses Multi Servis',
        period: 'June 2025 – Present',
        points: [
            'Engineered a data-driven statistical bidding algorithm using Python to identify market trends across 500+ operational units, successfully driving a 12% increase in gross profit margins.',
            'Architected and deployed automated data pipelines extracting raw metrics into Google BigQuery via Apps Script and Python, effectively eliminating manual reporting and improving data accessibility by 50%.',
            'Developed scalable enterprise BI architectures via Power BI, monitoring SLAs and KPIs for 10,000+ monthly transactions to enable robust self-service analytics for stakeholders.',
            'Restructured complex relational data models for 1,000+ SKUs, achieving 98% inventory accuracy and accelerating stock-picking time by 25% through systematic variance tracking.',
            'Executed comprehensive P&L analyses and cross-branch data validation, maintaining a 99.7% reporting accuracy rate that directly influenced executive decisions on strategic branch expansions.'
        ]
    },
    {
        role: 'Database Management (Intern)',
        company: 'PT. ASABRI (Persero) KC Malang',
        period: 'June – July 2024',
        points: [
            'Managed and audited 1,000+ sensitive participants\' records within the internal CMS, ensuring zero data-loss workflows and resolving inconsistencies to hit a 98% data accuracy rate.',
            'Programmed document archiving and scanning logic to replace legacy manual input setups, successfully reducing daily processing time by 40%.'
        ]
    }
];

const education = {
    school: 'State Islamic University of Maulana Malik Ibrahim Malang',
    degree: 'Bachelor of Science in Mathematics',
    gpa: 'GPA: 3.60',
    period: 'Aug 2021 – Dec 2024',
    details: 'Specialized in statistical modeling, logic, and pure mathematics. Formed the analytical foundation for machine learning pipelines and quantitative analysis.'
};

const skills = {
    technical: ['SQL (BigQuery, MySQL, PostgreSQL)', 'Python (Pandas, NumPy, Scikit-learn, NLP)', 'Tableau & Power BI', 'Advanced Excel (XLOOKUP, ARRAYFORMULA, VSTACK)'],
    analytics: ['Predictive Modeling', 'ETL Pipelines & Automation', 'Business Intelligence (BI)', 'Data Validation & Auditing'],
    frameworks: ['Google Cloud Platform (GCP)', 'Google Apps Script', 'Next.js & React', 'PHP & Laravel', 'Git & GitHub']
};

const topProjects = [
    {
        title: 'Analisis Sentimen RUU TNI (NLP)',
        category: 'Data Science / NLP',
        tech: ['Python', 'Sastrawi Stemmer', 'TF-IDF', 'Naïve Bayes'],
        description: 'Analyzed public sentiment regarding the Revision of the TNI Law. Built a custom Indonesian stemming and tokenization NLP pipeline to classify sentiments into Positive, Negative, and Neutral with high accuracy.'
    },
    {
        title: 'Klasifikasi Diabetes Sekuens DNA',
        category: 'Math & Machine Learning',
        tech: ['Python', 'DNA K-mers', 'Hamming Distance', 'SVM / KNN'],
        description: 'Peer-reviewed research and implementation presented at the 14th International Conference on Green Technology. Applied CNN and DNA K-mer distance metrics to classify genetic sequences for diabetes risk.'
    },
    {
        title: 'Kalkulator Average Down Saham IDX',
        category: 'Financial Modeling',
        tech: ['Next.js', 'TypeScript', 'TailwindCSS', 'Financial Formulas'],
        description: 'Interactive calculator for retail investors to model stock average-down costs, calculated required price rises, and floating loss reductions, providing clean data-driven portfolio management tools.'
    },
    {
        title: 'Enterprise Sales Analytics Dashboard',
        category: 'Business Intelligence',
        tech: ['Power BI', 'DAX', 'SQL Server', 'Star Schema'],
        description: 'Simulated interactive Power BI dashboard featuring dynamic sales pipeline metrics, performance indicators, and transaction trends across hundreds of distribution hubs.'
    },
    {
        title: 'Customer Churn Analytics & Retention',
        category: 'Predictive Analytics',
        tech: ['Python', 'Scikit-learn', 'Power BI', 'ETL Pipelines'],
        description: 'Built a predictive customer churn analytics dashboard, highlighting critical risk metrics, demographic breakdowns, and actionable customer retention triggers.'
    }
];

const certifications = [
    { title: 'International Conference Presenter (DNA Classification Paper)', issuer: 'GreenTech Conference', date: 'Oct 2024' },
    { title: 'AWS Certified Data Engineer - Associate', issuer: 'Udemy (Deepak Dubey)', date: 'Mar 2025' },
    { title: 'Data Science Mastery: Complete Bootcamp', issuer: 'Udemy (Vivian Aranha)', date: 'Jan 2025' },
    { title: 'Power BI Ultimate Course (Dual Certification)', issuer: 'Udemy (ExpertEase)', date: 'Mar 2025' },
    { title: 'Power BI Fundamentals A to Z', issuer: 'ExpertEase Education', date: 'Mar 2025' },
    { title: 'Master Tableau 2025: Complete Guide', issuer: 'Udemy (Programming Hub)', date: 'May 2025' }
];

export default function PrintPortfolio() {
    const handlePrint = () => {
        if (typeof window !== 'undefined') {
            window.print();
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 print:bg-white print:text-black font-sans pb-12">
            {/* Control Bar - Hidden in print */}
            <div className="bg-slate-900 border-b border-slate-800 px-6 py-4 sticky top-0 z-50 flex items-center justify-between print:hidden">
                <Link href="/" className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
                    <ArrowLeft className="w-4 h-4" />
                    Back to Portfolio Website
                </Link>
                <div className="flex items-center gap-3">
                    <span className="text-xs text-slate-400 font-mono hidden md:inline">
                        Tip: Set margins to "None" and tick "Background graphics" in print settings
                    </span>
                    <button
                        onClick={handlePrint}
                        className="bg-accent hover:bg-accent/80 text-background px-4 py-2 rounded-lg font-semibold text-sm transition-all flex items-center gap-2 cursor-pointer"
                    >
                        <Printer className="w-4 h-4" />
                        Print to PDF
                    </button>
                </div>
            </div>

            {/* A4 Sheet Wrapper */}
            <div className="max-w-[800px] mx-auto bg-slate-900 print:bg-white shadow-2xl print:shadow-none my-8 print:my-0 p-8 md:p-12 print:p-0 rounded-xl print:rounded-none border border-slate-800 print:border-none">
                {/* Header */}
                <div className="border-b-2 border-accent print:border-slate-800 pb-6 mb-6">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                        <div>
                            <h1 className="text-3xl font-extrabold tracking-tight text-white print:text-slate-900">
                                {personalInfo.name}
                            </h1>
                            <p className="text-accent font-mono text-sm mt-1 uppercase tracking-wider font-semibold">
                                {personalInfo.title}
                            </p>
                        </div>
                        {/* Contacts Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-1.5 text-xs text-slate-400 print:text-slate-600 font-mono">
                            <span className="flex items-center gap-1.5">
                                <Mail className="w-3.5 h-3.5 text-accent" />
                                {personalInfo.email}
                            </span>
                            <span className="flex items-center gap-1.5">
                                <Phone className="w-3.5 h-3.5 text-accent" />
                                {personalInfo.phone}
                            </span>
                            <span className="flex items-center gap-1.5">
                                <MapPin className="w-3.5 h-3.5 text-accent" />
                                {personalInfo.location}
                            </span>
                            <a href={personalInfo.linkedin} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 hover:text-white print:hover:text-black">
                                <Linkedin className="w-3.5 h-3.5 text-accent" />
                                linkedin.com/in/wildan-nuril
                            </a>
                            <a href={personalInfo.github} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 hover:text-white print:hover:text-black">
                                <Github className="w-3.5 h-3.5 text-accent" />
                                github.com/wheldnz
                            </a>
                            <a href={personalInfo.portfolio} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 hover:text-white print:hover:text-black">
                                <Globe className="w-3.5 h-3.5 text-accent" />
                                richdanz.vercel.app
                            </a>
                        </div>
                    </div>
                </div>

                {/* Summary */}
                <div className="mb-6">
                    <p className="text-sm text-slate-300 print:text-slate-700 leading-relaxed">
                        {summary}
                    </p>
                </div>

                {/* Main Content Layout */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Left Column (2/3 width) - Experience & Projects */}
                    <div className="md:col-span-2 space-y-6">
                        {/* Professional Experience */}
                        <div>
                            <h2 className="text-lg font-bold text-white print:text-slate-900 border-b border-slate-800 print:border-slate-200 pb-1.5 mb-3 flex items-center gap-2">
                                <Briefcase className="w-4 h-4 text-accent" />
                                Professional Experience
                            </h2>
                            <div className="space-y-5">
                                {experiences.map((exp, index) => (
                                    <div key={index}>
                                        <div className="flex justify-between items-baseline mb-1">
                                            <h3 className="font-bold text-sm text-white print:text-slate-900 font-sans">
                                                {exp.role}
                                            </h3>
                                            <span className="text-xs font-mono text-slate-400 print:text-slate-500">
                                                {exp.period}
                                            </span>
                                        </div>
                                        <p className="text-xs text-accent font-semibold mb-2">
                                            {exp.company}
                                        </p>
                                        <ul className="list-disc list-outside ml-4 space-y-1.5 text-xs text-slate-300 print:text-slate-700">
                                            {exp.points.map((pt, pIdx) => (
                                                <li key={pIdx} className="leading-relaxed">{pt}</li>
                                            ))}
                                        </ul>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Top Projects Showcase */}
                        <div>
                            <h2 className="text-lg font-bold text-white print:text-slate-900 border-b border-slate-800 print:border-slate-200 pb-1.5 mb-3 flex items-center gap-2">
                                <Code className="w-4 h-4 text-accent" />
                                Selected Projects Portfolio
                            </h2>
                            <div className="space-y-4">
                                {topProjects.map((proj, index) => (
                                    <div key={index} className="border-l-2 border-accent/30 print:border-slate-200 pl-3">
                                        <div className="flex justify-between items-baseline mb-1">
                                            <h3 className="font-bold text-xs text-white print:text-slate-900">
                                                {proj.title}
                                            </h3>
                                            <span className="text-[10px] font-mono text-accent print:text-slate-600 bg-accent/15 print:bg-slate-100 px-1.5 py-0.5 rounded">
                                                {proj.category}
                                            </span>
                                        </div>
                                        <p className="text-[11px] text-slate-400 print:text-slate-500 mb-1.5">
                                            <span className="font-semibold text-slate-300 print:text-slate-600">Tech:</span> {proj.tech.join(', ')}
                                        </p>
                                        <p className="text-xs text-slate-300 print:text-slate-700 leading-relaxed">
                                            {proj.description}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Right Column (1/3 width) - Education, Skills, Certs */}
                    <div className="space-y-6">
                        {/* Education */}
                        <div>
                            <h2 className="text-lg font-bold text-white print:text-slate-900 border-b border-slate-800 print:border-slate-200 pb-1.5 mb-3 flex items-center gap-2">
                                <GraduationCap className="w-4 h-4 text-accent" />
                                Education
                            </h2>
                            <div>
                                <h3 className="font-bold text-xs text-white print:text-slate-900">
                                    {education.degree}
                                </h3>
                                <p className="text-xs text-accent font-semibold mt-0.5 font-sans">
                                    {education.school}
                                </p>
                                <div className="flex justify-between text-[10px] font-mono text-slate-400 print:text-slate-500 mt-1">
                                    <span>{education.period}</span>
                                    <span className="font-bold text-accent">{education.gpa}</span>
                                </div>
                                <p className="text-[11px] text-slate-300 print:text-slate-600 mt-2 leading-relaxed">
                                    {education.details}
                                </p>
                            </div>
                        </div>

                        {/* Technical Skills */}
                        <div>
                            <h2 className="text-lg font-bold text-white print:text-slate-900 border-b border-slate-800 print:border-slate-200 pb-1.5 mb-3 flex items-center gap-2">
                                <Code className="w-4 h-4 text-accent" />
                                Core Skills
                            </h2>
                            <div className="space-y-3 text-xs">
                                <div>
                                    <span className="font-semibold text-slate-300 print:text-slate-800 block mb-1">Languages & Databases</span>
                                    <div className="flex flex-wrap gap-1">
                                        {skills.technical.map(s => (
                                            <span key={s} className="bg-slate-800 print:bg-slate-100 print:text-slate-800 text-[10px] px-1.5 py-0.5 rounded">
                                                {s}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <div>
                                    <span className="font-semibold text-slate-300 print:text-slate-800 block mb-1">Analytics Domains</span>
                                    <div className="flex flex-wrap gap-1">
                                        {skills.analytics.map(s => (
                                            <span key={s} className="bg-slate-800 print:bg-slate-100 print:text-slate-800 text-[10px] px-1.5 py-0.5 rounded">
                                                {s}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <div>
                                    <span className="font-semibold text-slate-300 print:text-slate-800 block mb-1">Tools & Platforms</span>
                                    <div className="flex flex-wrap gap-1">
                                        {skills.frameworks.map(s => (
                                            <span key={s} className="bg-slate-800 print:bg-slate-100 print:text-slate-800 text-[10px] px-1.5 py-0.5 rounded">
                                                {s}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Certifications */}
                        <div>
                            <h2 className="text-lg font-bold text-white print:text-slate-900 border-b border-slate-800 print:border-slate-200 pb-1.5 mb-3 flex items-center gap-2">
                                <Award className="w-4 h-4 text-accent" />
                                Certifications
                            </h2>
                            <ul className="space-y-2 text-xs text-slate-300 print:text-slate-700">
                                {certifications.map((c, idx) => (
                                    <li key={idx} className="border-b border-slate-800/50 print:border-slate-100 pb-1 last:border-0">
                                        <span className="font-semibold block text-slate-200 print:text-slate-800 leading-snug">
                                            {c.title}
                                        </span>
                                        <span className="text-[10px] font-mono text-slate-400 print:text-slate-500 flex justify-between mt-0.5">
                                            <span>{c.issuer}</span>
                                            <span>{c.date}</span>
                                        </span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
