import json
import uuid
import difflib
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError

from golden_dataset import GOLDEN_CASES


BASE_URL = "http://127.0.0.1:8000"


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} calling {url}: {body}") from e
    except URLError as e:
        raise RuntimeError(f"Failed to reach {url}: {e}") from e


def normalize(s: str) -> str:
    # strict-but-sane: normalize line endings and trailing spaces
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    return s.strip()


def main():
    total = len(GOLDEN_CASES)
    passed = 0
    failed_cases = []

    for case in GOLDEN_CASES:
        session_id = str(uuid.uuid4())
        user_message = case["user_message"]
        expected = normalize(case["expected_answer"])

        resp = post_json(f"{BASE_URL}/chat", {"message": user_message, "session_id": session_id})
        got = normalize(resp.get("response", ""))

        ok = (got == expected)
        if ok:
            passed += 1
        else:
            failed_cases.append((case["id"], user_message, expected, got))

        print(f"{case['id']}: {'PASS' if ok else 'FAIL'}")

    print("\n" + "=" * 60)
    print(f"RESULT: {passed}/{total} passed")

    if failed_cases:
        print("\nFAILED DETAILS:")
        for case_id, user_message, expected, got in failed_cases:
            print("\n" + "-" * 60)
            print(f"Case: {case_id}")
            print(f"User: {user_message}")
            print("\n--- Expected ---")
            print(expected)
            print("\n--- Got ---")
            print(got)
            print("\n--- Diff ---")
            diff = difflib.unified_diff(
                expected.splitlines(),
                got.splitlines(),
                fromfile="expected",
                tofile="got",
                lineterm="",
            )
            print("\n".join(diff))


if __name__ == "__main__":
    main()
