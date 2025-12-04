"""
Script to prepare ISO 27001 Annex A controls for ingestion into Weaviate.

This script processes ISO 27001:2022 Annex A controls from Secure Controls Framework (SCF)
and converts them into a structured JSON format compatible with the Weaviate schema.

Source: Secure Controls Framework (SCF) - https://github.com/securecontrolsframework/securecontrolsframework
"""

import json
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Install with: pip install pandas openpyxl")
    raise


def prepare_iso27001():
    """
    Prepare ISO 27001 Annex A controls from Secure Controls Framework Excel file.

    Reads from: data/raw/secure-controls-framework-scf-2025-3-1.xlsx
    Outputs to: data/prepared/iso27001.json

    ISO 27001:2022 Annex A contains 93 controls across 4 themes:
    - Organizational controls (A.5.x)
    - People controls (A.6.x)
    - Physical controls (A.7.x)
    - Technological controls (A.8.x)
    """

    # Load raw SCF Excel file
    raw_file = Path(__file__).parent / "raw" / "secure-controls-framework-scf-2025-3-1.xlsx"

    if not raw_file.exists():
        print(f"Error: Raw SCF file not found at {raw_file}")
        return

    # Read Excel file
    try:
        # Try to read the Excel file - may have multiple sheets
        excel_file = pd.ExcelFile(raw_file)
        print(f"Found {len(excel_file.sheet_names)} sheets: {excel_file.sheet_names[:5]}...")

        # Look for ISO 27001 data - try common sheet names
        iso_sheet = None
        for sheet_name in excel_file.sheet_names:
            # Look for sheets that might contain ISO 27001 data
            if any(keyword in sheet_name.lower() for keyword in ["iso", "27001", "annex", "control"]):
                iso_sheet = sheet_name
                break

        # If no specific sheet found, use the first sheet
        if not iso_sheet:
            iso_sheet = excel_file.sheet_names[0]
            print(f"No ISO-specific sheet found, using first sheet: {iso_sheet}")

        # Read the main SCF controls sheet
        df = pd.read_excel(excel_file, sheet_name="SCF 2025.3.1")
        print(f"Loaded sheet 'SCF 2025.3.1' with {len(df)} rows and {len(df.columns)} columns")

    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Find ISO 27001:2022 column
    iso_col = None
    for col in df.columns:
        if "iso" in str(col).lower() and "27001" in str(col).lower() and "2022" in str(col).lower():
            iso_col = col
            break

    # Find SCF control description column
    desc_col = None
    for col in df.columns:
        if "control description" in str(col).lower() or "scf" in str(col).lower() and "description" in str(col).lower():
            desc_col = col
            break

    # Find SCF control title/name column
    title_col = None
    for col in df.columns:
        if "scf control" in str(col).lower() and "description" not in str(col).lower():
            title_col = col
            break

    print("\nIdentified columns:")
    print(f"  ISO 27001:2022: {iso_col}")
    print(f"  Title: {title_col}")
    print(f"  Description: {desc_col}")

    if not iso_col:
        print("\nError: Could not find ISO 27001:2022 column")
        return

    # Extract ISO 27001 Annex A controls
    # SCF maps controls to ISO 27001 clauses, which may include Annex A references
    # We'll parse the ISO column to extract Annex A control IDs (A.X.X format)
    iso_controls_dict = {}  # Use dict to deduplicate controls

    for idx, row in df.iterrows():
        # Get ISO 27001:2022 mapping value (may contain multiple controls separated by newlines)
        iso_value = str(row[iso_col]).strip() if pd.notna(row[iso_col]) else ""

        if not iso_value or iso_value == "nan":
            continue

        # Get SCF control description and title
        scf_title = str(row[title_col]).strip() if title_col and pd.notna(row.get(title_col, "")) else ""
        scf_desc = str(row[desc_col]).strip() if desc_col and pd.notna(row.get(desc_col, "")) else ""

        # Parse ISO value - it may contain multiple control references separated by newlines
        # Format can be: "A.5.1", "5.1" (needs A. prefix), or multi-line
        iso_lines = iso_value.split("\n")

        for line in iso_lines:
            line = line.strip()
            if not line:
                continue

            # Extract Annex A control IDs (A.X.X format)
            # Also handle cases where it's just "5.1" which should become "A.5.1"
            control_id = None

            if line.startswith("A."):
                # Already in Annex A format
                parts = line.split()
                control_id = parts[0]  # Take first part (e.g., "A.5.1" from "A.5.1(a)")
            elif "." in line and line[0].isdigit():
                # Format like "5.1" - convert to "A.5.1"
                parts = line.split()
                first_part = parts[0]
                if first_part.count(".") >= 1:
                    control_id = f"A.{first_part.split('(')[0]}"  # Remove sub-items like "(a)"

            if not control_id or not control_id.startswith("A."):
                continue

            # Extract chapter from control ID (e.g., "A.5" from "A.5.1")
            parts = control_id.split(".")
            if len(parts) >= 2:
                chapter_id = f"{parts[0]}.{parts[1]}"  # e.g., "A.5"
            else:
                chapter_id = parts[0]  # e.g., "A"

            # Determine category/theme from control ID
            if chapter_id.startswith("A.5"):
                category = "Organizational Controls"
            elif chapter_id.startswith("A.6"):
                category = "People Controls"
            elif chapter_id.startswith("A.7"):
                category = "Physical Controls"
            elif chapter_id.startswith("A.8"):
                category = "Technological Controls"
            else:
                category = "General Controls"

            # Use SCF description if available, otherwise use title
            req_description = scf_desc if scf_desc else scf_title
            if not req_description:
                req_description = f"ISO 27001:2022 {control_id} - {category}"

            # Store control (deduplicate by control_id)
            if control_id not in iso_controls_dict:
                iso_controls_dict[control_id] = {
                    "standard": "ISO27001",
                    "req_id": control_id,  # e.g., "A.5.1"
                    "req_description": req_description,
                    "chapter_id": chapter_id,  # e.g., "A.5"
                    "chapter_name": category,  # e.g., "Organizational Controls"
                    "section_id": chapter_id,  # Use chapter_id as section_id
                    "section_name": category,  # Use category as section_name
                    "level": "",  # ISO 27001 doesn't have OWASP-style levels
                }
            else:
                # If control already exists, append additional description
                existing_desc = iso_controls_dict[control_id]["req_description"]
                if scf_desc and scf_desc not in existing_desc:
                    iso_controls_dict[control_id]["req_description"] += f" | {scf_desc}"

    # Convert dict to list
    iso_controls = list(iso_controls_dict.values())

    # Save to prepared directory
    output_file = Path(__file__).parent / "prepared" / "iso27001.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(iso_controls, f, indent=2, ensure_ascii=False)

    print(f"\nISO 27001 data prepared: {len(iso_controls)} controls")
    print(f"Saved to: {output_file}")

    # Print summary by category
    category_counts = {}
    for control in iso_controls:
        category = control.get("chapter_name", "Unknown")
        category_counts[category] = category_counts.get(category, 0) + 1

    print(f"\nControl categories: {len(category_counts)}")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} controls")


if __name__ == "__main__":
    prepare_iso27001()
