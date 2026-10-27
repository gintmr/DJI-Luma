# 留光 · Luma · GitHub Pages 展示站

网站在 `docs/`，纯静态 HTML/CSS/JavaScript，无 npm 依赖、构建步骤、Actions 工作流、数据库、统计或访客记录。不修改安卓工程，也不修改共享框架仓库。网站默认黑金主题，与 App 0.7.1 的 `#080808 / #CEAF70` 保持一致。

## 本地预览

在当前项目根目录执行：

```sh
python3 -m http.server 8767 --bind 127.0.0.1 --directory docs
```

打开 http://127.0.0.1:8767/ 。不要直接双击 HTML：导航原语使用原生 ES modules，需通过 HTTP 加载。退出服务器按 Ctrl+C。

## GitHub Pages 唯一必要配置

把网站文件提交到目标 GitHub 仓库后，在 **Settings → Pages → Build and deployment** 选择：

**Source: Deploy from a branch → Branch: main（或实际提交分支）→ Folder: /docs → Save**。

不需要 Vercel、Astro、自定义域名、环境变量、密钥或数据库配置。公开仓库为 `https://github.com/gintmr/DJI-Luma`。发布内容为 `docs/`、说明文档及静态站维护脚本；根目录 `.gitignore` 使用白名单，保留固件、工具缓存、签名密钥、设备诊断和安卓开发目录在本机。

所有站内资源与页面链接使用相对路径；同一套文件可以部署在 `https://<user>.github.io/` 或 `https://<user>.github.io/<项目名>/`。目录链接保留末尾 `/`，或直接访问 `index.html`，不设置根路径 `<base>`。不使用单页路由，因此刷新 `workflow.html` 可直接访问。

## 结构

- `docs/index.html`：项目展示、计划试算、工作流与架构、兼容性、APK 下载、FAQ、项目仓库入口。
- `docs/workflow.html`：完整复现手册：14 章页面规格、状态机、技术栈、真机操作、排错与验收；左侧目录可直达章节。
- `docs/workflow/agent-brief.md`：包含手册全文的 Agent 执行简报，含任务输入和逐阶段 Prompt。
- `docs/assets/site.css`：本项目的黑金令牌和专属布局。
- `docs/assets/site.js`：导航启动、纯本地计划试算、用户主动触发的复制。没有存储或网络请求。
- `docs/ui/`：共享框架的固定快照、MIT LICENSE、来源版本与 SHA-256。
- `docs/downloads/`：已存在的 0.7.1 测试 APK 快照、校验文件和第三方许可。当前仅 Action 4；其他手机需实测，Action 5 / 6 不支持。
- `docs/.nojekyll`：直接发布静态资源。

## gintmr-ui 的接入方式与更新

从 `gintmr-ui` 独立源码仓库的固定提交取文件，精确版本见 `docs/ui/provenance.json`：

1. `dist/gintmr-ui.css` 原样复制：复用令牌、重置、排版、顶栏、导航等基础样式。
2. 完整 `dist/gintmr-ui.js` 包包含 Visitor 模块，不在本站复制或引用。
3. 仅原样复制 `src/primitives/nav.js`，用原生 ES module 启动。该模块只有导航行为；不加载主题持久化、访客、媒体、粒子等模块。
4. 网站采用固定黑金主题，不载入 `theme-preload.js`，不访问 localStorage、cookie、IndexedDB。框架 CSS 中未实例化的组件规则不会创建组件或收集数据。
5. 以 `site.css` 覆盖框架的第一级调色令牌和项目布局；不在 vendor 文件中修改项目样式。

本次没有修改共享框架，因此无需构建或提交共享库。以后确需修复共享行为时，在独立 `gintmr-ui` 源码仓库修改 `src/`，执行 `npm run build`，检查 demo 后将源码与 `dist/` 一起提交并推送。然后在本项目执行：

```sh
python3 scripts/sync-ui.py /你的路径/gintmr-ui
python3 scripts/check-website.py
```

同步脚本只复制 CSS、导航和许可证，并更新来源哈希；发现导航模块新增存储或网络 API 时会停止。核对页面后提交本项目中的 `docs/ui/`。不使用 submodule，不依赖 Pages 拉取其他仓库。更新框架不会覆盖本项目的黑金样式。

## 更新 APK 和素材

APK 是 `android/build/luma-0.7.1.apk` 的独立复制，后续安卓构建不会悄悄改变网站下载文件。更新时复制明确版本，更新两页的版本/兼容信息、`SHA256SUMS.txt`、首页摘要和第三方许可，再检查下载文件哈希。App 展示图来自设备上安装的 0.7.1，分别运行 UiCheck 的 en/zh 两轮采集，共 36 个明暗语言状态。网站发布其中 32 张实际渲染，排除记录页；记录页以结构图展示。素材版本和 SHA-256 记录在 docs/assets/app/0.7.1/provenance.json。网页首页使用当前拍摄页，不再使用旧相机页或相机实物示意图。

