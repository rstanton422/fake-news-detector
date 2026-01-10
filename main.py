from fastapi import FastAPI
from pydantic import BaseModel
from classifier import article_analyzer

app = FastAPI()     # creates the application object

# adding security layer to handle cross-domain requests
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # allows any website to access API
    allow_methods = ["*"],  # allows all standard HTTP methods (GET, POST, etc)
    allow_headers = ["*"]   # allow all types of browser headers to be sent to the server
)

# defines what the incoming requestmust look like - JSON with a text field
class ArticleAnalyzer(BaseModel):
    text: str

@app.get("/")       # let's me know if the server is alive
def root():
    # ouptut when user visits main URL upon a successful GET request
    return {"Status": "API is running"}

@app.post("/analyze")       # the main endpoint
# This function receives the incoming data 
# FastAPI automatically maps the JSON body to the ArticleAnalyzer model 
# that was defined earlier.
def analyze(request: ArticleAnalyzer):
    result = article_analyzer(request.text)
    return result
