with open('server.js', 'r', encoding='utf-8') as f:
    s = f.read()
routes = """
// ========== ACADEMY PROFILE API ==========
app.get('/api/profile', async (req, res) => {
  try {
    const { data, error } = await supabase.from('academy_profile').select('*').eq('id','main').single();
    if (error) return res.json({});
    res.json(data || {});
  } catch(e) { res.json({}); }
});
app.post('/api/profile', authMiddleware, async (req, res) => {
  try {
    const { name,tagline,bio,email,phone,youtube,instagram,whatsapp,facebook,logo_url,social_categories } = req.body;
    const d = { id:'main', name, tagline, bio, email, phone, youtube, instagram, whatsapp, facebook,
      logo_url: logo_url||null,
      social_categories: social_categories||[],
      updated_at: new Date().toISOString() };
    const { data, error } = await supabaseAdmin.from('academy_profile').upsert(d).select().single();
    if (error) throw error;
    res.json({ success: true, data });
  } catch(e) { res.status(500).json({ error: e.message }); }
});
"""
s = s.replace(
    "app.get('*', (req, res) => {",
    routes + "\napp.get('*', (req, res) => {", 1
)
with open('server.js', 'w', encoding='utf-8') as f:
    f.write(s)
print('Server profile routes added!')
