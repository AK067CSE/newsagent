"use client";

import { createContext, useContext, useState, ReactNode } from "react";

interface SessionContextType {
  userId: string;
  sessionId: string;
  setUserId: (id: string) => void;
  setSessionId: (id: string) => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: ReactNode }) {
  const [userId, setUserId] = useState("user_" + Math.random().toString(36).substr(2, 9));
  const [sessionId, setSessionId] = useState("session_" + Math.random().toString(36).substr(2, 9));

  return (
    <SessionContext.Provider value={{ userId, sessionId, setUserId, setSessionId }}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error("useSession must be used within a SessionProvider");
  }
  return context;
}
