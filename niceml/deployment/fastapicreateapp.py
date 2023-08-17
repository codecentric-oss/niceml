from contextlib import asynccontextmanager

from fastapi import FastAPI


def create_fastapi_app(assets: dict, asset_loaders: dict):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Load the ML model
        for key, value in asset_loaders.items():
            assets[key] = value()
        yield
        # Clean up the ML models and release the resources
        assets.clear()

    app = FastAPI(lifespan=lifespan)
    return app
