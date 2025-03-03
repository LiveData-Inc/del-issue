from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import Settings, get_settings
from .db import get_engine, get_session_maker
from .models import SQLModel  # use this copy of SQLModel in order to import our models for `.metadata.create_all`
from .routes import router
from .seed_data import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    app.state.async_session_maker = get_session_maker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await seed_data(app.state.async_session_maker)

    yield

    await engine.dispose()


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()
    app = FastAPI(
        title="Test API",
        lifespan=lifespan
    )
    app.state.settings = settings
    app.include_router(router)
    return app


app = create_app()
