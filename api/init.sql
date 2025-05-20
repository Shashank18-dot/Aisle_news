-- Create the ai_news_raw table for storing all headlines
CREATE TABLE IF NOT EXISTS ai_news_raw (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    feed_source TEXT NOT NULL,
    feed_category TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(link, feed_source)
);

-- Create index on published_at for efficient time-based queries
CREATE INDEX IF NOT EXISTS idx_ai_news_raw_published_at ON ai_news_raw(published_at);

-- Create index on feed_source for efficient source-based queries
CREATE INDEX IF NOT EXISTS idx_ai_news_raw_feed_source ON ai_news_raw(feed_source);

-- Create index on feed_category for efficient category-based queries
CREATE INDEX IF NOT EXISTS idx_ai_news_raw_feed_category ON ai_news_raw(feed_category); 