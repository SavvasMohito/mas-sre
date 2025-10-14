"""
Script to prepare ISO 27001 Annex A controls for ingestion into Weaviate.

This script processes ISO 27001:2022 Annex A controls and converts them
into structured JSON format.

Source: ISO/IEC 27001:2022 Annex A
"""

import json
from pathlib import Path


def prepare_iso27001():
    """
    Prepare ISO 27001 Annex A controls as structured JSON.

    ISO 27001:2022 Annex A contains 93 controls across 4 themes:
    - Organizational controls
    - People controls
    - Physical controls
    - Technological controls
    """

    iso_controls = [
        # ORGANIZATIONAL CONTROLS
        {
            "standard_name": "ISO27001",
            "control_id": "A.5.1",
            "title": "Policies for Information Security",
            "description": "Information security policy and topic-specific policies should be defined, approved by management, published, communicated to and acknowledged by relevant personnel and relevant interested parties, and reviewed at planned intervals and if significant changes occur.",
            "category": "Organizational Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.5.7",
            "title": "Threat Intelligence",
            "description": "Information relating to information security threats should be collected and analyzed to produce threat intelligence.",
            "category": "Organizational Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.5.10",
            "title": "Acceptable Use of Information and Assets",
            "description": "Rules for the acceptable use and procedures for handling information and other associated assets should be identified, documented and implemented.",
            "category": "Organizational Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.5.14",
            "title": "Information Transfer",
            "description": "Information transfer rules, procedures, or agreements should be in place for all types of transfer facilities within the organization and between the organization and other parties.",
            "category": "Organizational Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.5.23",
            "title": "Information Security for Cloud Services",
            "description": "Processes for acquisition, use, management and exit from cloud services should be established in accordance with the organization's information security requirements.",
            "category": "Organizational Controls",
        },
        # PEOPLE CONTROLS
        {
            "standard_name": "ISO27001",
            "control_id": "A.6.1",
            "title": "Screening",
            "description": "Background verification checks on all candidates for employment should be carried out prior to joining the organization and on an ongoing basis taking into consideration applicable laws, regulations and ethics and be proportional to the business requirements, the classification of the information to be accessed and the perceived risks.",
            "category": "People Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.6.2",
            "title": "Terms and Conditions of Employment",
            "description": "The employment contractual agreements should state the employee's and the organization's responsibilities for information security.",
            "category": "People Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.6.3",
            "title": "Information Security Awareness, Education and Training",
            "description": "Personnel of the organization and relevant interested parties should receive appropriate information security awareness, education and training and regular updates of the organization's information security policy, topic-specific policies and procedures, as relevant for their job function.",
            "category": "People Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.6.4",
            "title": "Disciplinary Process",
            "description": "A disciplinary process should be formalized and communicated to take action against personnel and other relevant interested parties who have committed an information security policy violation.",
            "category": "People Controls",
        },
        # PHYSICAL CONTROLS
        {
            "standard_name": "ISO27001",
            "control_id": "A.7.1",
            "title": "Physical Security Perimeters",
            "description": "Security perimeters should be defined and used to protect areas that contain information and other associated assets.",
            "category": "Physical Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.7.2",
            "title": "Physical Entry",
            "description": "Secure areas should be protected by appropriate entry controls and access points.",
            "category": "Physical Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.7.4",
            "title": "Physical Security Monitoring",
            "description": "Premises should be continuously monitored for unauthorized physical access.",
            "category": "Physical Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.7.7",
            "title": "Clear Desk and Clear Screen",
            "description": "Clear desk rules for papers and removable storage media and clear screen rules for information processing facilities should be defined and appropriately enforced.",
            "category": "Physical Controls",
        },
        # TECHNOLOGICAL CONTROLS
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.1",
            "title": "User Endpoint Devices",
            "description": "Information stored on, processed by or accessible via user endpoint devices should be protected.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.2",
            "title": "Privileged Access Rights",
            "description": "The allocation and use of privileged access rights should be restricted and managed.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.3",
            "title": "Information Access Restriction",
            "description": "Access to information and other associated assets should be restricted in accordance with the established topic-specific policy on access control.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.5",
            "title": "Secure Authentication",
            "description": "Secure authentication technologies and procedures should be implemented based on information access restrictions and the topic-specific policy on access control.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.9",
            "title": "Configuration Management",
            "description": "Configurations, including security configurations, of hardware, software, services and networks should be established, documented, implemented, monitored and reviewed.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.10",
            "title": "Information Deletion",
            "description": "Information stored in information systems, devices or in any other storage media should be deleted when no longer required.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.11",
            "title": "Data Masking",
            "description": "Data masking should be used in accordance with the organization's topic-specific policy on access control and other related topic-specific policies, and business requirements, taking applicable legislation into consideration.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.16",
            "title": "Monitoring Activities",
            "description": "Networks, systems and applications should be monitored for anomalous behavior and appropriate action taken to evaluate potential information security incidents.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.23",
            "title": "Web Filtering",
            "description": "Access to external websites should be managed to reduce exposure to malicious content.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.24",
            "title": "Use of Cryptography",
            "description": "Rules for the effective use of cryptography, including cryptographic key management, should be defined and implemented.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.26",
            "title": "Application Security Requirements",
            "description": "Information security requirements should be identified, specified and approved when developing or acquiring applications.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.28",
            "title": "Secure Coding",
            "description": "Secure coding principles should be applied to software development.",
            "category": "Technological Controls",
        },
        {
            "standard_name": "ISO27001",
            "control_id": "A.8.31",
            "title": "Separation of Development, Test and Production Environments",
            "description": "Development, testing and production environments should be separated and secured.",
            "category": "Technological Controls",
        },
    ]

    # Save to prepared directory
    output_file = Path(__file__).parent / "prepared" / "iso27001.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(iso_controls, f, indent=2, ensure_ascii=False)

    print(f"ISO 27001 data prepared: {len(iso_controls)} controls")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    prepare_iso27001()
