"""Test script to view Weaviate database statistics."""

import os

import weaviate
import weaviate.classes as wvc
from dotenv import load_dotenv

load_dotenv()


def get_weaviate_stats():
    """Get statistics from the Weaviate database."""
    client = weaviate.connect_to_local(
        host=os.getenv("WEAVIATE_HOST", "localhost"),
        port=int(os.getenv("WEAVIATE_PORT", "8080")),
        grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
    )

    try:
        # Check if collection exists
        if not client.collections.exists("SecurityControl"):
            print("❌ SecurityControl collection does not exist!")
            return

        collection = client.collections.get("SecurityControl")

        # Get total count using aggregate
        total_count = collection.aggregate.over_all(total_count=True)
        print(f"\n{'='*50}")
        print(f"📊 WEAVIATE DATABASE STATISTICS")
        print(f"{'='*50}")
        print(f"\n📦 Total records: {total_count.total_count}")

        # Get counts per standard using aggregation
        print(f"\n{'─'*50}")
        print("📋 Records per standard:")
        print(f"{'─'*50}")

        # Aggregate by standard
        result = collection.aggregate.over_all(group_by=wvc.aggregate.GroupByAggregate(prop="standard"))

        standard_counts = {}
        for group in result.groups:
            standard_name = group.grouped_by.value
            count = group.total_count
            standard_counts[standard_name] = count

        # Sort by count descending
        sorted_standards = sorted(standard_counts.items(), key=lambda x: x[1], reverse=True)

        for standard, count in sorted_standards:
            percentage = (count / (total_count.total_count + 100) * 100) if total_count.total_count > 0 else 0
            bar = "█" * int(percentage / 2)
            print(f"  {standard:<20} {count:>6} ({percentage:>5.1f}%) {bar}")

        print(f"\n{'='*50}")

        # Show sample records from each standard
        print("\n📄 Sample records from each standard:")
        print(f"{'─'*50}")

        for standard, _ in sorted_standards[:5]:  # Show samples from top 5 standards
            sample = collection.query.fetch_objects(filters=wvc.query.Filter.by_property("standard").equal(standard), limit=2)
            print(f"\n  [{standard}]")
            for obj in sample.objects:
                req_id = obj.properties.get("req_id", "N/A")
                req_desc = obj.properties.get("req_description", "N/A")[:80]
                print(f"    • {req_id}: {req_desc}...")

    finally:
        client.close()


if __name__ == "__main__":
    get_weaviate_stats()
