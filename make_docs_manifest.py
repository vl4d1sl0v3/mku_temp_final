# make_docs_manifest.py (обновлён под новую структуру)
import json, os, sys

ROOT = os.path.join('files', 'docs_list')  # новая корневая папка
SKIP_NAMES = {'.DS_Store'}
SKIP_PREFIXES = ('~$',)

def walk(abs_dir, rel_dir):
    out = {}
    for name in sorted(os.listdir(abs_dir), key=lambda s: s.lower()):
        if name in SKIP_NAMES or any(name.startswith(p) for p in SKIP_PREFIXES):
            continue
        ap = os.path.join(abs_dir, name)
        rp = os.path.join(rel_dir, name) if rel_dir else name
        if os.path.isdir(ap):
            out[name] = walk(ap, rp)
        else:
            out[name] = rp.replace('\\','/')
    return out

def build_manifest():
    if not os.path.isdir(ROOT):
        print(f'Не найден каталог: {os.path.abspath(ROOT)}', file=sys.stderr)
        sys.exit(1)
    manifest = {}
    for top in sorted(os.listdir(ROOT), key=lambda s: s.lower()):
        if top in SKIP_NAMES or any(top.startswith(p) for p in SKIP_PREFIXES):
            continue
        ap = os.path.join(ROOT, top)
        if os.path.isdir(ap):
            manifest[top] = walk(ap, top)
    return manifest

if __name__ == '__main__':
    data = build_manifest()
    with open('docs-manifest.json','w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Готово: docs-manifest.json')
