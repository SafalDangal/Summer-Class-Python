import sqlite3

p = 'db.sqlite3'
conn = sqlite3.connect(p)
cur = conn.cursor()
try:
    cur.execute("SELECT app, name, applied FROM django_migrations WHERE app IN ('store','carts') ORDER BY app, name")
    rows = cur.fetchall()
    if not rows:
        print('No rows for store or carts')
    else:
        for app, name, applied in rows:
            print(f"{app}: {name} @ {applied}")
except Exception as e:
    print('ERR', type(e).__name__, e)
finally:
    conn.close()
