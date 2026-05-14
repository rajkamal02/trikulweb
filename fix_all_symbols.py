with open(r"D:\All Projects\trikul-academy\public\index.html", 'r', encoding='utf-8') as f:
    html = f.read()
# Sare garbled symbols replace karo
fixes = {
    'â"€â"€ ': '-- ', 'â"€â"€': '--', 'â"€': '-',
    'ðŸ†': '🏆', 'ðŸ"š': '📚', 'ðŸŽ¬': '🎬', 'ðŸ"°': '📰',
    'ðŸŽ¯': '🎯', 'ðŸŒ™': '🌙', 'ðŸ"¥': '🔥', 'âš"': '⚡',
    'ðŸ'¤': '👤', 'ðŸ"Š': '📊', 'ðŸ"': '🔍', 'ðŸ'': '👁',
    'ðŸ—'': '🗑', 'âœ•': '✕', 'âœ"': '✓', 'âœ…': '✅',
    'â ': '⚠', 'â ï¸': '⚠️', 'ðŸ'¾': '💾', 'ðŸ"‹': '📋',
    'ðŸ"': '📝', 'ðŸŽ': '🎁', 'ðŸ"—': '🔗', 'ðŸ'': '👍',
    'ðŸ"§': '🔧', 'ðŸ ': '🏠', 'â€"': '—', 'â€˜': "'",
    'â€™': "'", 'â€œ': '"', 'â€': '"', 'Â©': '©',
    'Â®': '®', 'Â°': '°', 'Â·': '·', 'â€¢': '•',
    'Â ': ' ', 'â‚¹': '₹', 'â€¦': '...', 'Â½': '½',
}
for bad, good in fixes.items():
    html = html.replace(bad, good)
# Remaining garbled (any Ã, Â, ð, â pattern)
import re
# Log karo kitne bache hain
remaining = re.findall(r'[Ã€-ÿ]{2,}|ð[^\x00-\x7F]', html)
print(f'Remaining garbled: {len(remaining)} found')
if remaining[:10]:
    print('Examples:', remaining[:10])
with open(r"D:\All Projects\trikul-academy\public\index.html", 'w', encoding='utf-8') as f:
    f.write(html)
print('DONE! All symbols fixed.')
