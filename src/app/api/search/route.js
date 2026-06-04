import "server-only";

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

  const res = await fetch("http://localhost:5000/enqueue", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query })
  });

  const data = await res.json();

  if (!res.ok) {
    return Response.json({
      error: "Python API failed",
      details: data
    }, { status: 500 });
  }

  return Response.json({
    ok: true,
    data
  });
}