import re
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
sc = html.rfind('<script>')
se = html.rfind('</script>')
before_script = html[:sc+8]
js = html[sc+8:se]
after_script = html[se:]
# 1. Extra catch blocks hatao jo try-catch fixer ne galat add kiye
js = re.sub(r'\}catch\(e\)\{console\.error\(e\);\}', '}', js)
# 2. addSocialCategory function add karo (renderCategories ke pehle)
if 'addSocialCategory' not in js:
    add_js = """
function addSocialCategory(){
  var icon = document.getElementById('cat-icon') ? document.getElementById('cat-icon').value.trim() : '';
  if(!icon) icon = String.fromCodePoint(0x1F517);
  var name = document.getElementById('cat-name').value.trim();
  var url = document.getElementById('cat-url').value.trim();
  if(!name || !url){ alert('Name aur URL dono bharo!'); return; }
  if(!window._cats) window._cats = [];
  window._cats.push({id: String(Date.now()), icon: icon, name: name, url: url});
  if(document.getElementById('cat-icon')) document.getElementById('cat-icon').value = '';
  document.getElementById('cat-name').value = '';
  document.getElementById('cat-url').value = '';
  renderCategories();
}
function removeCategory(id){
  if(!window._cats) return;
  window._cats = window._cats.filter(function(c){ return c.id !== id; });
  renderCategories();
}
"""
    js = js.replace('function renderCategories()', add_js + 'function renderCategories()')
    print('addSocialCategory added')
# 3. window._cats initialize karo agar nahi hai
if 'window._cats' not in js:
    js = js.replace('function renderCategories()', 'window._cats = [];\nfunction renderCategories()')
    print('window._cats initialized')
# 4. Profile auto-load add karo end mein (agar missing hai)
if 'const _sp' not in js and '_sp2' not in js and 'auto-apply' not in js:
    auto_load = """
// Auto-apply saved profile
(function(){
  var sp = {};
  try { sp = JSON.parse(localStorage.getItem('trikul_profile') || '{}'); } catch(e){}
  if(sp && sp.name){
    applyProfileToSite(sp);
    showUserProfileBanner(sp);
  }
})();
"""
    js = js + auto_load
    print('Profile auto-load added')
# 5. renderCategories ko _cats use karne do
js = js.replace('window._socialCategories', 'window._cats')
js = js.replace('_socialCategories', '_cats')
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(before_script + js + after_script)
print('JS fixed!')
# 6. p-bio field add karo HTML mein (agar missing hai)
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
if 'p-bio' not in html:
    old = '<div class="form-group"><label>Contact Email</label><input type="email" id="p-email"'
    new = '<div class="form-group" style="grid-column:1/-1"><label>Bio / About Academy</label><textarea id="p-bio" rows="3" style="width:100%;padding:8px;background:var(--bg3);border:1px solid var(--border);border-radius:8px;color:var(--text);resize:vertical;"></textarea></div>\n            <div class="form-group"><label>Contact Email</label><input type="email" id="p-email"'
    html = html.replace(old, new, 1)
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('p-bio field added')
else:
    print('p-bio already exists')
