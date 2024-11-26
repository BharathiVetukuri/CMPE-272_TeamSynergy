from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


def connect_db():
    client = MongoClient(os.environ["MONGO_DB_KEY"])
    db = client["synergy_db"]
    return db


class Article(BaseModel):
    title: str
    content: str
    author: str
    published_date: str


# Save an article
def save_article(article: Article):
    db = connect_db()  # Connect to the database
    collection = db["synergy"]  # Access the 'articles' collection
    result = collection.insert_one(article.dict())  # Insert the article data
    return str(result.inserted_id)  # Return the ID of the inserted article


# Fetch articles
def fetch_articles(query={}) -> List[Article]:
    db = connect_db()  # Connect to the database
    collection = db["articles"]  # Access the 'articles' collection
    articles = collection.find(query)  # Fetch articles based on the query
    return [
        Article(**article) for article in articles
    ]  # Return the fetched articles as a list of Article objects


# API endpoint to save a demo article
@app.post("/articles/demo/")
def create_demo_article():
    demo_article = Article(
        title="Demo Article",
        content="This is a demo article content.",
        author="Demo Author",
        published_date="2023-10-01",
    )
    article_id = save_article(demo_article)  # Save the demo article
    return {"article_id": article_id}  # Return the ID of the saved article


# API endpoint to fetch all articles
@app.get("/articles/", response_model=List[Article])
def get_all_articles():
    articles = fetch_articles()  # Fetch all articles
    return articles  # Return the list of articles


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
