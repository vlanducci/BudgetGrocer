import "server-only";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForResult(jobId) {
  while (true) {
    const res = await fetch(`http://localhost:5000/results/${jobId}`);
    const data = await res.json();
    console.log("poll response:", data, jobId);

    if (data.status === "finished") {
      return data.results;
    }

    if (data.status === "failed") {
      throw new Error(data.error);
    }

    await new Promise(r => setTimeout(r, 1000));
  }
}

export async function POST(req) {
  let body;

  try {
    body = await req.json();
  } catch {
    return Response.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const query = body?.query;

  if (!query) {
    return Response.json({ error: "Missing query" }, { status: 400 });
  }

  const enqueueRes = await fetch("http://localhost:5000/enqueue", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query })
  });

  const enqueueData = await enqueueRes.json();

  if (!enqueueRes.ok) {
    return Response.json(
      { error: "Python API failed", details: enqueueData },
      { status: 500 }
    );
  }

  const jobId = enqueueData.job_id;

  const results = await waitForResult(jobId);

  return Response.json(results);
}