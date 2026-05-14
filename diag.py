import re
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
sc = html.rfind('<script>')
se = html.rfind('</script>')
js = html[sc+8:se]
print('FILE: HTML lines=%d, JS lines=%d' % (html.count('\n'), js.count('\n')))
import collections
funcs = re.findall(r'function ([a-zA-Z0-9_]+)\s*\(', js)
cnt = collections.Counter(funcs)
print('\nDUPLICATE FUNCTIONS:')
[print('  DUPE: %s x%d' % (f,c)) for f,c in cnt.items() if c>1]
print('\nALL FUNCTIONS:')
[print('  '+f) for f in sorted(set(funcs))]
print('\nTRY/CATCH:')
print('  try: %d, catch: %d' % (js.count('try{')+js.count('try {'), js.count('catch(')+js.count('catch (')))
print('\nKEY CHECKS:')
checks = ['loadAll','switchTab','adminToken','saveProfile','loadProfile','showUserProfileBanner','updateNavDate','applyProfileToSite','renderCategories','addSocialCategory']
[print('  %s: %s' % (k, 'YES' if k in js else 'MISSING')) for k in checks]
print('\nHTML ELEMENTS:')
elems = ['pane-profile','academyProfileCard','userProfileBanner','userInfoCard','cat-list','p-bio','p-name','navDate','saveProfileBtn']
[print('  %s: %s' % (e, 'YES' if e in html else 'MISSING')) for e in elems]
print('\nAPI FETCH CALLS:')
apis = re.findall(r"fetch\('(/api/[^']+)'", js)
[print('  '+a) for a in apis]
print('\n_sp declarations: %d' % (js.count('const _sp')+js.count('var _sp')))
