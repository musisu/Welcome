import os
import aiosqlite

from bot.config import settings


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    contact TEXT NOT NULL,
    rp_experience TEXT NOT NULL,
    motivation TEXT NOT NULL,
    desired_role TEXT NOT NULL,
    extra TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
"""


async def init_db() -> None:
    os.makedirs(os.path.dirname(settings.database_path) or ".", exist_ok=True)
    async with aiosqlite.connect(settings.database_path) as db:
        await db.executescript(CREATE_SQL)
        await db.commit()


async def create_application(user_id: int, username: str | None, data: dict) -> int:
    async with aiosqlite.connect(settings.database_path) as db:
        cursor = await db.execute(
            """
            INSERT INTO applications
            (user_id, username, name, age, contact, rp_experience, motivation, desired_role, extra)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                data["name"],
                data["age"],
                data["contact"],
                data["rp_experience"],
                data["motivation"],
                data["desired_role"],
                data["extra"],
            ),
        )
        await db.commit()
        return cursor.lastrowid


async def get_latest_user_application(user_id: int):
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM applications WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        return await cursor.fetchone()


async def get_application(application_id: int):
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM applications WHERE id = ?",
            (application_id,),
        )
        return await cursor.fetchone()


async def update_application_status(application_id: int, status: str) -> bool:
    async with aiosqlite.connect(settings.database_path) as db:
        cursor = await db.execute(
            """
            UPDATE applications
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, application_id),
        )
        await db.commit()
        return cursor.rowcount > 0
