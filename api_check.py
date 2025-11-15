#!/usr/bin/env python3
"""
Simple API check script.
Usage:
  python api_check.py --url https://api.example.com/health --expect-status 200 --key status --expect-value ok
"""
import argparse
import sys
import requests

def check_api(url, expect_status=None, json_key=None, expect_value=None, timeout=10):
    try:
        resp = requests.get(url, timeout=timeout)
    except requests.RequestException as e:
        print(f"ERROR: request failed: {e}")
        return False

    print(f"HTTP {resp.status_code} - {url}")

    if expect_status is not None and resp.status_code != expect_status:
        print(f"FAIL: expected status {expect_status} but got {resp.status_code}")
        return False

    if json_key:
        try:
            data = resp.json()
        except ValueError:
            print("FAIL: response is not valid JSON")
            return False
        # simple nested key support with dot notation
        keys = json_key.split(".")
        val = data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                print(f"FAIL: key '{json_key}' not found in JSON")
                return False
        print(f"Found JSON {json_key} = {val!r}")
        if expect_value is not None and str(val) != str(expect_value):
            print(f"FAIL: expected value {expect_value!r} but got {val!r}")
            return False

    print("OK")
    return True

def main():
    p = argparse.ArgumentParser(description="Simple API health checker")
    p.add_argument("--url", required=True, help="API URL to check")
    p.add_argument("--expect-status", type=int, help="Expected HTTP status code")
    p.add_argument("--key", dest="json_key", help="JSON key to check (dot notation allowed)")
    p.add_argument("--expect-value", help="Expected value for the JSON key")
    p.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    args = p.parse_args()

    ok = check_api(args.url, args.expect_status, args.json_key, args.expect_value, args.timeout)
    sys.exit(0 if ok else 2)

if __name__ == "__main__":
    main()
