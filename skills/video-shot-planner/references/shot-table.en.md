# Shot table

[中文](shot-table.md)

Adapt fields to the task rather than forcing one excessively wide table.

| shot_id | Global start/end (units) | Local zero | Voiceover / claim_id | Audience question / visual purpose | Initial state → event → result |
|---|---|---|---|---|---|

| shot_id | source_id / in/out | Speed / loop / crop | Captions / information | Sound event / real anchor | Sources / rights | Gap / alternative |
|---|---|---|---|---|---|---|

## Clock examples: mappings only
Without retiming: `local = global - shot_start`.
At speed r, starting at in_point: `source = in_point + local * r`.
Nested retiming, freezes and loops require mappings matched to the real tool, not blind reuse of these formulas.

Check entry, before/after events, result reading time, exit and adjacent joins. Display the conclusion only when exact numbers and visual states agree.
