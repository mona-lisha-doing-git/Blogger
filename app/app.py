from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import create_db_and_tables, Post, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

app = FastAPI()

text_posts = {
    1: {"title": "Getting Started with FastAPI", "content": "FastAPI is a modern web framework for building APIs with Python."},
    2: {"title": "Understanding REST APIs", "content": "REST APIs use HTTP methods like GET, POST, PUT, DELETE."},
    3: {"title": "Python Tips", "content": "Use list comprehensions and generators for efficient code."},
    4: {"title": "Async vs Sync", "content": "Async programming helps handle multiple requests efficiently."},
    5: {"title": "Databases with SQLAlchemy", "content": "SQLAlchemy is a powerful ORM for Python."},
    6: {"title": "JWT Authentication", "content": "JWT is used for secure authentication between client and server."},
    7: {"title": "Error Handling in APIs", "content": "Always return proper HTTP status codes and messages."},
    8: {"title": "Project Ideas", "content": "Build a password manager or blog API using FastAPI."},
    9: {"title": "Deployment Guide", "content": "You can deploy FastAPI apps using Docker, Render, or GCP."},
    10: {"title": "Debugging Tips", "content": "Use logs and print statements to debug your application."}
}

@app.get("/posts")
def get_all_post(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title":post.title, "content":post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post

@app.delete("/posts/{id}")
def delete_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found!!!!")
    del_post = text_posts[id]
    del text_posts[id]
    return del_post