import uvicorn
from fastapi import FastAPI

from src.routes import monsters, users, players, encounters

app = FastAPI(title="Initiative Tracker")

app.include_router(users.router)
app.include_router(monsters.router)
app.include_router(players.router)
app.include_router(encounters.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=True)