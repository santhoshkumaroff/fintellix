"""All coding-round solutions with tests. Run: python coding_solutions.py"""
import json
import re
from collections import Counter, defaultdict

import numpy as np


def is_palindrome(s):
    clean = [c.lower() for c in s if c.isalnum()]
    return clean == clean[::-1]


def top_words(text, n=3):
    return Counter(text.lower().split()).most_common(n)


def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


def duplicates(items):
    seen, dups = set(), set()
    for x in items:
        (dups if x in seen else seen).add(x)
    return sorted(dups)


def second_largest(nums):
    first = second = float("-inf")
    for x in nums:
        if x > first:
            first, second = x, first
        elif first > x > second:
            second = x
    return None if second == float("-inf") else second


def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def valid_brackets(s):
    pairs, stack = {")": "(", "]": "[", "}": "{"}, []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack


def is_anagram(a, b):
    return Counter(a.replace(" ", "").lower()) == Counter(b.replace(" ", "").lower())


def fizzbuzz(n):
    return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
            for i in range(1, n + 1)]


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def flatten(lst):
    out = []
    for x in lst:
        out.extend(flatten(x)) if isinstance(x, list) else out.append(x)
    return out


def group_anagrams(words):
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return list(g.values())


def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for s, e in intervals:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def branch_summary(loans):
    out = {}
    for l in loans:
        b = out.setdefault(l["branch"], {"loans": 0, "total": 0.0, "npa": 0.0})
        b["loans"] += 1
        b["total"] += l["outstanding"]
        if l["dpd"] > 90:
            b["npa"] += l["outstanding"]
    for b in out.values():
        b["gnpa_pct"] = round(100 * b["npa"] / b["total"], 2) if b["total"] else 0.0
    return out


def mask_pii(text):
    text = re.sub(r"\b[A-Z]{5}\d{4}[A-Z]\b", "<PAN>", text)
    text = re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b", "<AADHAAR>", text)
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "<EMAIL>", text)
    text = re.sub(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}\b", "<PHONE>", text)
    return text


def chunk_words(text, size=100, overlap=20):
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


def top_k(query_vec, doc_matrix, k=3):
    q = query_vec / np.linalg.norm(query_vec)
    D = doc_matrix / np.linalg.norm(doc_matrix, axis=1, keepdims=True)
    scores = D @ q
    idx = np.argsort(scores)[::-1][:k]
    return list(zip(idx.tolist(), scores[idx].round(3).tolist()))


def extract_json(reply):
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")
    return json.loads(match.group())


if __name__ == "__main__":
    assert is_palindrome("A man, a plan, a canal: Panama") and is_palindrome("")
    assert top_words("loan atm loan card loan atm", 2) == [("loan", 3), ("atm", 2)]
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert duplicates(["L1", "L2", "L1", "L3", "L2"]) == ["L1", "L2"]
    assert second_largest([5, 1, 5, 3]) == 3 and second_largest([4, 4]) is None
    assert max_subarray([34, -50, 42, 14, -5, 86]) == 137
    assert valid_brackets("{[()]}") and not valid_brackets("(]") and not valid_brackets("((")
    assert is_anagram("listen", "silent")
    assert fizzbuzz(15)[-1] == "FizzBuzz" and fizzbuzz(5)[2] == "Fizz"
    assert fib(10) == 55
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert sorted(map(sorted, group_anagrams(["eat", "tea", "tan", "nat"]))) == [["eat", "tea"], ["nat", "tan"]]
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert binary_search([1, 3, 5, 7, 9], 7) == 3 and binary_search([1, 3], 4) == -1
    s = branch_summary([{"id": "L1", "branch": "BLR", "outstanding": 100, "dpd": 0},
                        {"id": "L2", "branch": "BLR", "outstanding": 50, "dpd": 120}])
    assert s["BLR"]["gnpa_pct"] == 33.33
    assert mask_pii("PAN ABCDE1234F, mail a.b@x.com, ph 9876543210") == "PAN <PAN>, mail <EMAIL>, ph <PHONE>"
    assert mask_pii("Aadhaar 1234 5678 9012") == "Aadhaar <AADHAAR>"
    chunks = chunk_words(" ".join(str(i) for i in range(250)), 100, 20)
    assert len(chunks) == 3 and chunks[1].split()[0] == "80"
    assert top_k(np.array([1.0, 0.0]), np.array([[1.0, 0.1], [0.0, 1.0]]), 1)[0][0] == 0
    assert extract_json('Sure! Here: {"category": "ATM_CASH", "confidence": 0.9}')["category"] == "ATM_CASH"

    text = "Debit ACC123456 Rs. 1,23,456.78 on 05-10-2026; credit ACC654321 Rs. 500"
    assert re.findall(r"ACC\d{6}", text) == ["ACC123456", "ACC654321"]
    assert [float(a.replace(",", "")) for a in re.findall(r"Rs\.\s?([\d,]+(?:\.\d+)?)", text)] == [123456.78, 500.0]
    print("All coding solutions passed.")
