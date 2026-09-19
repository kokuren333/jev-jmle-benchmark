from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; RUNS=ROOT/'runs'
DATA.mkdir(exist_ok=True); RUNS.mkdir(exist_ok=True)

CHOICE_RE=re.compile(r'(?:^|\n\s*)([a-z])\s+(.+?)(?=(?:\n\s*[a-z]\s+)|\Z)', re.S|re.I)

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

def parse_choices(text:str):
    hits=CHOICE_RE.findall(text.strip())
    out={k.lower(): re.sub(r'\s+',' ',v).strip() for k,v in hits}
    if not out: return None,None
    first=re.search(r'(?:^|\n\s*)[a-z]\s+', text, re.I)
    stem=text[:first.start()].strip() if first else text.strip()
    return stem,out

def norm_answer(xs):
    if isinstance(xs, str): xs=[xs]
    return tuple(sorted(str(x).strip().lower() for x in xs))

def topk_from_probs(probs:dict[str,float], k:int):
    ranked=sorted(((str(a).lower(), float(p)) for a,p in probs.items()), key=lambda x:(-x[1], x[0]))
    return tuple(sorted(a for a,_ in ranked[:k]))

def dump_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def load_jsonish(v, default):
    if v is None: return default
    if isinstance(v,(dict,list)): return v
    s=str(v).strip()
    if not s: return default
    try: return json.loads(s)
    except Exception: return default

def has_image_reference(row:dict)->bool:
    dep=str(row.get('image_dependency') or '').strip().lower()
    if dep and dep!='none': return True
    paths=load_jsonish(row.get('image_paths_json'),{})
    if isinstance(paths,dict) and any(paths.values()): return True
    image=row.get('image')
    return bool(str(image).strip()) if image is not None else False
