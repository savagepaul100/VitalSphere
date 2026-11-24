import re
import subprocess
import os

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script(?:\s+type=[\"\'](.*?)[\"\'])?[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Found {len(scripts)} scripts in public/index.html')
for i, (stype, scode) in enumerate(scripts):
    scode = scode.strip()
    if not scode:
        continue
    temp_file = f'target/temp_script_{i}.js'
    os.makedirs('target', exist_ok=True)
    with open(temp_file, 'w', encoding='utf-8') as sf:
        sf.write(scode)
    res = subprocess.run(['node', '--check', temp_file], capture_output=True, text=True)
    if res.returncode == 0:
        print(f'Script #{i} (type="{stype}") -> VALID SYNTAX')
    else:
        print(f'Script #{i} (type="{stype}") -> ERROR:\n{res.stderr}')

with open('public/m/index.html', 'r', encoding='utf-8') as f:
    m_html = f.read()

m_scripts = re.findall(r'<script(?:\s+type=[\"\'](.*?)[\"\'])?[^>]*>(.*?)</script>', m_html, re.DOTALL)
print(f'\nFound {len(m_scripts)} scripts in public/m/index.html')
for i, (stype, scode) in enumerate(m_scripts):
    scode = scode.strip()
    if not scode:
        continue
    temp_file = f'target/m_temp_script_{i}.js'
    with open(temp_file, 'w', encoding='utf-8') as sf:
        sf.write(scode)
    res = subprocess.run(['node', '--check', temp_file], capture_output=True, text=True)
    if res.returncode == 0:
        print(f'Mobile Script #{i} (type="{stype}") -> VALID SYNTAX')
    else:
        print(f'Mobile Script #{i} (type="{stype}") -> ERROR:\n{res.stderr}')
