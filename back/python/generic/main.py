from fastapi import FastAPI, APIRouter
from user.controller import router as user_router

app = FastAPI()

router = APIRouter(
    prefix="/api"
)
app.include_router(user_router)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
