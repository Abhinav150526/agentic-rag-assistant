from src.core.rag_service import answer_question

TEST_CASES = [
    {
        "question": "Who is my manager?",
        "expected_route": "MEMORY_READ, FINAL"
    },
    {
        "question": "What is today's date?",
        "expected_route": "DATE_TOOL, FINAL"
    },
    {
        "question": "How many leave days does John have?",
        "expected_route": "LEAVE_TOOL, FINAL"
    },
    {
        "question": "Do I have enough leave days to take a 15 day vacation?",
        "expected_route": "LEAVE_TOOL, CALCULATOR_TOOL, FINAL"
    }
]


def run_evaluation():
    passed = 0
    failed = 0

    print("Running Agent Evaluation...\n")

    for test in TEST_CASES:
        print(f"Testing: {test['question']}")

        result = answer_question(test["question"])

        actual_route = result["route"]
        expected_route = test["expected_route"]

        if actual_route == expected_route:
            print("Status: PASS")
            passed += 1
        else:
            print("Status: FAIL")
            failed += 1
            print(f"Expected Route: {expected_route}")
            print(f"Actual Route:   {actual_route}")

        print("-" * 50)

    route_accuracy = (passed / len(TEST_CASES)) * 100

    print()
    print("Evaluation Summary")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {len(TEST_CASES)}")
    print(f"Route Accuracy: {route_accuracy:.2f}%")


if __name__ == "__main__":
    run_evaluation()