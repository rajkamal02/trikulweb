# ⚔ Trikul Academy

A complete full-stack educational platform built with Node.js + Express + Supabase.

## 🚀 Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Start the server
npm start

# 3. Open in browser
http://localhost:3000
```

## 🔐 Admin Access

1. Look for the **tiny gold dot** in the bottom-left corner of the page
2. **Click it 3 times** → Admin Login modal opens
3. Login with:
   - Email: `admin@trikul.com`
   - Password: `trikul01234`

## 📁 Project Structure

```
trikul-academy/
├── server.js          # Express API server
├── .env               # Environment variables
├── package.json
└── public/
    └── index.html     # Full student + admin UI
```

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/login | Admin login |
| GET | /api/auth/verify | Verify JWT |
| GET | /api/pdfs | Get all PDFs |
| POST | /api/pdfs | Add PDF (auth) |
| PATCH | /api/pdfs/:id/view | Increment view |
| DELETE | /api/pdfs/:id | Delete PDF (auth) |
| GET | /api/videos | Get all videos |
| POST | /api/videos | Add video (auth) |
| PATCH | /api/videos/:id/click | Increment click |
| DELETE | /api/videos/:id | Delete video (auth) |
| GET | /api/affairs | Get all affairs |
| POST | /api/affairs | Publish affair (auth) |
| DELETE | /api/affairs/:id | Delete affair (auth) |
| GET | /api/tasks | Get latest task |
| POST | /api/tasks | Set task (auth) |
| POST | /api/streak/complete | Save streak |
| GET | /api/analytics | Get analytics (auth) |
| POST | /api/mcq/generate | AI MCQ (auth) |
| GET | /api/health | Health check |

## ⚙️ Environment Variables (.env)

```
PORT=3000
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key
JWT_SECRET=trikul_secret_2025
ADMIN_EMAIL=admin@trikul.com
ADMIN_PASS=trikul01234
ANTHROPIC_API_KEY=your_anthropic_key  # For AI MCQ generation
```

## 🗄️ Supabase Tables Required

Run these SQL commands in your Supabase SQL editor:

```sql
create table pdfs (id text primary key, title text, category text, url text, views int default 0, created_at timestamptz);
create table videos (id text primary key, title text, url text, clicks int default 0, created_at timestamptz);
create table affairs (id text primary key, title text, content text, date text, mcqs jsonb, created_at timestamptz);
create table tasks (id text primary key, question text, options jsonb, correct_index int, created_at timestamptz);
create table streaks (fingerprint text, date text, completed_at timestamptz, primary key (fingerprint, date));
create table analytics (id serial primary key, content_type text, content_id text, action text, created_at timestamptz);
```
