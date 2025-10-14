"""Weaviate schema setup and data ingestion utilities."""

import json
import os
from pathlib import Path

import weaviate
import weaviate.classes as wvc
from dotenv import load_dotenv

load_dotenv()


def setup_weaviate_schema():
    """Initialize Weaviate schema for security controls."""
    client = weaviate.connect_to_local(
        host=os.getenv("WEAVIATE_HOST", "localhost"),
        port=int(os.getenv("WEAVIATE_PORT", "8080")),
        grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
    )

    try:
        # Delete collection if it exists
        if client.collections.exists("SecurityControl"):
            client.collections.delete("SecurityControl")
            print("Deleted existing SecurityControl collection")

        # Create collection with schema
        client.collections.create(
            name="SecurityControl",
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(model="text-embedding-3-small"),
            properties=[
                wvc.config.Property(
                    name="standard",
                    data_type=wvc.config.DataType.TEXT,
                    description="The security standard (e.g., OWASP, NIST, ISO27001)",
                ),
                wvc.config.Property(
                    name="control_id",
                    data_type=wvc.config.DataType.TEXT,
                    description="Unique identifier for the control",
                ),
                wvc.config.Property(
                    name="title",
                    data_type=wvc.config.DataType.TEXT,
                    description="Title of the security control",
                ),
                wvc.config.Property(
                    name="description",
                    data_type=wvc.config.DataType.TEXT,
                    description="Detailed description of the control",
                ),
                wvc.config.Property(
                    name="category",
                    data_type=wvc.config.DataType.TEXT,
                    description="Category or domain of the control",
                ),
                wvc.config.Property(
                    name="full_text",
                    data_type=wvc.config.DataType.TEXT,
                    description="Complete text for vectorization",
                ),
            ],
        )

        print("SecurityControl collection created successfully")

    finally:
        client.close()


def ingest_security_standards(data_dir: str = "src/security_requirements_system/data/prepared"):
    """Ingest security standards from JSON files into Weaviate."""
    client = weaviate.connect_to_local(
        host=os.getenv("WEAVIATE_HOST", "localhost"),
        port=int(os.getenv("WEAVIATE_PORT", "8080")),
        grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
    )

    try:
        collection = client.collections.get("SecurityControl")

        # Find all JSON files in the prepared data directory
        data_path = Path(data_dir)
        json_files = list(data_path.glob("*.json"))

        if not json_files:
            print(f"No JSON files found in {data_dir}")
            return

        total_imported = 0

        for json_file in json_files:
            print(f"Processing {json_file.name}...")

            with open(json_file, "r", encoding="utf-8") as f:
                controls = json.load(f)

            # Prepare batch import
            objects_to_insert = []
            for control in controls:
                # Combine fields for better vectorization
                full_text = f"{control.get('title', '')} " f"{control.get('description', '')} " f"{control.get('category', '')}"

                obj = {
                    "standard": control.get("standard_name", "Unknown"),
                    "control_id": control.get("control_id", ""),
                    "title": control.get("title", ""),
                    "description": control.get("description", ""),
                    "category": control.get("category", ""),
                    "full_text": full_text,
                }
                objects_to_insert.append(obj)

            # Batch insert
            if objects_to_insert:
                collection.data.insert_many(objects_to_insert)
                total_imported += len(objects_to_insert)
                print(f"  Imported {len(objects_to_insert)} controls from {json_file.name}")

        print(f"\nTotal controls imported: {total_imported}")

    finally:
        client.close()


if __name__ == "__main__":
    print("Setting up Weaviate schema...")
    setup_weaviate_schema()

    print("\nIngesting security standards data...")
    ingest_security_standards()
