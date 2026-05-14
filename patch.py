import re
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
css = """
/* ENHANCED THEME v2 */
[data-theme="dark"]{
  --bg:#070b14;--bg2:#0d1420;--bg3:#111827;--card:#141e30;
  --border:#1e3a5f;--text:#e2e8f0;--text2:#7c8fa6;
  --gold:#f0a500;--gold2:#ffc63d;--teal:#0ea5e9;--blue:#6366f1;
  --green:#22c55e;--red:#ef4444;--shadow:0 4px 32px rgba(0,0,0,0.6);
  --nav-bg:rgba(7,11,20,0.97);
  --hero-gradient:linear-gradient(135deg,#070b14 0%,#0d1f3c 60%,#071a07 100%);
}
[data-theme="light"]{
  --bg:#f8faff;--bg2:#eef2ff;--bg3:#ffffff;--card:#ffffff;
  --border:#c7d2fe;--text:#1e1b4b;--text2:#6b7280;
  --gold:#b45309;--gold2:#d97706;--teal:#0891b2;--blue:#4f46e5;
  --green:#15803d;--red:#dc2626;--shadow:0 4px 24px rgba(79,70,229,0.12);
  --nav-bg:rgba(248,250,255,0.97);
  --hero-gradient:linear-gradient(135deg,#eef2ff 0%,#fdf4ff 50%,#ecfdf5 100%);
}
body{background:var(--bg);transition:background 0.3s,color 0.3s;}
#navbar{background:var(--nav-bg)!important;backdrop-filter:blur(12px);}
#hero{background:var(--hero-gradient)!important;}
.stat-card,.pdf-card,.video-card,.affair-item,.admin-section{
  background:var(--card)!important;border:1px solid var(--border)!important;
  transition:transform 0.2s,box-shadow 0.2s;
}
.stat-card:hover,.pdf-card:hover,.video-card:hover{
  transform:translateY(-4px);box-shadow:var(--shadow)!important;
}
#navDate{
  font-size:0.72rem;color:var(--text2);padding:4px 12px;
  background:var(--bg3);border-radius:20px;border:1px solid var(--border);
  white-space:nowrap;font-weight:500;letter-spacing:0.3px;
}
"""
html = html.replace('</style>\n</head>', css + '</style>\n</head>', 1)
html = html.replace('<button id="themeBtn"', '<span id="navDate"></span>\n    <button id="themeBtn"', 1)
html = html.replace(
    "onclick=\"switchTab('analytics')\">📊 Analytics</button>",
    "onclick=\"switchTab('analytics')\">📊 Analytics</button>\n      <button class=\"admin-tab\" onclick=\"switchTab('profile')\">👤 Profile</button>",
    1
)
html = html.replace(
    "const tabs = ['pdfs','videos','affairs','tasks','analytics'];",
    "const tabs = ['pdfs','videos','affairs','tasks','analytics','profile'];", 1
)
html = html.replace(
    "if (tab === 'analytics') loadAnalytics();",
    "if (tab === 'analytics') loadAnalytics();\n  if (tab === 'profile') loadProfile();", 1
)
profile_html = """
    <!-- PROFILE PANE -->
    <div id="pane-profile" class="admin-pane">
      <div class="admin-section">
        <h3>🏫 Academy Profile</h3>
        <div style="display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start;margin-bottom:20px;">
          <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
            <div id="logoPreview" style="width:110px;height:110px;border-radius:50%;background:var(--bg3);border:3px solid var(--gold);display:flex;align-items:center;justify-content:center;font-size:2.8rem;overflow:hidden;">⚔</div>
            <label class="btn btn-outline" style="cursor:pointer;font-size:0.8rem;padding:6px 14px;">
              📷 Upload Logo
              <input type="file" accept="image/*" id="logoUpload" style="display:none;" onchange="previewLogo(this)"/>
            </label>
          </div>
          <div style="flex:1;min-width:220px;display:grid;gap:12px;">
            <div class="form-group"><label>Academy Name</label><input type="text" id="p-name" placeholder="Trikul Academy"/></div>
            <div class="form-group"><label>Tagline</label><input type="text" id="p-tagline" placeholder="India's Premier Exam Prep Platform"/></div>
            <div class="form-group"><label>Contact Email</label><input type="email" id="p-email" placeholder="contact@trikul.com"/></div>
          </div>
        </div>
        <h3>📣 Social Media Links</h3>
        <div class="form-row">
          <div class="form-group"><label>📺 YouTube</label><input type="url" id="p-youtube" placeholder="https://youtube.com/@channel"/></div>
          <div class="form-group"><label>📘 Facebook</label><input type="url" id="p-facebook" placeholder="https://facebook.com/yourpage"/></div>
          <div class="form-group"><label>📸 Instagram</label><input type="url" id="p-instagram" placeholder="https://instagram.com/account"/></div>
          <div class="form-group"><label>💬 WhatsApp</label><input type="url" id="p-whatsapp" placeholder="https://wa.me/91XXXXXXXXXX"/></div>
          <div class="form-group"><label>📞 Phone</label><input type="tel" id="p-phone" placeholder="+91XXXXXXXXXX"/></div>
        </div>
        <button class="btn btn-gold" onclick="saveProfile()" style="margin-top:10px;">💾 Save Profile</button>
        <div id="p-msg"></div>
      </div>
    </div>
"""
html = html.replace('    <!-- ANALYTICS PANE -->', profile_html + '\n    <!-- ANALYTICS PANE -->', 1)
js = """
// DATE
function updateNavDate(){
  const el=document.getElementById('navDate');if(!el)return;
  const n=new Date(),dy=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
  mo=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  el.textContent=dy[n.getDay()]+', '+n.getDate()+' '+mo[n.getMonth()]+' '+n.getFullYear()+' | '+n.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'});
}
setInterval(updateNavDate,1000);updateNavDate();
// PROFILE
function loadProfile(){
  const p=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
  ['name','tagline','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
    const el=document.getElementById('p-'+k);if(el&&p[k])el.value=p[k];
  });
  const logo=localStorage.getItem('trikul_logo');
  if(logo){const lp=document.getElementById('logoPreview');if(lp)lp.innerHTML='<img src="'+logo+'" style="width:100%;height:100%;object-fit:cover;border-radius:50%"/>';}
  applyProfileToSite(p);
}
function saveProfile(){
  const p={};
  ['name','tagline','email','youtube','phone','instagram','whatsapp','facebook'].forEach(k=>{
    const el=document.getElementById('p-'+k);if(el)p[k]=el.value.trim();
  });
  try{
    localStorage.setItem('trikul_profile',JSON.stringify(p));
    applyProfileToSite(p);
    showUserProfileBanner(p);
    const m=document.getElementById('p-msg');
    if(m){m.innerHTML='<div style="color:var(--green);padding:8px;margin-top:8px;">✅ Profile saved!</div>';
    setTimeout(()=>{if(m)m.innerHTML='';},3000);}
  }catch(e){
    const m=document.getElementById('p-msg');
    if(m)m.innerHTML='<div style="color:var(--red);padding:8px;">❌ Error: '+e.message+'</div>';
  }
}
function previewLogo(input){
  if(!input.files[0])return;
  const r=new FileReader();
  r.onload=e=>{
    localStorage.setItem('trikul_logo',e.target.result);
    const lp=document.getElementById('logoPreview');
    if(lp)lp.innerHTML='<img src="'+e.target.result+'" style="width:100%;height:100%;object-fit:cover;border-radius:50%"/>';
  };r.readAsDataURL(input.files[0]);
}
function applyProfileToSite(p){
  if(p.name){const l=document.querySelector('.nav-logo');if(l)l.textContent='⚔ '+p.name.toUpperCase();}
  const footer=document.querySelector('footer');if(!footer)return;
  const links=[
    p.youtube&&'<a href="'+p.youtube+'" target="_blank">📺 YouTube</a>',
    p.facebook&&'<a href="'+p.facebook+'" target="_blank">📘 Facebook</a>',
    p.instagram&&'<a href="'+p.instagram+'" target="_blank">📸 Instagram</a>',
    p.whatsapp&&'<a href="'+p.whatsapp+'" target="_blank">💬 WhatsApp</a>',
    p.phone&&'<a href="tel:'+p.phone+'">📞 Call Us</a>',
    p.email&&'<a href="mailto:'+p.email+'">✉ '+p.email+'</a>',
  ].filter(Boolean).join(' • ');
  if(links){
    let sd=document.getElementById('footerSocials');
    if(!sd){sd=document.createElement('div');sd.id='footerSocials';
    sd.style.cssText='margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;font-size:0.85rem;';
    footer.appendChild(sd);}
    sd.innerHTML='<style>#footerSocials a{color:var(--gold);text-decoration:none;padding:4px 10px;border:1px solid var(--border);border-radius:14px;transition:all 0.2s;}#footerSocials a:hover{background:var(--gold);color:#000;}</style>'+links;
  }
}
function showUserProfileBanner(p){
  let b=document.getElementById('userProfileBanner');
  if(!b){
    b=document.createElement('div');b.id='userProfileBanner';
    b.style.cssText='background:var(--card);border-bottom:2px solid var(--border);padding:7px 20px;display:flex;align-items:center;gap:12px;font-size:0.83rem;color:var(--text2);flex-wrap:wrap;position:sticky;top:60px;z-index:99;';
    const nav=document.getElementById('navbar');
    if(nav)nav.insertAdjacentElement('afterend',b);else document.body.prepend(b);
  }
  const logo=localStorage.getItem('trikul_logo');
  const parts=[];
  if(logo)parts.push('<img src="'+logo+'" style="width:28px;height:28px;border-radius:50%;object-fit:cover;border:2px solid var(--gold)"/>');
  if(p.name)parts.push('<strong style="color:var(--text)">'+p.name+'</strong>');
  if(p.tagline)parts.push('<span>'+p.tagline+'</span>');
  const links=[];
  if(p.youtube)links.push('<a href="'+p.youtube+'" target="_blank">📺</a>');
  if(p.instagram)links.push('<a href="'+p.instagram+'" target="_blank">📸</a>');
  if(p.whatsapp)links.push('<a href="'+p.whatsapp+'" target="_blank">💬</a>');
  if(p.facebook)links.push('<a href="'+p.facebook+'" target="_blank">📘</a>');
  if(p.phone)links.push('<a href="tel:'+p.phone+'">📞</a>');
  if(links.length)parts.push('<span style="margin-left:auto;display:flex;gap:10px;">'+links.join('')+'</span>');
  b.innerHTML=parts.join(' <span style="opacity:0.25">|</span> ')+'<style>#userProfileBanner a{color:var(--gold);text-decoration:none;font-size:1.1rem;}</style>';
  b.style.display=p.name?'flex':'none';
}
// Auto-apply saved profile
const _sp=JSON.parse(localStorage.getItem('trikul_profile')||'{}');
applyProfileToSite(_sp);showUserProfileBanner(_sp);
"""
html = html.replace('loadAll();', js + '\nloadAll();', 1)
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Patch v1 (fresh) done!')
