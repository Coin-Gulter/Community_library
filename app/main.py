from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routers import auth
from app.api.routers.v1 import library as library_v1
from app.api.routers.latest import library as library_latest


# Middleware to handle API versioning based on a header
class APIVersionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # The client sends version info in the headers
        api_version = request.headers.get("x-api-version", "v1")

        # Rewrite the URL path to include the version prefix
        if request.url.path.startswith("/api/"):
            request.scope["path"] = request.scope["path"].replace("/api/", f"/api/{api_version}/")

        response = await call_next(request)
        return response


app = FastAPI(title="Library Management Service")

# Add the versioning middleware
app.add_middleware(APIVersionMiddleware)

# --- ROUTERS ---
# Include the authentication router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include the versioned library routers
app.include_router(library_v1.router, prefix="/api/v1", tags=["Library V1"])
app.include_router(library_latest.router, prefix="/api/latest", tags=["Library Latest"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Community Library API"}
