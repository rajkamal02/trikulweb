with open(r'D:\All Projects\trikul-academy\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Remaining garbled chars fix
html = html.replace('\u00e2\u009a\u00a1', '\u26a1')  # âš" -> ⚡
html = html.replace('\u00c3\u00a2\u00c5\u00a1\u00e2\u0082\u00ac\u00e2\u0084\u00a2', '\u26a1')
html = html.replace('\u00f0\u009f\u0094\u00a5', '\U0001f525')  # ðŸ"¥ -> 🔥
html = html.replace('\u00e2\u0080\u0094', '\u2014')  # â€" -> —
html = html.replace('\u00e2\u009a\u00a1', '\u26a1')
# Simple string replace approach
pairs = [
    ('âš"', '\u26a1'),
    ('ðŸ"¥', '\U0001f525'),
    ('â€"', '\u2014'),
    ('ðŸ"š', '\U0001f4da'),
    ('ðŸŽ¬', '\U0001f3ac'),
    ('ðŸ"°', '\U0001f4f0'),
    ('ðŸŽ¯', '\U0001f3af'),
    ('ðŸŒ™', '\U0001f319'),
    ('ðŸ†', '\U0001f3c6'),
    ('ðŸ'¤', '\U0001f464'),
    ('ðŸ"Š', '\U0001f4ca'),
    ('ðŸ'¾', '\U0001f4be'),
    ('ðŸ"', '\U0001f4dd'),
    ('â€"', '\u2014'),
    ('â€™', '\u2019'),
    ('â€˜', '\u2018'),
    ('Â©', '\u00a9'),
]
for bad, good in pairs:
    html = html.replace(bad, good)
with open(r'D:\All Projects\trikul-academy\public\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('DONE!')
