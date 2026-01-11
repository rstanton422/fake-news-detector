#==========================================================
#     IMPORTS
#==========================================================

# FastAPI - main class that creates application.  
# Depends - dependency injection system. let's us say:
#   "before running this function ,run this other function first and let me have the result"
from fastapi import FastAPI, Depends    

# this handles data validation
# When a class is defined inheriting from BaseModel, FastAPI automatically validates incoming JSON against that structure 
# If someone sends malformed data, FastAPI rejects it before your code even runs.
from pydantic import BaseModel

# every request passes through Middleware first
# CORSMiddleware adds headers and tells browsers "it's ok to call this API from other domains"
from fastapi.middleware.cors import CORSMiddleware

# this is a type hint
# doesn't do anything at runtime
# tells Python that this will be an SQLAlchemy session object
from sqlalchemy.orm import Session

# these are my own files with the needed modules
from database import SessionLocal, Analysis # this is my session factory and table model
from classifier import article_analyzer     # this is my ML function

#==========================================================
#     MY CODE
#==========================================================

# creates the application object
# this object is what uvicorn runs
# all routes get attached to this
app = FastAPI()     

# adding security layer to handle cross-domain requests
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # allows any website to access API
    allow_methods = ["*"],  # allows all standard HTTP methods (GET, POST, etc)
    allow_headers = ["*"]   # allow all types of browser headers to be sent to the server
)

def get_database():
    """
    Create a database session for a request.
    
    Yields a SQLAlchemy session that automatically closes when the request
    completes, even if an error occurs.
    
    Yields:
        Session: A SQLAlchemy database session.
    """
    database = SessionLocal()   # creates a new database session
    try:
        yield database          # pauses the functon and hands the session to the endpoint
    finally:                    # endpoint does its thing and after it finishes, it executes "finally"
        database.close()        # closes the db session - runs no matter what



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
# get_db() - creates a database, gives it to the endpoint, and then closes it when done
# Depends(get_db) - FastAPIs dependency injection - automatically calls get_db() and passes the session to the function
# after getting the prediction - create an Analysis object and save it
# database: Session = Depends(get_db) - FASTAPI sees Depends, calls get_db() and passes the yielded session as database
# this is dependency injection - function declares what it needs... FASTAPI provides it
def analyze(request: ArticleAnalyzer, database: Session = Depends(get_database)):
    """
    Analyze article text for fake news indicators.
    
    Takes article text, runs it through the classifier model, saves the
    result to the database, and returns the prediction.
    
    Args:
        request: Validated request body containing article text.
        db: Database session injected by FastAPI.
        
    Returns:
        dict: Contains 'label' (FAKE/TRUE) and 'confidence' (0-1).
    """
    result = article_analyzer(request.text) # calls classifier function  from classifier.py

    # save to database
    # creates and instance of the Analysis model
    # it's a Python object that represents a row in the DB table
    # not officially saved at this point - just exists in memory
    analysis = Analysis(
        text = request.text,
        label = result["Label"],
        confidence = result["Confidence"]
    )

    database.add(analysis)  # stages the object for insertion - it's "pending" being added to the table
    database.commit()       # this executes the SQL INSERT and saves to the DB - nothing happens with data until THIS is called

    # return prediction to the user
    return result
