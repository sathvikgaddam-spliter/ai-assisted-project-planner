import re
from typing import Dict, List


DOMAIN_KEYWORDS = {
    "analytics": [
        "power bi",
        "dashboard",
        "etl",
        "report",
        "reporting",
        "data pipeline",
        "metrics",
        "kpi",
    ],
    "software": [
        "app",
        "application",
        "platform",
        "saas",
        "tool",
        "tracker",
        "portal",
        "system",
        "web app",
        "e-commerce",
        "ecommerce",
        "mvp",
        "website",
        "api",
        "checkout",
        "mobile",
    ],
    "business": [
        "marketing",
        "campaign",
        "product launch",
        "launch plan",
        "go-to-market",
        "sales strategy",
        "brand",
    ],
    "academic": [
        "research",
        "study",
        "thesis",
        "literature review",
        "independent study",
        "academic",
    ],
    "healthcare": [
        "patient",
        "clinic",
        "healthcare",
        "hipaa",
        "appointment",
        "telemedicine",
        "ehr",
        "medical",
    ],
}

SOFTWARE_PRODUCT_KEYWORDS = [
    "app",
    "application",
    "platform",
    "saas",
    "tool",
    "tracker",
    "portal",
    "system",
    "web app",
]

VAGUE_PATTERNS = [
    r"\bsomething\b",
    r"\bproject\b$",
    r"\bapp\b$",
    r"\bdashboard\b$",
    r"\bfor students\b",
]

UNREALISTIC_TIMELINE_PATTERNS = [
    r"\bone week\b",
    r"\b1 week\b",
    r"\btwo weeks\b",
    r"\b2 weeks\b",
    r"\bin a week\b",
]

LARGE_SCOPE_KEYWORDS = [
    "enterprise",
    "marketplace",
    "payments",
    "inventory",
    "mobile apps",
    "analytics",
    "ehr integration",
    "billing",
    "video calls",
    "prescriptions",
    "hipaa-compliant",
]


def analyze_project(project_description: str) -> Dict[str, object]:
    """Return deterministic project understanding for Phase 1.

    This function is intentionally rule-based. It creates stable behavior for tests
    and preserves the future AI integration boundary.
    """
    description = project_description.strip()
    lowered = description.lower()

    domain = _infer_domain(lowered)
    project_type = _infer_project_type(lowered, domain)
    complexity = _infer_complexity(lowered, domain)
    warnings = _infer_warnings(lowered)
    missing_information = _infer_missing_information(lowered, domain)
    requires_clarification = domain == "unknown" or _is_vague(lowered)

    return {
        "domain": domain,
        "project_type": project_type,
        "complexity": complexity,
        "requires_clarification": requires_clarification,
        "missing_information": missing_information,
        "warnings": warnings,
    }


def _infer_domain(text: str) -> str:
    # Healthcare wins when compliance or clinical terms appear alongside software terms.
    if any(keyword in text for keyword in DOMAIN_KEYWORDS["healthcare"]):
        return "healthcare"

    # Product nouns like app/tracker/platform should win over analytics words
    # such as report when the request is clearly asking to build software.
    if _describes_software_product(text):
        return "software"

    for domain in ["analytics", "academic", "business", "software"]:
        if any(keyword in text for keyword in DOMAIN_KEYWORDS[domain]):
            return domain
    return "unknown"


def _describes_software_product(text: str) -> bool:
    has_product_keyword = any(keyword in text for keyword in SOFTWARE_PRODUCT_KEYWORDS)
    has_build_intent = any(term in text for term in ["build", "create", "develop", "design", "implement"])
    return has_product_keyword and has_build_intent


def _infer_project_type(text: str, domain: str) -> str:
    if domain == "analytics":
        if "power bi" in text:
            return "Power BI dashboard"
        if "etl" in text or "pipeline" in text:
            return "ETL reporting workflow"
        return "analytics reporting project"

    if domain == "software":
        if "saas" in text:
            return "SaaS platform"
        if "e-commerce" in text or "ecommerce" in text or "checkout" in text:
            return "e-commerce platform"
        if "delivery" in text:
            return "marketplace MVP"
        if "tracker" in text:
            return "software MVP"
        return "software application"

    if domain == "business":
        if "campaign" in text or "marketing" in text:
            return "digital marketing campaign"
        if "launch" in text:
            return "product launch plan"
        return "business planning project"

    if domain == "academic":
        if "independent study" in text:
            return "independent study plan"
        return "research workflow"

    if domain == "healthcare":
        return "healthcare workflow improvement"

    return "unknown project type"


def _infer_complexity(text: str, domain: str) -> str:
    large_scope_hits = sum(1 for keyword in LARGE_SCOPE_KEYWORDS if keyword in text)
    if large_scope_hits >= 4:
        return "high"
    if domain in {"healthcare", "software"} and large_scope_hits >= 2:
        return "high"
    if domain in {"software", "analytics", "healthcare"}:
        return "medium"
    if domain == "unknown":
        return "low"
    return "medium"


def _infer_warnings(text: str) -> List[str]:
    warnings = []
    has_unrealistic_timeline = any(re.search(pattern, text) for pattern in UNREALISTIC_TIMELINE_PATTERNS)
    large_scope_hits = sum(1 for keyword in LARGE_SCOPE_KEYWORDS if keyword in text)

    if has_unrealistic_timeline and large_scope_hits >= 3:
        warnings.append(
            "The requested scope appears unrealistic for the stated timeline. Reduce scope or extend the schedule."
        )
    elif has_unrealistic_timeline:
        warnings.append("The stated timeline may be aggressive and should be validated before planning execution.")

    if "hipaa" in text or "healthcare" in text or "patient" in text:
        warnings.append("Healthcare workflows may require privacy, compliance, and security review.")

    return warnings


def _infer_missing_information(text: str, domain: str) -> List[str]:
    missing = []

    if domain == "unknown":
        return [
            "project domain",
            "target users",
            "expected deliverable",
            "timeline",
            "success criteria",
        ]

    if not any(term in text for term in ["for ", "targeting", "users", "students", "managers", "staff", "patients"]):
        missing.append("target users")

    if not any(term in text for term in ["week", "month", "semester", "timeline", "deadline"]):
        missing.append("timeline")

    if domain in {"business", "analytics"} and "budget" not in text:
        missing.append("budget or resource constraints")

    return missing


def _is_vague(text: str) -> bool:
    if len(text.split()) < 4:
        return True
    if _describes_software_product(text) and any(
        keyword in text for keyword in ["tracker", "platform", "portal", "system", "tool", "web app"]
    ):
        return False
    return any(re.search(pattern, text) for pattern in VAGUE_PATTERNS) and len(text.split()) < 8
