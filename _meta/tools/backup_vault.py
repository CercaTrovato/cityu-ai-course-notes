# -*- coding: utf-8 -*-
"""
backup_vault.py — 把整个 vault（不含 .obsidian/plugins、course_files_export 可选）打成带时间戳的 zip，放到 vault 之外的目录，保留最近 N 份。

用法：
    /d/anaconda3/python.exe D:/上课资料/CityU/_meta/tools/backup_vault.py            # 默认：备份到 D:/上课资料/CityU_backups，含课程材料，保留 30 份
    /d/anaconda3/python.exe D:/上课资料/CityU/_meta/tools/backup_vault.py --no-materials   # 不含 course_files_export（约 13 MB）

建议：Windows 任务计划程序每天 1 次 + 每次派 agent 改笔记之前手动跑 1 次。
    schtasks /Create /SC DAILY /ST 03:00 /TN "CityU vault backup" /TR "D:\\anaconda3\\python.exe D:\\上课资料\\CityU\\_meta\\tools\\backup_vault.py"
"""
import os, sys, zipfile, datetime, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DEST = os.path.join(os.path.dirname(ROOT), os.path.basename(ROOT) + '_backups')
KEEP = 30
SKIP_DIRS = {'.obsidian/plugins', '__pycache__', '__MACOSX', '.git'}
no_materials = '--no-materials' in sys.argv

os.makedirs(DEST, exist_ok=True)
name = os.path.join(DEST, '%s-%s%s.zip' % (os.path.basename(ROOT), datetime.datetime.now().strftime('%Y%m%d-%H%M'), '-nomat' if no_materials else ''))
n = 0
with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as z:
    for dp, dns, fns in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).replace('\\', '/')
        if any(rel == s or rel.startswith(s + '/') for s in SKIP_DIRS): dns[:] = []; continue
        if no_materials and 'course_files_export' in rel: dns[:] = []; continue
        for fn in fns:
            if fn.endswith('.pyc'): continue
            p = os.path.join(dp, fn); z.write(p, os.path.relpath(p, ROOT)); n += 1
print('备份 %d 个文件 → %s（%.1f MB）' % (n, name, os.path.getsize(name) / 1048576))
olds = sorted(glob.glob(os.path.join(DEST, '*.zip')), key=os.path.getmtime)
for o in olds[:-KEEP]:
    os.remove(o); print('删除旧备份', os.path.basename(o))
