"""Hash a local source and optionally probe selected media fields. Never upload."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def source_entry(source):
    source = Path(source)
    if not source.is_file():
        raise ValueError("Source must be a regular file")
    digest = hashlib.sha256()
    with source.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    entry = {"filename": source.name, "bytes": source.stat().st_size,
             "sha256": digest.hexdigest(), "rights_status": "unknown",
             "probe_status": "unavailable"}
    if shutil.which("ffprobe"):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration:stream=codec_type,width,height,avg_frame_rate",
                 "-of", "json", str(source.resolve())],
                capture_output=True, timeout=30, check=True)
            raw = json.loads(result.stdout)
            entry["media"] = {
                "duration_seconds": raw.get("format", {}).get("duration"),
                "streams": [{k: s[k] for k in
                             ("codec_type", "width", "height", "avg_frame_rate") if k in s}
                            for s in raw.get("streams", [])]}
            entry["probe_status"] = "complete"
        except (subprocess.SubprocessError, OSError, ValueError):
            entry["probe_status"] = "failed"
    return entry


def write_manifest(source, output):
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise FileExistsError("Output already exists")
    data = {"schema_version": 1, "sources": [source_entry(source)]}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = write_manifest(args.source, args.output)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}))
        return 1
    print(json.dumps({"status": "complete", "sources": len(data["sources"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
