# 从数据到比较表

一行是customer_unique_id与snapshot_date共同确定的一位客户快照。历史窗口是预测日前六个自然月；合格事件为已批准且商品金额大于零的订单。商品明细先按订单汇总，再接客户并聚合；最终导出的订单状态不用于反推过去资格。未来90天是否出现同口径订单构成y，结束日不含在内。

核心八字段是R、F、M、平均商品明细行数、运费/(商品金额+运费)、近30天订单数、近30天商品金额、州。数值log1p及标准化、州one-hot都在训练数据学习；R3另有中位数填补及缺失指示，类别用众数填补且忽略未知类别。

新增G1按2号已交公式：delivery_pending_n=F-delivered_known_n；delivery_days_log=log1p(max(delivery_days_mean,0))；另加配送均值缺失指示。G2为评价均值、review_known_n/F和评价均值缺失指示。新列只做十月中位数填补和标准化，配送对数列不再log、星级不取log。实际拟合的填补/均值/标准差已保存，不冒称与未提供的成员私表字节完全相同。

配送使用预测日前有效实际送达；时长为批准到送达天数。迟到比例只用有效预计日期与实际日期均可比较的订单；预计日期的历史版本没有修改日志证明。评价先截断答复时间，再每单选最新有效1–5分，低分为<=2；缺评价不等于差评。

类别加权让少数复购案例在训练损失中更重要，不复制/删除客户。七方法筛选是3家族的普通/加权6配置加最近购买规则；F0/G1/G2仍是固定加权LR。每个比较保持相同客户、标签、名额、分数排序和ID并列处理。

对应数据：

|snapshot|history_start|label_end_exclusive|customers|positive_customers|role|
|---|---|---|---|---|---|
|2017-10-01|2017-04-01|2017-12-30|21160|211|ranking train|
|2018-01-01|2017-07-01|2018-04-01|29368|230|candidate comparison, not a blind test|
|2018-04-01|2017-10-01|2018-06-30|37813|299|fixed model test/check, no refit|
|2018-05-01|2017-11-01|2018-07-30|40025|284|fixed model test/check, no refit|
|2018-06-01|2017-12-01|2018-08-30|39804|271|fixed model test/check, no refit|

|snapshot|N|positive|negative|positive_rate|
|---|---|---|---|---|
|2017-10-01|21160|211|20949|0.009972|
|2018-01-01|29368|230|29138|0.007832|

[字段时点/限制](data/feature-availability.csv) · [1号原时点字典](data/source-field-time-audit.csv) · [冻结141输入列清单及类型](data/extension-141-field-dictionary.csv) · [原10项服务字段定义](data/service-field-definitions.csv) · [参数](data/model-parameters.csv) · [45行run身份](data/experiment-registry.csv)。标签、未来商品金额和订单数不作为预测输入。


141列清单来自原冻结data-manifest的raw_fields/categorical_fields，逐项列名和类型可核；它不是凭10项服务字段表推定的完整公式字典。原10项服务字段定义单独保留，其余字段构造查原源代码及冻结记录，不在本包编造未提供的公式。
