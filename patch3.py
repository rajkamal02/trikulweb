with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# 1. Save button ko robust banao - inline onclick ki jagah id do
html = html.replace(
    '<button class="btn btn-gold" onclick="saveProfile()" style="margin-top:10px;">💾 Save Profile</button>',
    '<button class="btn btn-gold" id="saveProfileBtn" style="margin-top:10px;">💾 Save Profile</button>'
)
# 2. User-facing profile card HTML - hero section ke baad add karo
user_card = """
    <!-- USER PROFILE CARD -->
    <div id="academyProfileCard" style="display:none;background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px 24px;margin:18px auto;max-width:900px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;box-shadow:var(--shadow);">
      <div id="upc-logo" style="width:64px;height:64px;border-radius:50%;background:var(--bg3);border:3px solid var(--gold);display:flex;align-items:center;justify-content:center;font-size:1.8rem;overflow:hidden;flex-shrink:0;">⚔</div>
      <div style="flex:1;min-width:180px;">
        <div id="upc-name" style="font-size:1.15rem;font-weight:700;color:var(--text);"></div>
        <div id="upc-tagline" style="font-size:0.83rem;color:var(--text2);margin-top:2px;"></div>
        <div id="upc-links" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;"></div>
      </div>
    </div>
"""
html = html.replace('<div id="main-content">', user_card + '\n    <div id="main-content">', 1)
# 3. JS - saveProfile fix + updateUserCard
old_js_end = "const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');\napplyProfileToSite(_sp);showUserProfileBanner(_sp);"
new_js_end = """
// Save button - addEventListener (onclick se zyada reliable)
document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('saveProfileBtn');
  if(btn) btn.addEventListener('click', saveProfile);
});
// User-facing profile card update
function updateUserCard(p){
  const card = document.getElementById('academyProfileCard');
  if(!card) return;
  if(!p.name){ card.style.display='none'; return; }
  card.style.display='flex';
  // Logo
  const logo = localStorage.getItem('trikul_logo');
  const logoEl = document.getElementById('upc-logo');
  if(logoEl && logo) logoEl.innerHTML='<img src="'+logo+'" style="width:100%;height:100%;object-fit:cover;border-radius:50%"/>';
  // Name & Tagline
  const nameEl = document.getElementById('upc-name');
  const tagEl  = document.getElementById('upc-tagline');
  if(nameEl) nameEl.textContent = p.name;
  if(tagEl)  tagEl.textContent  = p.tagline || '';
  // Social links
  const linksEl = document.getElementById('upc-links');
  if(linksEl){
    const items = [];
    const style = 'style="color:var(--gold);text-decoration:none;padding:3px 10px;border:1px solid var(--border);border-radius:12px;font-size:0.8rem;transition:all 0.2s;"';
    if(p.youtube)   items.push('<a href="'+p.youtube+'"   target="_blank" '+style+'>📺 YouTube</a>');
    if(p.instagram) items.push('<a href="'+p.instagram+'" target="_blank" '+style+'>📸 Instagram</a>');
    if(p.whatsapp)  items.push('<a href="'+p.whatsapp+'"  target="_blank" '+style+'>💬 WhatsApp</a>');
    if(p.facebook)  items.push('<a href="'+p.facebook+'"  target="_blank" '+style+'>📘 Facebook</a>');
    if(p.phone)     items.push('<a href="tel:'+p.phone+'" '+style+'>📞 '+p.phone+'</a>');
    if(p.email)     items.push('<a href="mailto:'+p.email+'" '+style+'>✉ '+p.email+'</a>');
    linksEl.innerHTML = items.join('');
  }
}
const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
applyProfileToSite(_sp);
showUserProfileBanner(_sp);
updateUserCard(_sp);
"""
html = html.replace(old_js_end, new_js_end)
# 4. saveProfile me bhi updateUserCard call karo
html = html.replace(
    'showUserProfileBanner(p);\n    const m=document.getElementById',
    'showUserProfileBanner(p);\n    updateUserCard(p);\n    const m=document.getElementById'
)
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Patch v3 done - Save fixed + User card added!')
