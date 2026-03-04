from .clause_mapper import extract_section_number
from .clause_mapper import detect_domain, detect_risk_category
from .clause_mapper import detect_severity, detect_data_type
from .clause_mapper import detect_regulatory_scope, compute_criticality
from policy_ingestor import ingest_policy_clause

def process_chunks(chunks, policy_id):
    for idx, chunk in enumerate(chunks):

        section_no = extract_section_number(chunk.section)
        clause_id = f"{section_no}.{idx+1}"

        domain = detect_domain(chunk.tags)
        risk_category = detect_risk_category(chunk.tags)
        severity = detect_severity(chunk.text)
        data_type = detect_data_type(chunk.text)
        regulatory_scope = detect_regulatory_scope(chunk.text)

        criticality_weight = compute_criticality(
            chunk.tags,
            severity,
            chunk.score
        )
        print(f"Ingesting {policy_id} - {clause_id} with risk {risk_category} and score {chunk.score}\n")
        ingest_policy_clause(
            policy_id=policy_id,
            section_title=chunk.section,
            clause_id=clause_id,
            clause_text=chunk.text,
            domain=domain,
            risk_category=risk_category,
            severity=severity,
            data_type=data_type,
            regulatory_scope=regulatory_scope,
            criticality_weight=criticality_weight
        )