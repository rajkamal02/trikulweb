import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# FIX 1: Remove duplicate profile panes
analytics_marker = '<!-- ANALYTICS PANE -->'
profile_marker = '<!-- PROFILE PANE -->'
first_pos = html.find(profile_marker)
second_pos = html.find(profile_marker, first_pos + 1)
analytics_pos = html.find(analytics_marker)
if second_pos != -1 and analytics_pos != -1:
    html = html[:second_pos] + html[analytics_pos:]
    print('FIX 1: Removed duplicate profile panes')
else:
    print('FIX 1: No duplicates found')
# FIX 2: Fix broken await injection
broken_await = '        await \n// DATE'
inj_start = html.find(broken_await)
if inj_start != -1:
    inj_end_marker = 'loadAll(); await loadAdminData();\n'
    inj_end = html.find(inj_end_marker, inj_start)
    if inj_end != -1:
        profile_js_raw = html[inj_start + len('        await \n'):inj_end]
        orphan_start = profile_js_raw.find('\n  card.style.display=')
        sp2_start = profile_js_raw.find('\n_sp2=')
        if orphan_start != -1 and sp2_start != -1:
            profile_js_raw = profile_js_raw[:orphan_start] + profile_js_raw[sp2_start:]
        profile_js_raw = profile_js_raw.replace('\n_sp2=JSON.parse', '\nvar _sp2=JSON.parse')
        profile_js_raw = profile_js_raw.replace(
            "  b.style.display=p.name?'flex':'none';\n  b.style.display=p.name?'flex':'none';",
            "  b.style.display=p.name?'flex':'none';"
        )
        html = html[:inj_start] + '        await loadAdminData();\n' + html[inj_end + len(inj_end_marker):]
        final_loadall = html.rfind('\nloadAll();')
        html = html[:final_loadall] + '\n' + profile_js_raw.strip() + '\n' + html[final_loadall:]
        print('FIX 2: Profile JS moved to correct location')
    else:
        print('FIX 2: End marker not found')
else:
    print('FIX 2: Already fixed or not found')
# FIX 3: Remove duplicate loadProfile calls
html = html.replace(
    "  if (tab === 'profile') loadProfile();\n  if (tab === 'profile') loadProfile();\n  if (tab === 'profile') loadProfile();",
    "  if (tab === 'profile') loadProfile();"
)
html = html.replace(
    "  if (tab === 'profile') loadProfile();\n  if (tab === 'profile') loadProfile();",
    "  if (tab === 'profile') loadProfile();"
)
print('FIX 3: switchTab duplicates removed')
# FIX 4: Add missing social category functions
if 'function addSocialCategory' not in html:
    cat_js = """
function addSocialCategory(){
  var iconEl=document.getElementById('cat-icon');
  var icon=iconEl?iconEl.value.trim():'';
  if(!icon)icon='🔗';
  var name=document.getElementById('cat-name').value.trim();
  var url=document.getElementById('cat-url').value.trim();
  if(!name||!url){alert('Name aur URL dono bharo!');return;}
  if(!window._cats)window._cats=[];
  window._cats.push({id:String(Date.now()),icon:icon,name:name,url:url});
  if(iconEl)iconEl.value='';
  document.getElementById('cat-name').value='';
  document.getElementById('cat-url').value='';
  renderCategories();
}
function removeCategory(id){
  if(!window._cats)window._cats=[];
  window._cats=window._cats.filter(function(c){return c.id!==id;});
  renderCategories();
}
function renderCategories(){
  var el=document.getElementById('cat-list');if(!el)return;
  if(!window._cats||!window._cats.length){el.innerHTML='';return;}
  el.innerHTML=window._cats.map(function(c){
    return '<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;">'+
    '<span style="font-size:1.2rem;">'+c.icon+'</span>'+
    '<span style="flex:1;font-weight:600;color:var(--text);font-size:0.88rem;">'+c.name+'</span>'+
    '<a href="'+c.url+'" target="_blank" style="color:var(--teal);font-size:0.75rem;">'+c.url.substring(0,25)+'...</a>'+
    '<button onclick="removeCategory('+JSON.stringify(c.id)+')" style="background:var(--red);color:#fff;border:none;border-radius:6px;padding:3px 10px;cursor:pointer;">x</button>'+
    '</div>';
  }).join('');
}
"""
    html = html.replace('function loadProfile(){', cat_js + 'function loadProfile(){', 1)
    print('FIX 4: addSocialCategory + renderCategories added')
else:
    print('FIX 4: Already exists')
# FIX 5: saveProfileBtn onclick
if 'id="saveProfileBtn"' in html and 'onclick="saveProfile()"' not in html:
    html = html.replace(
        'id="saveProfileBtn" style="margin-top:10px;">',
        'id="saveProfileBtn" onclick="saveProfile()" style="margin-top:10px;">',
        1
    )
    print('FIX 5: saveProfileBtn onclick added')
else:
    print('FIX 5: Already has onclick or button not found')
with open('index_fixed.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\nDONE! index_fixed.html saved in', __import__("os").getcwd())
