"""
Script to prepare NIST SP 800-53 Rev 5 data for ingestion into Weaviate.

This script processes NIST SP 800-53 controls from OSCAL format and converts
them into a structured JSON format compatible with the Weaviate schema.

Source: https://github.com/usnistgov/oscal-content/tree/v1.3.0/nist.gov/SP800-53/rev5/json
"""

import json
from pathlib import Path


def extract_prose(part: dict) -> str:
    """
    Recursively extract prose text from OSCAL part structure.

    Args:
        part: OSCAL part dictionary

    Returns:
        Combined prose text from the part and all nested parts
    """
    prose_parts = []

    # Add direct prose if present
    if "prose" in part:
        prose_parts.append(part["prose"])

    # Recursively process nested parts
    if "parts" in part:
        for subpart in part["parts"]:
            subprose = extract_prose(subpart)
            if subprose:
                prose_parts.append(subprose)

    return " ".join(prose_parts).strip()


def prepare_nist_sp80053():
    """
    Prepare NIST SP 800-53 Rev 5 controls from OSCAL catalog format.

    Reads from: data/raw/NIST_SP-800-53_rev5_catalog-min.json
    Outputs to: data/prepared/nist_sp80053.json

    The OSCAL format has:
    - catalog.groups[]: Control families (e.g., "ac" = Access Control)
    - Each group has controls[]: Individual controls (e.g., "ac-1")
    - Each control has parts[]: Statement, guidance, etc.
    """

    # Load raw NIST SP 800-53 OSCAL data
    raw_file = Path(__file__).parent / "raw" / "NIST_SP-800-53_rev5_catalog-min.json"

    if not raw_file.exists():
        print(f"Error: Raw NIST file not found at {raw_file}")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Extract catalog
    catalog = raw_data.get("catalog", {})
    groups = catalog.get("groups", [])

    # Transform the data structure
    nist_controls = []

    for group in groups:
        group_id = group.get("id", "").upper()  # e.g., "AC"
        group_title = group.get("title", "")  # e.g., "Access Control"

        # Process each control in the group
        for control in group.get("controls", []):
            control_id = control.get("id", "").upper()  # e.g., "AC-1"
            control_title = control.get("title", "")

            # Extract statement prose (main requirement text)
            statement_prose = ""
            guidance_prose = ""

            for part in control.get("parts", []):
                if part.get("name") == "statement":
                    statement_prose = extract_prose(part)
                elif part.get("name") == "guidance":
                    guidance_prose = extract_prose(part)

            # Use statement as primary description, append guidance if available
            if statement_prose:
                req_description = statement_prose
                if guidance_prose:
                    req_description += f" | Guidance: {guidance_prose}"
            elif control_title:
                req_description = control_title
            else:
                req_description = ""

            # Map to Weaviate schema format
            control_data = {
                "standard": "NIST",
                "req_id": control_id,  # e.g., "AC-1"
                "req_description": req_description,
                "chapter_id": group_id,  # e.g., "AC"
                "chapter_name": group_title,  # e.g., "Access Control"
                "section_id": group_id,  # Use group_id as section_id (NIST doesn't have sections)
                "section_name": group_title,  # Use group_title as section_name
                "level": "",  # NIST doesn't have OWASP-style levels
            }

            nist_controls.append(control_data)

    # Save to prepared directory
    output_file = Path(__file__).parent / "prepared" / "nist_sp80053.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(nist_controls, f, indent=2, ensure_ascii=False)

    print(f"NIST SP 800-53 Rev 5 data prepared: {len(nist_controls)} controls")
    print(f"Saved to: {output_file}")

    # Print summary by control family
    family_counts = {}
    for control in nist_controls:
        family = control.get("chapter_id", "Unknown")
        family_counts[family] = family_counts.get(family, 0) + 1

    print(f"\nControl families: {len(family_counts)}")
    print("Top 5 families by control count:")
    for family, count in sorted(family_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {family}: {count} controls")


if __name__ == "__main__":
    prepare_nist_sp80053()
