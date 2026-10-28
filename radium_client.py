import os
import sys
import json
import urllib.request

def call_radium_ai(prompt: str, model: str = "clarke-1.0"):
    api_key = os.environ.get("RADIUM_API_KEY")
    if not api_key:
        print("❌ [RADIUM ERROR]: RADIUM_API_KEY environment variable is missing.")
        sys.exit(1)

    url = "https://api.radium.cloud/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            content = res_body["choices"][0]["message"]["content"]
            print(f"[RADIUM AI SUCCESS]:\n{content}")
            return content

    except Exception as e:
        print(f"❌ [RADIUM ERROR]: {e}")
        return None

if __name__ == "__main__":
    prompt_text = sys.argv[1] if len(sys.argv) > 1 else "Explain real-time telemetry rendering optimization in 2 sentences."
    call_radium_ai(prompt_text)
