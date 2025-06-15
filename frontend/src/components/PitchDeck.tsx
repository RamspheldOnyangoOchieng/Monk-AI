import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { ChevronLeft, ChevronRight, Download } from 'lucide-react';
import { usePDF } from 'react-to-pdf';

const slides = [
  {
    title: "Monk AI: Autonomous Agent Platform",
    content: (
      <div className="space-y-4">
        <h2 className="text-3xl font-bold text-primary">Revolutionizing Business Automation</h2>
        <p className="text-xl">An intelligent platform that transforms how businesses interact with AI agents</p>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-primary/20 to-background"
  },
  {
    title: "Our Team",
    content: (
      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-2">
            <div className="w-32 h-32 rounded-full bg-primary/20 mx-auto mb-4"></div>
            <h3 className="text-xl font-semibold text-center">John Doe</h3>
            <p className="text-center text-muted-foreground">Lead Developer</p>
          </div>
          <div className="space-y-2">
            <div className="w-32 h-32 rounded-full bg-primary/20 mx-auto mb-4"></div>
            <h3 className="text-xl font-semibold text-center">Jane Smith</h3>
            <p className="text-center text-muted-foreground">AI Architect</p>
          </div>
          <div className="space-y-2">
            <div className="w-32 h-32 rounded-full bg-primary/20 mx-auto mb-4"></div>
            <h3 className="text-xl font-semibold text-center">Mike Johnson</h3>
            <p className="text-center text-muted-foreground">UX Designer</p>
          </div>
          <div className="space-y-2">
            <div className="w-32 h-32 rounded-full bg-primary/20 mx-auto mb-4"></div>
            <h3 className="text-xl font-semibold text-center">Sarah Wilson</h3>
            <p className="text-center text-muted-foreground">Product Manager</p>
          </div>
        </div>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-primary/20 to-background"
  },
  {
    title: "Technology Integration",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Advanced AI Architecture</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Multi-agent collaboration system</li>
          <li>Real-time task automation</li>
          <li>Intelligent decision-making capabilities</li>
          <li>Seamless API integrations</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-blue-500/20 to-background"
  },
  {
    title: "Autonomous Operations",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Self-Managing Agents</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>24/7 automated task execution</li>
          <li>Self-healing error recovery</li>
          <li>Adaptive learning capabilities</li>
          <li>Proactive problem-solving</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-green-500/20 to-background"
  },
  {
    title: "Business Impact",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Transformative Value</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>70% reduction in manual tasks</li>
          <li>50% faster process completion</li>
          <li>90% accuracy in operations</li>
          <li>Significant cost savings</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-purple-500/20 to-background"
  },
  {
    title: "Human-Agent Collaboration",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Enhanced Productivity</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Intuitive user interface</li>
          <li>Natural language interaction</li>
          <li>Real-time collaboration tools</li>
          <li>Seamless workflow integration</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-yellow-500/20 to-background"
  },
  {
    title: "Innovation & Originality",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Unique Approach</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Proprietary agent architecture</li>
          <li>Novel collaboration patterns</li>
          <li>Advanced learning algorithms</li>
          <li>Customizable agent behaviors</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-red-500/20 to-background"
  },
  {
    title: "Technical Excellence",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Robust Architecture</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Scalable microservices</li>
          <li>Real-time processing</li>
          <li>Advanced security features</li>
          <li>High availability design</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-indigo-500/20 to-background"
  },
  {
    title: "Market Potential",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Growth Opportunities</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Expanding AI market</li>
          <li>Growing automation demand</li>
          <li>Multiple industry applications</li>
          <li>Scalable business model</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-teal-500/20 to-background"
  },
  {
    title: "Implementation & ROI",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Quick Value Realization</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Rapid deployment</li>
          <li>Minimal training required</li>
          <li>Immediate productivity gains</li>
          <li>Measurable ROI metrics</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-orange-500/20 to-background"
  },
  {
    title: "Future Vision",
    content: (
      <div className="space-y-4">
        <h3 className="text-2xl font-semibold">Next Steps</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Advanced AI capabilities</li>
          <li>Industry-specific solutions</li>
          <li>Global market expansion</li>
          <li>Continuous innovation</li>
        </ul>
      </div>
    ),
    bgColor: "bg-gradient-to-br from-pink-500/20 to-background"
  }
];

export function PitchDeck() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const { toPDF, targetRef } = usePDF({
    filename: 'monk-ai-pitch-deck.pdf',
    page: { margin: 20 }
  });

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="absolute top-4 right-4 z-50">
        <Button
          variant="outline"
          onClick={() => toPDF()}
          className="flex items-center gap-2"
        >
          <Download className="h-4 w-4" />
          Download PDF
        </Button>
      </div>
      <div ref={targetRef}>
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
            className={`absolute inset-0 ${slides[currentSlide].bgColor} p-8`}
          >
            <Card className="h-full p-8">
              <div className="h-full flex flex-col">
                <h1 className="text-4xl font-bold mb-8">{slides[currentSlide].title}</h1>
                <div className="flex-1">
                  {slides[currentSlide].content}
                </div>
                <div className="flex justify-between items-center mt-8">
                  <Button
                    variant="outline"
                    onClick={prevSlide}
                    disabled={currentSlide === 0}
                  >
                    <ChevronLeft className="mr-2 h-4 w-4" />
                    Previous
                  </Button>
                  <span className="text-sm text-muted-foreground">
                    Slide {currentSlide + 1} of {slides.length}
                  </span>
                  <Button
                    variant="outline"
                    onClick={nextSlide}
                    disabled={currentSlide === slides.length - 1}
                  >
                    Next
                    <ChevronRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
} 