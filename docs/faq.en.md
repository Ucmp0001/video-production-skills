# FAQ: find the step that is blocking you

[English home](../README.en.md) · [简体中文](faq.zh-CN.md) · [Beginner guide](getting-started.en.md)

## What is a Skill? Will installing it automatically make a video?
A Skill is an operating guide for an assistant: what to do, what to deliver and how to check it. It is not a model, account or video generator. The assistant follows the instructions; voice, rendering and video generation still need suitable tools and working access.

## Do I need coding experience, Git, Python or FFmpeg?
Not for the first text exercise. Download the ZIP and copy one skill folder manually. Python 3.10+ is needed only for the repository's installer/check scripts. Git is an optional download/update method. Add media tools such as FFmpeg/ffprobe when the task actually needs them.

## Where do commands go?
Software installation, `py ...`, `python3 ...` and `claude --version` belong in the system terminal: PowerShell on Windows or Terminal on macOS. Requests such as “use this skill to write a script” go in the AI chat box.

## The assistant cannot find the skill
Open the project where you installed it. Confirm `.agents/skills/skill-name/SKILL.md` for Codex or `.claude/skills/skill-name/SKILL.md` for Claude Code, with no duplicated nested folder. Restart/start a new session. If necessary, ask the assistant to read the actual installed file and list its inputs. Discovery varies by client; ordinary web chat does not automatically read local folders.

## The examples file is missing
The exercise ships in the repository, not inside an installed skill. Open the extracted repository root and check that `examples` is directly inside it. In your own project, use your own sources or copy the exercise there.

## Python / py / python3 is not found
Continue with manual copying for the text exercise. For scripts, install Python 3.10+ from the official site, reopen the terminal and use whichever executable works on your system. Replace the tutorial's command name accordingly. “Can't open file” often means the wrong working directory: enter the repository root containing `scripts` first.

## The installer reports an existing destination
It is protecting your installed skills. It checks conflicts before copying and does not overwrite your edits. Compare versions, or install into a fresh practice project. To update, back up customizations before deliberately replacing the relevant folder; do not blindly delete your entire skills directory.

## The output is in the wrong language
Explicitly request “reply in English” or Chinese. `SKILL.md` is the shared discovery entrypoint; English instructions are in `SKILL.en.md` and English templates in `references/*.en.md`. Copy the entire skill folder rather than one Markdown file.

## Can I control this from ChatGPT on my phone?
A phone can be a remote entry point if your client and computer/cloud execution environment are connected and that environment can read the project and skills. Copying files onto a computer does not expose them to ordinary phone chat automatically. This repository provides no remote connection feature. Complete the computer exercise first, then use your client's official remote setup documentation.

## Can I use Claude without its website or through another provider?
Claude Code is a client; model access is a separate service layer. Availability depends on provider support, account permissions and actual returned models. Follow the client/provider's official instructions. This repository supplies no gateway, guarantees no particular model access and never needs your credentials. Keep configuration in local authentication systems, outside public repositories, screenshots and issue reports.

## Can I avoid appearing on camera or recording narration?
Use authorized footage, explanatory animation and conceptual shots. A configured, authorized voice tool can provide narration, or make a video without narration. Bring your own tools, budget and media/voice permissions. Private voices, music and finished footage are not included.

## Does open source mean everything is free?
The code and skills use the MIT license. Models, TTS, video generation and other services may charge separately. The first text exercise adds no media-service calls, but the assistant itself may cost money. Check a specific plan and budget before paid generation.

## Does filling in the example JSON run the workflow?
No. `project.example.json` is a handoff record, not executable configuration consumed by these tools. Null means unconfigured; changing a field does not supply authorization.

## Does this guarantee viral videos? How do I report a problem?
No audience outcome is guaranteed. The workflow improves structure and checks; topics, assets, expression and platform performance need real evaluation. Report your system, client version, steps, sanitized error and expected result. Exclude keys, private paths, real footage and account screenshots. See [security guidance](../SECURITY.en.md).
