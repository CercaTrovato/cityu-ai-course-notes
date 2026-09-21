# -*- coding: utf-8 -*-
"""sync_damage_check.py — 检出被 Remotely Save 同步"截成半截"的文件。

背景（2026-09-22 排查结论）：Obsidian 的 Remotely Save 经代理上传 >100 KB 文件时可能中途停滞，
dufs 把半截直接写在服务器目标路径，下一轮同步按"取较新"把半截拉回本地覆盖。被覆盖的文件有两个特征：
  ① 结构不完整（PDF 无 %%EOF、PNG 无 IEND、HTML 无 </html>、CSV/MD 末尾无换行、JSON 解析失败、ZIP 损坏）；
  ② mtime 的纳秒部分全为 0（Remotely Save 按服务器秒级时间回写 mtime；本机正常写入的文件纳秒不为 0）。
  注意 ② 有误报：从 zip 解压出来的文件也是秒级时间戳；所以 ② 只作线索，① 才是判定。

用法：python _meta/tools/sync_damage_check.py [vault 根目录，默认本仓库]
退出码：发现可疑文件 → 1；否则 0。收工时和 integrity_check.py verify 一起跑。
"""
import json, os, sys, zipfile

SKIP_DIRS = {'.git', '.obsidian', '__pycache__', '__MACOSX', '.claude'}
AUDIO = ('.mp3', '.wav', '.m4a', '.flac')
KNOWN_NO_NEWLINE = {'IS6400_Business_Data_Analytics/course_files_export/Airbnb.csv'}  # 原始文件本就无末尾换行，已核对末行完整


def check_structure(p, size):
    ext = p.lower().rsplit('.', 1)[-1] if '.' in os.path.basename(p) else ''
    with open(p, 'rb') as f:
        head = f.read(8); f.seek(max(0, size - 2048)); tail = f.read()
    if ext == 'pdf':
        return None if head.startswith(b'%PDF') and b'%%EOF' in tail else 'PDF 缺 %%EOF'
    if ext == 'png':
        return None if tail.rstrip().endswith(b'IEND\xaeB`\x82') else 'PNG 缺 IEND'
    if ext in ('docx', 'xlsx', 'pptx', 'zip'):
        try:
            return None if zipfile.ZipFile(p).testzip() is None else 'ZIP 内有坏块'
        except Exception as e:
            return f'ZIP 打不开：{type(e).__name__}'
    if ext in ('json', 'ipynb'):
        try:
            json.load(open(p, encoding='utf-8')); return None
        except Exception as e:
            return f'JSON 解析失败：{str(e)[:50]}'
    if ext in ('html', 'htm'):
        return None if b'</html>' in tail.lower() else 'HTML 缺 </html>'
    if ext in ('csv', 'md', 'txt', 'py'):
        return None if tail.endswith(b'\n') else '末尾无换行'
    return None


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..'))
    bad, pulled = [], []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for fn in files:
            p = os.path.join(d, fn); rel = os.path.relpath(p, root).replace('\\', '/')
            if rel.lower().endswith(AUDIO): continue
            st = os.stat(p)
            if st.st_size == 0: continue
            try:
                why = check_structure(p, st.st_size)
            except Exception as e:
                why = f'读取失败：{type(e).__name__}'
            if why and rel not in KNOWN_NO_NEWLINE:
                bad.append((st.st_size, why, rel))
            if st.st_mtime_ns % 1_000_000_000 == 0 and st.st_size > 0:
                pulled.append((st.st_size, rel))
    print(f'=== 结构不完整（疑似截断）{len(bad)} 个 ===')
    for s, why, rel in sorted(bad, key=lambda x: x[2]):
        print(f'{s:>10}  {why:<24} {rel}')
    print(f'\n=== mtime 纳秒为 0（曾被同步从服务器拉回覆盖）{len(pulled)} 个——不一定坏，但要核对 ===')
    for s, rel in sorted(pulled, key=lambda x: x[1]):
        print(f'{s:>10}  {rel}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
