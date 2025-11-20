"""Weaviate tool for querying security standards."""

import os
from typing import Optional, Type

import weaviate
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from weaviate.classes.query import Filter


class WeaviateQueryInput(BaseModel):
    """Input schema for WeaviateQueryTool.

    CRITICAL: This tool expects a dictionary with 'query' (string) and optionally 'limit' (int).
    Do NOT pass arrays or include previous tool results.
    """

    query: str = Field(
        ...,
        description="The search query string to find relevant security controls. Example: 'authentication', 'encryption', 'access control'. Must be a string, not an array or object.",
    )
    limit: int = Field(default=4, description="Number of results to return. Must be an integer (e.g., 4, 5, 8). Default is 4. Use 4 for focused results.")
    standard_filter: Optional[str] = Field(
        default=None,
        description="Optional filter by specific standard: 'OWASP', 'NIST', or 'ISO27001'. Leave as None/null to search all standards. Usually not needed.",
    )


class WeaviateQueryTool(BaseTool):
    """Tool to query Weaviate for security standards and controls."""

    name: str = "Query Security Standards Database"
    description: str = (
        "Search security standards database (OWASP ASVS, NIST SP 800-53, ISO 27001). "
        "Call with: {{'query': 'search term', 'limit': 4}}. "
        "Use limit=4 to get a focused set of results. Do NOT include previous results. "
        "Returns matching controls with exact IDs and descriptions."
    )
    args_schema: Type[BaseModel] = WeaviateQueryInput

    def _run(
        self,
        query: str = None,
        limit: int = 4,
        standard_filter: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Execute the query against Weaviate.

        Handles both dictionary and list inputs for flexibility.
        If query is None, tries to extract from kwargs or list format.
        """
        # Handle case where input might be passed as a list or in kwargs
        # This provides flexibility for different LLM output formats
        if query is None:
            # Try to extract from kwargs (in case of list format)
            if "query" in kwargs:
                query = kwargs["query"]
            elif kwargs:
                # If kwargs has other structure, try to find query
                for key in ["query", "search", "q"]:
                    if key in kwargs:
                        query = kwargs[key]
                        break

        # If still None, check if we received a list/array format
        # CrewAI might pass the raw input differently
        if query is None and kwargs:
            # Try to handle list format: [{"query": "...", "limit": 5}, ...]
            # Extract first dict from list if present
            for key, value in kwargs.items():
                if isinstance(value, list) and len(value) > 0:
                    if isinstance(value[0], dict):
                        query = value[0].get("query")
                        limit = value[0].get("limit", limit)
                        standard_filter = value[0].get("standard_filter", standard_filter)
                        break

        # Validate input types
        if query is None or not isinstance(query, str):
            return (
                f"Error: 'query' must be a string, got {type(query).__name__ if query else 'None'}.\n"
                f"Please call the tool with: {{'query': 'your search term', 'limit': 5}}\n"
                f"Or as a list: [{{'query': 'your search term', 'limit': 5}}]"
            )

        if not isinstance(limit, int):
            try:
                limit = int(limit)
            except (ValueError, TypeError):
                return (
                    f"Error: 'limit' must be an integer, got {type(limit).__name__}.\n"
                    f"Please call the tool with: {{'query': 'your search term', 'limit': 5}}"
                )

        try:
            # Connect to Weaviate
            client = weaviate.connect_to_local(
                host=os.getenv("WEAVIATE_HOST", "localhost"),
                port=int(os.getenv("WEAVIATE_PORT", "8080")),
                grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
            )

            try:
                collection = client.collections.get("SecurityControl")

                # Build query with optional filter
                query_kwargs = {
                    "query": query,
                    "limit": limit,
                }

                if standard_filter:
                    # Normalize standard filter to match data values
                    standard_map = {
                        "OWASP": "OWASP",
                        "NIST": "NIST",
                        "ISO27001": "ISO27001",
                        "ISO": "ISO27001",  # Allow ISO as shorthand
                    }
                    normalized_filter = standard_map.get(standard_filter.upper(), standard_filter)
                    response = collection.query.near_text(
                        query=query, limit=limit, filters=Filter.by_property("standard").equal(normalized_filter)
                    )
                else:
                    response = collection.query.near_text(**query_kwargs)

                # Format results
                if not response.objects:
                    return "No relevant security controls found."

                results = []
                for i, obj in enumerate(response.objects, 1):
                    props = obj.properties
                    result = (
                        f"{i}. [{props.get('standard', 'Unknown')}] {props.get('req_id', 'N/A')}\n"
                        f"   Chapter: {props.get('chapter_id', '')} - {props.get('chapter_name', '')}\n"
                        f"   Section: {props.get('section_id', '')} - {props.get('section_name', '')}\n"
                        f"   Level: {props.get('level', 'N/A')}\n"
                        f"   Requirement: {props.get('req_description', 'No description')}\n"
                    )
                    results.append(result)

                return "\n".join(results)

            finally:
                client.close()

        except Exception as e:
            return f"Error querying security standards database: {str(e)}"
