# 门诊数据小工具（clinic-tools）

一个用 Python + SQLite 写的命令行门诊数据查询工具，用来练习「业务查询 → 数据建模 → CLI 封装」的完整流程。

## 环境要求

- Python 3.11+
- 无需第三方依赖（只用标准库 `sqlite3` / `argparse`）

## 快速开始

```powershell
# 1. 创建并激活虚拟环境
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. 初始化数据库（建表 + 灌测试数据）
python clinic.py init

# 3. 开始查询
python clinic.py list
```

## 命令说明

| 命令 | 作用 | 示例 |
|---|---|---|
| `init` | 重建并填充 6 名患者、10+ 条就诊记录的测试数据 | `python clinic.py init` |
| `list` | 列出全部患者 | `python clinic.py list` |
| `search` | 按姓名模糊搜索（`--name` 必填） | `python clinic.py search --name 张` |
| `stats` | 按科室 + 日期区间统计人次与费用 | `python clinic.py stats --dept 内科 --start 2026-10-01 --end 2026-10-31` |

查看帮助：

```powershell
python clinic.py --help
python clinic.py search --help
```

## 数据表结构

`patients`（患者）

| 字段 | 类型 | 说明 |
|---|---|---|
| patient_id | TEXT | 就诊号，主键 |
| name | TEXT | 姓名 |
| dept | TEXT | 科室 |

`visits`（就诊记录）

| 字段 | 类型 | 说明 |
|---|---|---|
| visit_id | INTEGER | 自增主键 |
| patient_id | TEXT | 关联 patients |
| visit_date | TEXT | 就诊日期 `YYYY-MM-DD` |
| total_fee | REAL | 本次总费用 |
| diagnosis | TEXT | 诊断 |

## 已实现函数

| 函数 | 返回 | 说明 |
|---|---|---|
| `init_db()` | None | 建表 + 灌测试数据 |
| `query_all_patients()` | None | 打印全部患者 |
| `get_dept_visit_count(dept, start, end)` | int | 科室区间内就诊人次 |
| `get_dept_fee_summary(dept, start, end)` | dict | 人次 / 总费用 / 人均费用 |
| `search_patients_by_keyword(keyword)` | list[dict] | 姓名模糊搜索，无结果返回 `[]` |

## 踩过的坑（学习记录）

1. **`fetchone()` vs `fetchall()`**：前者返回"一行"，遍历它会得到各个字段值（字符串）；返回一批数据必须用 `fetchall()`。
2. **`return` 的缩进**：`return` 缩在 `for` 内部会导致只返回第一条；查无数据时函数隐式返回 `None`，而不是 `[]`。
3. **`conn.cursor` 少了括号**：会报 `'builtin_function_or_method' object has no attribute 'execute'`。
4. **`row_factory` 必须设在 `cursor()` 之前**：否则 `row["列名"]` 取不出值。
5. **`SUM`/`AVG` 查无数据返回 `None`**：直接 `round()` 会崩，需要先兜底。

## 目录结构

```
week1-sql-to-python/
├── clinic.py         # 主程序（业务函数 + CLI）
├── hello.py          # 第一个练习脚本
├── demo.py           # 函数入门示例
├── demo_row.py       # row_factory 对照实验
├── demo_fetch.py     # fetchone / fetchall 对照实验
├── .gitignore
└── README.md
```
