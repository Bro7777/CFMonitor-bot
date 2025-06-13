import sqlite3
conn=sqlite3.connect("cfmonitor_database.db")
cursor=conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_handles(
    discord_id TEXT PRIMARY KEY,
    cf_handle UNIQUE
    )
'''
)
conn.commit()

def link_handle(discord_id,handle):
    cursor.execute("INSERT OR IGNORE INTO user_handles (discord_id,cf_handle) VALUES (?,?)",(discord_id,handle))
    conn.commit()


def get_handle(discord_id):
    cursor.execute("SELECT * FROM user_handles WHERE discord_id=?",(discord_id,))
    return cursor.fetchone()

def unlink_handle(discord_id):
    cursor.execute("DELETE FROM user_handles WHERE discord_id=?",(discord_id,))
    conn.commit()