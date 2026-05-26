"use client"

export default function Home() {
  const runScraper = async () => {
    await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: "test" })
    });
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <button onClick={runScraper}>
        Run Python Scraper
      </button>
    </div>
  )
}