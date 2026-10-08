---
name: video-shot-planner
description: Turn a stable voiceover into event-based shots, source intervals, asset gaps and clock conventions for editing or animation.
---

[English instructions](SKILL.en.md) · 简体中文

For English-language tasks, read [SKILL.en.md](SKILL.en.md) and its English reference templates before proceeding. Both editions use the same tools and authorization boundaries.


# 分镜与素材覆盖
输入最新口播、来源、可用素材、画幅与实际音频。有录音按真实句子和事件排时序；没有录音时明确估时，不伪造精确锚点。

## 一张表连接实现
按 [分镜表](references/shot-table.md) 给每个 shot_id 写清：对应口播、观众问题、画面任务、前后状态、主要事件、素材源区间、屏幕文字/字幕、声音、权利、缺口与替代。
画面任务可为证据、人物行动、尺度、对比、机制或必要信息。每镜一个主要注意力中心；文字命名，事件解释，避免画面只复述旁白。

素材状态区分已有、待拍摄、待制作、待检索、待授权、可替代。优先直接相关真实材料，原声有叙事意义时保留；无关库存和快速切换不能替代真实信息。

## 三种时钟
- 全片：最终时间线的位置。
- 镜头局部：镜头内事件的零点。
- 素材：原文件入点及变速映射。
帧区间统一半开 `[startFrame, endFrame)`，相邻镜头共享边界；秒转帧按绝对边界换算，避免逐段取整累计漂移。裁切、速度、冻结、循环与嵌套组件要显式标映射，父层动画不能盲目按子时钟理解。

## 预检
检查拟使用完整源区间、画幅裁切、原字幕、证据阅读时间与转场。不能拼出虚假对话、反应或同场关系。
先排初始、变化、结果三个关键状态，再做复杂效果。开头视觉兑现第一句，最后镜头帮助回答问题。无需固定素材、动画比例或切镜密度。

交付分镜/素材覆盖表、关键事件锚点、缺口与低风险替代。工程协议以实际渲染器为准，本表不冒充任意工具的可执行输入。
