# -*- coding: utf-8 -*-
"""把 _meta/tools/git-hooks/ 里的钩子装进 .git/hooks/（.git/hooks 不进版本库，克隆后要跑一次）。

    PYTHONIOENCODING=utf-8 /d/anaconda3/python.exe _meta/tools/install_hooks.py
"""
import os, shutil, stat, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
src = os.path.join(HERE, 'git-hooks'); dst = os.path.join(ROOT, '.git', 'hooks')
if not os.path.isdir(dst): raise SystemExit('不是 git 仓库或找不到 .git/hooks')
for f in os.listdir(src):
    s, d = os.path.join(src, f), os.path.join(dst, f)
    shutil.copyfile(s, d); os.chmod(d, os.stat(d).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print('✓ 安装', f)
# 自检：带 Co-Authored-By 的信息必须被拒
test = os.path.join(dst, '_t.txt'); open(test, 'w', encoding='utf-8').write('x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n')
r = subprocess.run(['sh', os.path.join(dst, 'commit-msg'), test], capture_output=True)
os.remove(test); print('自检：', '钩子生效（AI 署名被拒）' if r.returncode != 0 else '✗ 钩子未生效')
