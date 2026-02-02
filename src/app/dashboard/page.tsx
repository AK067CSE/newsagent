"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  Search,
  Download,
  FileText,
  Tags,
  Sparkles,
  Save,
  BarChart3,
  TrendingUp,
  Globe,
  Brain,
  ArrowRight,
} from "lucide-react";
import { motion } from "@/components/ui/motion";
import { API_ENDPOINTS, apiCall } from "@/config/api";
import { useEffect } from "react";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalProcessed: 0,
    successRate: "0%",
    activeAgents: 0,
    lastUpdate: "Never"
  });
  const [loading, setLoading] = useState(true);

  // Fetch dashboard stats from backend
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiCall(API_ENDPOINTS.DASHBOARD_STATS);
        setStats({
          totalProcessed: data.total_articles || 0,
          successRate: `${data.success_rate || 0}%`,
          activeAgents: data.active_tasks || 0,
          lastUpdate: data.last_update || "Unknown"
        });
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    // Refresh stats every 30 seconds
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const agents = [
    {
      title: "News Discovery",
      description: "Multi-site news search and discovery across multiple sources",
      icon: Search,
      color: "blue",
      href: "/news-discoverer",
      status: "active"
    },
    {
      title: "WebRAG",
      description: "Ingest URLs and chat / retrieve answers from scraped content",
      icon: Download,
      color: "green",
      href: "/web-scraper",
      status: "active"
    },
    {
      title: "Content Classifier",
      description: "Entity classification and company tagging for news articles",
      icon: Tags,
      color: "purple",
      href: "/content-classifier",
      status: "active"
    },
    {
      title: "AI Summarizer",
      description: "Generate concise 30-40 word summaries with business focus",
      icon: Sparkles,
      color: "yellow",
      href: "/ai-summarizer",
      status: "active"
    },
    {
      title: "Data Exporter",
      description: "Export processed data in CSV, JSON, and ZIP formats",
      icon: Save,
      color: "orange",
      href: "/data-exporter",
      status: "active"
    }
  ];

  const recentActivity = [
    { action: "Processed 50 articles", time: "2 min ago", type: "success" },
    { action: "Exported CSV file", time: "5 min ago", type: "success" },
    { action: "Scraped 25 articles", time: "8 min ago", type: "success" },
    { action: "Classified entities", time: "12 min ago", type: "success" },
  ];

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <div className="mx-auto px-4 py-8 relative z-10">
        <BackgroundBlur />

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
            <Brain className="w-4 h-4 mr-2 text-purple-400" />
            <span className="text-sm font-medium text-white/80">
              AI News Aggregation System
            </span>
          </div>

          <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
            Intelligent News
            <br />
            <span className="gradient-text">Processing Hub</span>
          </h1>

          <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
            Advanced AI-powered news aggregation with multi-agent orchestration, 
            WebRAG scraping, and intelligent content processing.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card className="glass-card">
              <CardContent className="p-6 text-center">
                <BarChart3 className="h-8 w-8 text-blue-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-1">{stats.totalProcessed.toLocaleString()}</div>
                <div className="text-sm text-white/70">Articles Processed</div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="glass-card">
              <CardContent className="p-6 text-center">
                <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-1">{stats.successRate}</div>
                <div className="text-sm text-white/70">Success Rate</div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card className="glass-card">
              <CardContent className="p-6 text-center">
                <Globe className="h-8 w-8 text-purple-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-1">{stats.activeAgents}</div>
                <div className="text-sm text-white/70">Active Agents</div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card className="glass-card">
              <CardContent className="p-6 text-center">
                <FileText className="h-8 w-8 text-orange-400 mx-auto mb-3" />
                <div className="text-3xl font-bold text-white mb-1">{stats.lastUpdate}</div>
                <div className="text-sm text-white/70">Last Update</div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Agent Cards */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            AI Agent Suite
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent, index) => (
              <motion.div
                key={agent.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className={`glass-card hover:glass-card-hover transition-all duration-300 ${
                  agent.status === "coming-soon" ? "opacity-60" : ""
                }`}>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-3">
                      <div className={`p-2 rounded-lg bg-${agent.color}-500/20`}>
                        <agent.icon className={`h-5 w-5 text-${agent.color}-400`} />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-white">{agent.title}</h3>
                        {agent.status === "coming-soon" && (
                          <span className="text-xs text-yellow-400">Coming Soon</span>
                        )}
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-white/70 mb-4">{agent.description}</p>
                    {agent.status === "active" ? (
                      <Link href={agent.href}>
                        <Button className="w-full button-primary flex items-center gap-2">
                          Launch Agent
                          <ArrowRight className="h-4 w-4" />
                        </Button>
                      </Link>
                    ) : (
                      <Button disabled className="w-full button-secondary flex items-center gap-2">
                        Coming Soon
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-xl text-white flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-blue-400" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentActivity.map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className={`w-2 h-2 rounded-full ${
                          activity.type === "success" ? "bg-green-400" : "bg-yellow-400"
                        }`} />
                        <span className="text-sm text-white">{activity.action}</span>
                      </div>
                      <span className="text-xs text-white/50">{activity.time}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
          >
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-xl text-white flex items-center gap-2">
                  <Brain className="h-5 w-5 text-purple-400" />
                  System Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-white/70">WebRAG Scraper</span>
                    <span className="px-2 py-1 bg-green-500/20 border border-green-400 rounded text-xs text-green-300">
                      Online
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-white/70">AI Models</span>
                    <span className="px-2 py-1 bg-green-500/20 border border-green-400 rounded text-xs text-green-300">
                      Active
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-white/70">Database</span>
                    <span className="px-2 py-1 bg-green-500/20 border border-green-400 rounded text-xs text-green-300">
                      Connected
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-white/70">API Rate Limit</span>
                    <span className="px-2 py-1 bg-yellow-500/20 border border-yellow-400 rounded text-xs text-yellow-300">
                      75%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
