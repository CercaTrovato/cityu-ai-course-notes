# M09 v6 实际警告继承核对

候选 `a96bf9a2b4acdee09c4c8cde1b9e9d5f3d05fbdb3a8a041f67dbf77747ec5e47`。v6实际重跑current/strict：C.hard=0、R.hard=0，C.warn=9、R.warn=139。

逐条核了当前code/line/message，全部与v5同条一致；每条R警告的实际完整行也与v5相同。两处§9.5制造状态修正均在这些警告之后，没有以旧数量代替当前运行。每条具体处置理由、上下文、独审依据保留在JSON，不以“未变”代替原有实质核对。

v5警告清单与v4 FAIL均保留历史。这里仅处理可读性启发式和非内容页，不升级法律当前状态。
