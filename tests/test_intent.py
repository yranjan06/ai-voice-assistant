import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from intent import classify

def test(label, text, expected):
    results = classify(text)
    got = results[0]["intent"]
    conf = results[0]["confidence"]
    status = "PASS" if got == expected else "FAIL"
    print(f"{status} [{label}]: '{text}' -> {got} ({conf})")
    assert got == expected, f"expected {expected}, got {got}"

if __name__ == "__main__":
    print("running intent tests...\n")
    test("regex file",    "create a file called notes.txt",            "create_file")
    test("regex code",    "write a python function for binary search", "write_code")
    test("regex summary", "summarize this paragraph for me",           "summarize")
    test("regex folder",  "make a new folder called data",             "create_file")
    test("keyword",       "i need a script that reads csv",            "write_code")
    test("chat hello",    "hello how are you",                         "general_chat")
    test("chat question", "what is the capital of france",             "general_chat")
    print("\nall tests passed.")