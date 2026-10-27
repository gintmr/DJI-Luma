# 留光 · Luma

**给大疆 Action 补上间隔定时录像，留下日常 Vlog 片段。**

用安卓手机设好间隔与片段时长，点击启动，相机按计划记录，素材保存在相机 SD 卡。详细整理、下载与导出继续使用 DJI Mimo。

本仓库公开的是这套项目的 **Agent 复现工作流**：页面规格、技术栈、通信与任务状态机、分阶段 Prompt、手机调试步骤、排错记录和验收方法。你可以把完整任务包交给自己的 Agent，在自己的设备上完成搭建与验证；也可以先安装测试 APK 体验。

[项目网站](https://gintmr.github.io/DJI-Luma/) · [中文复现手册](docs/workflow/reproduction-manual.md) · [English handbook](docs/workflow/reproduction-manual-en.md) · [Agent 简报](docs/workflow/agent-brief.md)

![留光：给大疆 Action 补上间隔录像](docs/assets/promo/luma-douyin-landscape-4x3.png)

## 宣传与演示

- [87 秒中文 4K 宣传片](https://github.com/gintmr/DJI-Luma/raw/refs/heads/main/docs/assets/promo/luma-promo-zh-4k.mp4)
- [22 秒中文相机 × 手机同步演示](docs/assets/video/luma-split-zh-4k.mp4) · [English demo](docs/assets/video/luma-split-en-4k.mp4)
- 封面：[横版 4:3](docs/assets/promo/luma-douyin-landscape-4x3.png)、[竖版 3:4](docs/assets/promo/luma-douyin-portrait-3x4.png)、[方形 1:1](docs/assets/promo/luma-douyin-square-1x1.png)
- [宣传素材与音乐署名](docs/assets/promo/CREDITS.md)

## 开始复现

1. 准备安卓手机、数据线和相机；在手机打开开发者选项与 USB 调试，并授权自己的电脑。
2. 下载 [中文完整复现包](https://github.com/gintmr/DJI-Luma/raw/refs/heads/main/docs/workflow/reproduction-kit.zip)（[English kit](https://github.com/gintmr/DJI-Luma/raw/refs/heads/main/docs/workflow/reproduction-kit-en.zip)）。包内包含完整简报、手册、18 张结构图和 32 张原生界面参考。
3. 填入自己的设备信息，把简报交给 Agent，依次完成环境与界面、蓝牙拍摄、定时任务、Wi-Fi 辅助功能和实测回归。
4. 按手册的 ADB 操作、日志证据和验收表逐阶段验证，再运行长时间拍摄任务。

工作流保留了开发中已经验证的路线与排错过程，包括自定义相机名的发现、定时停止确认、蓝牙与 Wi-Fi 交接、预览比例和后台运行。

## 先体验测试版

[下载 Luma 0.7.1 测试 APK](https://github.com/gintmr/DJI-Luma/raw/refs/heads/main/docs/downloads/luma-0.7.1-test.apk) · [SHA-256](docs/downloads/SHA256SUMS.txt) · [第三方许可](docs/downloads/THIRD_PARTY_LICENSE.txt)

| 项目 | 当前测试版 |
| --- | --- |
| 相机 | 已验证 DJI Osmo Action 4；Action 5 / 6 尚未适配 |
| 手机 | Android 13+；实测 Samsung S25 FE，其他手机需验证 |
| 语言与外观 | 中文 / English / 跟随系统；浅色 / 深色 |
| 使用条件 | 相机保持开机、插入可写 SD 卡；初次使用先用 Mimo 完成官方激活 |
| 定时逻辑 | 间隔按两次开录的开始时间计算 |
| 自动唤醒 | 尚未实现，任务中需让相机保持开机 |

先试录短片，再验证锁屏、后台与长任务。首次连接、系统权限和后台设置见[安装与首轮验证](docs/workflow/reproduction-manual.md)。

## 许可

本仓库原创工作流与文档采用 [MIT License](LICENSE)。第三方代码、测试 APK 中的组件和宣传配乐遵循各自许可，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

Built with agents.
