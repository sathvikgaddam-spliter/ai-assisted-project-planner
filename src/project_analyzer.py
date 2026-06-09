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
    "game",
    "platform",
    "saas",
    "tool",
    "tracker",
    "portal",
    "system",
    "web app",
    "website",
    "workflow",
]

BUILD_INTENT_TERMS = ["build", "create", "develop", "design", "implement", "plan"]

GENERIC_PROJECT_OBJECTS = {
    "app",
    "application",
    "project",
    "software",
    "system",
    "tool",
    "dashboard",
    "website",
    "platform",
    "something",
}

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

PROJECT_TYPE_KEYWORDS = {
    "marketplace": ["marketplace", "buyers", "sellers", "listings"],
    "ecommerce application": ["e-commerce", "ecommerce", "online store", "checkout", "cart", "commerce"],
    "AI application": ["ai", "chatbot", "rag", "llm", "model", "recommendation", "assistant"],
    "dashboard": ["dashboard", "analytics", "metrics", "kpi", "reporting", "charts"],
    "SaaS application": ["saas", "subscription", "tenant", "workspace"],
    "mobile application": ["mobile", "ios", "android"],
    "backend platform": ["api", "backend", "service", "platform"],
}

TYPE_FEATURE_RULES = {
    "marketplace": {
        "target_users": ["buyers", "sellers", "marketplace administrators"],
        "likely_user_roles": ["buyer", "seller", "admin"],
        "likely_workflows": ["listing creation", "search and discovery", "purchase transaction", "review and rating"],
        "core_features": ["listings", "buyer/seller profiles", "transactions", "reviews", "messaging"],
        "likely_data_entities": ["User", "Listing", "Transaction", "Review", "Message"],
        "frontend_needs": ["listing browsing", "seller listing management", "checkout flow", "review interface"],
        "backend_api_needs": ["listing APIs", "transaction APIs", "profile APIs", "review APIs"],
        "infrastructure_testing_assumptions": ["payment and transaction flows require integration testing"],
    },
    "ecommerce application": {
        "target_users": ["customers", "store administrators"],
        "likely_user_roles": ["customer", "admin"],
        "likely_workflows": ["product browsing", "cart management", "checkout", "order tracking"],
        "core_features": ["products", "cart", "orders", "payments", "inventory"],
        "likely_data_entities": ["Product", "Cart", "Order", "Payment", "InventoryItem"],
        "frontend_needs": ["product catalog", "cart UI", "checkout flow", "order status pages"],
        "backend_api_needs": ["product APIs", "cart APIs", "order APIs", "payment integration"],
        "infrastructure_testing_assumptions": ["checkout and inventory updates require transactional tests"],
    },
    "AI application": {
        "target_users": ["end users", "content administrators"],
        "likely_user_roles": ["user", "admin"],
        "likely_workflows": ["prompt submission", "AI response review", "feedback collection", "content management"],
        "core_features": ["chat or recommendation workflow", "model integration", "prompt handling", "response history"],
        "likely_data_entities": ["User", "Prompt", "AIResponse", "Feedback", "KnowledgeSource"],
        "frontend_needs": ["prompt input", "response display", "history view", "feedback controls"],
        "backend_api_needs": ["AI orchestration API", "prompt API", "history API", "feedback API"],
        "infrastructure_testing_assumptions": ["AI responses require fallback handling and evaluation tests"],
    },
    "dashboard": {
        "target_users": ["analysts", "managers", "report viewers"],
        "likely_user_roles": ["viewer", "analyst", "admin"],
        "likely_workflows": ["metric review", "filtering", "chart exploration", "report export"],
        "core_features": ["metrics", "filters", "charts", "reporting", "data refresh"],
        "likely_data_entities": ["Metric", "Report", "Dashboard", "Filter", "DataSource"],
        "frontend_needs": ["chart layout", "filter controls", "summary cards", "export controls"],
        "backend_api_needs": ["metrics APIs", "report APIs", "data refresh endpoints"],
        "infrastructure_testing_assumptions": ["metric calculations require data validation tests"],
    },
    "SaaS application": {
        "target_users": ["workspace users", "account administrators"],
        "likely_user_roles": ["user", "admin", "owner"],
        "likely_workflows": ["account setup", "workspace management", "subscription management", "team collaboration"],
        "core_features": ["authentication", "workspaces", "role management", "billing or subscription readiness"],
        "likely_data_entities": ["User", "Workspace", "Membership", "Subscription", "AuditLog"],
        "frontend_needs": ["dashboard shell", "settings screens", "team management UI", "billing screens"],
        "backend_api_needs": ["auth APIs", "workspace APIs", "membership APIs", "subscription APIs"],
        "infrastructure_testing_assumptions": ["multi-tenant authorization requires focused security tests"],
    },
    "mobile application": {
        "target_users": ["mobile users", "administrators"],
        "likely_user_roles": ["mobile user", "admin"],
        "likely_workflows": ["onboarding", "mobile task completion", "notifications", "profile management"],
        "core_features": ["mobile UI", "offline-aware flows", "push notifications", "account management"],
        "likely_data_entities": ["User", "Device", "Notification", "Session", "Preference"],
        "frontend_needs": ["responsive or native mobile screens", "onboarding flow", "notification UI"],
        "backend_api_needs": ["mobile API endpoints", "notification APIs", "profile APIs"],
        "infrastructure_testing_assumptions": ["mobile flows require device and responsive testing"],
    },
    "backend platform": {
        "target_users": ["developers", "internal operators"],
        "likely_user_roles": ["developer", "operator", "admin"],
        "likely_workflows": ["API consumption", "service monitoring", "administration", "integration setup"],
        "core_features": ["API endpoints", "service layer", "authentication", "observability"],
        "likely_data_entities": ["User", "APIResource", "ServiceConfig", "AuditLog"],
        "frontend_needs": ["admin console or API documentation UI"],
        "backend_api_needs": ["REST or RPC APIs", "auth middleware", "validation", "logging"],
        "infrastructure_testing_assumptions": ["APIs require contract tests and integration tests"],
    },
    "generic web application": {
        "target_users": ["end users", "administrators"],
        "likely_user_roles": ["user", "admin"],
        "likely_workflows": ["user onboarding", "core feature usage", "content or data management", "reporting"],
        "core_features": ["authentication", "dashboard", "CRUD workflows", "notifications"],
        "likely_data_entities": ["User", "Account", "Item", "Activity", "Notification"],
        "frontend_needs": ["responsive UI", "forms", "dashboard views", "navigation"],
        "backend_api_needs": ["CRUD APIs", "authentication APIs", "validation", "authorization"],
        "infrastructure_testing_assumptions": ["core workflows require unit, integration, and end-to-end tests"],
    },
}


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
    meaningful_project_intent = _has_meaningful_project_intent(lowered)
    build_pack_understanding = infer_build_pack_understanding(description, domain)
    requires_clarification = domain == "unknown" or _is_vague(lowered) or _is_short_incomplete_project(lowered, meaningful_project_intent, missing_information)

    return {
        "domain": domain,
        "project_type": project_type,
        "detected_project_type": build_pack_understanding["detected_project_type"],
        "build_pack_understanding": build_pack_understanding,
        "complexity": complexity,
        "requires_clarification": requires_clarification,
        "meaningful_project_intent": meaningful_project_intent,
        "missing_information": missing_information,
        "warnings": warnings,
    }


