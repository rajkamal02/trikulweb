// Auto-ping - server ko jaagne rakho
const RENDER_URL = process.env.RENDER_URL || '';
if (RENDER_URL) {
  setInterval(() => {
    fetch(RENDER_URL + '/api/health')
      .then(() => console.log('Ping sent - server awake'))
      .catch(() => {});
  }, 840000); // har 14 minute mein ping
}require('dotenv').config({ override: true });
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { createClient } = require('@supabase/supabase-js');
const WebSocket = require('ws');
const path = require('path');
const fs = require('fs-extra');
const multer = require('multer');
const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(express.static(path.join(__dirname, 'public')));

// Ensure upload directories exist
const UPLOAD_DIR = path.join(__dirname, 'public', 'uploads');
const PDF_DIR = path.join(UPLOAD_DIR, 'pdfs');
const THUMB_DIR = path.join(UPLOAD_DIR, 'thumbs');
fs.ensureDirSync(PDF_DIR);
fs.ensureDirSync(THUMB_DIR);

// Multer setup for robust disk uploads (support large files)
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    if (file.fieldname === 'pdf') cb(null, PDF_DIR);
    else if (file.fieldname === 'thumbnail') cb(null, THUMB_DIR);
    else cb(null, UPLOAD_DIR);
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname) || '';
    cb(null, genId() + ext);
  }
});
const upload = multer({ storage, limits: { fileSize: 1024 * 1024 * 1024 } }); // up to 1GB

function generateSvgThumbnail(text, outPath) {
  const safe = String(text || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const svg = `<?xml version="1.0" encoding="UTF-8"?>
  <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675">
    <defs>
      <linearGradient id="g" x1="0" x2="1">
        <stop offset="0%" stop-color="#0f172a" />
        <stop offset="100%" stop-color="#0f766e" />
      </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="url(#g)" />
    <rect x="40" y="40" width="1120" height="595" rx="18" fill="#0b1220" opacity="0.12" />
    <text x="80" y="220" font-family="'Playfair Display', serif" font-size="56" fill="#ffffff" font-weight="700">${safe}</text>
    <text x="80" y="300" font-family="'DM Sans',sans-serif" font-size="28" fill="#cfece2">Trikul Academy</text>
  </svg>`;
  fs.writeFileSync(outPath, svg, 'utf8');
}
// Enhanced thumbnail generator with options
function generateSvgThumbnailWithOptions(text, outPath, opts = {}) {
  const safe = String(text || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const bgStart = opts.bgStart || '#0f172a';
  const bgEnd = opts.bgEnd || '#0f766e';
  const titleSize = opts.titleSize || 56;
  const subtitleSize = opts.subtitleSize || 28;
  const svg = `<?xml version="1.0" encoding="UTF-8"?>
  <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675">
    <defs>
      <linearGradient id="g" x1="0" x2="1">
        <stop offset="0%" stop-color="${bgStart}" />
        <stop offset="100%" stop-color="${bgEnd}" />
      </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="url(#g)" />
    <rect x="40" y="40" width="1120" height="595" rx="18" fill="#0b1220" opacity="0.12" />
    <text x="80" y="220" font-family="'Playfair Display', serif" font-size="${titleSize}" fill="#ffffff" font-weight="700">${safe}</text>
    <text x="80" y="300" font-family="'DM Sans',sans-serif" font-size="${subtitleSize}" fill="#cfece2">Trikul Academy</text>
  </svg>`;
  fs.writeFileSync(outPath, svg, 'utf8');
}
const nodeFetch = require('node-fetch');
const supabaseOptions = { realtime: { transport: WebSocket }, global: { fetch: nodeFetch } };
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY, supabaseOptions);
const supabaseAdmin = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY, supabaseOptions);
const JWT_SECRET = process.env.JWT_SECRET || 'trikul_secret_2025';
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@trikul.com';
const ADMIN_PASS = process.env.ADMIN_PASS || 'trikul01234';

// Initialize database tables if they don't exist
async function initializeDatabase() {
  try {
    console.log('Checking database tables...');
    // Test connection and create tables via Supabase SQL
    const { error } = await supabaseAdmin.rpc('create_tables_if_not_exist').catch(() => ({ error: null }));
    
    // Fallback: test if tables exist by querying them
    const tables = ['pdfs', 'videos', 'affairs', 'tasks', 'analytics', 'streaks'];
    for (const table of tables) {
      const { error } = await supabase.from(table).select('count()').limit(1);
      if (error && error.code === '42P01') {
        console.warn(`⚠️ Table "${table}" does not exist. Please create tables in Supabase dashboard or use migrations.`);
      }
    }
    console.log('✅ Database check complete');
  } catch (err) {
    console.warn('⚠️ Database initialization skipped:', err.message);
  }
}

