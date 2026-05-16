import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent / "memory.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                summary TEXT NOT NULL
            )
        """)


async def store_fact(user_id: int, key: str, value: str):
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO user_facts (user_id, key, value) VALUES (?, ?, ?)",
            (user_id, key, value),
        )
        await db.commit()


async def get_facts(user_id: int) -> list[tuple[str, str]]:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT key, value FROM user_facts WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchall()


async def store_summary(user_id: int, summary: str):
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO conversation_summaries (user_id, summary) VALUES (?, ?)",
            (user_id, summary),
        )
        await db.commit()


async def get_summary(user_id: int) -> str | None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT summary FROM conversation_summaries WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
