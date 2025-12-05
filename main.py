import fastapi
from routers.api import operator, lead, priority, source, contact

app = fastapi.FastAPI()


app.include_router(operator.router)
app.include_router(lead.router)
app.include_router(priority.router)
app.include_router(source.router)
app.include_router(contact.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)