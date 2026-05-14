-- Trikul Academy Database Setup
-- Run this SQL in Supabase SQL Editor to create all necessary tables

-- Create pdfs table
CREATE TABLE IF NOT EXISTS pdfs (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT,
  url TEXT NOT NULL,
  thumbnail_url TEXT,
  views INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create videos table
CREATE TABLE IF NOT EXISTS videos (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  thumbnail_url TEXT,
  clicks INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create affairs table
CREATE TABLE IF NOT EXISTS affairs (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  date TEXT,
  mcqs JSONB DEFAULT '[]',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  correct_index INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create analytics table
CREATE TABLE IF NOT EXISTS analytics (
  id BIGSERIAL PRIMARY KEY,
  content_type TEXT,
  content_id TEXT,
  action TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create streaks table
CREATE TABLE IF NOT EXISTS streaks (
  fingerprint TEXT NOT NULL,
  date TEXT NOT NULL,
  completed_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (fingerprint, date)
);

-- Enable RLS (Row Level Security) if needed
ALTER TABLE pdfs ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE affairs ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE streaks ENABLE ROW LEVEL SECURITY;

-- Create policies to allow public reads
CREATE POLICY "Allow public select on pdfs" ON pdfs FOR SELECT USING (true);
CREATE POLICY "Allow public select on videos" ON videos FOR SELECT USING (true);
CREATE POLICY "Allow public select on affairs" ON affairs FOR SELECT USING (true);
CREATE POLICY "Allow public select on tasks" ON tasks FOR SELECT USING (true);
CREATE POLICY "Allow public select on analytics" ON analytics FOR SELECT USING (true);
CREATE POLICY "Allow public select on streaks" ON streaks FOR SELECT USING (true);

-- Create policies to allow service role (admin) writes
CREATE POLICY "Allow service role insert on pdfs" ON pdfs FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role insert on videos" ON videos FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role insert on affairs" ON affairs FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role insert on tasks" ON tasks FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role insert on analytics" ON analytics FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow service role insert on streaks" ON streaks FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow service role update on pdfs" ON pdfs FOR UPDATE USING (true);
CREATE POLICY "Allow service role update on videos" ON videos FOR UPDATE USING (true);
CREATE POLICY "Allow service role update on tasks" ON tasks FOR UPDATE USING (true);

CREATE POLICY "Allow service role delete on pdfs" ON pdfs FOR DELETE USING (true);
CREATE POLICY "Allow service role delete on videos" ON videos FOR DELETE USING (true);
CREATE POLICY "Allow service role delete on affairs" ON affairs FOR DELETE USING (true);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_pdfs_created ON pdfs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_videos_created ON videos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_affairs_created ON affairs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_created ON analytics(created_at DESC);