def infer_build_pack_understanding(project_description: str, domain: str = "unknown") -> Dict[str, object]:
    text = project_description.lower()
    detected_project_type = _detect_build_pack_project_type(text)
    rules = TYPE_FEATURE_RULES[detected_project_type]
    understanding = {key: list(value) for key, value in rules.items()}

    if any(term in text for term in ["planner", "scheduling", "schedule", "appointment", "calendar", "timeline"]):
        _merge_unique(understanding["likely_workflows"], ["scheduling", "reminder management", "timeline review"])
        _merge_unique(understanding["core_features"], ["tasks or events", "reminders", "timelines"])
        _merge_unique(understanding["likely_data_entities"], ["Task", "Event", "Reminder", "Timeline"])
        _merge_unique(understanding["frontend_needs"], ["calendar or timeline views", "reminder controls"])
        _merge_unique(understanding["backend_api_needs"], ["schedule APIs", "reminder APIs"])

    if any(term in text for term in ["file", "document", "upload", "approval", "metadata"]):
        _merge_unique(understanding["likely_workflows"], ["file upload", "metadata management", "permission review"])
        _merge_unique(understanding["core_features"], ["uploads", "storage", "metadata", "permissions"])
        _merge_unique(understanding["likely_data_entities"], ["Document", "FileUpload", "Metadata", "Permission"])
        _merge_unique(understanding["frontend_needs"], ["upload UI", "document list", "permission controls"])
        _merge_unique(understanding["backend_api_needs"], ["file APIs", "metadata APIs", "permission APIs"])

    if domain == "healthcare":
        _merge_unique(understanding["target_users"], ["patients", "healthcare staff"])
        _merge_unique(understanding["likely_user_roles"], ["patient", "staff", "administrator"])
        _merge_unique(understanding["infrastructure_testing_assumptions"], ["privacy and compliance requirements need security review"])

    return {
        "detected_project_type": detected_project_type,
        "target_users": understanding["target_users"],
        "likely_user_roles": understanding["likely_user_roles"],
        "likely_workflows": understanding["likely_workflows"],
        "core_features": understanding["core_features"],
        "likely_data_entities": understanding["likely_data_entities"],
        "frontend_needs": understanding["frontend_needs"],
        "backend_api_needs": understanding["backend_api_needs"],
        "infrastructure_testing_assumptions": understanding["infrastructure_testing_assumptions"],
    }


