with open("public/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

emojis = ['🎉', '🩺', '🩸', '📄', '📞', '🏥', '🔔', '🚨', '🔑', '📍', '✍', '👥', '🏠', '🖥', '👁', '📎']

for i, l in enumerate(lines):
    found = [e for e in emojis if e in l]
    if found:
        print(f"Line {i+1}: {found} -> {l.strip()[:100]}")
