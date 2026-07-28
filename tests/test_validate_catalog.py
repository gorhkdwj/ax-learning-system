from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.validate_catalog import CatalogValidator, build_parser


class CatalogValidatorTest(unittest.TestCase):
    """정상 카탈로그와 핵심 실패 유형을 실제 파일 단위로 검증합니다."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace_root = Path(__file__).resolve().parents[1]
        cls.schema_dir = cls.workspace_root / "schemas"

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temporary_directory.name) / "valid"
        shutil.copytree(
            self.workspace_root / "examples" / "valid",
            self.fixture_root,
        )
        promoted_reference_source = (
            self.workspace_root
            / "catalog"
            / "items"
            / "unit.foundation.evidence-verification"
            / "resources"
            / "content-provenance-reference"
            / "resource.json"
        )
        promoted_reference_target = (
            self.fixture_root
            / "catalog"
            / "items"
            / "unit.foundation.evidence-verification"
            / "resources"
            / "content-provenance-reference"
            / "resource.json"
        )
        promoted_reference_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(promoted_reference_source, promoted_reference_target)
        self.signal_root = Path(self.temporary_directory.name) / "signals"
        shutil.copytree(
            self.workspace_root / "research" / "signals",
            self.signal_root,
        )
        self.candidate_root = Path(self.temporary_directory.name) / "candidates"
        candidate_directory = (
            self.candidate_root / "candidate.domain.capability-name"
        )
        candidate_directory.mkdir(parents=True)
        candidate_path = candidate_directory / "candidate.json"
        shutil.copy2(
            self.workspace_root
            / "templates"
            / "research"
            / "capability-candidate.template.json",
            candidate_path,
        )
        candidate_data = json.loads(candidate_path.read_text(encoding="utf-8"))
        candidate_data["discovery"]["lens_id"] = "ax-strategy-value"
        candidate_data["taxonomy"]["major_domain"] = "ax-strategy-value"
        candidate_data["taxonomy"]["subdomains"] = ["opportunity-discovery"]
        candidate_path.write_text(
            json.dumps(candidate_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        self.handoff_root = Path(self.temporary_directory.name) / "handoffs"
        handoff_directory = self.handoff_root / "2026-07-26-claude-to-codex"
        handoff_directory.mkdir(parents=True)
        shutil.copy2(
            self.workspace_root
            / "templates"
            / "research"
            / "phase2-handoff.template.json",
            handoff_directory / "handoff.json",
        )
        self.taxonomy_root = Path(self.temporary_directory.name) / "taxonomy"
        shutil.copytree(
            self.workspace_root / "taxonomy",
            self.taxonomy_root,
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def validate(self):
        validator = CatalogValidator(
            workspace_root=self.workspace_root,
            schema_dir=self.schema_dir,
        )
        return validator.validate(
            [
                self.fixture_root,
                self.signal_root,
                self.candidate_root,
                self.handoff_root,
                self.taxonomy_root,
            ]
        )

    def mutate(
        self,
        relative_path: str,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = self.fixture_root / relative_path
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def mutate_signal(
        self,
        relative_path: str,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = self.signal_root / relative_path
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def mutate_candidate(
        self,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = (
            self.candidate_root
            / "candidate.domain.capability-name"
            / "candidate.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def mutate_handoff(
        self,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = (
            self.handoff_root
            / "2026-07-26-claude-to-codex"
            / "handoff.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def mutate_taxonomy(
        self,
        change: Callable[[dict[str, Any]], None],
    ) -> None:
        path = self.taxonomy_root / "taxonomy.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def codes(report) -> set[str]:
        return {issue.code for issue in report.issues}

    def test_default_roots_include_regular_catalog_and_sets(self) -> None:
        args = build_parser().parse_args([])

        self.assertIn("catalog", args.roots)
        self.assertIn("sets", args.roots)

    def test_valid_examples_pass(self) -> None:
        report = self.validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)
        self.assertEqual(
            report.counts,
            {
                "unit": 2,
                "resource": 5,
                "set": 1,
                "signal": 3,
                "candidate": 1,
                "handoff": 1,
                "taxonomy": 1,
            },
        )

    def test_candidate_unknown_taxonomy_node_is_rejected(self) -> None:
        self.mutate_candidate(
            lambda data: data["taxonomy"].update(
                major_domain="unknown-domain"
            )
        )

        self.assertIn("TAXONOMY_NODE_NOT_FOUND", self.codes(self.validate()))

    def test_candidate_subdomain_must_belong_to_major_domain(self) -> None:
        self.mutate_candidate(
            lambda data: data["taxonomy"].update(
                subdomains=["impact-evaluation"]
            )
        )

        self.assertIn("TAXONOMY_PARENT_MISMATCH", self.codes(self.validate()))

    def test_unit_taxonomy_reference_must_exist(self) -> None:
        self.mutate(
            "catalog/items/unit.foundation.evidence-verification/unit.json",
            lambda data: data["taxonomy"].update(
                subdomains=["unknown-subdomain"]
            ),
        )

        self.assertIn("TAXONOMY_NODE_NOT_FOUND", self.codes(self.validate()))

    def test_taxonomy_hierarchy_cycle_is_rejected(self) -> None:
        def create_cycle(data: dict[str, Any]) -> None:
            nodes = {node["id"]: node for node in data["nodes"]}
            nodes["opportunity-discovery"]["parent_ids"] = ["value-framing"]
            nodes["value-framing"]["parent_ids"] = ["opportunity-discovery"]

        self.mutate_taxonomy(create_cycle)

        self.assertIn("TAXONOMY_HIERARCHY_CYCLE", self.codes(self.validate()))

    def test_taxonomy_external_mapping_framework_must_exist(self) -> None:
        def break_framework_reference(data: dict[str, Any]) -> None:
            node = next(
                item
                for item in data["nodes"]
                if item["id"] == "ax-strategy-value"
            )
            node["external_mappings"][0]["framework_id"] = "unknown-framework"

        self.mutate_taxonomy(break_framework_reference)

        self.assertIn(
            "TAXONOMY_FRAMEWORK_NOT_FOUND",
            self.codes(self.validate()),
        )

    def test_invalid_id_is_rejected_by_schema(self) -> None:
        self.mutate(
            "catalog/items/unit.foundation.evidence-verification/unit.json",
            lambda data: data.update(id="invalid id"),
        )

        self.assertIn("SCHEMA_ERROR", self.codes(self.validate()))

    def test_absolute_local_path_is_rejected(self) -> None:
        self.mutate(
            "catalog/items/unit.foundation.evidence-verification/resources/guide/resource.json",
            lambda data: data["location"].update(path="C:/absolute/content.md"),
        )

        codes = self.codes(self.validate())
        self.assertIn("SCHEMA_ERROR", codes)
        self.assertIn("UNSAFE_LOCAL_PATH", codes)

    def test_missing_exact_reference_is_rejected(self) -> None:
        self.mutate(
            "sets/set.workflow.evidence-based-briefing/set.json",
            lambda data: data["steps"][1]["unit_ref"].update(version="9.9.9"),
        )

        self.assertIn("MISSING_REFERENCE", self.codes(self.validate()))

    def test_unit_prerequisite_cycle_is_rejected(self) -> None:
        self.mutate(
            "catalog/items/unit.foundation.evidence-verification/unit.json",
            lambda data: data["relations"].append(
                {
                    "type": "prerequisite",
                    "target": {
                        "id": "unit.ai.grounded-output-evaluation",
                        "version": "1.0.0",
                    },
                    "required_level": "D2",
                }
            ),
        )

        self.assertIn("UNIT_PREREQUISITE_CYCLE", self.codes(self.validate()))

    def test_set_step_cycle_is_rejected(self) -> None:
        self.mutate(
            "sets/set.workflow.evidence-based-briefing/set.json",
            lambda data: data["steps"][0].update(
                depends_on=["evaluate-grounding"]
            ),
        )

        self.assertIn("SET_STEP_CYCLE", self.codes(self.validate()))

    def test_duplicate_id_and_version_is_rejected(self) -> None:
        source = (
            self.fixture_root
            / "catalog/items/unit.foundation.evidence-verification/unit.json"
        )
        duplicate = self.fixture_root / "catalog/items/duplicate/unit.json"
        duplicate.parent.mkdir(parents=True)
        shutil.copy2(source, duplicate)

        self.assertIn("DUPLICATE_ID_VERSION", self.codes(self.validate()))

    def test_owner_backreference_is_required(self) -> None:
        self.mutate(
            "catalog/items/unit.foundation.evidence-verification/unit.json",
            lambda data: data["resource_refs"].pop(0),
        )

        self.assertIn("OWNER_BACKREFERENCE_MISSING", self.codes(self.validate()))

    def test_every_outcome_needs_a_required_check(self) -> None:
        self.mutate(
            "catalog/items/unit.foundation.evidence-verification/unit.json",
            lambda data: data["validation"]["checks"][0][
                "learning_outcome_ids"
            ].remove("outcome.foundation.evidence-verification.guided"),
        )

        self.assertIn(
            "OUTCOME_WITHOUT_REQUIRED_CHECK",
            self.codes(self.validate()),
        )

    def test_signal_claim_must_reference_existing_evidence(self) -> None:
        self.mutate_signal(
            "signal.agent.agent-harness/signal.json",
            lambda data: data["claims"][0]["evidence_refs"][0].update(
                id="evidence.missing"
            ),
        )

        self.assertIn("SIGNAL_EVIDENCE_NOT_FOUND", self.codes(self.validate()))

    def test_signal_status_history_must_match_current_status(self) -> None:
        self.mutate_signal(
            "signal.agent.agent-control-loop/signal.json",
            lambda data: data["status_history"][-1].update(status="watching"),
        )

        self.assertIn("SIGNAL_STATUS_HISTORY", self.codes(self.validate()))

    def test_signal_related_reference_requires_exact_version(self) -> None:
        self.mutate_signal(
            "signal.agent.agent-harness/signal.json",
            lambda data: data["related_signal_refs"][0]["target"].update(
                version="9.9.9"
            ),
        )

        self.assertIn("MISSING_REFERENCE", self.codes(self.validate()))

    def test_cross_signal_name_collision_is_reported_as_warning(self) -> None:
        self.mutate_signal(
            "signal.agent.agent-control-loop/signal.json",
            lambda data: data["aliases"].append(
                {
                    "value": "Agent harness",
                    "kind": "synonym",
                    "language": "en",
                }
            ),
        )

        report = self.validate()
        self.assertTrue(report.is_valid)
        self.assertIn("SIGNAL_NAME_COLLISION", self.codes(report))

    def test_substantiated_signal_cannot_have_unresolved_critical_claim(self) -> None:
        self.mutate_signal(
            "signal.agent.agent-harness/signal.json",
            lambda data: data["claims"][0].update(status="unverified"),
        )

        self.assertIn("SIGNAL_NOT_SUBSTANTIATED", self.codes(self.validate()))

    def test_signal_hierarchy_cycle_is_rejected(self) -> None:
        self.mutate_signal(
            "signal.agent.agent-harness/signal.json",
            lambda data: data["related_signal_refs"][0].update(
                type="broader_than"
            ),
        )
        self.mutate_signal(
            "signal.agent.agent-control-loop/signal.json",
            lambda data: data["related_signal_refs"][0].update(
                type="broader_than"
            ),
        )

        self.assertIn("SIGNAL_HIERARCHY_CYCLE", self.codes(self.validate()))

    def test_accepted_candidate_requires_authoritative_evidence(self) -> None:
        def change(data):
            data["decision"].update(status="accepted", confidence="high")
            data["evidence"][0]["source_type"] = "community_signal"

        self.mutate_candidate(change)

        self.assertIn("CANDIDATE_NOT_ACCEPTABLE", self.codes(self.validate()))

    def test_candidate_merge_target_requires_exact_version(self) -> None:
        def change(data):
            data["classification"] = {
                "candidate_kind": "capability",
                "proposed_destination": "merge_existing",
                "merge_target": {
                    "kind": "unit",
                    "id": "unit.foundation.evidence-verification",
                    "version": "9.9.9",
                },
                "rationale": "기존 Unit과 학습성과가 동일하다고 판정했습니다.",
            }
            data["decision"].update(
                status="merged",
                confidence="medium",
                rationale="기존 Unit으로 병합할 후보입니다.",
            )

        self.mutate_candidate(change)

        self.assertIn("MISSING_REFERENCE", self.codes(self.validate()))

    def test_candidate_relation_requires_exact_version(self) -> None:
        self.mutate_candidate(
            lambda data: data["relations"].append(
                {
                    "type": "requires",
                    "target": {
                        "kind": "candidate",
                        "id": "candidate.domain.capability-name",
                        "version": "9.9.9",
                    },
                    "rationale": "정확한 후보 버전의 선행관계를 검증합니다.",
                }
            )
        )

        self.assertIn("MISSING_REFERENCE", self.codes(self.validate()))

    def test_candidate_relation_cycle_is_rejected(self) -> None:
        first_path = (
            self.candidate_root
            / "candidate.domain.capability-name"
            / "candidate.json"
        )
        first = json.loads(first_path.read_text(encoding="utf-8"))
        first["relations"].append(
            {
                "type": "requires",
                "target": {
                    "kind": "candidate",
                    "id": "candidate.domain.second-capability",
                    "version": "1.0.0",
                },
                "rationale": "두 번째 후보를 선수로 요구합니다.",
            }
        )
        first_path.write_text(
            json.dumps(first, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        second = json.loads(json.dumps(first))
        second["id"] = "candidate.domain.second-capability"
        second["title"] = "두 번째 후보 역량"
        second["canonical_name"] = "Second candidate capability"
        second["aliases"] = ["Second capability"]
        second["classification"]["proposed_unit_id"] = (
            "unit.domain.second-capability"
        )
        second["relations"] = [
            {
                "type": "requires",
                "target": {
                    "kind": "candidate",
                    "id": "candidate.domain.capability-name",
                    "version": "1.0.0",
                },
                "rationale": "첫 번째 후보를 선수로 요구합니다.",
            }
        ]
        second_directory = (
            self.candidate_root / "candidate.domain.second-capability"
        )
        second_directory.mkdir(parents=True)
        (second_directory / "candidate.json").write_text(
            json.dumps(second, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        self.assertIn(
            "CANDIDATE_RELATION_CYCLE",
            self.codes(self.validate()),
        )

    def test_handoff_candidate_total_must_match_disposition_counts(self) -> None:
        self.mutate_handoff(
            lambda data: data["execution"]["counts"].update(
                candidates_total=1,
            )
        )

        codes = self.codes(self.validate())
        self.assertIn("HANDOFF_COUNT_MISMATCH", codes)
        self.assertIn("HANDOFF_DECISION_COUNT_MISMATCH", codes)
        self.assertIn("HANDOFF_WORK_PACKAGE_COUNT_MISMATCH", codes)

    def test_handoff_requires_true_attestations(self) -> None:
        self.mutate_handoff(
            lambda data: data["attestations"].update(
                unverified_claims_disclosed=False,
            )
        )

        self.assertIn("SCHEMA_ERROR", self.codes(self.validate()))

    def test_phase_complete_handoff_requires_complete_coverage(self) -> None:
        def change(data):
            data["status"] = "phase_complete"
            data["scope"]["ended_at"] = "2026-07-26"
            data["resume"]["approval_required"] = False
            data["approval"].update(
                status="approved",
                approved_at="2026-07-26",
                approved_by="user",
            )
            for field_name in (
                "source_audit",
                "taxonomy_audit",
                "practicality_audit",
            ):
                data["quality"][field_name]["result"] = "pass"

        self.mutate_handoff(change)

        self.assertIn(
            "HANDOFF_PHASE_COVERAGE_INCOMPLETE",
            self.codes(self.validate()),
        )

    def test_handoff_missing_artifact_is_rejected(self) -> None:
        self.mutate_handoff(
            lambda data: data["artifacts"][0].update(
                path="research/capability-survey/missing.md",
            )
        )

        self.assertIn("LOCAL_PATH_NOT_FOUND", self.codes(self.validate()))


if __name__ == "__main__":
    unittest.main()
