# -*- coding: utf-8 -*-
"""
safe_write.py — 原子写文件 + 写后自检。所有改笔记的脚本必须用它，不许再用 open(path, 'w').write(...)。

为什么：open('w') 会先把文件清空再逐步写入；期间任何读者（Remotely Save 同步、Obsidian 重载、另一个 agent）
都可能拿到半截文件，同步插件还会把半截版当"更新"传回来覆盖完整版——2026-09-16/17 三篇笔记就是这么被截断的。

用法（脚本里）：
    import sys; sys.path.insert(0, 'D:/上课资料/CityU/_meta/tools'); from safe_write import atomic_write
    atomic_write(path, new_text)                      # 默认要求新内容 ≥ 旧内容的 70%，否则拒绝写并抛错
    atomic_write(path, new_text, min_ratio=0.0)       # 明确允许大幅缩短（例如整篇重写）时才这样传

命令行：
    python safe_write.py --check <文件>               # 只做自检：utf-8 可解码、结尾完整
"""
import os, io, sys, tempfile

def _tail_ok(text):
    """笔记末尾应是完整的一行（不是半个字、半个表格行）。"""
    if not text: return False
    last = text.rstrip('\n').split('\n')[-1]
    return not (last.startswith('|') and not last.rstrip().endswith('|'))

def atomic_write(path, text, min_ratio=0.7, encoding='utf-8'):
    """把 text 原子地写到 path：先写同目录临时文件，fsync，再 os.replace。
    写前检查：与旧文件相比不得缩短超过 (1 - min_ratio)；写后回读校验字节数一致。"""
    if not isinstance(text, str): raise TypeError('text 必须是 str')
    data = text.encode(encoding)
    if os.path.exists(path):
        old = os.path.getsize(path)
        if old > 0 and len(data) < old * min_ratio:
            raise ValueError('拒绝写入：新内容 %d 字节 < 旧文件 %d 字节的 %d%%。若确实要大幅缩短，显式传 min_ratio=0.0' % (len(data), old, min_ratio * 100))
    if not _tail_ok(text):
        raise ValueError('拒绝写入：内容以不完整的表格行结尾，疑似截断')
    d = os.path.dirname(os.path.abspath(path)) or '.'
    fd, tmp = tempfile.mkstemp(prefix='.sw_', suffix='.tmp', dir=d)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try: os.remove(tmp)
            except OSError: pass
    back = os.path.getsize(path)
    if back != len(data):
        raise IOError('写后校验失败：磁盘 %d 字节 ≠ 内容 %d 字节' % (back, len(data)))
    return back

def check(path):
    b = open(path, 'rb').read()
    try: t = b.decode('utf-8')
    except UnicodeDecodeError as e: return False, 'utf-8 在字节 %d 处断裂（典型的写到一半被截断）' % e.start
    if not _tail_ok(t): return False, '结尾是不完整的表格行'
    return True, '%d 字节，%d 行' % (len(b), t.count('\n') + 1)

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--check':
        ok, msg = check(sys.argv[2]); print(('OK ' if ok else 'BAD ') + msg); sys.exit(0 if ok else 1)
    print(__doc__)
