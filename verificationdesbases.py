import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

cursor.execute("SELECT * FROM produit")
commande_items = cursor.fetchall()
for play in commande_items:
   print(play)
