import os, sys

files = ['login.html', 'finanzas.html']
subs = {
    '__SUPA_URL__':  os.environ['SUPA_URL'],
    '__SUPA_KEY__':  os.environ['SUPA_KEY'],
    '__GATE_HASH__': os.environ['GATE_HASH'],
}

for fname in files:
    with open(fname, encoding='utf-8') as f:
        content = f.read()
    for k, v in subs.items():
        if k not in content:
            print(f'WARN: {k} no encontrado en {fname}')
            sys.exit(1)
        content = content.replace(k, v)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}')
