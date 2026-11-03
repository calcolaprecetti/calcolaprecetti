#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlli da eseguire prima di pubblicare, dopo python3 _sorgenti/genera.py.

1. check_site.js: il sito servito in locale come su GitHub Pages, a computer e telefono: errori degli script,
   risorse mancanti, collegamenti interni, larghezza della pagina.
2. test_conta.js: il contatore delle visite non invia importi, date, testi inseriti né cookie.
3. preview.py + check.js: anteprima autosufficiente delle pagine (in una cartella temporanea) e controllo
   di calcoli, casi di verifica e collegamenti.

Uso: python3 _sorgenti/controlla.py   (servono Python 3, Node.js e Playwright con Chromium)
"""
import os
import subprocess
import sys
import tempfile
import time

GEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen')
SITE = os.path.dirname(os.path.dirname(GEN))
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
esito = []

server = subprocess.Popen([sys.executable, '-m', 'http.server', '8765', '--bind', '127.0.0.1', '--directory', SITE],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(1)
    for nome, cmd in (('check_site.js', ['node', os.path.join(GEN, 'check_site.js')]),
                      ('test_conta.js', ['node', os.path.join(GEN, 'test_conta.js')])):
        print('==', nome)
        esito.append((nome, subprocess.run(cmd, env=ENV).returncode))
finally:
    server.terminate()

anteprima = os.path.join(tempfile.gettempdir(), 'anteprima-calcolaprecetti')
print('== preview.py')
esito.append(('preview.py', subprocess.run([sys.executable, os.path.join(GEN, 'preview.py'), anteprima], env=ENV).returncode))
print('== check.js')
esito.append(('check.js', subprocess.run(['node', os.path.join(GEN, 'check.js'), anteprima], env=ENV).returncode))

print()
for nome, rc in esito:
    print('%-14s %s' % (nome, 'ok' if rc == 0 else 'ERRORE (codice %d)' % rc))
sys.exit(0 if all(rc == 0 for _, rc in esito) else 1)
