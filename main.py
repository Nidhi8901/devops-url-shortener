from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random, string

app = FastAPI()
url_db = {}

class URLItem(BaseModel):
    long_url: str

def generate_short_code(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API! Use POST /shorten to shorten a URL."}

@app.post("/shorten")
def shorten_url(item: URLItem):
    code = generate_short_code()
    url_db[code] = item.long_url
    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect_url(code: str):
    if code in url_db:
        return {"long_url": url_db[code]}
    raise HTTPException(status_code=404, detail="URL not found")
