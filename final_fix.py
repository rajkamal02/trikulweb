import re
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
sc = html.rfind('<script>')
se = html.rfind('</script>')
B = html[:sc+8]
js = html[sc+8:se]
A = html[se:]
# 1. Extra catch blocks remove karo
js = re.sub(r'\}catch\(e\)\{console\.error\(e\);\}', '}', js)
print('1. Extra catch removed')
# 2. addSocialCategory + removeCategory add karo
if 'function addSocialCategory' not in js:
    cat_funcs = '''
function addSocialCategory(){
  var iconEl=document.getElementById("cat-icon");
  var icon=iconEl?iconEl.value.trim():"";
  if(!icon) icon="Link";
  var name=document.getElementById("cat-name").value.trim();
  var url=document.getElementById("cat-url").value.trim();
  if(!name||!url){alert("Name aur URL bharo!");return;}
  if(!window._cats)window._cats=[];
  window._cats.push({id:String(Date.now()),icon:icon,name:name,url:url});
  if(iconEl)iconEl.value="";
  document.getElementById("cat-name").value="";
  document.getElementById("cat-url").value="";
  renderCategories();
}
function removeCategory(id){
  if(!window._cats)window._cats=[];
  window._cats=window._cats.filter(function(c){return c.id!==id;});
  renderCategories();
}
'''
    js=js.replace('function renderCategories()', cat_funcs+'function renderCategories()')
    print('2. addSocialCategory added')
else:
    print('2. addSocialCategory already exists')
# 3. _cats initialize karo
if 'window._cats=[]' not in js and 'window._cats = []' not in js:
    js='window._cats=[];\n'+js
    print('3. _cats initialized')
# 4. _socialCategories ko _cats se replace karo
js=js.replace('window._socialCategories','window._cats')
js=js.replace('_socialCategories','_cats')
# 5. Profile auto-load add karo end mein
if 'auto-apply' not in js and 'const _sp' not in js:
    auto='''
// auto-apply
(function(){
  try{
    var sp=JSON.parse(localStorage.getItem("trikul_profile")||"{}");
    if(sp&&sp.name){applyProfileToSite(sp);showUserProfileBanner(sp);}
  }catch(e){}
})();
'''
    js=js+auto
    print('4. Auto-load added')
# 6. Duplicate profile banner remove (sirf 1 rakhna)
# academyProfileCard HTML remove (agar bacha ho)
html_fixed = B+js+A
html_fixed=re.sub(r'<!--\s*USER PROFILE CARD\s*-->.*?</div>\s*</div>','',html_fixed,flags=re.DOTALL)
# userInfoCard JS remove (3x fix)
js_part=html_fixed[html_fixed.rfind('<script>')+8:html_fixed.rfind('</script>')]
js_part=re.sub(r'let uc=document\.getElementById\(.[uU]serInfoCard.\).*?uc\.style\.display[^;]+;','',js_part,flags=re.DOTALL)
sc2=html_fixed.rfind('<script>')
se2=html_fixed.rfind('</script>')
html_fixed=html_fixed[:sc2+8]+js_part+html_fixed[se2:]
print('5. Duplicate profile displays removed')
with open('public/index.html','w',encoding='utf-8') as f:
    f.write(html_fixed)
print('JS done!')
# 7. p-bio field add karo
with open('public/index.html','r',encoding='utf-8') as f:
    html2=f.read()
if 'p-bio' not in html2:
    old_field='<div class="form-group"><label>Contact Email</label><input type="email" id="p-email"'
    new_field='<div class="form-group" style="grid-column:1/-1"><label>Bio</label><textarea id="p-bio" rows="3" style="width:100%;padding:8px;background:var(--bg3);border:1px solid var(--border);border-radius:8px;color:var(--text);resize:vertical;font-size:0.9rem;"></textarea></div>\n<div class="form-group"><label>Contact Email</label><input type="email" id="p-email"'
    html2=html2.replace(old_field,new_field,1)
    with open('public/index.html','w',encoding='utf-8') as f:
        f.write(html2)
    print('6. p-bio added')
else:
    print('6. p-bio exists')
# 8. saveProfile mein bio + _cats include karo
with open('public/index.html','r',encoding='utf-8') as f:
    html3=f.read()
old_keys='"name","tagline","email","youtube","phone","instagram","whatsapp","facebook"'
new_keys='"name","tagline","bio","email","youtube","phone","instagram","whatsapp","facebook"'
html3=html3.replace(old_keys,new_keys)
old_keys2="'name','tagline','email','youtube','phone','instagram','whatsapp','facebook'"
new_keys2="'name','tagline','bio','email','youtube','phone','instagram','whatsapp','facebook'"
html3=html3.replace(old_keys2,new_keys2)
with open('public/index.html','w',encoding='utf-8') as f:
    f.write(html3)
print('7. bio key added to save/load')
print('ALL DONE!')
