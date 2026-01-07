from fastapi import FastAPI
from pydantic import BaseModel
from classifier import article_analyzer

app = FastAPI()     # creates the application

# defines what the incoming requestmust look like - JSON with a text field
class ArticleAnalyzer(BaseModel):
    text: str

@app.get("/")       # let's me know if the server is alive
def root():
    return {"Status": "API is running"}

@app.post("/analyze")       # the main endpoint
def analyze(request: ArticleAnalyzer):
    result = article_analyzer(request.text)
    return result
