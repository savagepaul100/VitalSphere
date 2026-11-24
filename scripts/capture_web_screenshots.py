import subprocess
import time
import os

os.makedirs('target/screenshots', exist_ok=True)
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

shots = [
    {
        "url": "https://vitalsphere-9351.web.app/?view=desktop",
        "output": "target/screenshots/web_hero.png",
        "size": "1366,900"
    },
    {
        "url": "https://vitalsphere-9351.web.app/#register",
        "output": "target/screenshots/web_donor_reg.png",
        "size": "1366,1050"
    },
    {
        "url": "https://vitalsphere-9351.web.app/#request",
        "output": "target/screenshots/web_emergency_req.png",
        "size": "1366,1050"
    },
    {
        "url": "https://vitalsphere-9351.web.app/m/index.html",
        "output": "target/screenshots/web_mobile.png",
        "size": "412,915"
    }
]

for s in shots:
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={s['size']}",
        f"--screenshot={os.path.abspath(s['output'])}",
        s["url"]
    ]
    print(f"Capturing {s['output']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(s['output']):
        print(f" -> SUCCESS: {os.path.getsize(s['output'])} bytes")
    else:
        print(f" -> FAILED: {res.stderr}")
