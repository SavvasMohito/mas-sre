"""
Script to prepare OWASP ASVS data for ingestion into Weaviate.

This script processes OWASP ASVS (Application Security Verification Standard)
requirements and converts them into a structured JSON format.

Source: https://github.com/OWASP/ASVS
"""

import json
from pathlib import Path


def prepare_owasp_asvs():
    """
    Prepare OWASP ASVS controls as structured JSON.

    This is a sample structure. For production use, you should:
    1. Download the OWASP ASVS repository or documentation
    2. Parse the actual requirements from the source
    3. Extract all verification requirements
    """

    # Sample OWASP ASVS controls (expand with actual data)
    owasp_controls = [
        {
            "standard_name": "OWASP",
            "control_id": "V1.2.1",
            "title": "Security Architecture Documentation",
            "description": "Verify the use of a secure software development lifecycle that addresses security in all stages of development.",
            "category": "Architecture, Design and Threat Modeling",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V2.1.1",
            "title": "Password Strength Requirements",
            "description": "Verify that user set passwords are at least 12 characters in length.",
            "category": "Authentication",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V2.1.7",
            "title": "Password Complexity",
            "description": "Verify that passwords submitted during account registration, login, and password change are checked against a set of breached passwords either locally or using an external API.",
            "category": "Authentication",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V3.1.1",
            "title": "Session Token Requirements",
            "description": "Verify the application never reveals session tokens in URL parameters or error messages.",
            "category": "Session Management",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V4.1.1",
            "title": "Access Control Enforcement",
            "description": "Verify that the application enforces access control rules on a trusted service layer, especially if client-side access control is present and could be bypassed.",
            "category": "Access Control",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V5.1.1",
            "title": "Input Validation",
            "description": "Verify that the application has defenses against HTTP parameter pollution attacks, particularly if the application framework makes no distinction about the source of request parameters.",
            "category": "Validation, Sanitization and Encoding",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V5.3.1",
            "title": "Output Encoding",
            "description": "Verify that output encoding is relevant for the interpreter and context required.",
            "category": "Validation, Sanitization and Encoding",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V6.2.1",
            "title": "Cryptographic Standards",
            "description": "Verify that all cryptographic modules fail securely, and errors are handled in a way that does not enable Padding Oracle attacks.",
            "category": "Cryptography",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V7.1.1",
            "title": "Error Handling",
            "description": "Verify that the application does not log credentials or payment details. Session tokens should only be stored in logs in an irreversible, hashed form.",
            "category": "Error Handling and Logging",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V8.1.1",
            "title": "Data Protection in Transit",
            "description": "Verify the application protects sensitive data from being cached in server components such as load balancers and application caches.",
            "category": "Data Protection",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V8.2.1",
            "title": "Data Protection at Rest",
            "description": "Verify that all sensitive data is sent to the server in the HTTP message body or headers, and that query string parameters from any HTTP verb do not contain sensitive data.",
            "category": "Data Protection",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V9.1.1",
            "title": "Communications Security",
            "description": "Verify that TLS is used for all client connectivity, and does not fall back to insecure or unencrypted communications.",
            "category": "Communications",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V10.1.1",
            "title": "Malicious Code Protection",
            "description": "Verify that a code analysis tool is in use that can detect potentially malicious code, such as time functions, unsafe file operations and network connections.",
            "category": "Malicious Code",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V11.1.1",
            "title": "Business Logic Security",
            "description": "Verify the application will only process business logic flows for the same user in sequential step order and without skipping steps.",
            "category": "Business Logic",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V12.1.1",
            "title": "File Upload Validation",
            "description": "Verify that the application will not accept large files that could fill up storage or cause a denial of service.",
            "category": "File and Resources",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V13.1.1",
            "title": "API Security",
            "description": "Verify that all application components, libraries, modules, frameworks, platform, and operating systems are current and patched.",
            "category": "API and Web Service",
        },
        {
            "standard_name": "OWASP",
            "control_id": "V14.1.1",
            "title": "Configuration Hardening",
            "description": "Verify that the application build and deployment processes are performed in a secure and repeatable way, such as CI / CD automation.",
            "category": "Configuration",
        },
    ]

    # Save to prepared directory
    output_file = Path(__file__).parent / "prepared" / "owasp_asvs.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(owasp_controls, f, indent=2, ensure_ascii=False)

    print(f"OWASP ASVS data prepared: {len(owasp_controls)} controls")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    prepare_owasp_asvs()
