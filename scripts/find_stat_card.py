with open("public/index.html", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("ENROLLED DONORS")
if idx != -1:
    print(text[idx-100:idx+200])
else:
    print("ENROLLED DONORS not found")
