import sqlite3

conn = sqlite3.connect("AriBilgi.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS ogrenciler(id INTEGER PRIMARY KEY, ad TEXT, soyad TEXT, telefon INTEGER)")
conn.commit()