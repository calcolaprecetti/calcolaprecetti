#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera il sito nella radice del repository.

Ordine: guide (build_guides.py), pagine (build_pages.py), home e interessi moratori (patch_site.py, che alla fine
lancia finalize.py: accessibilità, copia statica per i crawler, sitemap con le date, robots.txt).
Si può rilanciare quante volte serve: se i sorgenti non cambiano, non cambia nessun file pubblicato.

Uso: python3 _sorgenti/genera.py
"""
import os
import subprocess
import sys

GEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen')
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')  # niente cartelle __pycache__ nel repository
for script in ('build_guides.py', 'build_pages.py', 'patch_site.py'):
    print('==', script)
    subprocess.run([sys.executable, os.path.join(GEN, script)], check=True, env=ENV)
print('== sito generato. Prima di pubblicare: python3 _sorgenti/controlla.py')
