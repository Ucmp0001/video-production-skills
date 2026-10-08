# Voice and subtitle synchronization

[中文 / canonical entry](SKILL.md)

Identify whether the task uses existing original audio, the user's recording, authorized TTS or a local subtitle repair. Reuse original sound when appropriate. Respect specified voices, services and music; do not default to cloning a voice or switching providers.

## Audio and script
Lock the latest script. For new TTS, read the user's voice permissions, provider/model, expression and audio settings. Use existing environment authentication. Keep expression instructions separate from spoken text. If a tool cannot honor requirements, mark narration pending instead of silently changing voices/interfaces.

Keep voice settings consistent across segments. Curiosity, clear explanation or emphatic turns should fit content and user style, not a fixed exaggerated emotion. Cache keys include the full script, model, voice, expression and audio parameters. Recover unclear tasks before creating another paid request.

## Timing and captions
Bundled tool: [check_srt.py](scripts/check_srt.py).

Measure actual audio, then build timing from its timestamps or local transcription. ASR is a candidate: listen to names, numbers, foreign words, joins, negation and key qualifiers. If a standard spelling conflicts with the speaker's meaning, flag it rather than silently changing the speaker's claim.

Segment by meaning and retain UTF-8 soft subtitles. Resolve `skill_dir` to the installed `SKILL.md` directory. From any working directory run `python "<skill_dir>/scripts/check_srt.py" "<absolute-captions.srt>" --duration <measured-seconds>`. Optional `--max-cps` and `--min-duration` tune checks. Format/bounds issues are errors; reading speed and overlap are observation warnings. Multiple speakers may overlap legitimately; use strict mode as needed.

Use the [audio/caption checklist](references/audio-captions.en.md) to record word/sentence timestamp granularity, boundaries and unknown intervals. Final captions must not rely on script estimates. Audio changes require updating affected shots, motion events, captions and chapters; do not hide inadequate timing through forced speedup.

## Actual review and delivery
Burn-in is optional; save a new version and preserve soft subtitles. Inspect line breaks, safe areas, occlusion and existing text at the current aspect ratio and phone size; one fixed font size is not universally readable.

Loudness, peaks and waveforms are technical checks only. Listen to pronunciation, delivery, pauses, joins and music/voice balance. Verify rights to the specific music when used, smooth the start/end and preserve separate tracks. Missing listening/image capability means explicit pending scope, not acceptance based on transcripts or successful generation.

Deliver current audio, SRT/optional ASS, source/permission records, measured duration, configuration fingerprint and observations. Keep private voice references and service logs in the working project, outside public repositories.
