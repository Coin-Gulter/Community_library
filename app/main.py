from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routers import auth, users
from app.api.routers.v1 import library as library_v1
from app.api.routers.latest import library as library_latest


# Middleware to handle API versioning based on a header
class APIVersionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # The client sends version info in the headers
        api_version = request.headers.get("x-api-version", "v1")

        # Check if the path already contains a version prefix
        path = request.scope["path"]
        if path.startswith("/api/v1/") or path.startswith("/api/latest/"):
            # If it does, do nothing and proceed
            pass
        elif path.startswith("/api/"):
            # If it doesn't, rewrite the URL to include the version
            request.scope["path"] = path.replace("/api/", f"/api/{api_version}/")

        response = await call_next(request)
        return response


app = FastAPI(title="Library Management Service")

app.add_middleware(APIVersionMiddleware)

# --- ROUTERS ---
# Include the authentication router
# Include the authentication and new users router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"]) # Add this line

# Include the versioned library routers
app.include_router(library_v1.router, prefix="/api/v1", tags=["Library V1"])
app.include_router(library_latest.router, prefix="/api/latest", tags=["Library Latest"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Community Library API"}
