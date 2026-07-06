from fastapi import FastAPI

app = FastAPI(title="Flora API")

@app.get("/")
def root():
    return {"message": "Flora Backend Running"}