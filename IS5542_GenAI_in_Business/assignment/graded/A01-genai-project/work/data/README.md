# 数据来源说明

## 美团 INFORMS TSL 研究挑战数据

- 来源：<https://github.com/meituan/Meituan-INFORMS-TSL-Research-Challenge>，文件 `all_waybill_info_meituan_0322.csv.zip`（SHA-256 `38b51431a12dd7e73deb4fc750b1275067fbc29cfce2c4b4492339738c988ce2`），2026-10-31 下载。
- 许可：CC BY-NC 4.0，仅限非商业用途，未经许可不得向第三方分发。因此原始数据只保存在库外的本地目录，不放进本仓库。
- 致谢（用于 slides 和报告）：This research was supported by data provided by Meituan. / 本研究由美团提供数据支持。

## 本目录文件

- `meituan_lateness_stats.py`：读取本地 zip，按订单计算“实际送达时间减承诺送达时间”，只输出汇总统计。
- `meituan_lateness_stats.json`：上面脚本的输出，只含比例、分位数和按小时汇总的数据，没有逐单记录。

运行方式（在 `work/app` 的环境里）：

```bash
uv run --project ../app python -I meituan_lateness_stats.py <本地 zip 路径> meituan_lateness_stats.json
```
