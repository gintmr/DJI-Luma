#!/usr/bin/env python3
"""Check local links, project-prefix paths, vendored integrity, and privacy boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import hashlib,json,re,zipfile,posixpath
root=Path(__file__).resolve().parents[1]/'docs'
class Page(HTMLParser):
    def __init__(self,text):super().__init__();self.refs=[];self.ids=set();self.scripts=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id'in a:self.ids.add(a['id'])
        for key in ('href','src','poster'):
            if key in a:self.refs.append(a[key])
        if tag=='script':self.scripts.append(a.get('src',''))
        assert tag not in ('iframe','form'), 'No embedded third-party pages or forms expected'
        assert not any(k.startswith('on') for k in a),'Inline event handler'
pages={p.relative_to(root).as_posix():Page(p.read_text())for p in root.glob('*.html')}
checked=0
for prefix in ('/','/DJI-Luma/','/a-different-project/'):
    for name,page in pages.items():
        for ref in page.refs:
            if urlsplit(ref).scheme in ('https','mailto'):continue
            assert not ref.startswith(('/', '//')),'Root-absolute local link: '+ref
            url=urlsplit(urljoin('https://example.github.io'+prefix+name,ref))
            assert url.path.startswith(prefix),'Path escaped project prefix: '+ref
            path=unquote(url.path[len(prefix):]) or 'index.html'
            target=root/path
            assert target.is_file(),'Missing: '+str(target)
            if url.fragment:
                assert path in pages and unquote(url.fragment) in pages[path].ids,'Missing anchor: '+ref
            checked+=1
        assert page.scripts==['./assets/site.js'],'Only project entrypoint allowed'
jsfiles=list(root.rglob('*.js'))
for p in jsfiles:
    text=p.read_text()
    for forbidden in ('fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'document.cookie','supabase','analytics','visitor-card'):
        assert forbidden.lower() not in text.lower(),str(p)+': '+forbidden
assert {p.relative_to(root).as_posix() for p in jsfiles}=={'assets/site.js','ui/nav.js'}
for p in root.rglob('*.css'):
    # No remote font/CDN/import request; comments may mention @import as build documentation.
    assert not re.search(r'url\(\s*[\'"]?(?:https?:|//)',p.read_text())
    assert not re.search(r'^\s*@import\s',p.read_text(),re.M)
manifest=json.loads((root/'ui/provenance.json').read_text())
for name,meta in manifest['files'].items():assert hashlib.sha256((root/'ui'/name).read_bytes()).hexdigest()==meta['sha256'], 'Vendor changed: '+name
release=json.loads((root/'release.json').read_text());apk=root/release['apk'];digest=hashlib.sha256(apk.read_bytes()).hexdigest();assert digest==release['sha256'] and apk.stat().st_size==release['bytes']
assert (root/'downloads/SHA256SUMS.txt').read_text().startswith(digest)
assert digest in (root/'index.html').read_text()
assert not any(p.suffix in ('.jks','.keystore','.bin','.pcap')for p in root.rglob('*'))
assert (root/'.nojekyll').exists()
print(f'PASS: {len(pages)} pages, {checked} local links at three Pages prefixes, hashes, two local scripts, no collection/storage/network APIs.')

# Keep the public brief and kit synchronized with the complete specification.
manual=(root/'workflow/reproduction-manual.md').read_text()
brief=(root/'workflow/agent-brief.md').read_text()
assert manual in brief and len(manual)>15000,'Brief is incomplete'
assert len(re.findall(r'^## ',manual,re.M))==14
assert len(list((root/'assets/screens').glob('*.svg')))==18
with zipfile.ZipFile(root/'workflow/reproduction-kit.zip')as kit:
    assert kit.read('workflow/reproduction-manual.md').decode()==manual
    assert kit.read('workflow/agent-brief.md').decode()==brief
    for image in re.findall(r'!\[[^]]*\]\(([^)]+)\)',manual):
        assert posixpath.normpath(posixpath.join('workflow',image)) in kit.namelist(),'Broken kit image: '+image
    captures=json.loads((root/'assets/app'/release['version']/'provenance.json').read_text())
    assert captures['app_version']==release['version'] and len(captures['files'])==32
    for name,meta in captures['files'].items():
        relative='assets/app/'+release['version']+'/'+name
        assert hashlib.sha256((root/relative).read_bytes()).hexdigest()==meta['sha256']
        assert kit.read(relative)==(root/relative).read_bytes()
        assert 'history' not in name,'Raw event screenshots are not public assets'
for name in pages:
    source=(root/name).read_text()
    assert 'Built with agents.' in source
    assert 'data-project-repository="https://github.com/gintmr/DJI-Luma" href="https://github.com/gintmr/DJI-Luma"' in source
    assert 'aria-disabled="true"' not in source
    for removed in ('Built by','https://gintmr.github.io/','这个网站会记录','无访问收集'):
        assert removed not in source,'Removed copy returned: '+removed
    assert ('留光' in source or name.endswith('-en.html')) and 'Luma' in source and release['version'] in source
    assert '间录' not in source and 'jianlu-0.6' not in source
print('PASS: complete handbook and brief, 18 references, zip image paths, concise footer and active project link.')
print('PASS: Luma '+release['version']+' branding, APK, 32 current native renders, source hashes and kit assets.')

video=json.loads((root/'assets/video/manifest.json').read_text())
assert (video['width'],video['height'],video['fps'],video['duration_seconds'])==(3840,2160,30,22)
for name,meta in video['files'].items():
    asset=root/'assets/video'/name
    assert asset.stat().st_size==meta['bytes'] and hashlib.sha256(asset.read_bytes()).hexdigest()==meta['sha256']
assert '<video controls playsinline preload="none"' in (root/'index.html').read_text()
print('PASS: 4K video and poster hashes, native player, project-relative media paths.')

# Language pages keep the same structure and select their own video and guide.
for lang,suffix in [('zh',''),('en','-en')]:
    home=(root/('index'+suffix+'.html')).read_text()
    assert re.findall(r'<section[^>]* id="([^"]+)"',home)==['animation','interface','workflow','download','faq']
    assert 'meta-strip' not in home and 'id="approach"' not in home and 'id="features"' not in home
    movie=video['languages'][lang]
    assert './assets/video/'+movie['video'] in home and './assets/video/'+movie['poster'] in home
    assert './workflow'+suffix+'.html' in home
    other='' if suffix else '-en'
    assert 'class="language-switch" href="./index'+other+'.html"' in home
    guide=(root/('workflow'+suffix+'.html')).read_text()
    assert 'class="language-switch" href="./workflow'+other+'.html"' in guide
    m=(root/('workflow/reproduction-manual'+suffix+'.md')).read_text()
    b=(root/('workflow/agent-brief'+suffix+'.md')).read_text()
    assert m in b and len(re.findall(r'^## ',m,re.M))==14
    with zipfile.ZipFile(root/('workflow/reproduction-kit'+suffix+'.zip')) as kit:
        assert kit.read('workflow/reproduction-manual'+suffix+'.md').decode()==m
        assert kit.read('workflow/agent-brief'+suffix+'.md').decode()==b
        for image in re.findall(r'!\[[^]]*\]\(([^)]+)\)',m):
            assert posixpath.normpath(posixpath.join('workflow',image)) in kit.namelist()
assert '支持中英双语</h2>' in (root/'index.html').read_text()
print('PASS: compact section order, bilingual home/guide/brief/kit, matching language-specific video and poster.')
