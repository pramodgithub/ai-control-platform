from dotenv import load_dotenv
load_dotenv()

from app.ingestion.policy_ingestor import ingest_policy_clause


policy_chunks = [
    {
        "policy_id": "SEC-01",
        "section_title": "Encryption at Rest",
        "clause_id": "2.1",
        "clause_text": "All personally identifiable information must be encrypted at rest using AES-256 or stronger encryption standards.",
        "domain": "SECURITY",
        "risk_category": "DATA_ENCRYPTION",
        "severity": "HIGH",
        "data_type": "PII",
        "regulatory_scope": "EU",
        "criticality_weight": 0.9
    },
    {
        "policy_id": "SEC-02",
        "section_title": "Anonymized Data Handling",
        "clause_id": "1.1",
        "clause_text": "Anonymized or aggregated analytics data that cannot identify individuals is permitted to be stored without encryption requirements.",
        "domain": "DATA_GOVERNANCE",
        "risk_category": "ANONYMIZED_DATA",
        "severity": "LOW",
        "data_type": "ANONYMIZED",
        "regulatory_scope": "GLOBAL",
        "criticality_weight": 0.1
    },
    {
        "policy_id": "SEC-03",
        "section_title": "Cross-Border Data Transfer",
        "clause_id": "3.1",
        "clause_text": "EU personal data must not be transferred outside the EU unless approved safeguards such as Standard Contractual Clauses are in place.",
        "domain": "COMPLIANCE",
        "risk_category": "DATA_TRANSFER",
        "severity": "HIGH",
        "data_type": "PII",
        "regulatory_scope": "EU",
        "criticality_weight": 0.8
    },
    {
        "policy_id": "SEC-04",
        "section_title": "Access Control",
        "clause_id": "2.1",
        "clause_text": "All systems storing customer data must enforce role-based access control (RBAC) to restrict unauthorized access.",
        "domain": "SECURITY",
        "risk_category": "ACCESS_CONTROL",
        "severity": "MEDIUM",
        "data_type": "CUSTOMER_DATA",
        "regulatory_scope": "GLOBAL",
        "criticality_weight": 0.6
    },
    {
        "policy_id": "SEC-05",
        "section_title": "Data Retention",
        "clause_id": "1.1",
        "clause_text": "Customer data must not be retained beyond 24 months without documented business justification.",
        "domain": "DATA_GOVERNANCE",
        "risk_category": "DATA_RETENTION",
        "severity": "MEDIUM",
        "data_type": "CUSTOMER_DATA",
        "regulatory_scope": "GLOBAL",
        "criticality_weight": 0.5
    },
    {
        "policy_id": "SEC-06",
        "section_title": "Multi-Factor Authentication",
        "clause_id": "1.1",
        "clause_text": "Administrative access to production systems must require multi-factor authentication (MFA).",
        "domain": "SECURITY",
        "risk_category": "ACCESS_CONTROL",
        "severity": "HIGH",
        "data_type": "SYSTEM_ACCESS",
        "regulatory_scope": "GLOBAL",
        "criticality_weight": 0.85
    },
    {
        "policy_id": "SEC-07",
        "section_title": "Data Residency",
        "clause_id": "2.1",
        "clause_text": "EU customer data must be stored within EU geographic regions unless explicit regulatory approval is obtained.",
        "domain": "COMPLIANCE",
        "risk_category": "DATA_RESIDENCY",
        "severity": "HIGH",
        "data_type": "PII",
        "regulatory_scope": "EU",
        "criticality_weight": 0.9
    },
    {
        "policy_id": "SEC-08",
        "section_title": "Right to Erasure",
        "clause_id": "3.2",
        "clause_text": "Upon verified request, customer personal data must be permanently deleted within 30 days.",
        "domain": "DATA_PRIVACY",
        "risk_category": "DATA_DELETION",
        "severity": "HIGH",
        "data_type": "PII",
        "regulatory_scope": "EU",
        "criticality_weight": 0.8
    },
    {
        "policy_id": "SEC-09",
        "section_title": "Audit Logging",
        "clause_id": "1.3",
        "clause_text": "All access to sensitive customer data must be logged and retained for a minimum of 12 months.",
        "domain": "SECURITY",
        "risk_category": "AUDIT_LOGGING",
        "severity": "MEDIUM",
        "data_type": "CUSTOMER_DATA",
        "regulatory_scope": "GLOBAL",
        "criticality_weight": 0.6
    },
    {
        "policy_id": "SEC-10",
        "section_title": "Automated Decision Transparency",
        "clause_id": "4.1",
        "clause_text": "Any automated system making decisions that materially impact customers must provide explainability and human appeal mechanisms.",
        "domain": "AI_GOVERNANCE",
        "risk_category": "AI_TRANSPARENCY",
        "severity": "MEDIUM",
        "data_type": "AI_DECISION",
        "regulatory_scope": "GLOBAL",
        "criticality_weight": 0.7
    }
]


if __name__ == "__main__":
    for policy in policy_chunks:
        print(f"Ingesting {policy['policy_id']} - {policy['clause_id']}")

        ingest_policy_clause(
            policy_id=policy["policy_id"],
            section_title=policy["section_title"],
            clause_id=policy["clause_id"],
            clause_text=policy["clause_text"],
            domain=policy["domain"],
            risk_category=policy["risk_category"],
            severity=policy["severity"],
            data_type=policy["data_type"],
            regulatory_scope=policy["regulatory_scope"],
            criticality_weight=policy["criticality_weight"]
        )

    print("\nAll policy chunks inserted successfully.")