"""
Remove 'carts' migration records from the sqlite3 django_migrations table
This script uses sqlite directly and must be run from the project root where
`db.sqlite3` lives. It does NOT import Django to avoid import/setting issues.
"""
import sqlite3
import os
import sys

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
if not os.path.exists(DB):
    print('db not found at', DB)
    sys.exit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations'")
    if not cur.fetchone():
        print('django_migrations table not found')
        sys.exit(1)

    cur.execute("SELECT COUNT(*) FROM django_migrations WHERE app=?", ('carts',))
    before = cur.fetchone()[0]
    print('carts rows before:', before)
    if before > 0:
        cur.execute("DELETE FROM django_migrations WHERE app=?", ('carts',))
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM django_migrations WHERE app=?", ('carts',))
        after = cur.fetchone()[0]
        print('carts rows after:', after)
    else:
        print('no carts rows to delete')
finally:
    conn.close()
