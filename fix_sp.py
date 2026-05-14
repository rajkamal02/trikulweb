with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Duplicate _sp hatao - sirf pehli occurrence rakhni hai
first = html.find("const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');")
second = html.find("const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');", first + 1)
if second != -1:
    html = html[:second] + html[second:].replace(
        "const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');",
        "_sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}')",  # const hata do
        1
    )
    print('Duplicate _sp fixed!')
else:
    print('No duplicate found - already ok!')
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
