"use client"

export default function Home() {
  const runScraper = async () => {
    await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: "test" })
    })
  }

  return (
    <div >
      {/* background */}
      <div className="mx-auto my-auto min-h-screen w-full max-w-5xl px-10 py-10 bg-gradient-to-b from-[#FCF7F8] to-[#8ED081]">
        {/* Inside main container */}
        <div className="flex items-center justify-center gap-x-4 rounded-xl bg-white p-20 shadow-lg dark:bg-[#FCF7F8]/50">
          <div className="flex flex-col items-center text-center">
            <div className="text-center p-2 text-4xl font-bold bg-gradient-to-r from-[#04724D] from-51% to-[#8ED081] to-49% bg-clip-text text-transparent">
              BudgetGrocer
            </div>

            <p className="text-gray-500 dark:text-[#04724D]">
              Your personal budget-friendly grocery shopping assistant
            </p>

            <div className="pt-10 flex items-center text-center gap-3">
              <input
                type="text"
                placeholder="Search for a product..."
                className="dark:text-[#04724D]/70 bg-[#FCF7F8] rounded-full border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#04724D] focus:border-transparent"
              />

              <button
                className="dark:text-[#FCF7F8] bg-[#8ED081] hover:bg-[#8ED081]/50 rounded-full p-2"
                onClick={runScraper}
              >
                Search
              </button>
            </div>

            <div className="bg-[#FCF7F8] rounded-lg p-2 mt-1"></div>
          </div>
        </div>
      </div>
    </div>
  )
}