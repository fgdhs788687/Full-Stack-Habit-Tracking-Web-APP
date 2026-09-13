import uvicorn
from fastapi import FastAPI
from app.core.database import Base, engine
import app.models.db_models
from app.api.routers import auth, habits, chat
from slowapi import _rate_limit_exceeded_handler # this handles the rate limit exceeded error
from slowapi.errors import RateLimitExceeded
from app.api.rate_limiting_setting import limiter

# print("Connecting to the database and creating tables...")
# We can remove this or comment this line as alembic will create updated tables automatically:
# Base.metadata.create_all(bind=engine) # This only creates table when the tables doesnt exist and from the 2nd time it does nothing
# print("Tables have been created sucessfully.")

app = FastAPI(title="Habit Tracking API")
# We need to do this setting for rate limiting to work:
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler
)


app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(habits.router, prefix='/habits', tags=['Habits'])
app.include_router(chat.router, prefix='/chat', tags=['Chat'])

@app.get("/")
def home() -> dict:
    return {"message": "Welcome from backend"}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)