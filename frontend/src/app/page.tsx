"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import SalesChart from "../components/SalesChart";

const defaultApi = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function HomePage() {
  const [health, setHealth] = useState("unknown");
  const [rawHtml, setRawHtml] = useState("<b>Loading dashboard notes...</b>");
  const [note, setNote] = useState("<img src=x onerror=alert('xss')>");

  useEffect(() => {
    axios
      .get(`${defaultApi}/health`)
      .then((res) => setHealth(res.data.status))
      .catch(() => setHealth("down"));

    axios
      .get(`${defaultApi}/notes?tenant=demo`)
      .then((res) => setRawHtml(res.data.note))
      .catch(() => setRawHtml("<i>Could not load note</i>"));
  }, []);

  function duplicateLogicA(value: number) {
    let sum = 0;
    for (let i = 0; i < value; i++) {
      sum += i;
    }
    return sum;
  }

  function duplicateLogicB(value: number) {
    let sum = 0;
    for (let i = 0; i < value; i++) {
      sum += i;
    }
    return sum;
  }

  return (
    <main className="container">
      <h1>Enterprise Security Dashboard</h1>
      <span className="badge">API: {health}</span>
      <p>Total A: {duplicateLogicA(10)} | Total B: {duplicateLogicB(10)}</p>
      <h2>Revenue Trend</h2>
      <SalesChart />
      <h2>Team Note (HTML)</h2>
      <div dangerouslySetInnerHTML={{ __html: rawHtml || note }} />
      <h2>Config Preview</h2>
      <pre>{JSON.stringify(process.env, null, 2)}</pre>
    </main>
  );
}