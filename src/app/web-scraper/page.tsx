"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  ArrowLeft,
  MessageCircle,
  Database,
  Search,
  Link as LinkIcon,
} from "lucide-react";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";
import { apiCall, API_ENDPOINTS } from "@/config/api";

export default function WebScraperPage() {
  const [urlsText, setUrlsText] = useState("");
  const [ingestLoading, setIngestLoading] = useState(false);
  const [qaLoading, setQaLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [chunksCreated, setChunksCreated] = useState<number | null>(null);

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant" | "system"; content: string }>>([]);

  const { userId, sessionId: _sessionId } = useSession();

  const handleIngest = async () => {
    setIngestLoading(true);
    try {
      const urls = urlsText
        .split("\n")
        .map((u) => u.trim())
        .filter(Boolean);

      if (urls.length === 0) {
        alert("Provide at least one URL");
        return;
      }

      const payload: any = {
        urls,
        session_id: sessionId || undefined,
        chunk_size: 1000,
        chunk_overlap: 200,
      };

      const resp = await apiCall(API_ENDPOINTS.WEBRAG_INGEST, {
        method: "POST",
        body: JSON.stringify(payload),
      });

      setSessionId(resp.session_id);
      setChunksCreated(resp.chunks_created);
      setMessages((m) => [
        ...m,
        {
          role: "system",
          content: `Ingested ${resp.urls_ingested} URL(s). session_id=${resp.session_id} chunks=${resp.chunks_created}`,
        },
      ]);
    } catch (err) {
      console.error("Ingest error:", err);
      alert("WebRAG ingest failed: " + (err as Error).message);
    } finally {
      setIngestLoading(false);
    }
  };

  const handleAsk = async () => {
    setQaLoading(true);
    try {
      if (!sessionId) {
        alert("Ingest at least one URL first");
        return;
      }
      if (!question.trim()) {
        alert("Ask a question");
        return;
      }

      const q = question.trim();
      setMessages((m) => [...m, { role: "user", content: q }]);

      const resp = await apiCall(API_ENDPOINTS.WEBRAG_QUERY, {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, question: q, top_k: 5 }),
      });

      setMessages((m) => [
        ...m,
        { role: "assistant", content: resp.answer || "" },
        { role: "system", content: JSON.stringify(resp.sources || [], null, 2) },
      ]);

      setQuestion("");
    } catch (err) {
      console.error("Query error:", err);
      setMessages((m) => [...m, { role: "assistant", content: "Failed to answer." }]);
      alert("WebRAG query failed: " + (err as Error).message);
    } finally {
      setQaLoading(false);
    }
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
              <MessageCircle className="w-4 h-4 mr-2 text-green-400" />
              <span className="text-sm font-medium text-white/80">
                WebRAG AI Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              WebRAG
              <br />
              <span className="gradient-text">Ingest + Chat</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Ingest URLs (scrape + chunk) and ask questions. This mirrors the Streamlit WebRAG tab.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <Database className="h-6 w-6 text-green-400" />
                WebRAG Ingest
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-white/80">
                    URLs to ingest (one per line)
                  </label>
                </div>
                <textarea
                  placeholder={'https://example.com/article1\nhttps://example.com/article2'}
                  value={urlsText}
                  onChange={(e) => setUrlsText(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-green-400 font-mono text-sm"
                />
              </div>

              <Button
                onClick={handleIngest}
                disabled={ingestLoading || !urlsText.trim()}
                className="w-full button-primary flex items-center gap-2"
              >
                {ingestLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Ingesting...
                  </>
                ) : (
                  <>
                    <LinkIcon className="h-4 w-4" />
                    Ingest URLs
                  </>
                )}
              </Button>

              <div className="text-sm text-white/70">
                <div>Session: <span className="text-white">{sessionId || "(none)"}</span></div>
                {chunksCreated !== null && (
                  <div>Chunks created: <span className="text-white">{chunksCreated}</span></div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Chat */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <Search className="h-6 w-6 text-yellow-400" />
                WebRAG Chat
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white/80 mb-2">Question</label>
                <input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask a question about the ingested pages"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-yellow-400"
                />
              </div>

              <Button
                onClick={handleAsk}
                disabled={qaLoading || !question.trim()}
                className="w-full button-primary flex items-center gap-2"
              >
                {qaLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Answering...
                  </>
                ) : (
                  <>
                    <MessageCircle className="h-4 w-4" />
                    Ask
                  </>
                )}
              </Button>

              {messages.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="space-y-3"
                >
                  {messages.slice(-12).map((m, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border ${
                        m.role === "user"
                          ? "bg-blue-500/10 border-blue-400/20"
                          : m.role === "assistant"
                          ? "bg-green-500/10 border-green-400/20"
                          : "bg-white/5 border-white/10"
                      }`}
                    >
                      <div className="text-xs text-white/60 mb-1">{m.role}</div>
                      <pre className="whitespace-pre-wrap text-sm text-white/80 font-sans">
                        {m.content}
                      </pre>
                    </div>
                  ))}
                </motion.div>
              )}
            </CardContent>
          </Card>

          {/* Info */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-2xl text-white flex items-center gap-3">
                    <Database className="h-6 w-6 text-purple-400" />
                    Notes
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-white/70 space-y-2">
                    <div>
                      This uses backend endpoints:
                      <div className="font-mono text-xs text-white/60">POST /webrag/ingest</div>
                      <div className="font-mono text-xs text-white/60">POST /webrag/query</div>
                    </div>
                    <div>
                      For the assignment requirements, you can:
                      <div className="font-mono text-xs text-white/60">1) Discover news</div>
                      <div className="font-mono text-xs text-white/60">2) Ingest article URLs here</div>
                      <div className="font-mono text-xs text-white/60">3) Ask questions or generate summaries (Summaries tab/page)</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
