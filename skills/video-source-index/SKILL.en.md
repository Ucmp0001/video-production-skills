# Video source index

[中文 / canonical entry](SKILL.md)

Use for existing videos, interviews, screen recordings and references. Metadata, transcription and visual observation provide different evidence; none replaces the others.

## Procedure
Bundled tool: [source_manifest.py](scripts/source_manifest.py).

1. Preserve originals. Record source_id, filename, hash, media properties, provenance and acquisition method. Resolve `skill_dir` to the directory containing the installed `SKILL.md`. Run `python "<skill_dir>/scripts/source_manifest.py" "<absolute-source-path>" --output "<new-absolute-manifest-path>"` from any working directory. The tool saves filenames and selected properties; keep full local paths only in the user's working project.
2. Check available tools. ffprobe reads properties; ASR produces transcript candidates. Preserve original interview sound and meaning. Confirm permission to upload before external transcription; prefer local tools when available.
3. Sample broadly, then inspect key transitions, actions, charts and intended source intervals more closely. Actually open frames with image capability and watch/listen at normal speed when available. State the scope if only stills or transcripts were inspected.
4. Use the [index template](references/content-index.en.md) for time ranges, visible objects/text, speech, sound events, claims and reusable clips. Separate direct observation, automatic transcription, the original author's claims and editorial judgment.
5. Check the entire intended interval, including subjects, existing captions, crop and context. A matching title or single frame does not establish suitability. Track acquisition, rights verification, actual edit use, rejection or specific blockers.

## Boundaries and delivery
Check factual citation and media usage rights separately. Public availability and attribution do not automatically grant commercial permission. Generic stock is not footage of a particular company's event; generated media is not documentary evidence. Repeated ASR phrases, music hallucinations and unknown speakers need listening before summarization.

Deliver the source manifest, content index, usable intervals, rights and gaps. Mark missing files as not acquired, unheard speech as candidate transcription and unseen intervals as unknown. Indexing does not prove full audiovisual acceptance.
