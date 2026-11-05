"""Small validated planning handoff shared by trials and the existing engine.

Meaning and selected narrative are caller-owned data, never a model rewrite.
A writing plan can annotate their beats, but cannot replace them with public copy.
"""
from copy import deepcopy

def _keys(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError("PLANNING_CONTRACT: unexpected or missing fields")

def _text(value, limit=600):
    if not isinstance(value, str) or not value.strip() or len(value)>limit:
        raise ValueError("PLANNING_CONTRACT: missing or unbounded planning text")

def freeze_handoff(meaning, narrative):
    _keys(meaning, ["thesis","reader_consequence","facts","qualification"])
    for key in ["thesis","reader_consequence","qualification"]:_text(meaning[key])
    facts=meaning["facts"]
    if not isinstance(facts,list) or not 1<=len(facts)<=2:
        raise ValueError("PLANNING_CONTRACT: one or two load-bearing facts required")
    ids=[]
    for fact in facts:
        _keys(fact,["claim_id","text","source_ids"])
        _text(fact["claim_id"],80);_text(fact["text"])
        if not isinstance(fact["source_ids"],list) or not fact["source_ids"]:
            raise ValueError("PLANNING_CONTRACT: source IDs required")
        for source in fact["source_ids"]:_text(source,100)
        ids.append(fact["claim_id"])
    if len(set(ids))!=len(ids):raise ValueError("PLANNING_CONTRACT: duplicate claim ID")
    _keys(narrative,["form","beats","symbol"])
    if narrative["form"] not in ("literal","symbolic"):
        raise ValueError("PLANNING_CONTRACT: unsupported narrative form")
    if not isinstance(narrative["beats"],list) or not 1<=len(narrative["beats"])<=8:
        raise ValueError("PLANNING_CONTRACT: narrative beats required")
    for beat in narrative["beats"]:_text(beat,240)
    symbol=narrative["symbol"]
    if narrative["form"]=="literal":
        if symbol is not None:raise ValueError("PLANNING_CONTRACT: literal form has no symbol")
    else:
        _keys(symbol,["image","mapping","boundary"])
        _text(symbol["image"],240);_text(symbol["boundary"],600)
        if not isinstance(symbol["mapping"],list) or not 1<=len(symbol["mapping"])<=6:
            raise ValueError("PLANNING_CONTRACT: symbolic mapping required")
        for part in symbol["mapping"]:
            _keys(part,["symbol_part","real_relationship"])
            for value in part.values():_text(value,240)
    return deepcopy({"version":1,"meaning":meaning,"narrative":narrative})

def attach_writing_plan(handoff, plan):
    base=freeze_handoff(handoff["meaning"],handoff["narrative"])
    _keys(plan,["beats","attribution"])
    beats=plan["beats"]
    if not isinstance(beats,list) or len(beats)!=len(base["narrative"]["beats"]):
        raise ValueError("PLANNING_CONTRACT: plan must cover selected beats")
    for index,beat in enumerate(beats,1):
        _keys(beat,["index","delivery"])
        if type(beat["index"]) is not int or beat["index"]!=index:
            raise ValueError("PLANNING_CONTRACT: selected beat order changed")
        _text(beat["delivery"],240)
    attribution=plan["attribution"]
    if not isinstance(attribution,list):raise ValueError("PLANNING_CONTRACT: attribution list required")
    ids=[]
    for claim in attribution:
        _keys(claim,["claim_id","source_name"])
        _text(claim["claim_id"],80);_text(claim["source_name"],120)
        ids.append(claim["claim_id"])
    if sorted(ids)!=sorted(f["claim_id"] for f in base["meaning"]["facts"]):
        raise ValueError("PLANNING_CONTRACT: attribution must cover frozen facts")
    base["writing_plan"]=deepcopy(plan)
    return base

def validate_handoff(handoff):
    if not isinstance(handoff,dict) or (type(handoff.get("version")) is not int or handoff.get("version")!=1):
        raise ValueError("PLANNING_CONTRACT: unsupported handoff")
    _keys(handoff,["version","meaning","narrative"]+(["writing_plan"] if "writing_plan" in handoff else []))
    result=freeze_handoff(handoff["meaning"],handoff["narrative"])
    return attach_writing_plan(result,handoff["writing_plan"]) if "writing_plan" in handoff else result

def plan_writing(handoff, voice, sources, client):
    """One optional planning call; reject malformed copy before any draft call."""
    import json
    frozen = validate_handoff(handoff)
    system = (
        "Plan delivery only. Return JSON with exactly beats and attribution. "
        "No post, title, hook sentences, body, editorial copy or finished paragraphs. "
        "Use short planning fragments, not publishable prose. "
        "The supplied meaning and selected narrative are frozen; do not rewrite or return them. "
        "Annotate EVERY selected beat in its supplied order. Each beats entry has exactly "
        "index (one-based integer) and delivery (at most 240 characters). "
        "Each attribution entry has exactly claim_id and source_name; cover every frozen fact once. "
        "Name only a supplied source publisher. Voice affects delivery inside the selected narrative. "
        "A symbol illustrates a relationship and contributes no evidence; retain its stated boundary."
    )
    raw = client.call(system, json.dumps({"handoff": frozen, "voice": voice, "sources": sources},
                                       ensure_ascii=False), response_json=True)["text"]
    try:
        plan = json.loads(raw)
    except (ValueError, TypeError) as exc:
        raise ValueError("PLANNING_CONTRACT: structured annotations required") from exc
    result = attach_writing_plan(frozen, plan)
    publishers = {s["source_id"]: str(s.get("publisher") or s.get("title") or "") for s in sources}
    facts = {f["claim_id"]: f for f in frozen["meaning"]["facts"]}
    for attribution in plan["attribution"]:
        names = {publishers.get(s) for s in facts[attribution["claim_id"]]["source_ids"]}
        if attribution["source_name"] not in names:
            raise ValueError("PLANNING_CONTRACT: attribution not bound to the fact source")
    return result
