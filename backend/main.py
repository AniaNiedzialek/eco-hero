from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# routers
from routers.rules import router as rule_router # rules 
from routers.collection import router as collection_router
from routers.scanner import router as scanner_router
from routers.bin import router as bin_router

app = FastAPI(title="Eco Hero API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=[
        "https://eco-hero-2ec20.web.app",
        "https://eco-hero-2ec20.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(rule_router, prefix="/api")
app.include_router(collection_router, prefix="/api")
app.include_router(scanner_router, prefix="/api")
app.include_router(bin_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
