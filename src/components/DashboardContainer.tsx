'use client';

import { useState } from 'react';
import { Play, Image as ImageIcon } from 'lucide-react';
import InteractiveDashboard from './InteractiveDashboard';

interface DashboardContainerProps {
  slug: string;
}

export default function DashboardContainer({ slug }: DashboardContainerProps) {
  const [activeTab, setActiveTab] = useState<'interactive' | 'screenshot'>('screenshot');

  const imageUrls: Record<string, string> = {
    'analisis-sentimen-ruu-tni': '/images/projects/analisis-sentimen-ruu-tni.png',
    'toko-online': '/images/projects/toko-online.png',
    'klasifikasi-diabetes-dna': '/images/projects/klasifikasi-diabetes-dna.png',
    'cs-ai-agent': '/images/projects/cs-ai-agent.png',
    'avg-down-idx': '/images/projects/avg-down-idx.png',
    'data-saham-indonesia': '/images/projects/data-saham-indonesia.png',
  };

  const imageSrc = imageUrls[slug] || '/images/projects/analisis-sentimen-ruu-tni.png';

  return (
    <div className="w-full">
      {/* Tab Controls */}
      <div className="flex gap-2 border-b border-card-border pb-3 mb-6">
        <button
          onClick={() => setActiveTab('screenshot')}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg cursor-pointer transition-all ${
            activeTab === 'screenshot'
              ? 'bg-accent text-background font-bold shadow-md shadow-accent/15'
              : 'glass-card hover:bg-accent/10 text-foreground-muted'
          }`}
        >
          <ImageIcon className="w-4 h-4" />
          Real Dashboard Screenshot
        </button>
        <button
          onClick={() => setActiveTab('interactive')}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg cursor-pointer transition-all ${
            activeTab === 'interactive'
              ? 'bg-accent text-background font-bold shadow-md shadow-accent/15'
              : 'glass-card hover:bg-accent/10 text-foreground-muted'
          }`}
        >
          <Play className="w-4 h-4" />
          Interactive Mockup Simulator
        </button>
      </div>

      {/* Content Rendering */}
      <div className="w-full flex justify-center transition-all duration-300">
        {activeTab === 'screenshot' ? (
          <div className="glass-card p-2 bg-background-secondary border border-card-border overflow-hidden rounded-2xl w-full shadow-lg group">
            <div className="relative aspect-video w-full overflow-hidden rounded-xl">
              <img
                src={imageSrc}
                alt="Real Dashboard Screenshot"
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.02]"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background/40 to-transparent pointer-events-none" />
            </div>
            <div className="p-3 text-center text-xs text-foreground-muted font-medium border-t border-card-border mt-2">
              High-fidelity Power BI Dashboard layout. Switch to the simulator to test filters dynamically.
            </div>
          </div>
        ) : (
          <InteractiveDashboard slug={slug} />
        )}
      </div>
    </div>
  );
}
