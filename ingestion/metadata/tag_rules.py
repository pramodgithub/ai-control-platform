import re

TAG_RULES = {
    "definition": [
        r"\bis\b defined\b",
        r"\brefers to\b",
        r"\bis\b a\b",
        r"\bthe term\b",
    ],

    "risk": [
        r"\brisk\b",
        r"\bthreat\b",
        r"\bvulnerability\b",
        r"\bnegative impact\b",
    ],

    "compliance": [
        r"\bISO\b",
        r"\bstandard\b",
        r"\bregulation\b",
        r"\brequirement\b",
        r"\bcompliance\b",
    ],

    "security-principle": [
        r"\bconfidentiality\b",
        r"\bintegrity\b",
        r"\bavailability\b",
    ],

    "access-control": [
        r"\baccess control\b",
        r"\bauthorised\b",
        r"\bprivilege\b",
        r"\bidentity\b",
    ],

    "incident-management": [
        r"\bincident\b",
        r"\brespons(e|e plan)\b",
        r"\breporting\b",
    ],

    "business-continuity": [
        r"\bbusiness continuity\b",
        r"\bdisaster recovery\b",
        r"\brecovery plan\b",
    ],

    "privacy": [
        r"\bprivacy\b",
        r"\bpersonal data\b",
        r"\bdata protection\b",
    ],

    "responsibilities": [
        r"\bresponsibilit(y|ies)\b",
        r"\broles?\b",
        r"\bduties\b",
        r"\bcommittee\b",
    ],

    "objectives": [
        r"\bobjective\b",
        r"\bstrategic\b",
        r"\bgoal\b",
    ],

    "policy-purpose": [
        r"\bpurpose of this document\b",
        r"\bthis policy aims\b",
        r"\bobjective of this policy\b",
        r"\bthis document establishes\b",
    ],

    "scope": [
        r"\bthis policy applies\b",
        r"\bapplicable to\b",
        r"\ball users\b",
        r"\ball employees\b",
    ],

    "asset-management": [
        r"\basset\b",
        r"\binformation assets\b",
        r"\bclassification\b",
        r"\bdata classification\b",
    ],
}
