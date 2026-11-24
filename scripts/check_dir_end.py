with open("public/directory-data.js", "r", encoding="utf-8") as f:
    text = f.read()

print("Length of directory-data.js:", len(text))
print("End of directory-data.js:\n", text[-300:])
