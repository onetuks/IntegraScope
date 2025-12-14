from fastapi import FastAPI

app = FastAPI()
  _app.add_middleware(
      CORSMiddleware,
      allow_origins=allowed_origins(),
      allow_credentials=True,
      allow_methods=allowed_methods(),
      allow_headers=allowed_headers(),
  )


@app.get("/health")
def health():
    return {"health": "ok"}
