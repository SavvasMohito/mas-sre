"""
Script to prepare NIST Cybersecurity Framework data for ingestion into Weaviate.

This script processes NIST CSF controls and converts them into structured JSON format.

Source: https://www.nist.gov/cyberframework
"""

import json
from pathlib import Path


def prepare_nist_csf():
    """
    Prepare NIST Cybersecurity Framework controls as structured JSON.

    This includes sample controls from the five core functions:
    - Identify (ID)
    - Protect (PR)
    - Detect (DE)
    - Respond (RS)
    - Recover (RC)
    """

    nist_controls = [
        # IDENTIFY
        {
            "standard_name": "NIST",
            "control_id": "ID.AM-1",
            "title": "Physical Devices and Systems Inventory",
            "description": "Physical devices and systems within the organization are inventoried.",
            "category": "Asset Management",
        },
        {
            "standard_name": "NIST",
            "control_id": "ID.AM-2",
            "title": "Software Platforms and Applications Inventory",
            "description": "Software platforms and applications within the organization are inventoried.",
            "category": "Asset Management",
        },
        {
            "standard_name": "NIST",
            "control_id": "ID.RA-1",
            "title": "Asset Vulnerabilities Identification",
            "description": "Asset vulnerabilities are identified and documented.",
            "category": "Risk Assessment",
        },
        {
            "standard_name": "NIST",
            "control_id": "ID.RA-2",
            "title": "Cyber Threat Intelligence",
            "description": "Cyber threat intelligence is received from information sharing forums and sources.",
            "category": "Risk Assessment",
        },
        {
            "standard_name": "NIST",
            "control_id": "ID.GV-1",
            "title": "Organizational Cybersecurity Policy",
            "description": "Organizational cybersecurity policy is established and communicated.",
            "category": "Governance",
        },
        # PROTECT
        {
            "standard_name": "NIST",
            "control_id": "PR.AC-1",
            "title": "Authorized User Identity Management",
            "description": "Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes.",
            "category": "Identity Management and Access Control",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.AC-3",
            "title": "Remote Access Management",
            "description": "Remote access is managed.",
            "category": "Identity Management and Access Control",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.AC-4",
            "title": "Access Permissions and Authorizations",
            "description": "Access permissions and authorizations are managed, incorporating the principles of least privilege and separation of duties.",
            "category": "Identity Management and Access Control",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.AT-1",
            "title": "Security Awareness Training",
            "description": "All users are informed and trained on their cybersecurity responsibilities.",
            "category": "Awareness and Training",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.DS-1",
            "title": "Data-at-Rest Protection",
            "description": "Data-at-rest is protected using encryption and other appropriate mechanisms.",
            "category": "Data Security",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.DS-2",
            "title": "Data-in-Transit Protection",
            "description": "Data-in-transit is protected using encryption and other security measures.",
            "category": "Data Security",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.DS-5",
            "title": "Data Leak Protection",
            "description": "Protections against data leaks are implemented.",
            "category": "Data Security",
        },
        {
            "standard_name": "NIST",
            "control_id": "PR.IP-1",
            "title": "Baseline Configuration",
            "description": "A baseline configuration of information technology/industrial control systems is created and maintained incorporating security principles.",
            "category": "Information Protection Processes",
        },
        # DETECT
        {
            "standard_name": "NIST",
            "control_id": "DE.AE-1",
            "title": "Baseline Network Operations",
            "description": "A baseline of network operations and expected data flows for users and systems is established and managed.",
            "category": "Anomalies and Events",
        },
        {
            "standard_name": "NIST",
            "control_id": "DE.AE-2",
            "title": "Detected Events Analysis",
            "description": "Detected events are analyzed to understand attack targets and methods.",
            "category": "Anomalies and Events",
        },
        {
            "standard_name": "NIST",
            "control_id": "DE.CM-1",
            "title": "Network Monitoring",
            "description": "The network is monitored to detect potential cybersecurity events.",
            "category": "Security Continuous Monitoring",
        },
        {
            "standard_name": "NIST",
            "control_id": "DE.CM-3",
            "title": "Personnel Activity Monitoring",
            "description": "Personnel activity is monitored to detect potential cybersecurity events.",
            "category": "Security Continuous Monitoring",
        },
        # RESPOND
        {
            "standard_name": "NIST",
            "control_id": "RS.RP-1",
            "title": "Response Plan Execution",
            "description": "Response plan is executed during or after an incident.",
            "category": "Response Planning",
        },
        {
            "standard_name": "NIST",
            "control_id": "RS.CO-1",
            "title": "Personnel Incident Notification",
            "description": "Personnel know their roles and order of operations when a response is needed.",
            "category": "Communications",
        },
        {
            "standard_name": "NIST",
            "control_id": "RS.AN-1",
            "title": "Incident Investigation",
            "description": "Notifications from detection systems are investigated.",
            "category": "Analysis",
        },
        {
            "standard_name": "NIST",
            "control_id": "RS.MI-1",
            "title": "Incident Containment",
            "description": "Incidents are contained to prevent further damage.",
            "category": "Mitigation",
        },
        # RECOVER
        {
            "standard_name": "NIST",
            "control_id": "RC.RP-1",
            "title": "Recovery Plan Execution",
            "description": "Recovery plan is executed during or after a cybersecurity incident.",
            "category": "Recovery Planning",
        },
        {
            "standard_name": "NIST",
            "control_id": "RC.IM-1",
            "title": "Recovery Plan Implementation",
            "description": "Recovery plans incorporate lessons learned from past incidents.",
            "category": "Improvements",
        },
        {
            "standard_name": "NIST",
            "control_id": "RC.CO-1",
            "title": "Public Relations Management",
            "description": "Public relations are managed during recovery operations.",
            "category": "Communications",
        },
    ]

    # Save to prepared directory
    output_file = Path(__file__).parent / "prepared" / "nist_csf.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(nist_controls, f, indent=2, ensure_ascii=False)

    print(f"NIST CSF data prepared: {len(nist_controls)} controls")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    prepare_nist_csf()
