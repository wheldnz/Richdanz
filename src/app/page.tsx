'use client';

import dynamic from 'next/dynamic';
import Navigation from '@/components/Navigation';
import Hero from '@/sections/Hero';
import Projects from '@/sections/Projects';
import About from '@/sections/About';
import Certificates from '@/sections/Certificates';
import Contact from '@/sections/Contact';

// Dynamically import ParticleBackground to avoid SSR issues with canvas
const ParticleBackground = dynamic(
  () => import('@/components/ParticleBackground'),
  { ssr: false }
);

export default function Home() {
  return (
    <div className="relative min-h-screen bg-background">
      {/* Animated Particle Background */}
      <ParticleBackground />

      {/* Grid Pattern Overlay */}
      <div className="fixed inset-0 bg-grid pointer-events-none opacity-30 z-0" />

      {/* Navigation */}
      <Navigation />

      {/* Main Content */}
      <main className="relative z-10">
        <Hero />
        <Projects />
        <About />
        <Certificates />
        <Contact />
      </main>
    </div>
  );
}
