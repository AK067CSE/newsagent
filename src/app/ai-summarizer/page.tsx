"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  ArrowLeft,
  FileText,
  Clock,
  CheckCircle,
  Zap,
  Sparkles,
} from "lucide-react";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";
import { apiCall, API_ENDPOINTS } from "@/config/api";

type SummarizeApiResponse = {
  status: string;
  summary: string;
  word_count: number;
  url?: string | null;
};

export default function AISummarizerPage() {
  const [url, setUrl] = useState("");
  const [minWords, setMinWords] = useState(30);
  const [maxWords, setMaxWords] = useState(40);
  const [result, setResult] = useState<SummarizeApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const { userId, sessionId } = useSession();

  const handleSummarize = async () => {
    setLoading(true);
    setResult(null);
    try {
      const payload = {
        url: url.trim(),
        min_words: minWords,
        max_words: maxWords,
      };

      const data = await apiCall(API_ENDPOINTS.SUMMARIZE, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setResult(data as SummarizeApiResponse);
    } catch (err) {
      console.error('Error:', err);
      alert("Failed to summarize: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const loadSampleUrl = () => {
    setUrl("https://example.com");
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <div className="mx-auto px-4 py-8 relative z-10">
        <BackgroundBlur />

        {/* Navigation */}
        <div className="flex items-center justify-between mb-8">
          <Link href="/dashboard">
            <Button className="button-secondary flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Button>
          </Link>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Hero section */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
              <Sparkles className="w-4 h-4 mr-2 text-yellow-400" />
              <span className="text-sm font-medium text-white/80">
                AI Summarizer Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              AI-Powered
              <br />
              <span className="gradient-text">Summarization</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Generate concise, factual summaries of news articles using advanced AI 
              models with precise word count control and business impact focus.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <FileText className="h-6 w-6 text-yellow-400" />
                Summarization Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-white/80">
                    Article URL
                  </label>
                  <Button
                    onClick={loadSampleUrl}
                    variant="outline"
                    size="sm"
                    className="text-xs"
                  >
                    Load Sample
                  </Button>
                </div>
                <input
                  placeholder="https://..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-yellow-400"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    Minimum Words
                  </label>
                  <input
                    type="number"
                    value={minWords}
                    onChange={(e) => setMinWords(Number(e.target.value))}
                    min="10"
                    max="100"
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-yellow-400"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    Maximum Words
                  </label>
                  <input
                    type="number"
                    value={maxWords}
                    onChange={(e) => setMaxWords(Number(e.target.value))}
                    min="20"
                    max="200"
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-yellow-400"
                  />
                </div>
              </div>

              <div className="p-4 bg-yellow-500/10 border border-yellow-400/20 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="h-4 w-4 text-yellow-400" />
                  <span className="text-sm font-medium text-yellow-300">Word Count Range</span>
                </div>
                <p className="text-xs text-yellow-200">
                  Summaries will be generated between {minWords} and {maxWords} words, 
                  focusing on business impact and factual information.
                </p>
              </div>

              <Button
                onClick={handleSummarize}
                disabled={loading || !url.trim()}
                className="w-full button-primary flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Generating Summaries...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    Generate Summary
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-2xl text-white flex items-center gap-3">
                    <CheckCircle className="h-6 w-6 text-green-400" />
                    Summarization Results
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <FileText className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">1</div>
                      <div className="text-sm text-white/70">URL Summarized</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Zap className="h-8 w-8 text-yellow-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">
                        {result.word_count || 0}
                      </div>
                      <div className="text-sm text-white/70">Word Count</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <CheckCircle className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.status}</div>
                      <div className="text-sm text-white/70">Status</div>
                    </div>
                  </div>

                  <div className="p-4 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border border-yellow-400/20 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="h-4 w-4 text-yellow-400" />
                      <span className="text-sm font-medium text-yellow-300">AI Summary</span>
                      <span className="text-xs text-yellow-200">
                        ({result.word_count || 0} words)
                      </span>
                    </div>
                    <p className="text-sm text-white leading-relaxed">
                      {result.summary}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
