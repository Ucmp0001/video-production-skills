# Video Production Skills

**把一句制作需求，拆成助手能逐步执行的视频工作流。**

简体中文 · [English](README.en.md) · [关注作者：X @eazymoney888](https://x.com/eazymoney888)

11 个可组合的 AI 视频制作技能，适用于 Codex、Claude Code 等支持 `SKILL.md` 的助手。覆盖资料、口播、分镜、解释动画、概念镜头、配音字幕、封面和交付。可只装一个，不绑定指定模型、音色或操作系统。

## 第一次来？从这里开始

**[从零安装软件，完成第一份60秒视频稿 →](docs/getting-started.zh-CN.md)**

不懂代码也可以先手动复制一个技能，无需 Git、Python 或 FFmpeg。教程包含 Windows / macOS 的软件下载、解压、放文件、发指令和每步成功标志。第一份练习只做文字；你需要自己的可用助手账号，助手本身可能收费。

| 你现在想做什么 | 去哪里 |
|---|---|
| 从安装软件开始 | [新手教程](docs/getting-started.zh-CN.md) |
| 装全部技能，接完整流程 | [进阶用法](docs/usage.zh-CN.md) |
| 找不到技能、命令报错、想用手机 | [常见问题](docs/faq.zh-CN.md) |
| 看一个没有私人资料的案例 | [虚构产能练习](examples/fictional-capacity-story.md) |

## 这套技能有什么特点？

- **每道工序有可交接的产物。** 从证据到稿件、镜头、字幕和封面，写清输入、输出及下一步。
- **已有项目可以接着做。** 只修字幕就检查受影响部分，保留原件和历史版本。
- **画面要解释内容。** 用实际状态变化说明机制，2D 与 3D 按需要组合；封面单独设计、独立看图。
- **检查绑定实际文件。** 区分脚本通过、技术检查、实际看图、播放和听辨，缺项就明确标出。
- **工具可以自己选。** 支持不出镜、用授权配音的制作路线；渲染、配音、生视频和手机远程接入由你另行配置。

仓库提供工作方法、模板和小型检查工具。它不附带模型账号或 API 额度，也不保证自动生成成片或获得特定流量。

## 11 个技能

| Skill | 什么时候用 | 主要产物 |
|---|---|---|
| [video-workflow](skills/video-workflow/SKILL.md) | 不知道下一步做什么 | 当前阶段、计划和交付状态 |
| [video-source-index](skills/video-source-index/SKILL.md) | 已有视频、采访或录屏 | 素材索引、可用片段、来源与权利 |
| [evidence-story-script](skills/evidence-story-script/SKILL.md) | 把资料写成口播 | 故事稿、证据和开头兑现 |
| [video-shot-planner](skills/video-shot-planner/SKILL.md) | 稿子有了，画面怎么做 | 分镜、素材缺口和替代 |
| [explainer-motion](skills/explainer-motion/SKILL.md) | 解释流程、机制和数据 | 2D/3D 动画设计、实现与预览 |
| [generated-broll](skills/generated-broll/SKILL.md) | 需要 AI 概念镜头 | 生成计划、预算、任务恢复 |
| [voice-subtitle-sync](skills/voice-subtitle-sync/SKILL.md) | 配音或字幕对不上 | 实测时间轴、字幕与检查 |
| [cover-art-direction](skills/cover-art-direction/SKILL.md) | 需要有吸引力的封面 | 文案、构图和多比例封面 |
| [cover-independent-review](skills/cover-independent-review/SKILL.md) | 封面做好了，独立把关 | 实际审图报告 |
| [video-release-qa](skills/video-release-qa/SKILL.md) | 交付前检查、写平台文案 | 验收记录、文案与交付索引 |
| [video-reference-study](skills/video-reference-study/SKILL.md) | 学习参考视频的做法 | 观察记录、方法和适用条件 |

## 已有环境？快速安装

在下载并解压后的仓库根目录执行，需要 Python 3.10+（Windows 可把 `python` 换成 `py`；macOS 可换成 `python3`）：

```sh
python scripts/install_skills.py --target ~/.agents/skills --skill evidence-story-script
```

这是 Codex 个人目录。Claude Code 改成 `--target ~/.claude/skills`；本项目内安装分别用 `.agents/skills` 或 `.claude/skills`。省略 `--skill` 安装全部 11 个。安装器不覆盖同名技能；中英文文件一起复制。软件入口和目录依据见[官方资料](docs/software-sources.md)。

打开仓库根目录，在助手聊天框说：

```text
使用 evidence-story-script，读取 examples/fictional-capacity-story.md。
写一条中文60秒解释稿，标明是虚构演练，不得写成新闻。
只输出标题、完整口播、开头兑现和素材缺口，不调用媒体服务、不发布。
```

`SKILL.md` 是统一发现入口；英文任务读取旁边的 `SKILL.en.md` 和英文模板。不同客户端触发方式有差别，无法自动识别时让助手读取实际安装路径的文件。

## 贡献与许可

```sh
python scripts/validate_package.py .
python scripts/privacy_scan.py .
python -m unittest discover -s tests -v
```

[贡献方式](CONTRIBUTING.md) · [安全与隐私](SECURITY.md) · [为什么拆成11个](docs/design-retrospective.md) · [验证范围](docs/validation.md)

欢迎用匿名案例提交可复现问题。如果有帮助，欢迎 Star。MIT 许可；[第三方方法与许可](THIRD_PARTY_NOTICES.md)。