def _detect_build_pack_project_type(text: str) -> str:
    for project_type, keywords in PROJECT_TYPE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return project_type
    return "generic web application"


def _merge_unique(target: List[str], values: List[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


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
    if _has_meaningful_project_intent(text):
        return "software"
    return "unknown"


def _describes_software_product(text: str) -> bool:
    has_product_keyword = any(keyword in text for keyword in SOFTWARE_PRODUCT_KEYWORDS)
    has_build_intent = any(term in text for term in BUILD_INTENT_TERMS)
    return has_product_keyword and has_build_intent


def _infer_project_type(text: str, domain: str) -> str:
    if domain == "analytics":
        if "power bi" in text:
            return "Power BI dashboard"
        if "etl" in text or "pipeline" in text:
            return "ETL reporting workflow"
        return "analytics reporting project"

    if domain == "software":
        if "game" in text:
            return "game application"
        if "saas" in text:
            return "SaaS platform"
        if "e-commerce" in text or "ecommerce" in text or "checkout" in text:
            return "e-commerce platform"
        if "delivery" in text:
            return "marketplace MVP"
        if "tracker" in text:
            return "software MVP"
        if "website" in text:
            return "website project"
        if "workflow" in text:
            return "workflow automation project"
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


def _has_meaningful_project_intent(text: str) -> bool:
    words = [word.strip(".,:;!?()[]").lower() for word in text.split()]
    for index, word in enumerate(words):
        if word not in BUILD_INTENT_TERMS:
            continue
        object_words = [item for item in words[index + 1 :] if item not in {"a", "an", "the", "new", "simple"}]
        if len(object_words) < 2:
            return False
        if object_words[0] == "something":
            return False
        meaningful_words = [item for item in object_words if item not in GENERIC_PROJECT_OBJECTS]
        return bool(meaningful_words)
    return False


def _is_short_incomplete_project(text: str, meaningful_project_intent: bool, missing_information: List[str]) -> bool:
    return meaningful_project_intent and bool(missing_information) and len(text.split()) <= 5
