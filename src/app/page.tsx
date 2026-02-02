"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  Search,
  Download,
  FileText,
  Tags,
  Sparkles,
  Save,
  Brain,
  ArrowRight,
  Globe,
  TrendingUp,
} from "lucide-react";
import { motion } from "@/components/ui/motion";

export default function HomePage() {
  const agents = [
    {
      title: "News Discovery",
      description: "Multi-site news search and discovery across multiple sources",
      icon: Search,
      color: "blue",
      href: "/news-discoverer",
      features: ["Multi-site search", "RSS feeds", "Real-time discovery"]
    },
    {
      title: "WebRAG",
      description: "Ingest URLs and chat / retrieve answers from scraped content",
      icon: Download,
      color: "green",
      href: "/web-scraper",
      features: ["URL ingest", "Chunking + retrieval", "Chat over sources"]
    },
    {
      title: "Content Classifier",
      description: "Entity classification and company tagging for news articles",
      icon: Tags,
      color: "purple",
      href: "/content-classifier",
      features: ["Company tagging", "Entity recognition", "Smart filtering"]
    },
    {
      title: "AI Summarizer",
      description: "Generate concise 30-40 word summaries with business focus",
      icon: Sparkles,
      color: "yellow",
      href: "/ai-summarizer",
      features: ["30-40 word summaries", "Business focus", "AI-powered"]
    },
    {
      title: "Data Exporter",
      description: "Export processed data in CSV, JSON, and ZIP formats",
      icon: Save,
      color: "orange",
      href: "/data-exporter",
      features: ["Multiple formats", "Submission-ready", "Metadata included"]
    },
    {
      title: "Dashboard",
      description: "Central hub for monitoring and managing all agents",
      icon: Brain,
      color: "pink",
      href: "/dashboard",
      features: ["Real-time stats", "System monitoring", "Activity tracking"]
    }
  ];

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <BackgroundBlur />

      <div className="relative z-10">
        {/* Hero Section */}
        <div className="text-center px-4 py-16 md:py-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
              <Brain className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-white/80">
                AI-Powered News Aggregation
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Intelligent News
              <br />
              <span className="gradient-text">Processing System</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed mb-8">
              Advanced AI-powered news aggregation with WebRAG technology, 
              multi-agent orchestration, and intelligent content processing.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/dashboard">
                <Button className="button-primary text-lg px-8 py-4">
                  <Brain className="w-5 h-5 mr-2" />
                  Launch Dashboard
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Link href="/news-discoverer">
                <Button className="button-secondary text-lg px-8 py-4">
                  <Search className="w-5 h-5 mr-2" />
                  Quick Start
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Features Grid */}
        <div className="px-4 py-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Multi-Agent Architecture
            </h2>
            <p className="text-lg text-white/70 max-w-2xl mx-auto">
              Six specialized AI agents working together to deliver comprehensive news processing
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
            {agents.map((agent, index) => (
              <motion.div
                key={agent.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <div className="glass-card glass-card-hover p-6 h-full">
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`p-3 rounded-lg bg-${agent.color}-500/20`}>
                      <agent.icon className={`h-6 w-6 text-${agent.color}-400`} />
                    </div>
                    <h3 className="text-xl font-semibold text-white">{agent.title}</h3>
                  </div>
                  
                  <p className="text-white/70 mb-6">{agent.description}</p>
                  
                  <div className="space-y-2 mb-6">
                    {agent.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-green-400"></div>
                        <span className="text-sm text-white/60">{feature}</span>
                      </div>
                    ))}
                  </div>

                  <Link href={agent.href}>
                    <Button className="w-full button-secondary">
                      Launch Agent
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Stats Section */}
        <div className="px-4 py-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="max-w-4xl mx-auto"
          >
            <div className="glass-card p-8">
              <h3 className="text-2xl font-bold text-white text-center mb-8">
                System Capabilities
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <Globe className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white mb-1">50+</div>
                  <div className="text-sm text-white/70">News Sources</div>
                </div>
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white mb-1">98.5%</div>
                  <div className="text-sm text-white/70">Success Rate</div>
                </div>
                <div className="text-center">
                  <Brain className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white mb-1">6</div>
                  <div className="text-sm text-white/70">AI Agents</div>
                </div>
                <div className="text-center">
                  <FileText className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white mb-1">1000+</div>
                  <div className="text-sm text-white/70">Articles/Day</div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* CTA Section */}
        <div className="px-4 py-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="text-center"
          >
            <div className="glass-card p-8 max-w-2xl mx-auto">
              <h3 className="text-2xl font-bold text-white mb-4">
                Ready to Transform Your News Processing?
              </h3>
              <p className="text-white/70 mb-6">
                Experience the power of AI agents working together to deliver 
                comprehensive news aggregation and analysis.
              </p>
              <Link href="/dashboard">
                <Button className="button-primary text-lg px-8 py-4">
                  Get Started Now
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
