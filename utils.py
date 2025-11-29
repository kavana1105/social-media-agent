# utils.py
import os
import json
import pandas as pd
from typing import List
from agent import PlanItem

def plan_to_dataframe(items: List[PlanItem]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=["post_date","platform","post_type","idea_title","key_points","cta","hashtags"])
    data = [item.model_dump() for item in items]
    return pd.DataFrame(data)

def save_session(name: str, plan_items: List[PlanItem], base_dir: str = "sessions") -> str:
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, f"{name}.json")
    data = [item.model_dump() for item in plan_items]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def load_session(path: str) -> List[PlanItem]:
    from agent import PlanItem  # local import to avoid circular
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [PlanItem(**x) for x in raw]