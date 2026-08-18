from fastapi import FastAPI

app = FastAPI(title="Data Quality Platform")


@app.get("/health")

def health():
    return{"status": "ok"}