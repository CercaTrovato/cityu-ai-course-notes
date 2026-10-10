# 图源复现入口

源与课程原数据只读；默认输出到脚本同目录。复核时指定独立输出目录，避免覆盖现有 SVG：

```powershell
D:\anaconda3\python.exe -X utf8 "figures.py" --output-dir "E:/app-data/codex/scratchpad/your-task/output"
```

在本图源目录执行，或把脚本参数换成它的绝对路径。所有算法输入、版本与结果保存在同目录 JSON；SVG 保留可检索文字。PNG 预览由授权 release/preview_svg.py 生成，不作为唯一图源。
