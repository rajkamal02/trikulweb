# Trikul Academy - Database Setup Guide

## 🚀 Quick Start

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a free project
2. Copy your `Project URL` and `API Key` (anon key)
3. Go to Settings → API → Service Role Key and copy that too

### 2. Set Environment Variables
Create a `.env` file in the project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here
JWT_SECRET=your-secret-key-here
ADMIN_EMAIL=admin@trikul.com
ADMIN_PASS=trikul01234
```

### 3. Create Database Tables
1. Go to your Supabase project dashboard
2. Click **SQL Editor** (left sidebar)
3. Click **New Query**
4. Copy all SQL from `setup.sql` file in the project root
5. Paste it into the SQL editor
6. Click **Run** to execute

### 4. Start Server
```bash
npm install
npm start
```

## ✅ Verify Setup

Visit http://localhost:3000 in your browser. If tables are set up correctly:
- PDFs section should load (empty initially)
- Videos section should load (empty initially)
- Current Affairs section should load (empty initially)
- Daily Task section should load (empty initially)

## 🔒 Admin Login

Click the small dot in bottom-left corner 3 times to open admin panel:
- **Email:** `admin@trikul.com`
- **Password:** `trikul01234`

Then you can add PDFs, videos, and current affairs.

## 🐛 Troubleshooting

### "Failed to load resource: 500 Internal Server Error"
**Solution:** Tables aren't created. Run the SQL from `setup.sql` in Supabase SQL Editor.

### "EADDRINUSE: address already in use :::3000"
**Solution:** Port 3000 is in use. Kill the process:
```bash
npx lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

### Supabase API Key errors
**Solution:** Make sure `.env` file has correct credentials copied from your Supabase project settings.

---

**Need help?** Check [Supabase Docs](https://supabase.com/docs) or project README.md
