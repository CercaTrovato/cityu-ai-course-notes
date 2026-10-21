# -*- coding: utf-8 -*-
"""日常备份已改用 Git/GitHub；仅显式 --create 时生成临时全库归档，不自动删包。"""
import argparse
import datetime
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT.parent / (ROOT.name + '_backups')
SKIP_DIRS = {'.obsidian/plugins', '__pycache__', '__MACOSX', '.git'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--create', action='store_true', help='仅在用户明确要求临时全库归档时使用')
    parser.add_argument('--no-materials', action='store_true', help='排除 course_files_export；仍可能包含其他大文件')
    args = parser.parse_args(argv)
    if not args.create:
        print('日常全库 ZIP 已停用：请按备份与公开发布规则提交、推送并核实 GitHub。')
        print('未创建或删除任何归档。临时归档仅在用户明确要求时传 --create。')
        return 0

    DEST.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    suffix = '-nomat' if args.no_materials else ''
    target = DEST / f'{ROOT.name}-{stamp}{suffix}.zip'
    pending = target.with_suffix('.zip.partial')
    count = 0
    try:
        with zipfile.ZipFile(pending, 'x', zipfile.ZIP_DEFLATED) as archive:
            for directory, subdirs, filenames in os.walk(ROOT):
                relative = Path(directory).relative_to(ROOT).as_posix()
                if any(relative == item or relative.startswith(item + '/') for item in SKIP_DIRS):
                    subdirs[:] = []
                    continue
                if args.no_materials and 'course_files_export' in Path(relative).parts:
                    subdirs[:] = []
                    continue
                for filename in filenames:
                    if filename.endswith('.pyc') or filename.startswith('~$'):
                        continue
                    source = Path(directory) / filename
                    archive.write(source, source.relative_to(ROOT))
                    count += 1
        with zipfile.ZipFile(pending) as archive:
            bad = archive.testzip()
            if bad is not None:
                raise ValueError(f'ZIP CRC 校验失败：{bad}')
        os.replace(pending, target)
    except BaseException:
        pending.unlink(missing_ok=True)
        raise
    print(f'临时归档 {count} 个文件 → {target}（{target.stat().st_size / 1048576:.1f} MB），CRC 通过。')
    print('未自动清理其他归档。归档含个人材料，不能直接作为未经检查的发布包。')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
