import re
with open(r"D:\All Projects\trikul-academy\public\index.html", 'r', encoding='utf-8') as f:
    html = f.read()
# FIX 1: Garbled mojibake characters fix
replacements = {
    'â"€': '-', 'â"€â"€': '--', 'âš"': '⚡',
    'ðŸ†': '🏆', 'ðŸ"š': '📚', 'ðŸŽ¬': '🎬',
    'ðŸ"°': '📰', 'ðŸŽ¯': '🎯', 'ðŸŒ™': '🌙',
    'ðŸ"¥': '🔥', 'â€"': '—', 'â€˜': "'", 'â€™': "'",
    'Â©': '©', 'Â®': '®', 'â€¢': '•',
}
for bad, good in replacements.items():
    html = html.replace(bad, good)
print('FIX 1: Garbled symbols fixed')
# FIX 2: Remove duplicate ENHANCED THEME CSS blocks (keep only first)
theme_marker = '/* ENHANCED THEME v2 */'
first = html.find(theme_marker)
second = html.find(theme_marker, first + 1)
if second != -1:
    third = html.find(theme_marker, second + 1)
    style_end = html.find('</style>', second)
    if third != -1:
        html = html[:second] + html[style_end:]
    else:
        html = html[:second] + html[style_end:]
    print('FIX 2: Duplicate CSS blocks removed')
else:
    print('FIX 2: No duplicates found')
# FIX 3: Remove duplicate navDate spans (keep only first)
html = re.sub(
    r'(<span id="navDate">[^<]*</span>\s*){2,}',
    '<span id="navDate"></span>\n    ',
    html
)
print('FIX 3: Duplicate navDate spans removed')
with open(r"D:\All Projects\trikul-academy\public\index.html", 'w', encoding='utf-8') as f:
    f.write(html)
print('DONE! File saved.')
