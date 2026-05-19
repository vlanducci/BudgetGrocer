"use client"

export default function Home() {
  const runScraper = async () => {
    await fetch("/api/scrape", { method: "POST" })
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <button onClick={runScraper}>
        Run Python Scraper
      </button>
    </div>
  )
}