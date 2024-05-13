from fastapi import applications, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi_offline_swagger_ui
import os
from pydantic import BaseModel, Field
from typing import Annotated
from .services import (
    EnqueueDocumentProcessorJob,
)


app = FastAPI(
    title="Invoice Track",
    description="Invoice Track is a invoice data query webservice.",
    version="0.0.1",
    contact={
        "url": "https://github.com/Cellpap/invoice_track/"
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)
token_auth_scheme = HTTPBearer()

assets_path = fastapi_offline_swagger_ui.__path__[0]
if os.path.exists(assets_path + "/swagger-ui.css") and os.path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")
    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )
    applications.get_swagger_ui_html = swagger_monkey_patch


def get_token(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token = credentials.credentials
    if not token or token != os.getenv("RAILS_CLIENT_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")

    return token


# API Definitions Start
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"


class DocumentBody(BaseModel):
    document_url: str = Field(description="Document to process upon")


@app.post("/document/process", tags=["Endpoints"])
async def document_process(token: Annotated[str, Depends(get_token)], body: DocumentBody):
    # TODO: Assuming for the time being that the document is hosted and the link is available
    if document_url is not None:
        process_result = EnqueueDocumentProcessorJob(document_url).perform()
    else:
        raise HTTPException(status_code=400, detail="No uploaded file sent")

    result = {
        "process_result": process_result,
    }

    return result
