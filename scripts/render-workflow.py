#!/usr/bin/env python3
"""Render the authored handbook into static HTML and a self-contained Agent brief."""
from pathlib import Path
import html,re,zipfile,sys
root=Path(__file__).resolve().parents[1]; site=root/'docs'
en='--lang=en' in sys.argv
suffix='-en' if en else ''
manual_name='reproduction-manual'+suffix+'.md'
brief_name='agent-brief'+suffix+'.md'
kit_name='reproduction-kit'+suffix+'.zip'
page_name='workflow'+suffix+'.html'
manual=(site/'workflow'/manual_name).read_text()
brief='''# Agent 复现任务包

请读取下面的完整规格和随附页面参考图，在我的电脑与已授权的安卓手机上完成实现、安装、调试和验收。先填写设备信息，按第 10 节的阶段推进；每阶段使用第 12、13 节的检查留下证据。

项目仓库链接：https://github.com/gintmr/DJI-Luma
UI 图：随附的 assets/screens/ 为结构图；assets/app/0.7.1/ 为中英文明暗实际界面。
按以下规格实现全部页面、控制链路与验收流程。

'''+manual
if en:brief='''# Agent reproduction brief

Read the complete specification and attached screen references. Implement, install, debug and verify the app on my computer and authorized Android phone. Fill in device details first, follow chapter 10, and retain evidence using chapters 12–13.

Project repository: https://github.com/gintmr/DJI-Luma
References: assets/screens/ contains structure diagrams; assets/app/0.7.1/ contains native Chinese/English light/dark UI renders.

'''+manual
(site/'workflow'/brief_name).write_text(brief)
old=(site/page_name).read_text()
head=old.split('<body>')[0]+'<body>'
head=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="完整复现相机定时拍摄 App：页面规格、技术栈、状态机、ADB 真机操作、阶段 Prompt、排错记录和验收表。">',head)
if en:head=head.replace('完整复现相机定时拍摄 App：页面规格、技术栈、状态机、ADB 真机操作、阶段 Prompt、排错记录和验收表。','Reproduce Luma: screen specifications, protocols, scheduling, ADB operation, staged prompts, troubleshooting and acceptance checks.')
header=old[old.index('<header class="gintmr_ui-header'):old.index('</header>')+9]
footer='''<div class="wrap"><footer class="project-footer"><span>Built with agents.</span><a class="project-repo" data-project-repository="https://github.com/gintmr/DJI-Luma" href="https://github.com/gintmr/DJI-Luma" aria-label="项目 GitHub 仓库">GitHub ↗</a></footer></div>'''
if en:footer=footer.replace('项目 GitHub 仓库','Project GitHub repository')
ids=['brief','pages','design','stack','prepare','device-debug','ble','scheduler','wifi','stages','troubleshooting','tests','acceptance','first-run']
def inline(s):
    # Protect inline code before processing Markdown links.
    codes=[]
    def code(m):codes.append('<code>'+html.escape(m[1])+'</code>');return f'@@CODE{len(codes)-1}@@'
    s=re.sub(r'`([^`]+)`',code,s);s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<a href="'+html.escape(m[2],quote=True)+'">'+m[1]+'</a>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    for i,c in enumerate(codes):s=s.replace(f'@@CODE{i}@@',c)
    return s
lines=manual.splitlines();out=[];toc=[];i=0;section=False;number=0
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('# '):i+=1;continue
    if line.startswith('## '):
        if section:out.append('</section>')
        title=line[3:];anchor=ids[number];number+=1;toc.append((anchor,title));out.append(f'<section id="{anchor}"><h2>{inline(title)}</h2>');section=True;i+=1;continue
    if line.startswith('### '):out.append('<h3>'+inline(line[4:])+'</h3>');i+=1;continue
    if line.startswith('```'):
        code=[];i+=1
        while i<len(lines)and not lines[i].startswith('```'):code.append(lines[i]);i+=1
        out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines)and lines[i].startswith('|'):
            cells=[c.strip()for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',c)for c in cells):rows.append(cells)
            i+=1
        table='<div class="table-scroll"><table class="doc-table"><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>'for c in rows[0])+'</tr></thead><tbody>'
        table+=''.join('<tr>'+''.join('<td>'+inline(c)+'</td>'for c in row)+'</tr>'for row in rows[1:])+'</tbody></table></div>'
        out.append(table);continue
    if line.startswith('!['):
        images=[]
        while i<len(lines)and lines[i].startswith('!['):
            m=re.fullmatch(r'!\[([^]]+)\]\(([^)]+)\)',lines[i]);alt,path=m.groups();path='./'+path.removeprefix('../');images.append(f'<figure><a href="{path}"><img src="{path}" alt="{html.escape(alt)}" loading="lazy"></a><figcaption>{html.escape(alt)}</figcaption></figure>');i+=1
        out.append('<div class="screen-gallery">'+''.join(images)+'</div>');continue
    if re.match(r'^(- |\d+\. )',line):
        ordered=not line.startswith('- ');tag='ol'if ordered else'ul';items=[]
        while i<len(lines)and bool(re.match(r'^\d+\. ',lines[i]))==ordered and re.match(r'^(- |\d+\. )',lines[i]):items.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',lines[i]))+'</li>');i+=1
        out.append('<'+tag+'>'+''.join(items)+'</'+tag+'>');continue
    paras=[]
    while i<len(lines)and lines[i].strip()and not re.match(r'^(#|```|\||!\[|- |\d+\. )',lines[i]):paras.append(lines[i]);i+=1
    out.append('<p>'+inline(' '.join(paras))+'</p>')
