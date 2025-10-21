import json
from pathlib import Path

def read_json(p):
    return json.load(open(p))

def write_json(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    json.dump(obj, open(p,'w'), indent=2)
