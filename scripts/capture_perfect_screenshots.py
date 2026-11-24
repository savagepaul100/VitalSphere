import subprocess
import os
from PIL import Image

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs('target/screenshots', exist_ok=True)

# 1. Full Desktop Web Landing Page
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--window-size=1366,2600",
    "--screenshot=" + os.path.abspath("target/screenshots/web_full_desktop.png"),
    "https://vitalsphere-9351.web.app/?view=desktop"
]
subprocess.run(cmd, check=True)

# 2. Hero Desktop
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--window-size=1366,850",
    "--screenshot=" + os.path.abspath("target/screenshots/web_hero.png"),
    "https://vitalsphere-9351.web.app/?view=desktop"
]
subprocess.run(cmd, check=True)

# 3. Mobile Web Experience
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--window-size=412,915",
    "--screenshot=" + os.path.abspath("target/screenshots/web_mobile.png"),
    "https://vitalsphere-9351.web.app/m/index.html"
]
subprocess.run(cmd, check=True)

# Crop sections from full desktop
full_img = Image.open("target/screenshots/web_full_desktop.png")
w, h = full_img.size
print(f"Full desktop size: {w}x{h}")

# Crop Donor Registration Form
# Looking at layout, register section is in the middle
crop_donor = full_img.crop((40, 950, 1326, 1750))
crop_donor.save("target/screenshots/web_donor_reg.png")

# Crop Emergency Request Form
crop_req = full_img.crop((40, 1750, 1326, 2550))
crop_req.save("target/screenshots/web_emergency_req.png")

print("All screenshots processed successfully!")
