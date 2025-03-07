import os
import praw
from textblob import TextBlob
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit credentials
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")

# Database URL (Neon)
db_url = os.getenv("DATABASE_URL")
print(f"Database URL: {db_url}")  # Debug

# Connect to PostgreSQL (Neon)
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

# Stream Reddit submissions
subreddit = reddit.subreddit("all")  # Stream from all subreddits or specify one (e.g., "python")
for submission in subreddit.stream.submissions():
    sentiment = TextBlob(submission.title).sentiment.polarity
    print(f"Post: {submission.title}, Sentiment: {sentiment}")
    cursor.execute(
        "INSERT INTO posts (post_id, title, sentiment) VALUES (%s, %s, %s) ON CONFLICT (post_id) DO NOTHING",
        (submission.id, submission.title, sentiment)
    )
    conn.commit()

# Close database connection (won’t reach unless interrupted)
conn.close()