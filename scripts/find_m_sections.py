with open("public/m/index.html", "r", encoding="utf-8") as f:
    text = f.read()

idx1 = text.find("Desktop [PC]")
if idx1 != -1:
    print("Desktop [PC] surrounding:")
    print(text[idx1-100:idx1+300])

idx2 = text.find("stat-chip")
if idx2 != -1:
    print("stat-chip surrounding:")
    print(text[idx2-100:idx2+400])
