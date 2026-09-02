"use client";

import { useEffect, useState } from "react";
import { subscribeToResearch, ResearchEvent } from "../lib/research-stream";

export function ResearchProgress({ briefId }: { briefId: number }) {
  const [event, setEvent] = useState<ResearchEvent>({ status: "queued", progress: 0, message: "Waiting to start" });
  const [connected, setConnected] = useState(false);

  useEffect(() => subscribeToResearch(briefId, setEvent, setConnected), [briefId]);

  return (
    <section aria-label="Research progress">
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <strong>{event.status}</strong>
        <span>{connected ? "Live" : "Reconnecting"}</span>
      </div>
      <progress max={100} value={event.progress} style={{ width: "100%" }} />
      <p>{event.message}</p>
    </section>
  );
}
