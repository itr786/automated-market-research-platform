"use client";

import { useEffect, useState } from "react";

type Brief = { id: number; market_name: string; question: string; status: string; progress: number };

export default function Home() {
  const [briefs, setBriefs] = useState<Brief[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/research/`)
      .then((r) => r.json())
      .then(setBriefs)
      .catch(() => setBriefs([]));
  }, []);

  return (
    <main style={{ maxWidth: 960, margin: "40px auto", padding: 24, fontFamily: "sans-serif" }}>
      <h1>Market Research</h1>
      <p>Track research briefs and live analysis progress.</p>
      {briefs.map((brief) => (
        <article key={brief.id} style={{ border: "1px solid #ddd", borderRadius: 10, padding: 18, marginTop: 16 }}>
          <strong>{brief.market_name}</strong>
          <p>{brief.question}</p>
          <small>{brief.status} · {brief.progress}%</small>
          <progress value={brief.progress} max={100} style={{ display: "block", width: "100%", marginTop: 10 }} />
        </article>
      ))}
    </main>
  );
}
