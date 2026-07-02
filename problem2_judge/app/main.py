import json
from app.config import TEST_SUITE
from app.judge import judge

with open(TEST_SUITE, "r", encoding="utf-8") as f:
    test_cases = json.load(f)

for i, test in enumerate(test_cases, 1):
    print(f"\n===== Test Case {i} =====")

    input_text = test.get("input", test.get("question"))
    expected = test.get("expected_output", test.get("expected"))
    model_output = test.get("model_output", test.get("output", ""))

    if input_text is None or expected is None:
        print("Skipping test case because required fields are missing.")
        continue

    if not model_output:
        print("Skipping test case because 'model_output' is missing.")
        continue

    result = judge(
        input_text,
        expected,
        model_output
    )

    print(json.dumps(result, indent=4))
    