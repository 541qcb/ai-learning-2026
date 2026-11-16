1. 语法错误导致 worker 崩溃，端口仍被占用 → 浏览器一直转圈不报错
2. `basemodel` 大小写 / `class` 少冒号
3. SQL 里 `inset`、`paitent` 拼错，sqlite 报错信息极难读
4. **全角逗号 `，` 混进代码** → `SyntaxError: invalid character`，编辑器却提示 "括号未闭合"
5. 重复 POST 撞主键 → **500 改成 409 + 中文提示**
6. `Undocumented` → 接口文档要主动声明错误码