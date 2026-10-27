from pathlib import Path
from html import escape
p=Path(__file__).resolve().parents[1]/'docs/assets/screens';p.mkdir(parents=True,exist_ok=True)
screens={
'shooting':('拍摄',['Action 4 · 未连接','搜索相机       连接上次','已完成 0 段    下次 —    电量 —','拍摄计划','日常记录    更密集    ✓ 快速测试','间隔 ✎       片段 ✎       时长 ✎','30 秒          5 秒           3 分','每 30 秒 / 5 秒 / 约 6 段','试录 10 秒       停止录像','开始拍摄']),
'camera':('相机',['拍摄模式','✓ 普通视频             拍照','开始手动录像','拍摄信息','模式                         视频','规格            4K 16:9 / 30 fps','增稳                  RockSteady','剩余空间                相机值','本次照片                     0 张','打开取景器 ↗']),
'history':('活动记录',['最近事件                       复制','12:00:00 开始连接','12:00:01 配对已确认','12:00:02 状态：待机','12:00:10 请求开始录像','12:00:11 相机确认开始','12:00:21 请求停止录像','12:00:22 相机确认停止','示例日志 · 不含配对码或设备地址','清空记录']),
'settings':('设置',['语言','跟随系统       ✓ 中文       English','外观','跟随系统       浅色         ✓ 深色','后台运行','电池设置 ↗','设备                         断开相机','实验室                  诊断选项 +','留光 · Luma                    0.7','第三方许可']),
'live':('取景器',['蓝牙 已连接 / Wi-Fi 已连接','画面 ✓       参数       相册','@preview','LIVE · 1280 × 720 · 16:9','全屏      1.0×      构图      参考帧','双指缩放 / 拖动 / 双击','构图：关闭、三分线、十字、2.39:1','参考帧：内存叠加，点按清除']),
'live-4-3':('取景器 · 4:3',['蓝牙 已连接 / Wi-Fi 已连接','画面 ✓       参数       相册','@preview43','LIVE · 1280 × 720 · 4:3','全屏      1.0×      构图      参考帧','显示比例来自相机当前拍摄格式']),
'parameters':('取景器',['蓝牙 已连接 / Wi-Fi 已连接','画面       参数 ✓       相册','拍摄参数','视频格式           4K 16:9 / 30 fps','曝光模式                         自动','ISO                              自动','快门                      当前模式值','白平衡                           自动','曝光补偿                      0.0 EV','视角                             标准','刷新参数']),
'album':('取景器',['蓝牙 已连接 / Wi-Fi 已连接','画面       参数       相册 ✓','相机相册','[缩略图]   VIDEO_001.MP4   视频','[缩略图]   IMAGE_001.JPG   照片','[缩略图]   VIDEO_002.MP4   视频','加载更多','点击照片 → 图片弹窗','点击视频 → 播放器弹窗','关闭回放 → 返回实时预览'])}
for theme in ['dark','light']:
 bg,fg,muted,gold,line=('#080808','#f1f1f1','#969696','#ceaf70','#292929')if theme=='dark'else('#fafafa','#161616','#686868','#87672c','#e1e1e1')
 for key,(title,rows)in screens.items():
  parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 780"><rect width="360" height="780" fill="{bg}"/><g font-family="sans-serif" fill="{fg}"><text x="20" y="30" font-size="12" fill="{gold}">留光 · Luma</text><text x="340" y="30" text-anchor="end" font-size="9" fill="{muted}">界面结构参考</text><text x="20" y="80" font-size="26" font-weight="600">{title}</text>']
  y=105 if key=='shooting' else 130
  if key=='shooting':parts[0]=parts[0].replace(f'<text x="20" y="80" font-size="26" font-weight="600">{title}</text>','')
  for i,row in enumerate(rows):
   if row.startswith('@preview'):
    h=240 if row.endswith('43') else 180
    parts.append(f'<rect x="20" y="{y-8}" width="320" height="{h}" fill="{bg}" stroke="{line}"/><path d="M126 {y-8}v{h}m107 -{h}v{h}M20 {y-8+h/3}h320M20 {y-8+h*2/3}h320" stroke="{muted}" opacity=".5"/><text x="180" y="{y+h/2}" text-anchor="middle" fill="{muted}" font-size="11">相机实时画面区域</text>');y+=h+20;continue
   accent=i==len(rows)-1 and key in ('shooting','camera')
   if accent:parts.append(f'<rect x="20" y="{y-22}" width="320" height="46" fill="{gold}"/>')
   parts.append(f'<text x="{180 if accent else 20}" y="{y+5}" text-anchor="{"middle" if accent else "start"}" font-size="{13 if accent else 12}" fill="{bg if accent else fg}">{escape(row)}</text>')
   if not accent:parts.append(f'<path d="M20 {y+24}h320" stroke="{line}"/>')
   y+=49 if len(rows)<11 else 45
  if key in ('shooting','camera','history','settings'):
   for i,name in enumerate(['拍摄','相机','记录','设置']):parts.append(f'<text x="{50+i*86}" y="745" text-anchor="middle" fill="{gold if key==["shooting","camera","history","settings"][i] else muted}" font-size="11">{name}</text>')
  parts.append(f'<text x="180" y="775" text-anchor="middle" font-size="8" fill="{muted}">按源码绘制 · 示例状态 · 尺寸以手册 dp/sp 为准</text></g></svg>')
  (p/f'{key}-{theme}.svg').write_text(''.join(parts))
 (p/f'fullscreen-{theme}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 360"><rect width="780" height="360" fill="{bg}"/><rect x="150" y="0" width="480" height="360" fill="{bg}" stroke="{line}"/><path d="M310 0v360M470 0v360M150 120h480M150 240h480" stroke="{muted}" opacity=".5"/><g font-family="sans-serif" text-anchor="middle"><text x="390" y="175" fill="{fg}" font-size="16">4:3 完整画面 · 两侧留边</text><text x="390" y="200" fill="{muted}" font-size="11">双指缩放 / 拖动查看 / 点按隐藏工具</text><rect x="190" y="297" width="400" height="43" fill="{bg}" stroke="{muted}"/><text x="390" y="324" fill="{gold}" font-size="13">退出全屏　　1.0×　　构图　　参考帧</text><text x="390" y="354" fill="{muted}" font-size="8">按源码绘制 · 全屏参考 · 保留 TextureView 与连接</text></g></svg>''')
print('Generated',len(list(p.glob('*.svg'))),'diagram references')
