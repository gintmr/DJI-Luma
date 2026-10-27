#!/usr/bin/env python3
"""Copy the audited static UI subset. No package installation or network access."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys
if len(sys.argv)!=2:raise SystemExit('Usage: python3 scripts/sync-ui.py /path/to/gintmr-ui')
source = Path(sys.argv[1]).expanduser()
target = Path(__file__).resolve().parents[1] / 'docs/ui'
files = {'gintmr-ui.css':'dist/gintmr-ui.css', 'nav.js':'src/primitives/nav.js', 'LICENSE':'LICENSE'}
for name in files.values():
    if not (source/name).is_file():
        raise SystemExit('Missing framework file: '+str(source/name))
# Keep the navigation-only selection fail-closed if an upstream update adds data collection.
nav = (source/'src/primitives/nav.js').read_text()
for forbidden in ('fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'document.cookie', 'visitor', 'supabase'):
    if forbidden.lower() in nav.lower():
        raise SystemExit('Review upstream nav.js before syncing: '+forbidden)
target.mkdir(parents=True,exist_ok=True)
for name,origin in files.items():shutil.copyfile(source/origin,target/name)
manifest = {'repository':'https://github.com/gintmr/gintmr-ui','commit':subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip(),'version':(source/'dist/VERSION').read_text().strip(),'files':{name:{'source':origin,'sha256':hashlib.sha256((source/origin).read_bytes()).hexdigest()}for name,origin in files.items()},'selection':'dist CSS + standalone navigation primitive; full JS bundle intentionally not included.'}
(target/'provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Synced static CSS and navigation only. Commit docs/ui after checking both pages.')
