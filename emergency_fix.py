with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
import re
# Puri broken profile JS section hatao aur clean version dalo
# Step 1: cat_js ka broken version hatao
html = re.sub(r'// ========== SOCIAL CATEGORIES ==========.*?window\._socialCategories=\[\];', 
    'window._socialCategories=[];', html, flags=re.DOTALL)
# Step 2: broken userInfoCard section hatao
html = re.sub(r'  // Bio \+ categories user card.*?uc\.style\.display=\(p\.bio\|\|cats\.length\)\?\'block\':\'none\';\n\}', 
    "  b.style.display=p.name?'flex':'none';\n}", html, flags=re.DOTALL)
# Step 3: broken fetch/auto-load hatao
html = re.sub(r"window\._socialCategories=\[\];\nfetch\('/api/profile'\).*?showUserProfileBanner\(_sp\);\n\}\);",
    "_sp2=JSON.parse(localStorage.getItem('trikul_profile')||'{}');\napplyProfileToSite(_sp2);\nshowUserProfileBanner(_sp2);",
    html, flags=re.DOTALL)
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Cleaned!')
