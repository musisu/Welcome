import os

import aiosqlite

from bot.config import settings


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    rp_experience TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


async def init_db() -> None:
    os.makedirs(
        os.path.dirname(settings.database_path) or ".",
        exist_ok=True,
    )

    async with aiosqlite.connect(
        settings.database_path
    ) as db:
        await db.execute(CREATE_TABLE_SQL)
        await db.commit()


async def create_application(
    user_id: int,
    username: str,
    rp_experience: str,
) -> int:
    async with aiosqlite.connect(
        settings.database_path
    ) as db:
        cursor = await db.execute(
            """
            INSERT INTO applications (
                user_id,
                username,
                rp_experience
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                username,
                rp_experience,
            ),
        )

        await db.commit()

        return cursor.lastrowid
