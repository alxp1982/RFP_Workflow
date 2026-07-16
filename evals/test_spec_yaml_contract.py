"""Validate prd.spec.yaml / stories.spec.yaml shape and ID conventions (no LLM)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

FR_ID = re.compile(r"^FR-\d{2}$")
NFR_ID = re.compile(r"^NFR-\d{2}$")
STORY_ID = re.compile(r"^S\d{2}\.\d{2}\.\d{2}$")
EPIC_ID = re.compile(r"^E\d{2}$")
SCENARIO_KIND = frozenset({"happy", "edge"})


def load_yaml(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    assert isinstance(data, dict), f"{path} must parse to a mapping"
    return data


def validate_prd_spec(data: dict[str, Any], *, path_label: str) -> None:
    assert data.get("spec_version") == 1, f"{path_label}: spec_version must be 1"
    meta = data.get("meta")
    assert isinstance(meta, dict), f"{path_label}: meta must be an object"
    for key in ("product_name", "prd_status", "updated_at"):
        assert key in meta and meta[key] != "", f"{path_label}: meta.{key} required"

    scope = data.get("scope")
    assert isinstance(scope, dict), f"{path_label}: scope must be an object"
    assert isinstance(scope.get("in_scope"), list), f"{path_label}: scope.in_scope must be a list"
    assert isinstance(scope.get("out_of_scope"), list), f"{path_label}: scope.out_of_scope must be a list"

    req = data.get("requirements")
    assert isinstance(req, dict), f"{path_label}: requirements must be an object"
    frs = req.get("functional")
    nfrs = req.get("nonfunctional")
    assert isinstance(frs, list) and isinstance(nfrs, list), f"{path_label}: requirements.functional/nonfunctional must be lists"

    fr_ids: set[str] = set()
    for item in frs:
        assert isinstance(item, dict), f"{path_label}: functional item must be mapping"
        fid = item.get("id")
        assert isinstance(fid, str) and FR_ID.match(fid), f"{path_label}: bad FR id {fid!r}"
        assert item.get("title"), f"{path_label}: FR {fid} needs title"
        assert fid not in fr_ids, f"{path_label}: duplicate FR {fid}"
        fr_ids.add(fid)
        acc = item.get("acceptance", [])
        if acc is not None:
            assert isinstance(acc, list), f"{path_label}: acceptance must be list for {fid}"

    nfr_ids: set[str] = set()
    for item in nfrs:
        assert isinstance(item, dict), f"{path_label}: NFR item must be mapping"
        nid = item.get("id")
        assert isinstance(nid, str) and NFR_ID.match(nid), f"{path_label}: bad NFR id {nid!r}"
        assert item.get("title"), f"{path_label}: NFR {nid} needs title"
        assert nid not in nfr_ids, f"{path_label}: duplicate NFR {nid}"
        nfr_ids.add(nid)

    assert isinstance(data.get("assumptions"), list), f"{path_label}: assumptions must be list"
    assert isinstance(data.get("open_questions"), list), f"{path_label}: open_questions must be list"


def validate_stories_spec(data: dict[str, Any], *, path_label: str) -> None:
    assert data.get("spec_version") == 1, f"{path_label}: spec_version must be 1"
    meta = data.get("meta")
    assert isinstance(meta, dict), f"{path_label}: meta must be an object"
    for key in ("product_name", "updated_at"):
        assert key in meta and meta[key] != "", f"{path_label}: meta.{key} required"

    stories = data.get("stories")
    assert isinstance(stories, list) and stories, f"{path_label}: stories must be a non-empty list"
    seen: set[str] = set()
    for s in stories:
        assert isinstance(s, dict), f"{path_label}: story must be mapping"
        sid = s.get("id")
        assert isinstance(sid, str) and STORY_ID.match(sid), f"{path_label}: bad story id {sid!r}"
        assert sid not in seen, f"{path_label}: duplicate story {sid}"
        seen.add(sid)
        assert s.get("title"), f"{path_label}: story {sid} needs title"
        eid = s.get("epic_id")
        assert isinstance(eid, str) and EPIC_ID.match(eid), f"{path_label}: bad epic_id {eid!r}"
        assert s.get("persona") and s.get("user_story"), f"{path_label}: story {sid} needs persona and user_story"
        trace = s.get("prd_trace")
        assert isinstance(trace, list) and trace, f"{path_label}: story {sid} needs prd_trace list"
        for t in trace:
            assert isinstance(t, str), f"{path_label}: prd_trace entries must be strings"
            assert FR_ID.match(t) or NFR_ID.match(t), f"{path_label}: bad prd_trace id {t!r}"

        scenarios = s.get("scenarios")
        assert isinstance(scenarios, list) and scenarios, f"{path_label}: story {sid} needs scenarios"
        for sc in scenarios:
            assert isinstance(sc, dict), f"{path_label}: scenario must be mapping"
            assert sc.get("name"), f"{path_label}: scenario needs name"
            kind = sc.get("kind")
            assert kind in SCENARIO_KIND, f"{path_label}: scenario kind must be happy|edge"
            for key in ("setup", "steps", "assertions"):
                v = sc.get(key)
                assert isinstance(v, list) and v, f"{path_label}: scenario {sc.get('name')} needs {key} list"

        ac = s.get("acceptance_criteria")
        assert isinstance(ac, list) and ac, f"{path_label}: story {sid} needs acceptance_criteria"


def prd_trace_ids_from_stories(data: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for s in data["stories"]:
        for t in s["prd_trace"]:
            out.add(t)
    return out


def fr_nfr_ids_from_prd(data: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for item in data["requirements"]["functional"]:
        out.add(item["id"])
    for item in data["requirements"]["nonfunctional"]:
        out.add(item["id"])
    return out


@pytest.mark.parametrize(
    "rel_path",
    [
        "examples/minimal-prd.spec.yaml",
        "examples/minimal-stories.spec.yaml",
    ],
)
def test_minimal_examples_parse_and_validate(repo_root: Path, rel_path: str) -> None:
    path = repo_root / rel_path
    assert path.is_file(), f"missing {rel_path}"
    data = load_yaml(path)
    label = rel_path
    if "prd" in rel_path:
        validate_prd_spec(data, path_label=label)
    else:
        validate_stories_spec(data, path_label=label)


def test_stories_prd_trace_refs_exist_in_minimal_prd(repo_root: Path) -> None:
    prd = load_yaml(repo_root / "examples/minimal-prd.spec.yaml")
    stories = load_yaml(repo_root / "examples/minimal-stories.spec.yaml")
    validate_prd_spec(prd, path_label="prd")
    validate_stories_spec(stories, path_label="stories")
    allowed = fr_nfr_ids_from_prd(prd)
    for tid in prd_trace_ids_from_stories(stories):
        assert tid in allowed, f"story prd_trace {tid} not defined in prd.spec"


def test_skeleton_templates_are_valid_yaml(repo_root: Path) -> None:
    for rel in ("templates/prd.spec.yaml", "templates/stories.spec.yaml"):
        path = repo_root / rel
        text = path.read_text(encoding="utf-8")
        yaml.safe_load(text)
