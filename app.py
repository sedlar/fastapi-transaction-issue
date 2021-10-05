import databases
import sqlalchemy
from fastapi import FastAPI

from pydantic.main import BaseModel

DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"


metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

database = databases.Database(DATABASE_URL)


class NoteIn(BaseModel):
    text: str
    completed: bool


app = FastAPI()


async def execute_some_query():
    query = notes.select().where(notes.c.id == 1)
    await database.fetch_one(query)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/notes/")
async def create_note(note: NoteIn):
    # WHEN We execute some query outside transaction
    await execute_some_query()

    # AND THEN execute some other inside transaction
    async with database.transaction():
        query = notes.insert().values(text=note.text, completed=note.completed)
        await database.execute(query)
        raise Exception()
    # The transaction is not rollbacked
    return {}
