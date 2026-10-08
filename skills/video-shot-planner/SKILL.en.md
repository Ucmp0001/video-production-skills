# Shots and asset coverage

[中文 / canonical entry](SKILL.md)

Use the latest voiceover, sources, available assets, aspect ratio and actual audio. With a recording, plan around real sentences/events. Without one, label timings as estimates; do not invent exact anchors.

## Connect planning to implementation
For every shot_id, use the [shot table](references/shot-table.en.md) to record voiceover, audience question, visual purpose, before/after states, main event, source interval, text/captions, sound, rights, gaps and alternatives.

A shot can supply evidence, action, scale, comparison, mechanism or essential information. Give each shot one main attention target. Labels name things; events explain them. Avoid visuals that merely repeat narration.

Distinguish assets already available, to shoot, to create, to research, pending permission and replaceable. Prefer directly relevant real material and preserve original sound when narratively useful. Irrelevant stock and rapid cuts cannot replace information.

## Three clocks
- Global: position on the final timeline.
- Shot-local: zero point of events within a shot.
- Source: original media in-point and speed mapping.

Use half-open frame intervals `[startFrame, endFrame)` with shared adjacent boundaries. Convert absolute time boundaries to frames instead of accumulating rounded segment durations. Explicitly map crop, speed, freeze, loops and nesting; do not interpret parent animation through a child's clock automatically.

## Preflight and delivery
Inspect the full intended source interval, aspect crop, original captions, evidence reading time and transitions. Do not create false conversations, reactions or co-presence through editing.

Plan initial state, change and result before complex effects. The opening image delivers the first sentence; the final shot helps answer the question. No fixed footage/animation share or cut frequency is required.

Deliver shot/coverage tables, key event anchors, gaps and low-risk alternatives. Follow the actual renderer's interface; these tables are not universal executable project files.
