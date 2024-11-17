# type: ignore

import os
from typing import Any, Dict

from bv_app.db.db import Database
from bv_app.db.trending_videos import query_trending_videos
from bv_app.util.date import now_local
from bv_app.util.io import make_export_json, write_json


def gen_trending_json(db: Database, json_dir: str) -> Dict[str, Any]:
    todays_popular = query_trending_videos(db, 30)
    # Strip out the description to reduce payload size.
    for vid in todays_popular:
        vid.description = ""
    content: Dict[str, Any] = make_export_json(now_local(), todays_popular, "trending", "")
    if json_dir:
        out = os.path.join(json_dir, "trending.json")
        write_json(content=content, also_gzip=True, out_path=out)
    return content
