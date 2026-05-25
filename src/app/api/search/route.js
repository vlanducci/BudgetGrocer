import { Queue } from "bullmq"
import IORedis from "ioredis"

const connection = new IORedis({ host: "localhost", port: 6379 })

export async function POST(req) {
  const { query } = await req.json()

  const queue = new Queue("default", { connection })

  await queue.add("scrape", {
    query
  })

  return Response.json({ status: "queued" })
}