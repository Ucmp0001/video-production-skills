---
name: voice-subtitle-sync
description: Prepare or repair voice and subtitles using authorized recordings or configured TTS, measured audio timing, transcript checks and SRT validation.
---

[English instructions](SKILL.en.md) · 简体中文

For English-language tasks, read [SKILL.en.md](SKILL.en.md) and its English reference templates before proceeding. Both editions use the same tools and authorization boundaries.


# 配音与字幕同步
先判断是已有原声字幕、本人录音、授权配音还是字幕局部修复。原声优先复用；用户指定声音、服务、音乐时保持，不默认克隆声音或更换服务。

## 音频与正文
锁定最新正文。新的 TTS 读取使用者的音色授权、服务/模型、表达和音频参数，凭据由现有环境提供。表达指令与正文分离，防止被朗读；无法消费要求的工具明确待配音，不静默换声或接口。
分段保持声音状态，开场好奇、解释清楚、转折有力等仅按内容与用户风格使用，不固定夸张情绪。缓存绑定完整正文、模型、声音、表达与音频参数；结果不明先恢复原任务，避免重复付费。

## 时间与字幕
工具文件：[check_srt.py](scripts/check_srt.py)，随技能目录一起安装。
测量实际音频后，按本次时间戳或本地转写建立时间线。ASR 是候选，回听名称、数字、外文、拼接、否定词与关键限定；权威写法与原意冲突时标注，不暗改说话者事实。
按语义分段，保留 UTF-8 软字幕。先将 `skill_dir` 定位为本 `SKILL.md` 所在目录，再从任意工作目录运行 `python "<skill_dir>/scripts/check_srt.py" "<字幕绝对路径.srt>" --duration <实际时长秒>`，可配置 `--max-cps`、`--min-duration`；格式/越界为错误，阅读速度与交叠为待观察提示。多说话者交叠可能合理，严格模式按需求使用。
使用 [音频字幕检查](references/audio-captions.md) 记录单词时间与句子时间的粒度、边界和未知区间。最终字幕不使用稿件估时。声音改变要同步重建受影响的分镜、动画事件、字幕和章节，不靠硬加速掩盖不足。

## 实际审阅
烧录是可选工序，另存版本，保留软字幕。字幕在当前画幅和手机大小检查换行、安全区、遮挡与原有画面文字；不要把固定字号当通用可读标准。
响度、峰值与波形只做技术检查。试听实际文件的发音、语气、停顿、段落接缝、音乐与人声关系；需要音乐时核验具体曲目使用权，平滑首尾并保留分轨。
没有听辨或读图能力就写清待验收范围，不能仅凭转写、成功生成或工程参数签听感通过。

交付当前音频、SRT/按需ASS、来源与授权记录、实际时长、配置指纹和观察记录。私人声音引用与服务日志留在工作项目，不提交到公开仓库。
