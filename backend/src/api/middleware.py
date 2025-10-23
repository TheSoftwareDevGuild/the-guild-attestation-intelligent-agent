import logging
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger=logging.getLogger(__name__)

class RequestIdMiddleware(BaseHTTPMiddleware):
    "Middleware that adds a request id to each request"

    async def dispatch(self,request:Request,call_next):
        request_id=str(uuid.uuid4())
        request.state.request_id=request_id
        logger.info(f"RequestStarted: {request.method} {request.url.path} (request_id: {request_id})")
        response= await call_next(request)
        response.headers["X-Request-Id"]=request_id
        logger.info(f"Request completed: {request.method} {request.url.path} (request_id: {request_id})")
        return response