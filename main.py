import fastapi

from routers.api.operator import router as router_operator
from routers.api.source import router as router_source
from routers.api.contact import router as router_contact
from routers.api.lead import router as router_lead
from routers.api.priority import router as router_priority

app = fastapi.FastAPI()

app.include_router(router_operator)
app.include_router(router_source)
app.include_router(router_contact)
app.include_router(router_lead)
app.include_router(router_priority)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)