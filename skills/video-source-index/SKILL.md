---
name: video-source-index
description: Index local interviews, recordings or video sources with hashes, observed timecoded content, reusable intervals, provenance and rights status.
---

[English instructions](SKILL.en.md) · 简体中文

For English-language tasks, read [SKILL.en.md](SKILL.en.md) and its English reference templates before proceeding. Both editions use the same tools and authorization boundaries.


# 视频素材索引
适用于已有视频、采访、录屏与参考片。元数据、语音转写和画面观察分别提供信息，不能互相代替。

## 执行
工具文件：[source_manifest.py](scripts/source_manifest.py)，随技能目录一起安装。
1. 保留原件，记录 source_id、文件名、哈希、媒体参数、来源及获取方式。先将 `skill_dir` 定位为本 `SKILL.md` 所在目录，再使用绝对脚本路径运行 `python "<skill_dir>/scripts/source_manifest.py" "<源文件绝对路径>" --output "<新清单绝对路径>"`；不依赖用户当前工作目录。只保存文件名和精选参数，完整路径留在用户工作项目索引。
2. 检查可用工具：ffprobe 仅取参数，ASR 仅给语音候选。原采访先保留原声原意。使用外部转写服务前核对该素材的上传许可；本地工具可用时优先本地。
3. 全片广泛采样，关键转场、人物动作、数据图和拟使用区间加密观察。用读图能力实际看帧；有播放器/音频能力时正常速度看听。仅静帧或转写时写清覆盖范围。
4. 按 [索引模板](references/content-index.md) 输出内容时间段、可见对象/文字、说了什么、音事件、主张与可复用片段。区分直接观察、自动转写、原作者声称和编辑判断。
5. 全区间检查主体、原字幕、裁切与语境。素材标题或单帧命中不代表整段适合。把候选落到取得、权利核验、剪入、弃用或具体受阻状态。

## 重要区分
事实引用权与图像/声音使用权分别核对；公开视频和“注明出处”不能自动证明商用许可。通用库存不能当特定人物/公司的现场，生成素材不能当实拍证据。重复 ASR 句、音乐误识别及未知说话者须回听，不据此编摘要。

## 产物
来源清单、content-index、可用区间、权利与缺口。未取得文件写待取得，未听辨写语音候选，未观察的区间保持未知。不得把索引完成写成全片视听通过。