function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}
function genId() {
  return Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
}
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  if (email === ADMIN_EMAIL && password === ADMIN_PASS) {
    const token = jwt.sign({ email }, JWT_SECRET, { expiresIn: '7d' });
    return res.json({ token, email });
  }
  res.status(401).json({ error: 'Invalid credentials' });
});
app.get('/api/auth/verify', authMiddleware, (req, res) => {
  res.json({ valid: true, user: req.user });
});
app.get('/api/health', (req, res) => res.json({ status: 'ok', time: new Date() }));
app.get('/api/pdfs', async (req, res) => {
  const { data, error } = await supabase.from('pdfs').select('*').order('created_at', { ascending: false });
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});
app.post('/api/pdfs', authMiddleware, async (req, res) => {
  const { title, category, url } = req.body;
  const { data, error } = await supabaseAdmin.from('pdfs').insert({ id: genId(), title, category, url, views: 0, created_at: new Date() }).select().single();
  if (error) return res.status(500).json({ error: error.message });
  await supabaseAdmin.from('analytics').insert({ content_type: 'pdf', content_id: data.id, action: 'created', created_at: new Date() });
  res.json(data);
});

// Upload PDF file (multipart). Fields: pdf (file), thumbnail (optional image), title, category
app.post('/api/pdfs/upload', authMiddleware, upload.fields([{ name: 'pdf', maxCount: 1 }, { name: 'thumbnail', maxCount: 1 }]), async (req, res) => {
  try {
    const title = req.body.title || 'Untitled PDF';
    const category = req.body.category || '';
    const pdfFile = req.files['pdf'] && req.files['pdf'][0];
    if (!pdfFile) return res.status(400).json({ error: 'No PDF file uploaded' });
    const pdfUrl = '/uploads/pdfs/' + path.basename(pdfFile.path);

    // Handle thumbnail
    let thumbUrl = null;
    const thumbFile = req.files['thumbnail'] && req.files['thumbnail'][0];
    if (thumbFile) {
      thumbUrl = '/uploads/thumbs/' + path.basename(thumbFile.path);
    } else {
      // auto-generate SVG thumbnail
      const thumbName = genId() + '.svg';
      const outPath = path.join(THUMB_DIR, thumbName);
      generateSvgThumbnailWithOptions(title, outPath, { bgStart: req.body.thumb_bg, bgEnd: req.body.thumb_bg_end, titleSize: parseInt(req.body.thumb_fs) || undefined });
      thumbUrl = '/uploads/thumbs/' + thumbName;
    }

    const record = { id: genId(), title, category, url: pdfUrl, thumbnail_url: thumbUrl, views: 0, created_at: new Date() };
    const { data, error } = await supabaseAdmin.from('pdfs').insert(record).select().single();
    if (error) return res.status(500).json({ error: error.message });
    await supabaseAdmin.from('analytics').insert({ content_type: 'pdf', content_id: data.id, action: 'created', created_at: new Date() });
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
app.patch('/api/pdfs/:id/view', async (req, res) => {
  const { id } = req.params;
  const { data: pdf } = await supabase.from('pdfs').select('views').eq('id', id).single();
  const { data, error } = await supabaseAdmin.from('pdfs').update({ views: (pdf?.views || 0) + 1 }).eq('id', id).select().single();
  if (error) return res.status(500).json({ error: error.message });
  await supabaseAdmin.from('analytics').insert({ content_type: 'pdf', content_id: id, action: 'view', created_at: new Date() });
  res.json(data);
});
app.delete('/api/pdfs/:id', authMiddleware, async (req, res) => {
  const { error } = await supabaseAdmin.from('pdfs').delete().eq('id', req.params.id);
  if (error) return res.status(500).json({ error: error.message });
  res.json({ success: true });
});
app.get('/api/videos', async (req, res) => {
  const { data, error } = await supabase.from('videos').select('*').order('created_at', { ascending: false });
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});
app.post('/api/videos', authMiddleware, async (req, res) => {
  const { title, url } = req.body;
  const { data, error } = await supabaseAdmin.from('videos').insert({ id: genId(), title, url, clicks: 0, created_at: new Date() }).select().single();
  if (error) return res.status(500).json({ error: error.message });
  await supabaseAdmin.from('analytics').insert({ content_type: 'video', content_id: data.id, action: 'created', created_at: new Date() });
  res.json(data);
});

// Upload video metadata with optional thumbnail
app.post('/api/videos/upload', authMiddleware, upload.single('thumbnail'), async (req, res) => {
  try {
    const { title, url } = req.body;
    let thumbUrl = null;
    if (req.file) thumbUrl = '/uploads/thumbs/' + path.basename(req.file.path);
    else {
      // generate SVG thumbnail from title
      const thumbName = genId() + '.svg';
      const outPath = path.join(THUMB_DIR, thumbName);
      generateSvgThumbnailWithOptions(title || 'Video', outPath, { bgStart: req.body.thumb_bg, bgEnd: req.body.thumb_bg_end, titleSize: parseInt(req.body.thumb_fs) || undefined });
      thumbUrl = '/uploads/thumbs/' + thumbName;
    }
    const record = { id: genId(), title, url, thumbnail_url: thumbUrl, clicks: 0, created_at: new Date() };
    const { data, error } = await supabaseAdmin.from('videos').insert(record).select().single();
    if (error) return res.status(500).json({ error: error.message });
    await supabaseAdmin.from('analytics').insert({ content_type: 'video', content_id: data.id, action: 'created', created_at: new Date() });
    res.json(data);
  } catch (err) { res.status(500).json({ error: err.message }); }
});
app.patch('/api/videos/:id/click', async (req, res) => {
  const { id } = req.params;
  const { data: vid } = await supabase.from('videos').select('clicks').eq('id', id).single();
  const { data, error } = await supabaseAdmin.from('videos').update({ clicks: (vid?.clicks || 0) + 1 }).eq('id', id).select().single();
  if (error) return res.status(500).json({ error: error.message });
  await supabaseAdmin.from('analytics').insert({ content_type: 'video', content_id: id, action: 'click', created_at: new Date() });
  res.json(data);
});
app.delete('/api/videos/:id', authMiddleware, async (req, res) => {
  const { error } = await supabaseAdmin.from('videos').delete().eq('id', req.params.id);
  if (error) return res.status(500).json({ error: error.message });
  res.json({ success: true });
});
app.get('/api/affairs', async (req, res) => {
  const { data, error } = await supabase.from('affairs').select('*').order('created_at', { ascending: false });
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});
app.post('/api/affairs', authMiddleware, async (req, res) => {
  const { title, content, date, mcqs } = req.body;
  const { data, error } = await supabaseAdmin.from('affairs').insert({ id: genId(), title, content, date, mcqs: mcqs || [], created_at: new Date() }).select().single();
  if (error) return res.status(500).json({ error: error.message });
  await supabaseAdmin.from('analytics').insert({ content_type: 'affair', content_id: data.id, action: 'created', created_at: new Date() });
  res.json(data);
});
app.delete('/api/affairs/:id', authMiddleware, async (req, res) => {
  const { error } = await supabaseAdmin.from('affairs').delete().eq('id', req.params.id);
  if (error) return res.status(500).json({ error: error.message });
  res.json({ success: true });
});
app.get('/api/tasks', async (req, res) => {
  const { data, error } = await supabase.from('tasks').select('*').order('created_at', { ascending: false }).limit(1);
  if (error) return res.status(500).json({ error: error.message });
  res.json(data[0] || null);
});
app.post('/api/tasks', authMiddleware, async (req, res) => {
  const { question, options, correct_index } = req.body;
  const { data, error } = await supabaseAdmin.from('tasks').insert({ id: genId(), question, options, correct_index, created_at: new Date() }).select().single();
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});
app.post('/api/streak/complete', async (req, res) => {
  const { fingerprint } = req.body;
  const date = new Date().toISOString().split('T')[0];
  const { data, error } = await supabaseAdmin.from('streaks').upsert({ fingerprint, date, completed_at: new Date() }, { onConflict: 'fingerprint,date' }).select().single();
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});
app.get('/api/analytics', authMiddleware, async (req, res) => {
  const { data, error } = await supabaseAdmin.from('analytics').select('*').order('created_at', { ascending: false }).limit(100);
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});
app.post('/api/mcq/generate', authMiddleware, async (req, res) => {
  const { topic } = req.body;
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey || apiKey === 'your_key_here') return res.status(400).json({ error: 'Anthropic API key not configured' });
  try {
    const fetch = require('node-fetch');
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: 'claude-haiku-4-5-20251001', max_tokens: 500, messages: [{ role: 'user', content: `Generate 1 MCQ for competitive exam about: ${topic}. Return ONLY valid JSON: {"question":"...","options":["A","B","C","D"],"correct_index":0,"explanation":"..."}` }] })
    });
    const resultText = await response.text();
    let parsed = null;
    try {
      // Attempt to parse JSON out of the response
      const jsonAttempt = JSON.parse(resultText);
      parsed = jsonAttempt;
    } catch (e) {
      // Try to extract JSON blob inside string
      const inner = resultText.replace(/```json|```/g, '').trim();
      try { parsed = JSON.parse(inner); } catch (e2) {
        console.error('MCQ generation: could not parse response', resultText);
        return res.status(500).json({ error: 'MCQ generation parse error', raw: resultText });
      }
    }
    res.json(parsed);
  } catch (err) {
    res.status(500).json({ error: 'MCQ generation failed: ' + err.message });
  }
});

// Global error logging
process.on('uncaughtException', (err) => {
  console.error('Uncaught exception:', err && err.stack ? err.stack : err);
});
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection:', reason);
});

// Log key env presence for diagnostics
console.log('SUPABASE_URL present?', !!process.env.SUPABASE_URL);
console.log('SUPABASE_KEY present?', !!process.env.SUPABASE_KEY);
console.log('SUPABASE_SERVICE_KEY present?', !!process.env.SUPABASE_SERVICE_KEY);

// Initialize database
initializeDatabase().catch(err => console.error('Init error:', err));


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

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Trikul Academy running at http://localhost:${PORT}`));







