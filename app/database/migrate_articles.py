import sqlite3

DB_PATH = "data/newspulse.db"


columns = {
    "content": "TEXT",
    "content_type": "TEXT DEFAULT 'article'",
    "scraped_at": "DATETIME",
}


with sqlite3.connect(DB_PATH) as connection:

    cursor = connection.cursor()

    existing_columns = {
        row[1]
        for row in cursor.execute(
            "PRAGMA table_info(articles)"
        ).fetchall()
    }

    added = 0

    for column_name, column_definition in columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE articles
                ADD COLUMN {column_name} {column_definition}
                """
            )

            added += 1

            print(f"Added column: {column_name}")

        else:
            print(f"Already exists: {column_name}")

    connection.commit()

print(f"\nMigration complete. Columns added: {added}")