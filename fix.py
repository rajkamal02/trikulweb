with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Remove duplicate JS injections - keep only first occurrence
import re
# Fix duplicate updateNavDate blocks
parts = html.split('// DATE\nfunction updateNavDate()')
if len(parts) > 2:
    # Keep everything before first injection + first injection + everything after last injection end
    # Find where the JS block ends (before loadAll)
    clean = parts[0] + '// DATE\nfunction updateNavDate()' + parts[1]
    # Now parts[2] onwards are duplicates - find loadAll in remaining and keep from there
    remaining = '// DATE\nfunction updateNavDate()'.join(parts[2:])
    loadall_idx = remaining.find('loadAll();')
    if loadall_idx >= 0:
        clean += remaining[loadall_idx:]
    html = clean
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed! Duplicates removed.')
