from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app);
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(content={'Error': str(e)}, status_code=500)