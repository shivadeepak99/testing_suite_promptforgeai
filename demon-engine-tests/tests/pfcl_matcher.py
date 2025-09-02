
# ==========================
# tests/test_pfcl_matcher.py  (unit test stubs)
# ==========================
import json
from services.brain_engine.pfcl import PFCLParser
from services.brain_engine.compendium import Compendium
from services.brain_engine.matcher import TechniqueMatcher


def test_pfcl_parse_basic():
    p = PFCLParser()
    cmds, rem = p.parse("/clean /structure n=2 hello world")
    assert [c.name for c in cmds] == ["/clean","/structure"]
    assert rem == "hello world"


def test_matcher_selects_structure(tmp_path):
    # minimal compendium stub
    comp = {
        "defaults": {"budget_tokens": {"free": 1.0}},
        "pfcl": {"commands": {"/structure": {"maps_to": ["json_schema_guided"]}}},
        "scoring": {"signals": {"pfcl_alias": 2.0}},
        "techniques": [
            {"id":"json_schema_guided","aliases":["/structure"],"phase":["post"],"cost_estimate":{"tokens":0.5}}
        ]
    }
    path = tmp_path/"brain.json"; path.write_text(json.dumps(comp), encoding="utf-8")
    compo = Compendium.from_path(path)
    m = TechniqueMatcher(compo)
    cmds, rem = PFCLParser().parse("/structure make it json please")
    plan = m.select(rem, cmds, surface="web", tier="free")
    assert any(c["id"]=="json_schema_guided" for c in plan["chosen"])  # selected
