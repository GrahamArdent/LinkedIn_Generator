from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def render_to_files(payload: dict[str, Any], out_dir: Path, basename: str) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{basename}.md"
    meta_path = out_dir / f"{basename}.meta.json"

    body = payload.get("body", "")
    first_comment = payload.get("first_comment", "")
    reply_prompts = payload.get("reply_prompts", {})

    md = []
    md.append(body)
    md.append("\n---\n")
    md.append("**First comment**\n")
    md.append(first_comment)
    if reply_prompts:
        md.append("\n---\n**Reply prompts**\n")
        for k, lst in reply_prompts.items():
            for s in lst:
                md.append(f"- ({k}) {s}")
    md_path.write_text("\n".join(md), encoding="utf-8")

    meta = {
        "persona": payload.get("persona"),
        "post_type": payload.get("post_type"),
        "citations": payload.get("citations", []),
        "metadata": payload.get("metadata", {}),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"md": md_path, "meta": meta_path}
