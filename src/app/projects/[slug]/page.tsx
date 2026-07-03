import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { marked } from 'marked';
import Link from 'next/link';
import { ArrowLeft, Calendar, Tag } from 'lucide-react';
import DashboardContainer from '@/components/DashboardContainer';

interface PageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function ProjectPage({ params }: PageProps) {
  const { slug } = await params;
  
  const filePath = path.join(process.cwd(), 'src/content/projects', `${slug}.md`);
  
  if (!fs.existsSync(filePath)) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center">
        <h1 className="text-2xl font-bold text-foreground">Project Not Found</h1>
        <p className="text-foreground-muted mt-2">The project you are looking for does not exist.</p>
        <Link href="/" className="btn-primary mt-6">
          Back to Home
        </Link>
      </div>
    );
  }
  
  // Read and parse markdown file
  const fileContent = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(fileContent);
  const htmlContent = marked(content);
  
  return (
    <div className="min-h-screen bg-background relative py-16 px-6 md:px-12">
      {/* Decorative Grid Background Overlay */}
      <div className="fixed inset-0 bg-grid pointer-events-none opacity-20 z-0" />
      
      <div className="max-w-4xl mx-auto relative z-10">
        {/* Back Button */}
        <Link 
          href="/" 
          className="inline-flex items-center gap-2 text-sm font-semibold text-foreground-muted hover:text-accent transition-colors mb-8 cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Lab
        </Link>
        
        {/* Project Header */}
        <div className="border-b border-foreground/10 pb-8 mb-8">
          <span className="text-accent font-mono text-xs uppercase tracking-widest block mb-3">
            {data.category === 'data' ? 'Data Analyst Project' : 'Project'}
          </span>
          <h1 className="text-3xl md:text-5xl font-black tracking-tight mb-4 text-foreground">
            {data.title}
          </h1>
          <p className="text-lg text-foreground-muted leading-relaxed mb-6">
            {data.description}
          </p>
          
          <div className="flex flex-wrap items-center gap-6 text-sm text-foreground-muted">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-accent" />
              <span>Project Duration: 2022 - 2025</span>
            </div>
            <div className="flex items-center gap-2">
              <Tag className="w-4 h-4 text-accent" />
              <div className="flex gap-2">
                {data.tags?.map((tag: string) => (
                  <span key={tag} className="bg-foreground/5 text-foreground-muted px-2 py-0.5 rounded text-xs font-mono">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Dashboard Simulation Section */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-foreground">Dashboard View & Simulation</h3>
            <span className="text-xs bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 px-2 py-0.5 rounded-full font-semibold">
              Live Assets
            </span>
          </div>
          <p className="text-sm text-foreground-muted mb-6 leading-relaxed">
            Berikut adalah tampilan real dashboard Power BI dan simulasinya. Klik tab di bawah untuk beralih antara melihat screenshot visual asli atau mencoba simulator interaktif secara langsung.
          </p>
          
          <div className="w-full">
            <DashboardContainer slug={slug} />
          </div>
        </div>

        {/* Case Study Content (Rendered Markdown) */}
        <div 
          className="prose-custom text-foreground"
          dangerouslySetInnerHTML={{ __html: htmlContent }} 
        />
      </div>
    </div>
  );
}
