# 可复跑的报告证据，不默认重新训练

Python环境见requirements-report.txt和environment.json。将命令中的<pack>和<repo>替换为本包/仓库绝对路径，不要把尖括号原样输入。以下命令在任意工作目录执行，显式指定包目录与输出目录；输出选在本机scratch或另一个隔离目录，不覆盖原数据/模型。

```powershell
D:/anaconda3/python.exe -X utf8 <pack>/source/verify_report.py --pack <pack> --output E:/app-data/codex/scratchpad/is6400-report-replay --render
```

它核聚合算术、全部10图文件指纹，并从复制的聚合CSV重新画图，比较SVG/PDF字节。它没有fit调用，不读取逐客户数据。没有必要为查看报告重新训练模型。

本机授权私有目录另保存本批F0/G1/G2权重、January输入、分数；在上命令加`--private-dir <private-dir>`可加载3个模型predict_proba回放，与保存分数、独立pandas排序和AP/AUC核对。未指定时明确只完成公开聚合/图的核验，不假称完成私有模型复算。

R3成员元数据可独立再生：

```powershell
python <repo>/research/team-round3-20261112/members/role03/run_round3.py --metadata-only --output-dir <isolated-output>
python <repo>/research/team-round3-20261112/members/role03/run_group_models.py --metadata-only --output-dir <isolated-output>
```

默认source-dir为脚本目录，读取同目录保存的聚合CSV。元数据区分保存结果可用与这次未训练，记录CV条件及再生环境，不倒填原历史训练环境。两次重复输出已实际比较一致。原训练/评分函数AST保持。

要完整重复新增的3配置训练，需用户授权输入及独立输出位置，参考local-inputs.example.json填绝对路径；明确传`--fit`：

```powershell
python <pack>/source/run_fixed_features.py --repo <repo> --config <local-inputs.json> --output <new-isolated-output> --fit
```

完整训练后，运行python <pack>/source/build_replay_inputs.py --config <local-inputs.json>只读重建January私有回放输入，然后可用前述verify_report的--private-dir检查。该适配器没有fit调用，并拒绝覆盖内容不一致的已有输入。

不传--fit会拒绝训练；已有计划目录会拒绝覆盖。输入SHA和计划先写，再只解析十月/一月，输出模型/逐客户分数只进private_output。原始ZIP和数据不进入公开包；旧全部模型的私有依赖不因新wrapper而自动公开。此训练步骤不是默认报告检查。
