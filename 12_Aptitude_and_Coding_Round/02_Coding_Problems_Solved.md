# Coding Round – Solved Problems (Python)

> Expect 1–3 easy-to-medium problems. For each one: clarify the inputs → state the approach and complexity → code → test edge cases out loud. All solutions below were run and checked. Test file: `coding_solutions.py`.

### P1. Reverse a string / check palindrome (ignore case and non-alphanumeric)
```python
def is_palindrome(s: str) -> bool:
    clean = [c.lower() for c in s if c.isalnum()]
    return clean == clean[::-1]
# is_palindrome("A man, a plan, a canal: Panama") -> True
```
O(n) time. Edge cases: empty string → True.

### P2. Count word / character frequency
```python
from collections import Counter
def top_words(text: str, n: int = 3):
    words = text.lower().split()
    return Counter(words).most_common(n)
```
Banking twist: the most common complaint words in a ticket dump.

### P3. Two Sum (indices of two numbers adding to target)
```python
def two_sum(nums, target):
    seen = {}                         # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
# two_sum([2, 7, 11, 15], 9) -> [0, 1]
```
O(n) with a dict instead of O(n²) nested loops. **Say this trade-off out loud.**
Banking twist: find two transactions that sum to a reconciliation difference.

### P4. Find duplicates in a list
```python
def duplicates(items):
    seen, dups = set(), set()
    for x in items:
        (dups if x in seen else seen).add(x)
    return sorted(dups)
# duplicates(["L1","L2","L1","L3","L2"]) -> ['L1', 'L2']
```

### P5. Second largest number (without sorting)
```python
def second_largest(nums):
    first = second = float("-inf")
    for x in nums:
        if x > first:
            first, second = x, first
        elif first > x > second:
            second = x
    return None if second == float("-inf") else second
# second_largest([5, 1, 5, 3]) -> 3
```

### P6. Maximum subarray sum (Kadane's algorithm) – asked at many companies
```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
# max_subarray([34, -50, 42, 14, -5, 86]) -> 137
```
Banking twist: the best consecutive run of net cash inflows.

### P7. Valid parentheses
```python
def valid_brackets(s):
    pairs, stack = {")": "(", "]": "[", "}": "{"}, []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack
# valid_brackets("{[()]}") -> True ; valid_brackets("(]") -> False
```
Twist: validate that a JSON-like LLM output has balanced braces before parsing.

### P8. Anagram check
```python
from collections import Counter
def is_anagram(a, b): return Counter(a.replace(" ", "").lower()) == Counter(b.replace(" ", "").lower())
# is_anagram("listen", "silent") -> True
```

### P9. FizzBuzz (warm-up)
```python
def fizzbuzz(n):
    return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
            for i in range(1, n + 1)]
```

### P10. Fibonacci (iterative) and factorial
```python
def fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
# fib(10) -> 55
```

### P11. Flatten a nested list
```python
def flatten(lst):
    out = []
    for x in lst:
        out.extend(flatten(x)) if isinstance(x, list) else out.append(x)
    return out
# flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]
```

### P12. Group anagrams / group by key
```python
from collections import defaultdict
def group_anagrams(words):
    g = defaultdict(list)
    for w in words: g["".join(sorted(w))].append(w)
    return list(g.values())
```

### P13. Merge overlapping intervals
```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for s, e in intervals:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged
# merge_intervals([[1,3],[2,6],[8,10],[15,18]]) -> [[1,6],[8,10],[15,18]]
```
Twist: merge overlapping loan moratorium periods.

### P14. Binary search
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        if arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```
O(log n). It requires a sorted array.

### P15. Domain task: classify loans and summarise (very likely for this role)
**Task:** Given a list of loans `{"id", "branch", "outstanding", "dpd"}`, return per branch: number of loans, total outstanding, NPA amount and GNPA %.
```python
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
```
Pandas version:
```python
df.assign(npa=df.outstanding.where(df.dpd > 90, 0)).groupby("branch").agg(
    loans=("id", "count"), total=("outstanding", "sum"), npa=("npa", "sum")
).assign(gnpa_pct=lambda x: (100 * x.npa / x.total).round(2))
```

### P16. Domain task: parse a messy log / text with regex
**Task:** Extract all account numbers (format `ACC` + 6 digits) and amounts (₹1,23,456.78 style) from text.
```python
import re
text = "Debit ACC123456 Rs. 1,23,456.78 on 05-10-2026; credit ACC654321 Rs. 500"
accounts = re.findall(r"ACC\d{6}", text)                              # ['ACC123456', 'ACC654321']
amounts = [float(a.replace(",", "")) for a in re.findall(r"Rs\.\s?([\d,]+(?:\.\d+)?)", text)]  # [123456.78, 500.0]
```

### P17. Domain task: mask PII before sending text to an LLM
```python
import re
def mask_pii(text: str) -> str:
    text = re.sub(r"\b[A-Z]{5}\d{4}[A-Z]\b", "<PAN>", text)            # PAN
    text = re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b", "<AADHAAR>", text)     # 12-digit Aadhaar
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "<EMAIL>", text)
    text = re.sub(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}\b", "<PHONE>", text)
    return text
# mask_pii("PAN ABCDE1234F, mail a.b@x.com, ph 9876543210") -> "PAN <PAN>, mail <EMAIL>, ph <PHONE>"
```

### P18. Domain task: chunk a text for RAG with overlap
```python
def chunk_words(text, size=100, overlap=20):
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]
```

### P19. Domain task: cosine similarity top-k without libraries beyond NumPy
```python
import numpy as np
def top_k(query_vec, doc_matrix, k=3):
    q = query_vec / np.linalg.norm(query_vec)
    D = doc_matrix / np.linalg.norm(doc_matrix, axis=1, keepdims=True)
    scores = D @ q
    idx = np.argsort(scores)[::-1][:k]
    return list(zip(idx.tolist(), scores[idx].round(3).tolist()))
```

### P20. Domain task: safely parse JSON from an LLM reply that may include extra text
```python
import json, re
def extract_json(reply: str):
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")
    return json.loads(match.group())
# extract_json('Sure! Here it is: {"category": "ATM_CASH", "confidence": 0.9}') -> {...}
```

## How to talk during live coding
1. Restate the problem and ask about edge cases (empty input? duplicates? negatives?).
2. Say the brute force and its complexity, then the better approach.
3. Write clean code with good names.
4. Walk through one example by hand.
5. Mention tests: normal, edge, invalid input.
