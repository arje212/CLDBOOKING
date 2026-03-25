path = r'C:\Users\cldto\OneDrive\Desktop\trainroom\booking\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the corruption - the raw heredoc text that got appended
markers = ["    @'\r\n", "    @'\n", "@'\r\n", "@'\n"]
cut = -1
for m in markers:
    idx = content.find(m)
    if idx != -1:
        cut = idx
        break

if cut == -1:
    print("ERROR: Could not find corruption marker. File may be OK or differently corrupted.")
    print("Last 200 chars:", repr(content[-200:]))
else:
    clean = content[:cut].rstrip() + '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(clean)
    print("SUCCESS: File cleaned. Cut at position", cut)
