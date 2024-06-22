from fastapi import FastAPI
from backend.config import DatabaseSession
from contextlib import asynccontextmanager

def init_app() -> FastAPI:
    db = DatabaseSession()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await db.create_all()
        try:
            yield
        finally:
            await db.close()

    app = FastAPI(
        lifespan=lifespan,
        title="Db Catalog Backend Server",
        description="Db Catalog Backend Server",
        debug=True)


    @app.get("/")
    def read_root():
        return "Welocome to Db Catalog Backend Server"


    return app


app: FastAPI = init_app()
