import json
import os


def save_data(data: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, fp=f, ensure_ascii=False)


def load_data(path: str) -> dict:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                return json.load(fp=f, ensure_ascii=False)
    except:
        pass
    return {}