## 检查

```sh
python3 scripts/check-website.py
node --check docs/assets/site.js
node --check docs/ui/nav.js
```

检查覆盖站点根目录、`/DJI-Luma/` 和不同项目子路径下的本地链接/锚点、资源存在性、共享框架与 APK 哈希、脚本白名单、无远程字体/CDN与无存储/收集 API。浏览器还需检查响应式布局、菜单、计划试算与简报复制。

网站没有自己的访问收集；静态托管服务 GitHub Pages 的平台日志由 GitHub 管理，不属于站点新增的访客记录功能。

## 完整手册维护

主文档：`docs/workflow/reproduction-manual.md`。页面结构参考图的生成脚本为 `scripts/render-reference-pages.py`，来自源码规格的图均标明“示例状态”。实际记录页截图包含配对日志，不进入公开包。

编辑主文档后执行：

```sh
python3 scripts/render-workflow.py
python3 scripts/check-website.py
```

脚本产出静态 `workflow.html`、含全文的 `agent-brief.md` 和 `reproduction-kit.zip`；Pages 直接发布产物，部署时无需运行生成器。复现包包含完整手册、完整简报、18 张明暗参考图和 32 张实际 App 界面参考。

手册、安装包与实际界面已统一到 0.7.1。新版首页移除重复的“定时拍摄”标题；中文名称为留光，英文为 Luma，页面保留语言与主题切换。

页脚只展示 Built with agents 与项目 GitHub 入口。项目地址为 `https://github.com/gintmr/DJI-Luma`，首页和双语手册页脚均指向该仓库。`scripts/render-workflow.py` 同步维护页脚与任务包中的仓库链接。

## 发布版本与截图一致性

`docs/release.json` 记录当前名称、版本、APK 路径、文件大小与 SHA-256。更新网站时同时更新此记录、下载区、首页和手册，再运行检查。检查脚本还会校验实际界面来源哈希、ZIP 中的图像和版本号，避免只替换文案后继续显示旧图。

0.7.1 的 UI 采集检查在 `analysis/website-ui-0.7.1-en.txt` 和 `analysis/website-ui-0.7.1-zh.txt`；手机锁屏时的横屏图是布局渲染，未将其计作新一轮物理旋转验证。站点显示图只用于界面展示。

## 产品定位

留光为 DJI Action 补充间隔定时录像，用于采集日常 Vlog 片段。首页按“设好计划 → Action 自动记录 → 回到 Mimo 整理素材”讲述使用流程；取景、参数和相册作为开拍前检查与观察辅助，开发架构集中在完整复现手册。

## 4K 功能动画

首页 `#animation` 使用原生视频播放器，视频与封面位于 `docs/assets/video/`，支持全屏。源代码与制作规格位于 `video/interval-demo/`，后续视频标准见 `video/PRODUCTION.md`。更新成片后同步视频、封面与 manifest.json，再运行 `python3 scripts/check-website.py`。

## 双语与首页章节

首页顺序：核心用途 → 视频 → UI 界面 → 复现流程 → 测试 APK → 常见问题。重复功能卡和三步记录图已移除。

中文版为 `index.html`、`workflow.html`，英文版为 `index-en.html`、`workflow-en.html`。语言切换使用相对路径静态链接，关闭 JavaScript 也可使用。两种语言引用各自的 4K 视频及封面，不同时加载两版。

维护 `docs/workflow/reproduction-manual.md` 和 `reproduction-manual-en.md` 后，分别执行 `python3 scripts/render-workflow.py` 与 `python3 scripts/render-workflow.py --lang=en`，同步各自完整简报与 ZIP。页面结构图保留中文标注，英文手册使用实际英文界面并说明图示语言。最后运行 `python3 scripts/check-website.py`。

GitHub Pages 设置仍为：从分支部署，选择 `main` 分支的 `/docs` 文件夹。本地 `python3 -m http.server 8767 --directory docs`，分别访问 `/` 和 `/index-en.html`。

## 左右分区动画

首页视频现为左相机、右手机的 3840×2160 合成动画，中英文分别引用 `luma-split-zh-4k.mp4` 和 `luma-split-en-4k.mp4`。源代码、同步规格、原生手机状态采集与哈希位于 `video/interval-demo/split/`。手机画面来自三星上的 Luma 原生 View 渲染，模拟状态不触发真实录制。
