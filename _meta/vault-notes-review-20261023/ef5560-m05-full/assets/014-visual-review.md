# 实际显示核对与证据承接

主代理 `/root`（请求模型 gpt-6.1-sol），最终候选 `candidate.md` SHA-256 `365c6086f9f03d173b1ecbcfbf9c9a4020fb36c309c9bd10c81e3478e25d44a3`。

## 本次实际查看

1. 用 ChatGPT in-app browser 自建后台标签打开本任务 `http://127.0.0.1:8814/preview.html`，随后打开 `preview-final.html`。没有操作别的会话标签，没有动 8810。Chrome DevTools MCP 首次因共享 profile 已被占用无法创建标签；未改配置/停浏览器，改用独立 IAB 标签。
2. 同源显示由 Python Markdown（tables/fenced_code/md_in_html）、MathJax SVG 和既有本地 Mermaid runtime 生成。第一次预览发现 HTML details 内 Markdown 未展开解析，已只修预览器的 md_in_html 处理并重看；候选 Markdown 本身的原题未改。此处明确是浏览器载体，不冒称原生 Obsidian 阅读视图。
3. 初版新题面数学与图片 DOM 检查：919 个 MathJax container、0 个 `mjx-merror`，8 个 SVG 均加载完成。最终修复版：950 个 MathJax container、0 个 `mjx-merror`；这是解析检查，不代表950式逐式实看。
4. 实际阅读窗口截图宽1265、高712（页面预期正文宽1080）。逐一展开 p.21/25/26/27/43/49 原题：四股表头、数值、完整小问、全部选项、公式上下标与英文参考答案清楚；长题用相邻两个窗口查看。截图 `visual-p21.png`、`visual-p21-answers.png`、`visual-p25.png`、`visual-p25-answers.png`、`visual-p26.png`、`visual-p27.png`、`visual-p43.png`、`visual-p49.png`。未见负号丢失、选项错列、公式源码露出或横向截断。
5. 最终 B1 四行数据/交叉项/两个半轴配平方/零端点，实际分三窗口读完：`visual-lasso-input.png`、`visual-lasso-squares.png`、`visual-lasso-boundary.png`。公式中括号、负号、平方及常数0.0162/0.01875可辨，表格与正文单位一致。`visual-meanvariance-square.png` 实看新增无需微积分的“常数减距离平方”解释及其公式。
6. B2/B3 新增课堂段：`visual-characteristic-example.png`、`visual-etf-example.png`、`visual-capm-classroom.png`。读到了规模/价值两侧、理想化正负倍数与真实产品边界、未知股名/未核网页值、同期解释与事前预测的区分；无拥挤/遮盖。未把这些截图称为网页源数据或真实产品表现。
7. 通过 `view_image` 实际看既有 `interpretation-page-12.png`：四图轴、单位、极端下降与阶梯形状和正文目测近似读法对应。其来源 PDF 的历史基线 SHA 与当前 PDF 相同，映射在 `inherited-evidence.json`。p12无网格/原森林，仍不可称逐点复算。

## 未变显示证据按真实版本承接

候选保留10个原Mermaid源块及8个SVG路径，实际是否逐字保持由最终完整性证据记录。七张m05数值SVG、generate.py、results.json及其20CSV/README/manifest共22输入与历史SHA一致；历史核对记录 `notes/figures/m05/核对记录.md` 载明7张SVG/10个Mermaid/22显示公式在浏览器实际看过。CAPM教学SVG及图源/三点输入来自 `notes/figures/readability-v2/`。本轮不因全文重审而重画相同图，也不把旧观看写成本轮重新观看。

本次在浏览器加载并读了新增/受影响公式与原题。未逐式实看所有950个行内/显示公式，也未打开原生Obsidian。未变范围承接既有同源图文证据，不能扩展为本次重新训练/重新核音/真实高中生试读。

视觉结论：本轮新增/受影响显示已实际核对；未变图文的证据按当前源/hash承接。没有关键新图显示受阻，原生Obsidian与逐声核听仍属未执行边界。


最终纯维护映射：独审实际复核版本 SHA 为 `2a4dd1bd8af1f995093802fbd88e16ccd5120e73999407d5fdadd8b5a59e46d9`；其后仅按 `format-only.diff` 分段及将 `<` 改为等价 LaTeX `\lt`。主代理核差异不改变教学含义，并在 IAB 实看 `visual-format-lasso.png`、`visual-format-natr.png`，950个容器中无mjx-merror。最终 SHA 为 `365c6086f9f03d173b1ecbcfbf9c9a4020fb36c309c9bd10c81e3478e25d44a3`，映射保存在 maintenance-mapping.json。未声称原独审者读过此格式版哈希，不因无语义变化重开全文审查。
