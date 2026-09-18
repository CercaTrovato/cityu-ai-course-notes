# -*- coding: utf-8 -*-
"""复算 IS5542 Lecture 3 p.76「Cost per accepted outcome」的数字，并做两个敏感性例子（笔记 M03 §2.10.5）。

    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe IS5542_GenAI_in_Business/code/m03_cost_per_accepted.py

公式：C_acc = (n * c + H) / (n * a)
    n = 尝试次数，c = 每次尝试的模型/工具变动成本，H = 人工审核与支持总费用，a = 接受率
讲义数字（虚构试点）：n = 1000，c = HK$1.20，H = HK$800，接受 800 个 → a = 0.80 → C_acc = HK$2.50
"""

def cost_per_accepted(n, c, H, a):
    return (n * c + H) / (n * a)

n, c, H = 1000, 1.20, 800
model_tool = n * c                      # 1200
total = model_tool + H                  # 2000
accepted = 800
a = accepted / n                        # 0.80
C = cost_per_accepted(n, c, H, a)
print(f'模型/工具费 = {n} × {c:.2f} = {model_tool:.0f}')
print(f'总变动成本 = {model_tool:.0f} + {H} = {total:.0f}')
print(f'被接受 = {n} × {a:.2f} = {n * a:.0f}')
print(f'每接受结果成本 = {total:.0f} ÷ {n * a:.0f} = {C:.2f}')
assert abs(model_tool - 1200) < 1e-9 and abs(total - 2000) < 1e-9 and abs(C - 2.50) < 1e-9, '与讲义 p.76 不一致'

# 敏感性：接受率 0.80 → 0.50（人工不变）
C50 = cost_per_accepted(n, c, H, 0.50)
print(f'接受率 0.50 时 = {total:.0f} ÷ {n * 0.5:.0f} = {C50:.2f}（涨 {(C50 / C - 1) * 100:.0f}%）')
assert abs(C50 - 4.00) < 1e-9

# 边界：接受率 → 1 时 C = c + H/n
C1 = cost_per_accepted(n, c, H, 1.0)
print(f'接受率 1.00 时 = {C1:.2f}（= c + H/n = {c + H / n:.2f}）')
assert abs(C1 - (c + H / n)) < 1e-9
print('与讲义 p.76 一致')
