import uvicorn
from fastapi import FastAPI

from app.api.v1 import user, post
from app.core.config import config
from app.core.logging import setup_logging
from app.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)

# Register routes
app.include_router(user.router, prefix="/api/v1")
app.include_router(post.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # pragma: no cover
