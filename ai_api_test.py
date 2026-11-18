import os
import httpx
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY") or ""
r = httpx.post("https://api.groq.com/openai/v1/chat/completions",
               headers={"Authorization": f"Bearer {key}"},
               json={"model": "openai/gpt-oss-20b",
                     "messages": [{"role": "user", "content":
                                   'Reply with ONLY a JSON object like {"greeting": "..."} saying hi.'}],
                     "response_format": {"type": "json_object"},
                     "reasoning_effort": "low"}, timeout=45)
print(r.status_code)
print(r.text[:600])