if section:out.append('</section>')
intro='''<main class="wrap handbook" id="main"><div class="handbook-intro"><a class="text-link" href="./index.html">← 项目首页</a><p class="eyebrow">Build · debug · reproduce</p><h1>完整复现手册</h1><p>四个主页面、三个取景器标签与全屏状态。从环境准备到真实相机验收，按步骤交给 Agent 执行。</p><div class="actions"><a class="btn primary" href="./workflow/reproduction-kit.zip" download>下载完整复现包 ↓</a><a class="btn" href="./workflow/agent-brief.md" download>下载完整 Agent 简报</a><button class="btn" type="button" data-copy="agent-prompt">复制完整简报</button></div><span class="status" id="copy-status" role="status"></span><details class="kit-contents"><summary>复现包内容</summary><p>完整手册、完整 Agent 简报、18 张明暗主题页面结构图、0.7.1 中英文明暗实际界面、设计与文件索引。技术路线、调试步骤和排错案例均在手册中。</p></details></div>'''
if en:intro='''<main class="wrap handbook" id="main"><div class="handbook-intro"><a class="text-link" href="./index-en.html">← Project home</a><p class="eyebrow">Build · debug · reproduce</p><h1>Complete reproduction guide</h1><p>Four main screens, three viewfinder tabs and fullscreen. Follow the steps from environment setup to real-camera verification with your Agent.</p><div class="actions"><a class="btn primary" href="./workflow/reproduction-kit-en.zip" download>Download full kit ↓</a><a class="btn" href="./workflow/agent-brief-en.md" download>Download full Agent brief</a><button class="btn" type="button" data-copy="agent-prompt">Copy full brief</button></div><span class="status" id="copy-status" role="status"></span><details class="kit-contents"><summary>Kit contents</summary><p>The complete guide and Agent brief, 18 light/dark structure diagrams, native 0.7.1 bilingual UI renders and a file index. The guide includes protocols, device debugging and troubleshooting.</p></details></div>'''
nav='<aside class="manual-toc" aria-label="手册目录"><span>CONTENTS</span><nav>'+''.join(f'<a href="#{anchor}">{html.escape(title)}</a>'for anchor,title in toc)+'</nav></aside>'
if en:nav=nav.replace('手册目录','Guide contents')
body='<div class="manual-layout">'+nav+'<article class="doc manual-body">'+''.join(out)+'</article></div><pre id="agent-prompt" class="full-brief" hidden tabindex="0">'+html.escape(brief)+'</pre></main>'
(site/page_name).write_text(head+'<a class="gintmr_ui-skip-link" href="#main">'+('Skip to content' if en else '跳至正文')+'</a>'+header+intro+body+footer+'</body></html>\n')
index='''# 复现包索引

1. 先阅读 workflow/reproduction-manual.md。
2. 把 workflow/agent-brief.md 全文交给 Agent，并填写设备信息。
3. assets/screens/ 为 18 张按源码绘制的页面结构图（9 种状态 × 明暗主题）；图片明确标注示例状态。
4. assets/app/0.7.1/ 为留光 0.7.1 中英 / 明暗实际界面参考；活动记录页以示例结构图提供。
5. App 中文名为留光，英文 Luma；网站下载包与手册版本为 0.7.1。
6. 仓库链接由项目所有者后续填写；本包未包含相机身份、Wi-Fi 密码、私人取景或完整安卓源码。
'''
if en:index='''# Reproduction kit

Read workflow/reproduction-manual-en.md, then give workflow/agent-brief-en.md and your device details to your Agent. assets/screens/ contains 18 illustrative light/dark diagrams with Chinese labels. assets/app/0.7.1/ contains native bilingual light/dark UI renders. Brand: Luma / 留光, version 0.7.1. The project repository will be supplied later. Camera identities, Wi-Fi passwords, private footage and full Android source are not included.
'''
index_name='KIT-README'+suffix+'.md'
(site/'workflow'/index_name).write_text(index)
with zipfile.ZipFile(site/'workflow'/kit_name,'w',zipfile.ZIP_DEFLATED)as z:
    for name in (manual_name,brief_name):z.write(site/'workflow'/name,'workflow/'+name)
    z.write(site/'workflow'/index_name,'KIT-README.md')
    for p in sorted((site/'assets/screens').glob('*.svg')):z.write(p,'assets/screens/'+p.name)
    for p in sorted((site/'assets/app/0.7.1').glob('*.png')):z.write(p,'assets/app/0.7.1/'+p.name)
    z.write(site/'assets/app/0.7.1/provenance.json','assets/app/0.7.1/provenance.json')
print('Rendered',number,'chapters;',len(manual),'characters; kit contains',len(list((site/'assets/screens').glob('*.svg'))),'references.')
