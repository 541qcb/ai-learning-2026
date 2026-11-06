import sqlite3

DB_PATH = "clinic.db"

# ---------- 情况 A：不设 row_factory（默认是 tuple） ----------
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients LIMIT 2")
    rows = cur.fetchall()

print("=== 情况 A：不设 row_factory ===")
for row in rows:
    print("整行：", row)
    print("类型：", type(row))
    print("按编号取 row[0] =", row[0])
    # print(row["name"])            # 取消注释会报 TypeError
    print("-" * 40)

# ---------- 情况 B：设了 row_factory（返回 Row 对象） ----------
with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row       # 只有这一行的区别
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients LIMIT 2")
    rows = cur.fetchall()

print("=== 情况 B：设了 row_factory = sqlite3.Row ===")
for row in rows:
    print("整行：", tuple(row))
    print("类型：", type(row))
    print("按编号取 row[0] =", row[0])
    print("按列名取 row['name'] =", row["name"])
    print("所有列名：", row.keys())
    print("-" * 40)
