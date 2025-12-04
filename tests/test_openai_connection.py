#!/usr/bin/env python3
"""Test script to verify OpenAI API connectivity and model availability."""

import os
import sys
import time

from crewai import LLM


def test_openai_connection(model: str = "openai/gpt-5-mini", timeout: int = 30):
    """Test OpenAI API connection with the specified model."""
    print("Testing OpenAI API connection...")
    print(f"Model: {model}")
    print(f"Timeout: {timeout}s")
    print("-" * 60)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        return False

    print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    print()

    try:
        # Initialize LLM with same config as DomainSecurityCrew
        print("Initializing LLM...")
        llm = LLM(model=model, timeout=timeout, max_retries=3)
        print("✓ LLM initialized")
        print()

        # Test simple completion
        print("Sending test request...")
        start_time = time.time()

        response = llm.call(
            messages=[{"role": "user", "content": "Say 'Connection test successful' if you can read this."}],
            tools=[],
        )

        elapsed = time.time() - start_time
        print(f"✓ Response received in {elapsed:.2f}s")
        print()
        print("Response:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        print()
        print("✅ Connection test PASSED")
        return True

    except Exception as e:
        print()
        print("❌ Connection test FAILED")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print()

        # Provide helpful diagnostics
        error_str = str(e).lower()
        if "connection reset" in error_str or "reset by peer" in error_str:
            print("💡 Diagnosis: Connection was reset by the server")
            print("   - This could be network instability")
            print("   - Or API rate limiting")
            print("   - Try again in a few seconds")
        elif "timeout" in error_str:
            print("💡 Diagnosis: Request timed out")
            print("   - Increase timeout value")
            print("   - Check network connection")
        elif "api key" in error_str or "authentication" in error_str:
            print("💡 Diagnosis: Authentication failed")
            print("   - Check your API key is correct")
            print("   - Verify API key has proper permissions")
        elif "rate limit" in error_str or "quota" in error_str:
            print("💡 Diagnosis: Rate limit or quota exceeded")
            print("   - Check your OpenAI account quota")
            print("   - Wait before retrying")
        elif "model" in error_str and ("not found" in error_str or "invalid" in error_str):
            print("💡 Diagnosis: Model not available")
            print("   - Check if model name is correct")
            print("   - Verify model is available in your region/account")

        return False


def test_multiple_requests():
    """Test multiple sequential requests to check for rate limiting or connection issues."""
    print("\n" + "=" * 60)
    print("Testing multiple sequential requests...")
    print("=" * 60)

    try:
        llm = LLM(model="openai/gpt-5-mini", timeout=30, max_retries=3)

        print("Sending 3 sequential requests...")
        for i in range(3):
            start_time = time.time()
            response = llm.call(
                messages=[{"role": "user", "content": f"Say 'Request {i + 1} successful'"}],
                tools=[],
            )
            elapsed = time.time() - start_time
            print(f"  Request {i + 1}: ✓ ({elapsed:.2f}s)")
            time.sleep(1)  # Small delay between requests

        print("✓ Multiple requests test PASSED")
        return True

    except Exception as e:
        print(f"❌ Multiple requests test FAILED: {e}")
        error_str = str(e).lower()
        if "rate limit" in error_str:
            print("💡 Rate limiting detected - this is normal for rapid requests")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("OpenAI API Connection Test")
    print("=" * 60)
    print()

    # Parse command line arguments
    model = "openai/gpt-5-mini"
    timeout = 30

    if len(sys.argv) > 1:
        model = sys.argv[1]
    if len(sys.argv) > 2:
        timeout = int(sys.argv[2])

    # Run basic connection test
    success = test_openai_connection(model=model, timeout=timeout)

    # Run multiple requests test if basic test passed
    if success:
        test_multiple_requests()

    print()
    print("=" * 60)
    sys.exit(0 if success else 1)
