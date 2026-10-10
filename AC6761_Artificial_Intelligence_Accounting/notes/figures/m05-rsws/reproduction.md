# RSWS 同源图复现

`model.json` 保存 9 个类、9 条关联、18 个端点、30 个类属性和 4 个关联属性。结构图与全属性图只在类内字段显示上不同。

依赖：Node.js、`@viz-js/viz` 3.31.0（Graphviz 16.1.0）。在本目录运行：

```powershell
node ./render-rsws.mjs --input ./model.json --output ./rsws-full --runtime-dir E:/app-data/diagram-tools
node ./render-rsws.mjs --input ./model.json --output ./rsws-overview --overview --runtime-dir E:/app-data/diagram-tools
```

也可将 `--input`、`--output`、`--runtime-dir` 改为相应绝对路径。输出是 DOT、SVG、布局 JSON 和生成记录，均由临时文件原子替换，不依赖作者的 manage.py 或 work 路径。

代码源于库内通用 Graphviz 渲染器的本包副本。本轮只改间距与端点标签布局：水平关系沿线放置带白底的多重性标签；竖向 Duality 端点保留侧向偏移，避开关系名与分配属性。无箭头线始终是关联，不是业务动作方向。

Cash 的 ResourceType 原标记、Supplier 范围限制与 AP-bond 未知保持不变。生成记录只证明语法和结构，不能代替业务语义与最终载体验收。
