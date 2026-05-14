with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# ---- 1. Bio field add karo (tagline ke baad) ----
html = html.replace(
    '<div class="form-group"><label>Tagline</label><input type="text" id="p-tagline"',
    '<div class="form-group"><label>Tagline</label><input type="text" id="p-tagline"'
)
html = html.replace(
    'placeholder="India\'s Premier Exam Prep Platform"/></div>\n          </div>',
    'placeholder="India\'s Premier Exam Prep Platform"/></div>\n            <div class="form-group" style="grid-column:1/-1"><label>\U0001f4dd Bio / About Academy</label><textarea id="p-bio" rows="3" placeholder="Apni academy ke baare mein likhein..." style="width:100%;padding:8px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:8px;color:var(--text);resize:vertical;font-family:inherit;font-size:0.9rem;"></textarea></div>\n          </div>'
)
# ---- 2. Social Categories section add karo (p-msg ke baad) ----
html = html.replace(
    '<div id="p-msg"></div>\n      </div>\n    </div>',
    '''<div id="p-msg"></div>
        <hr style="border:none;border-top:1px solid var(--border);margin:20px 0;"/>
        <h3>\U0001f5c2\ufe0f Custom Social Categories</h3>
        <p style="color:var(--text2);font-size:0.82rem;margin-bottom:12px;">Batches, groups, notes — koi bhi custom link add karo jo users ko dikhega</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
          <input type="text" id="cat-icon" placeholder="\U0001f4da Icon (emoji)" style="width:80px;padding:8px;background:var(--bg3);border:1px solid var(--border);border-radius:8px;color:var(--text);text-align:center;font-size:1.1rem;"/>
          <input type="text" id="cat-name" placeholder="Category Name (e.g. SSC Batch 2025)" style="flex:1;min-width:140px;padding:8px;background:var(--bg3);border:1px solid var(--border);border-radius:8px;color:var(--text);"/>
          <input type="url" id="cat-url" placeholder="https://wa.me/... ya koi bhi link" style="flex:2;min-width:180px;padding:8px;background:var(--bg3);border:1px solid var(--border);border-radius:8px;color:var(--text);"/>
          <button class="btn btn-gold" onclick="addSocialCategory()" style="white-space:nowrap;">\u2795 Add</button>
        </div>
        <div id="cat-list" style="display:flex;flex-direction:column;gap:6px;"></div>
      </div>
    </div>'''
)
# ---- 3. academyProfileCard div hatao (3x display fix) ----
import re
html = re.sub(
    r'\s*<!-- USER PROFILE CARD -->.*?</div>\s*</div>\s*\n\s*<div id="main-content">',
    '\n    <div id="main-content">',
    html, flags=re.DOTALL
)
# ---- 4. JS - sab kuch update karo ----
# updateUserCard hatao
html = re.sub(r'\n// User-facing profile card update\nfunction updateUserCard\(p\)\{.*?\}\n', '\n', html, flags=re.DOTALL)
html = html.replace('    updateUserCard(p);\n', '')
html = html.replace('updateUserCard(_sp);\n', '')
# loadProfile - API se load karo
old_load = """function loadProfile(){
  const p=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
  ['name','tagline','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
    const el=document.getElementById('p-'+k);if(el&&p[k])el.value=p[k];
  });
  const logo=localStorage.getItem('trikul_logo');
  if(logo){const lp=document.getElementById('logoPreview');if(lp)lp.innerHTML='<img src="'+logo+'" style="width:100%;height:100%;object-fit:cover;border-radius:50%"/>';}
  applyProfileToSite(p);
}"""
new_load = """function loadProfile(){
  const token = localStorage.getItem('adminToken')||localStorage.getItem('trikul_token')||'';
  fetch('/api/profile')
    .then(r=>r.json())
    .then(p=>{
      if(!p) return;
      ['name','tagline','bio','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
        const el=document.getElementById('p-'+k);if(el&&p[k])el.value=p[k];
      });
      if(p.logo_url){
        const lp=document.getElementById('logoPreview');
        if(lp)lp.innerHTML='<img src="'+p.logo_url+'" style="width:100%;height:100%;object-fit:cover;border-radius:50%"/>';
        localStorage.setItem('trikul_logo',p.logo_url);
      }
      if(p.social_categories){
        window._socialCategories = p.social_categories;
        renderCategories();
      }
      localStorage.setItem('trikul_profile',JSON.stringify(p));
      applyProfileToSite(p);
      showUserProfileBanner(p);
    })
    .catch(()=>{
      const p=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
      ['name','tagline','bio','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
        const el=document.getElementById('p-'+k);if(el&&p[k])el.value=p[k];
      });
      applyProfileToSite(p);
    });
}"""
html = html.replace(old_load, new_load)
# saveProfile - API me save karo
old_save_start = "function saveProfile(){"
old_save = """function saveProfile(){
  const p={};
  ['name','tagline','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
    const el=document.getElementById('p-'+k);if(el)p[k]=el.value.trim();
  });
  try{
    localStorage.setItem('trikul_profile',JSON.stringify(p));
    applyProfileToSite(p);
    showUserProfileBanner(p);
    const m=document.getElementById('p-msg');
    if(m){m.innerHTML='<div style="color:var(--green);padding:8px;margin-top:8px;">\u2705 Profile saved!</div>';
    setTimeout(()=>{if(m)m.innerHTML='';},3000);}
  }catch(e){
    const m=document.getElementById('p-msg');
    if(m)m.innerHTML='<div style="color:var(--red);padding:8px;">\u274c Error: '+e.message+'</div>';
  }
}"""
new_save = """function saveProfile(){
  const p={};
  ['name','tagline','bio','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
    const el=document.getElementById('p-'+k);if(el)p[k]=el.value.trim();
  });
  p.social_categories = window._socialCategories||[];
  const logo=localStorage.getItem('trikul_logo');
  if(logo) p.logo_url=logo;
  const m=document.getElementById('p-msg');
  const token=localStorage.getItem('adminToken')||localStorage.getItem('trikul_token')||'';
  fetch('/api/profile',{
    method:'POST',
    headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},
    body:JSON.stringify(p)
  })
  .then(r=>r.json())
  .then(res=>{
    if(res.success){
      localStorage.setItem('trikul_profile',JSON.stringify(p));
      applyProfileToSite(p);
      showUserProfileBanner(p);
      if(m){m.innerHTML='<div style="color:var(--green);padding:8px;margin-top:8px;">\u2705 Profile saved to database!</div>';
      setTimeout(()=>{if(m)m.innerHTML='';},3000);}
    } else {
      if(m)m.innerHTML='<div style="color:var(--red);padding:8px;">\u274c Save failed: '+(res.error||'Unknown error')+'</div>';
    }
  })
  .catch(e=>{
    localStorage.setItem('trikul_profile',JSON.stringify(p));
    applyProfileToSite(p);
    showUserProfileBanner(p);
    if(m){m.innerHTML='<div style="color:orange;padding:8px;">\u26a0\ufe0f Offline mode - locally saved</div>';
    setTimeout(()=>{if(m)m.innerHTML='';},3000);}
  });
}"""
html = html.replace(old_save, new_save)
# ---- 5. Categories JS add karo ----
cat_js = """
// ========== SOCIAL CATEGORIES ==========
window._socialCategories = [];
function addSocialCategory(){
  const icon=(document.getElementById('cat-icon').value.trim()||'\U0001f517');
  const name=document.getElementById('cat-name').value.trim();
  const url=document.getElementById('cat-url').value.trim();
  if(!name||!url){alert('Name aur URL dono bharo!');return;}
  window._socialCategories.push({id:Date.now().toString(),icon,name,url});
  document.getElementById('cat-icon').value='';
  document.getElementById('cat-name').value='';
  document.getElementById('cat-url').value='';
  renderCategories();
}
function removeCategory(id){
  window._socialCategories=window._socialCategories.filter(c=>c.id!==id);
  renderCategories();
}
function renderCategories(){
  const el=document.getElementById('cat-list');if(!el)return;
  el.innerHTML=window._socialCategories.map(c=>
    '<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;">'+
    '<span style="font-size:1.2rem;">'+c.icon+'</span>'+
    '<span style="flex:1;font-weight:600;color:var(--text);font-size:0.88rem;">'+c.name+'</span>'+
    '<a href="'+c.url+'" target="_blank" style="color:var(--teal);font-size:0.75rem;max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'+c.url+'</a>'+
    '<button onclick="removeCategory(\''+c.id+'\')" style="background:var(--red);color:#fff;border:none;border-radius:6px;padding:3px 10px;cursor:pointer;font-size:0.8rem;">\u2715</button>'+
    '</div>'
  ).join('');
}
"""
# showUserProfileBanner me bio + categories bhi show karo
old_banner_end = "  b.innerHTML=parts.join(' <span style=\"opacity:0.25\">|</span> ')+'<style>#userProfileBanner a{color:var(--gold);text-decoration:none;font-size:1.1rem;}</style>';\n  b.style.display=p.name?'flex':'none';\n}"
new_banner = """  b.innerHTML=parts.join(' <span style="opacity:0.25">|</span> ')+'<style>#userProfileBanner a{color:var(--gold);text-decoration:none;font-size:1.1rem;}</style>';
  b.style.display=p.name?'flex':'none';
  // Bio + categories user card
  let uc=document.getElementById('userInfoCard');
  if(!uc){
    uc=document.createElement('div');uc.id='userInfoCard';
    uc.style.cssText='background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px 22px;margin:14px auto;max-width:900px;';
    b.insertAdjacentElement('afterend',uc);
  }
  let ucHtml='';
  if(p.bio)ucHtml+='<p style="color:var(--text2);font-size:0.88rem;margin:0 0 12px 0;line-height:1.6;">'+p.bio+'</p>';
  const cats=p.social_categories||window._socialCategories||[];
  if(cats.length){
    ucHtml+='<div style="display:flex;gap:8px;flex-wrap:wrap;">';
    cats.forEach(c=>{
      ucHtml+='<a href="'+c.url+'" target="_blank" style="color:var(--gold);text-decoration:none;padding:5px 14px;border:1px solid var(--border);border-radius:20px;font-size:0.82rem;display:flex;align-items:center;gap:5px;transition:all 0.2s;background:var(--bg3);">'+(c.icon||'\U0001f517')+' '+c.name+'</a>';
    });
    ucHtml+='</div>';
  }
  uc.innerHTML=ucHtml;
  uc.style.display=(p.bio||cats.length)?'block':'none';
}"""
html = html.replace(old_banner_end, new_banner)
# ---- 6. Auto-load profile from API on page load ----
old_auto = """const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
applyProfileToSite(_sp);
showUserProfileBanner(_sp);"""
new_auto = """window._socialCategories=[];
fetch('/api/profile').then(r=>r.json()).then(p=>{
  if(!p||!p.name) return;
  localStorage.setItem('trikul_profile',JSON.stringify(p));
  if(p.logo_url)localStorage.setItem('trikul_logo',p.logo_url);
  if(p.social_categories){window._socialCategories=p.social_categories;renderCategories();}
  applyProfileToSite(p);
  showUserProfileBanner(p);
}).catch(()=>{
  const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
  applyProfileToSite(_sp);showUserProfileBanner(_sp);
});"""
html = html.replace(old_auto, new_auto)
# Cat JS insert karo (before auto-load)
html = html.replace("window._socialCategories=[];", cat_js + "\nwindow._socialCategories=[];")
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML patch done!')
