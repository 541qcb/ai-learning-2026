import sqlite3  

DB_PATH = "clinic.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()


        # 建 patients 表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT,
                dept TEXT
            )
        """)

        # 建 visits 表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                visit_date TEXT,
                total_fee REAL,
                diagnosis TEXT
            )
        """)

        # 清空旧数据（不然重复跑会主键冲突）
        cur.execute("DELETE FROM visits")
        cur.execute("DELETE FROM patients")

        # === 患者表：自己补全到 6 个 ===
        patients = [
            ("P001", "张三", "内科"),
            ("P002", "李四", "外科"),
            ("P003", "王五", "儿科"),
            ("P004", "张丽", "神经内科"),
            ("P005", "张可", "神经外科"),
            ("P006", "张忍", "呼吸内科"),
            # TODO: 再加 3 个，内科/外科/儿科都要有
        ]
        cur.executemany("INSERT INTO patients VALUES (?, ?, ?)", patients)

        # === 就诊表：自己补全到 10 条 ===
        # 格式：(patient_id, 日期, 费用, 诊断)
        visits = [
            ("P001", "2026-10-05", 235.5, "高血压"),
            ("P002", "2026-10-12", 240.0, "高血压复诊"),
            ("P003", "2026-10-08", 1580.0, "阑尾炎术后"),
            ("P001", "2026-10-13", 1500.0, "感冒"),
            ("P005", "2026-10-14", 150.0, "胸痛"),
            ("P006", "2026-10-15", 1860.0, "头晕"),
            ("P001", "2026-10-16", 160.0, "腿痛"),
            ("P008", "2026-10-17", 80.0, "风湿病"),
            ("P001", "2026-10-18", 2080.0, "呼吸道感染"),
            ("P010", "2026-10-19", 800.0, "手骨折"),
            # TODO: 再加 7 条，日期都在 2026-10 月
        ]
        cur.executemany(
            "INSERT INTO visits (patient_id, visit_date, total_fee, diagnosis) VALUES (?, ?, ?, ?)",
            visits
        )

        


        conn.commit()

    print("数据库初始化完成")

def query_all_patients():
         with sqlite3.connect(DB_PATH) as conn:
          conn.row_factory = sqlite3.Row   # 关键这行：让返回的行能按列名取值
         cur = conn.cursor()
         cur.execute("SELECT * FROM patients")
         rows = cur.fetchall()            # 取出所有行

         print("=== 全部患者 ===")
         for row in rows:
          print(row["patient_id"], row["name"], row["dept"])

def get_dept_visit_count(dept: str, start_date: str, end_date: str) -> int:
    """统计某科室在日期范围内的就诊人次"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM visits v
            JOIN patients p ON v.patient_id = p.patient_id
            WHERE p.dept = ? AND v.visit_date BETWEEN ? AND ?
        """, (dept, start_date, end_date))
        row = cur.fetchone()
        return row[0]

def get_dept_fee_summary(dept: str, start_date: str, end_date: str) -> dict:
    """计算总价"""    
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
SELECT
    COUNT(*),
    SUM(total_fee) ,
    AVG(total_fee)
FROM visits v
JOIN patients p ON v.patient_id = p.patient_id
WHERE p.dept = ? AND v.visit_date BETWEEN ? AND ?
""",(dept,start_date,end_date))
        row = cur.fetchone()

        visits=row[0]
        total_fee= row[1]  if row[1] is not None else 0
        avg_fee = round(row[2] ,2)  if row[2] is not None else 0
        return {
            "dept":dept,
            "visits":visits,
            "total_fee":round(total_fee ,2),
            "avg_fee":avg_fee

        }
def search_patients_by_keyword(keyword: str) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients WHERE name LIKE ?", (f"%{keyword}%",))
        rows = cur.fetchall()
        result = []                      # 建一个空列表
        for row in rows:                 # 遍历每一行
         result.append({
             "patient_id": row["patient_id"], 
             "name": row["name"], 
             "dept": row["dept"]})
    return result



def list_patients() -> list[dict]:
    """返回全部患者（给接口层用，不打印）"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients")
        rows = cur.fetchall()

    return [
        {"patient_id": r["patient_id"], "name": r["name"], "dept": r["dept"]}
        for r in rows
    ]


def create_patient(patient_id: str, name: str, dept: str) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO patients (patient_id, name, dept) VALUES (?, ?, ?)",
            (patient_id, name, dept),
        )
        conn.commit()

    return {"patient_id": patient_id, "name": name, "dept": dept}

