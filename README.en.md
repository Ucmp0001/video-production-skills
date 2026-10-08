# Video Production Skills

**Turn a video request into a workflow your AI assistant can follow.**

[简体中文](README.md) · English · [Follow on X: @eazymoney888](https://x.com/eazymoney888)

11 composable skills for Codex, Claude Code and assistants supporting `SKILL.md`. Cover sources, scripts, shots, explanatory motion, conceptual footage, voice/captions, covers and delivery. Install one or combine them, without a required model, voice or operating system.

## New here? Start with one small result

**[Install an assistant and finish your first 60-second script →](docs/getting-started.en.md)**

Start by copying one skill manually: no Git, Python or FFmpeg needed. The guide covers Windows/macOS downloads, extraction, folder placement, prompts and success checks. The first exercise is text-only. Bring working assistant access; the assistant itself may charge subscription or usage fees.

| What you need | Read this |
|---|---|
| Start from installing software | [Beginner guide](docs/getting-started.en.md) |
| Install all skills and connect stages | [Advanced usage](docs/usage.en.md) |
| Fix discovery/command errors or understand phone access | [FAQ](docs/faq.en.md) |
| Try an exercise without private material | [Fictional capacity story](examples/fictional-capacity-story.en.md) |

## What makes this workflow useful?

- **Concrete handoffs at each stage.** Evidence connects to scripts, shots, captions and covers through explicit inputs and outputs.
- **Resume existing work.** A subtitle repair checks the affected parts while preserving originals and prior versions.
- **Visuals explain the content.** Observable state changes demonstrate mechanisms; 2D and 3D serve the explanation. Covers receive dedicated design and independent inspection.
- **Checks refer to actual files.** Code checks, technical checks, image inspection, playback and listening have distinct scopes; missing observations stay explicit.
- **Choose your own tools.** Off-camera production and authorized synthetic narration are possible. Rendering, TTS, generated video and phone remote access require your own setup.

This repository supplies methods, templates and small validation tools. It includes no model accounts or API credits and does not guarantee automatic finished videos or audience growth.

## The 11 skills

| Skill | When to use it | Main outputs |
|---|---|---|
| [video-workflow](skills/video-workflow/SKILL.en.md) | Resume or plan a project | Current stage, plan and delivery status |
| [video-source-index](skills/video-source-index/SKILL.en.md) | Index existing footage | Timecoded intervals, provenance and rights |
| [evidence-story-script](skills/evidence-story-script/SKILL.en.md) | Turn sources into a script | Voiceover, evidence and opening payoff |
| [video-shot-planner](skills/video-shot-planner/SKILL.en.md) | Plan visuals for a script | Shots, asset gaps and alternatives |
| [explainer-motion](skills/explainer-motion/SKILL.en.md) | Explain processes and data | 2D/3D motion brief, implementation and preview |
| [generated-broll](skills/generated-broll/SKILL.en.md) | Add conceptual generated shots | Plan, budget and recoverable tasks |
| [voice-subtitle-sync](skills/voice-subtitle-sync/SKILL.en.md) | Prepare voice and captions | Measured timing, subtitles and checks |
| [cover-art-direction](skills/cover-art-direction/SKILL.en.md) | Design a publication cover | Headline, composition and ratio exports |
| [cover-independent-review](skills/cover-independent-review/SKILL.en.md) | Review covers independently | Report based on actual images |
| [video-release-qa](skills/video-release-qa/SKILL.en.md) | Check exports and platform copy | QA record, copy and delivery index |
| [video-reference-study](skills/video-reference-study/SKILL.en.md) | Learn from a reference video | Observations, methods and applicability |

## Already have an assistant? Quick installation

From the downloaded, extracted repository root, with Python 3.10+ (use `py` on Windows or `python3` on macOS if needed):

```sh
python scripts/install_skills.py --target ~/.agents/skills --skill evidence-story-script
```

This is Codex's personal directory. For Claude Code use `--target ~/.claude/skills`. Project-local destinations are `.agents/skills` and `.claude/skills` respectively. Omit `--skill` to install all 11. Existing skill folders are never overwritten. Both languages are copied together. See [official software sources](docs/software-sources.md) for installation references.

Open the repository root in your assistant and send:

```text
Use evidence-story-script and read examples/fictional-capacity-story.en.md.
Write an English 60-second explainer labeled as a fictional exercise, not news.
Provide a title, full voiceover, opening payoff and asset gaps.
Do not call media services or publish anything.
```

`SKILL.md` remains the discovery entrypoint. For English tasks, it routes to adjacent `SKILL.en.md` and English templates. Discovery and invocation differ by client; explicitly request the actual installed file if needed.

## Contribute and license

```sh
python scripts/validate_package.py .
python scripts/privacy_scan.py .
python -m unittest discover -s tests -v
```

[Contributing](CONTRIBUTING.en.md) · [Security](SECURITY.en.md) · [Why 11 skills](docs/design-retrospective.en.md) · [Validation scope](docs/validation.en.md)

Reproducible issues and anonymized examples are welcome. Star the repository if it helps. MIT license; see [third-party references and licenses](THIRD_PARTY_NOTICES.en.md).
