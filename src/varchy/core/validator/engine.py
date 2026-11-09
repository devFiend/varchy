"""Deterministic 100-Point Validation and Readiness Scoring Engine."""

from varchy.core.models.blueprint import Blueprint
from varchy.core.models.common import RiskLevel, Severity
from varchy.core.models.validation import CategoryScore, ReadinessReport, ValidationIssue


class ValidationEngine:
    """
    Evaluates project blueprints deterministically.
    Total score is out of 100 points across 7 weighted categories.
    Any critical blocker flags the project as blocked regardless of numerical score.
    """

    MAX_SCORES = {
        "product_requirements": 20,
        "technical_architecture": 20,
        "uiux_specifications": 15,
        "development_planning": 15,
        "database_api_contracts": 10,
        "testing_strategy": 10,
        "security_deployment": 10,
    }

    def evaluate(self, blueprint: Blueprint) -> ReadinessReport:
        critical_blockers: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []
        recommendations: list[ValidationIssue] = []
        category_scores: list[CategoryScore] = []

        # 1. Product Requirements (20 pts)
        req_score, req_issues = self._evaluate_product(blueprint)
        category_scores.append(
            CategoryScore(
                category="product_requirements",
                max_points=self.MAX_SCORES["product_requirements"],
                awarded_points=req_score,
            )
        )
        self._sort_issues(req_issues, critical_blockers, warnings, recommendations)

        # 2. Technical Architecture (20 pts)
        arch_score, arch_issues = self._evaluate_architecture(blueprint)
        category_scores.append(
            CategoryScore(
                category="technical_architecture",
                max_points=self.MAX_SCORES["technical_architecture"],
                awarded_points=arch_score,
            )
        )
        self._sort_issues(arch_issues, critical_blockers, warnings, recommendations)

        # 3. UI/UX Specifications (15 pts)
        ux_score, ux_issues = self._evaluate_design(blueprint)
        category_scores.append(
            CategoryScore(
                category="uiux_specifications",
                max_points=self.MAX_SCORES["uiux_specifications"],
                awarded_points=ux_score,
            )
        )
        self._sort_issues(ux_issues, critical_blockers, warnings, recommendations)

        # 4. Development Planning (15 pts)
        plan_score, plan_issues = self._evaluate_planning(blueprint)
        category_scores.append(
            CategoryScore(
                category="development_planning",
                max_points=self.MAX_SCORES["development_planning"],
                awarded_points=plan_score,
            )
        )
        self._sort_issues(plan_issues, critical_blockers, warnings, recommendations)

        # 5. Database & API Contracts (10 pts)
        data_score, data_issues = self._evaluate_data_api(blueprint)
        category_scores.append(
            CategoryScore(
                category="database_api_contracts",
                max_points=self.MAX_SCORES["database_api_contracts"],
                awarded_points=data_score,
            )
        )
        self._sort_issues(data_issues, critical_blockers, warnings, recommendations)

        # 6. Testing Strategy (10 pts)
        test_score, test_issues = self._evaluate_testing(blueprint)
        category_scores.append(
            CategoryScore(
                category="testing_strategy",
                max_points=self.MAX_SCORES["testing_strategy"],
                awarded_points=test_score,
            )
        )
        self._sort_issues(test_issues, critical_blockers, warnings, recommendations)

        # 7. Security & Deployment (10 pts)
        sec_score, sec_issues = self._evaluate_security(blueprint)
        category_scores.append(
            CategoryScore(
                category="security_deployment",
                max_points=self.MAX_SCORES["security_deployment"],
                awarded_points=sec_score,
            )
        )
        self._sort_issues(sec_issues, critical_blockers, warnings, recommendations)

        # Check unconfirmed high-risk assumptions
        for asm in blueprint.assumptions:
            if not asm.confirmed and asm.risk_level == RiskLevel.HIGH:
                critical_blockers.append(
                    ValidationIssue(
                        category="assumptions",
                        severity=Severity.CRITICAL,
                        entity_id=asm.id,
                        message=f"Unconfirmed high-risk assumption: {asm.statement}",
                        suggestion="Confirm or resolve this assumption before proceeding to build.",
                    )
                )

        total_score = round(sum(cs.awarded_points for cs in category_scores), 1)
        passed = (total_score >= 80.0) and (len(critical_blockers) == 0)

        return ReadinessReport(
            total_score=total_score,
            max_score=100.0,
            passed=passed,
            category_scores=category_scores,
            critical_blockers=critical_blockers,
            warnings=warnings,
            recommendations=recommendations,
        )

    def _sort_issues(
        self,
        issues: list[ValidationIssue],
        critical: list[ValidationIssue],
        warnings: list[ValidationIssue],
        recs: list[ValidationIssue],
    ) -> None:
        for issue in issues:
            if issue.severity == Severity.CRITICAL:
                critical.append(issue)
            elif issue.severity == Severity.WARNING:
                warnings.append(issue)
            else:
                recs.append(issue)

    def _evaluate_product(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 20.0
        issues: list[ValidationIssue] = []

        if not bp.product.requirements:
            issues.append(
                ValidationIssue(
                    category="product_requirements",
                    severity=Severity.CRITICAL,
                    message="Blueprint contains zero product requirements.",
                )
            )
            return 0.0, issues

        # Check acceptance criteria for each requirement
        missing_ac = [r for r in bp.product.requirements if not r.acceptance_criteria]
        if missing_ac:
            deduction = min(8.0, len(missing_ac) * 2.0)
            score -= deduction
            for r in missing_ac:
                issues.append(
                    ValidationIssue(
                        category="product_requirements",
                        severity=Severity.WARNING,
                        entity_id=r.id,
                        message=f"Requirement '{r.title}' has no acceptance criteria.",
                        suggestion="Add concrete, verifiable acceptance criteria.",
                    )
                )

        if not bp.product.personas:
            score -= 3.0
            issues.append(
                ValidationIssue(
                    category="product_requirements",
                    severity=Severity.INFO,
                    message="No user personas defined.",
                )
            )

        return max(0.0, score), issues

    def _evaluate_architecture(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 20.0
        issues: list[ValidationIssue] = []

        if not bp.architecture.tech_stack:
            issues.append(
                ValidationIssue(
                    category="technical_architecture",
                    severity=Severity.CRITICAL,
                    message="No technology stack specified.",
                )
            )
            return 0.0, issues

        # Check justifications
        unjustified = [t for t in bp.architecture.tech_stack if not t.justification.strip()]
        if unjustified:
            score -= min(5.0, len(unjustified) * 1.5)
            for t in unjustified:
                issues.append(
                    ValidationIssue(
                        category="technical_architecture",
                        severity=Severity.WARNING,
                        message=f"Tech choice '{t.name}' lacks architecture trade-off rationale.",
                    )
                )

        if not bp.architecture.service_boundaries:
            score -= 3.0
            issues.append(
                ValidationIssue(
                    category="technical_architecture",
                    severity=Severity.INFO,
                    message="No explicit service boundaries defined.",
                )
            )

        return max(0.0, score), issues

    def _evaluate_design(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 15.0
        issues: list[ValidationIssue] = []

        if not bp.design.screens:
            issues.append(
                ValidationIssue(
                    category="uiux_specifications",
                    severity=Severity.WARNING,
                    message="No screen specifications defined.",
                )
            )
            return 4.0, issues

        for screen in bp.design.screens:
            if not screen.interaction_states:
                score -= 1.0
                issues.append(
                    ValidationIssue(
                        category="uiux_specifications",
                        severity=Severity.INFO,
                        entity_id=screen.id,
                        message=f"Screen '{screen.title}' has no defined interaction states (e.g. Loading/Error/Empty).",
                    )
                )

        return max(0.0, score), issues

    def _evaluate_planning(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 15.0
        issues: list[ValidationIssue] = []

        if not bp.planning.tasks:
            issues.append(
                ValidationIssue(
                    category="development_planning",
                    severity=Severity.CRITICAL,
                    message="No implementation tasks planned.",
                )
            )
            return 0.0, issues

        # Check for circular dependencies in tasks
        task_map = {t.id: t for t in bp.planning.tasks}
        cycle = self._detect_task_cycle(task_map)
        if cycle:
            issues.append(
                ValidationIssue(
                    category="development_planning",
                    severity=Severity.CRITICAL,
                    entity_id=cycle[0],
                    message=f"Circular dependency detected in tasks: {' -> '.join(cycle)}",
                    suggestion="Break the circular dependency cycle.",
                )
            )
            return 0.0, issues

        # Check orphaned tasks (tasks referring to non-existent REQs)
        known_req_ids = {r.id for r in bp.product.requirements}
        for task in bp.planning.tasks:
            for req_id in task.requirement_ids:
                if req_id not in known_req_ids:
                    score -= 2.0
                    issues.append(
                        ValidationIssue(
                            category="development_planning",
                            severity=Severity.WARNING,
                            entity_id=task.id,
                            message=f"Task '{task.id}' references non-existent requirement '{req_id}'.",
                        )
                    )

        return max(0.0, score), issues

    def _evaluate_data_api(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 10.0
        issues: list[ValidationIssue] = []

        if not bp.data_api.entities and not bp.data_api.endpoints:
            issues.append(
                ValidationIssue(
                    category="database_api_contracts",
                    severity=Severity.INFO,
                    message="No database entities or API endpoints defined.",
                )
            )
            return 5.0, issues

        # Check entities have primary keys
        for ent in bp.data_api.entities:
            has_pk = any(attr.is_primary_key for attr in ent.attributes)
            if not has_pk and ent.attributes:
                score -= 1.5
                issues.append(
                    ValidationIssue(
                        category="database_api_contracts",
                        severity=Severity.WARNING,
                        entity_id=ent.id,
                        message=f"Database entity '{ent.name}' has no defined primary key.",
                    )
                )

        return max(0.0, score), issues

    def _evaluate_testing(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 10.0
        issues: list[ValidationIssue] = []

        if not bp.testing.test_cases:
            issues.append(
                ValidationIssue(
                    category="testing_strategy",
                    severity=Severity.WARNING,
                    message="No concrete test cases specified.",
                )
            )
            return 2.0, issues

        # Verify test cases map to actual requirements or APIs
        known_targets = {r.id for r in bp.product.requirements} | {
            e.id for e in bp.data_api.endpoints
        }
        unmapped = [tc for tc in bp.testing.test_cases if tc.target_id not in known_targets]
        if unmapped:
            score -= min(4.0, len(unmapped) * 1.0)
            for tc in unmapped:
                issues.append(
                    ValidationIssue(
                        category="testing_strategy",
                        severity=Severity.WARNING,
                        entity_id=tc.id,
                        message=f"Test '{tc.id}' targets unknown entity '{tc.target_id}'.",
                    )
                )

        return max(0.0, score), issues

    def _evaluate_security(self, bp: Blueprint) -> tuple[float, list[ValidationIssue]]:
        score = 10.0
        issues: list[ValidationIssue] = []

        sec = bp.architecture.security
        if not sec.authentication.strip():
            score -= 3.0
            issues.append(
                ValidationIssue(
                    category="security_deployment",
                    severity=Severity.WARNING,
                    message="Authentication specification is empty.",
                )
            )

        if not sec.secret_management.strip():
            score -= 2.0
            issues.append(
                ValidationIssue(
                    category="security_deployment",
                    severity=Severity.WARNING,
                    message="Secret management strategy is not documented.",
                )
            )

        return max(0.0, score), issues

    def _detect_task_cycle(self, task_map: dict[str, any]) -> list[str] | None:
        """Cycle detection using depth-first search."""
        visited: set[str] = set()
        rec_stack: set[str] = set()
        cycle_path: list[str] = []

        def dfs(node: str, current_path: list[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            current_path.append(node)

            task = task_map.get(node)
            if task:
                for dep in task.dependencies:
                    if dep not in visited:
                        if dfs(dep, current_path):
                            return True
                    elif dep in rec_stack:
                        current_path.append(dep)
                        return True

            rec_stack.remove(node)
            current_path.pop()
            return False

        for task_id in task_map:
            if task_id not in visited:
                path: list[str] = []
                if dfs(task_id, path):
                    return path
        return None

