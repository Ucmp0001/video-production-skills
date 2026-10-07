"""Check SRT syntax and timing. Readability warnings require actual review."""
import argparse
import json
import math
from pathlib import Path
import re

TIMING = re.compile(r"^(\d{2,}):([0-5]\d):([0-5]\d),(\d{3}) --> "
                    r"(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})$")


def seconds(groups):
    h, m, s, ms = map(int, groups)
    return 3600 * h + 60 * m + s + ms / 1000


def check(text, duration=None, max_cps=20.0, min_duration=0.65):
    if duration is not None and (not math.isfinite(duration) or duration < 0):
        raise ValueError("Duration must be finite and nonnegative")
    if not math.isfinite(max_cps) or max_cps <= 0:
        raise ValueError("max_cps must be finite and positive")
    if not math.isfinite(min_duration) or min_duration < 0:
        raise ValueError("min_duration must be finite and nonnegative")
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip()
    errors, warnings, cues = [], [], []
    if not normalized:
        return {"errors": [{"block": 0, "code": "empty_file"}], "warnings": [], "cues": 0}
    previous_start, previous_end = -1.0, -1.0
    for number, block in enumerate(re.split(r"\n[ \t]*\n", normalized), 1):
        lines = block.splitlines()
        if len(lines) < 3 or not re.fullmatch(r"\d+", lines[0]):
            errors.append({"block": number, "code": "invalid_structure"})
            continue
        if int(lines[0]) != number:
            errors.append({"block": number, "code": "nonsequential_index"})
        match = TIMING.fullmatch(lines[1])
        if not match:
            errors.append({"block": number, "code": "invalid_timestamp"})
            continue
        start, end = seconds(match.groups()[:4]), seconds(match.groups()[4:])
        content = "\n".join(lines[2:]).strip()
        if not content:
            errors.append({"block": number, "code": "empty_caption"})
        if end <= start:
            errors.append({"block": number, "code": "nonpositive_duration"})
        if start < previous_start:
            errors.append({"block": number, "code": "nonmonotonic_start"})
        if start < previous_end:
            warnings.append({"block": number, "code": "overlap"})
        if duration is not None and end > duration + 0.001:
            errors.append({"block": number, "code": "exceeds_media"})
        span = end - start
        if span > 0:
            visible = re.sub(r"<[^>]+>|\s", "", content)
            if span < min_duration:
                warnings.append({"block": number, "code": "short_hold"})
            if len(visible) / span > max_cps:
                warnings.append({"block": number, "code": "reading_speed",
                                 "characters_per_second": round(len(visible) / span, 2)})
        previous_start, previous_end = start, max(previous_end, end)
        cues.append((start, end))
    return {"errors": errors, "warnings": warnings, "cues": len(cues)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("srt", type=Path)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--max-cps", type=float, default=20)
    parser.add_argument("--min-duration", type=float, default=0.65)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()
    try:
        result = check(args.srt.read_text(encoding="utf-8-sig"), args.duration,
                       args.max_cps, args.min_duration)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"error_type": type(error).__name__}))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return int(bool(result["errors"] or (args.strict and result["warnings"])))


if __name__ == "__main__":
    raise SystemExit(main())
