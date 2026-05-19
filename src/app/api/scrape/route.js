import { execFile } from "child_process";

export async function POST() {
  return new Promise((resolve) => {
    execFile(
      ".venv\\Scripts\\python.exe",
      ["scraper.py"],
      (error, stdout, stderr) => {
        if (error) {
          console.log("ERROR:", error);
          console.log("STDERR:", stderr);
          resolve(Response.json({ error: stderr || error.message }, { status: 500 }));
          return;
        }

        resolve(Response.json({ result: stdout }));
      }
    );
  });
}