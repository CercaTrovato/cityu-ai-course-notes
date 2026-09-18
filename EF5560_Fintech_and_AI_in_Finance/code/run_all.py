"""
run_all.py · 按编号顺序跑全部分析脚本
=====================================
用法：cd code && /d/python/python run_all.py
每个脚本独立运行（subprocess），一个失败不影响其余；最后汇总。
"""
import subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
scripts = sorted(p for p in ROOT.glob("L*/[0-9][0-9]_*.py"))
results = []
for s in scripts:
    print(f"\n{'='*70}\n▶ {s.relative_to(ROOT)}\n{'='*70}")
    r = subprocess.run([sys.executable, str(s)], cwd=ROOT, env=env)
    results.append((s.relative_to(ROOT), r.returncode))

print(f"\n{'='*70}\n汇总\n{'='*70}")
for name, code in results:
    print(f"{'✅' if code == 0 else '❌'} {name}")
sys.exit(0 if all(c == 0 for _, c in results) else 1)
