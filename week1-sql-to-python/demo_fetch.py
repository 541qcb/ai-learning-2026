import sqlite3

DB_PATH = "clinic.db"


def show(title, value):
    print(f"{title:<28} -> {value}  (类型: {type(value).__name__})")


# ---------- 实验 1：同一个游标，fetchone 两次，再 fetchall ----------
print("=== 实验1：游标是个'指针'，取过的不会重复给 ===")
with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT patient_id, name FROM patients")   # 一共 6 条

    show("第1次 fetchone()", tuple(cur.fetchone()))
    show("第2次 fetchone()", tuple(cur.fetchone()))
    rest = cur.fetchall()
    show("随后 fetchall() 剩余行数", len(rest))
    print("   剩余内容:", [tuple(r) for r in rest])

# ---------- 实验 2：查不到数据时两者返回值不同 ----------
print()
print("=== 实验2：查不到数据 ===")
with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT patient_id, name FROM patients WHERE name = '赵六'")
    show("fetchone()", cur.fetchone())

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT patient_id, name FROM patients WHERE name = '赵六'")
    show("fetchall()", cur.fetchall())

# ---------- 实验 3：聚合查询只有一行，两者都能用 ----------
print()
print("=== 实验3：COUNT 只有一行 ===")
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM patients")
    show("COUNT 的 fetchone()", cur.fetchone())

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM patients")
    show("COUNT 的 fetchall()", cur.fetchall())
