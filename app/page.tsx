"use client";

import { useState } from "react";
import type { PolishResult } from "./api/polish/route";
import styles from "./page.module.css";

const CARDS = [
  { key: "interview", label: "면접용" },
  { key: "sns", label: "SNS용" },
  { key: "presentation", label: "발표용" },
] as const;

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<PolishResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim() || loading) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/polish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "다듬기에 실패했습니다.");
      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "다듬기에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>한 줄 자기소개 다듬기</h1>
      <p className={styles.subtitle}>자기소개 한 줄을 넣으면 면접용 · SNS용 · 발표용으로 다듬어 드려요.</p>

      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          className={styles.input}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="예) 경영학과 3학년이고, 데이터로 문제 푸는 걸 좋아합니다"
          maxLength={200}
        />
        <button className={styles.button} disabled={loading || !text.trim()}>
          {loading ? "다듬는 중…" : "다듬기"}
        </button>
      </form>

      {error && <p className={styles.error}>{error}</p>}

      {result && (
        <>
          <div className={styles.cards}>
            {CARDS.map(({ key, label }) => (
              <section key={key} className={styles.card}>
                <h2 className={styles.cardLabel}>{label}</h2>
                <p className={styles.cardText}>{result[key]}</p>
              </section>
            ))}
          </div>
          <p className={styles.model}>
            답한 모델 — <code>{result.model}</code>
          </p>
        </>
      )}
    </main>
  );
}
