def calc_avg(total_fee, visit_count):
    if visit_count == 0:
        return 0
    return round(total_fee / visit_count, 2)


result1 = calc_avg(12345.6, 15)
print("人均费用：", result1)

result2 = calc_avg(0, 0)
print("空数据时：", result2)
