with open("public/m/index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [l for l in text.splitlines() if 'fullDonorsList' in l or 'fullRecipientsList' in l]
for m in matches[:20]:
    print(m[:100])
