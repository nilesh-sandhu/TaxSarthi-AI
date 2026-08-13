import json
import urllib.request
import sys


def post_question(question: str):
    url = 'http://127.0.0.1:8000/ai/chat'
    data = json.dumps({'question': question}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def assert_contains(text: str, substrings):
    for s in substrings:
        if s not in text:
            raise AssertionError(f"Expected '{s}' in response text")


def run_tests():
    tests = [
        ("What is the GST on Laptop?", ["HSN Code", "GST Rate", "18"]),
        ("What is the GST on Tea?", ["HSN Code", "GST Rate", "5"]),
    ]

    for question, checks in tests:
        print('\nTesting:', question)
        resp = post_question(question)
        if not resp.get('success'):
            print('FAIL: success=false', resp)
            sys.exit(2)

        answer = resp.get('response', {}).get('answer', '')
        try:
            assert_contains(answer, checks)
        except AssertionError as e:
            print('FAIL:', e)
            print('Full response:', json.dumps(resp, ensure_ascii=False, indent=2))
            sys.exit(3)

        print('PASS')

    print('\nAll smoke tests passed')


if __name__ == '__main__':
    run_tests()
