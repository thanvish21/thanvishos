---
title: Interview Prep Session — 2026-10-08
date: 2026-10-08
tags: [interview-prep, coding, exam-alert, mathematics, DO3, bioinformatics]
status: draft
---

# 🎯 Evening Interview Prep — 2026-10-08

```
DATE: 2026-10-08 | DAY: Thursday | DO: DO3 | SESSION MODE: 20 min (Pre-Exam Mode)
```

---

## ⚠️ EXAM ALERT
**Mathematics exam on Oct 9 at 12:30–02:10 PM. Prioritize revision tonight.**

Because your CT1 Mathematics exam is tomorrow, tonight's interview prep is scaled down to a **20-minute minimum warm-up**. Behavioral and System Design sections are skipped. Guard your mental energy and pivot immediately to calculus and matrices after this!

---

## 🏢 Company of the Day (DO3 Rotation)
**Google / Microsoft India**
*(Full interview deep-dive deferred to your next DO3 day due to tomorrow's exam.)*

---

## 🧩 Coding Problem — Easy Warm-Up (Bio+CS Twist)

### Problem: Counting Point Mutations (Hamming Distance)
**Difficulty:** Easy | **Topic:** Strings, Counting | **Time target:** 15 min

**Problem Statement:**
Given two DNA strings `s` and `t` of equal length, return the Hamming distance between them. The Hamming distance is the number of corresponding symbols that differ in `s` and `t`. This represents the minimum number of point mutations required to change one DNA sequence into the other.

**Constraints:**
- 1 ≤ s.length = t.length ≤ 1000
- `s` and `t` consist only of characters `'A'`, `'C'`, `'G'`, and `'T'`.

**Examples:**
```
Input:  s = "GAGCCTACTAACGGGAT", t = "CATCGTAATGACGGCCT"
Output: 7

Input:  s = "A", t = "A"
Output: 0

Input:  s = "", t = ""  (Edge case: empty strings)
Output: 0
```

---

### 💡 Hints (try before reading)
1. You only need to compare characters at the exact same index in both strings.
2. A single loop iterating from `0` to `length - 1` is sufficient.
3. Keep a counter variable. Increment it whenever `s[i] != t[i]`.

---

### 🐢 Brute Force & ⚡ Optimal Solution

For this problem, the brute force approach of checking each character index-by-index is also the optimal approach.

**Python:**
```python
def hamming_distance(s: str, t: str) -> int:
    mutations = 0
    for i in range(len(s)):
        if s[i] != t[i]:
            mutations += 1
    return mutations

# Pythonic optimal one-liner using zip:
def hamming_distance_pythonic(s: str, t: str) -> int:
    return sum(1 for a, b in zip(s, t) if a != b)

# Test
print(hamming_distance("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT"))  # 7
```

**JavaScript:**
```javascript
function hammingDistance(s, t) {
    let mutations = 0;
    for (let i = 0; i < s.length; i++) {
        if (s[i] !== t[i]) {
            mutations++;
        }
    }
    return mutations;
}

// Test
console.log(hammingDistance("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT"));  // 7
```

**Time Complexity:** O(n) where n is the length of the string. We visit each character exactly once.
**Space Complexity:** O(1) as we only use a single counter variable.

---

### 🔍 Explanation
We iterate through both sequences simultaneously. At each position `i`, we check if the nucleotide in sequence `s` differs from the nucleotide in sequence `t`. If they are different, we have found a point mutation and increment our counter. 

### ❌ Common Mistakes
- Trying to split the string into arrays first (unnecessary memory overhead, Strings are iterable/indexable).
- Forgetting to handle edge cases like empty strings (though constraints often guarantee length ≥ 1).
- Overcomplicating with maps or sets—order matters here!

### 🔁 Follow-Up Questions
1. How would you handle strings of *unequal* length? (Requires sequence alignment like Needleman-Wunsch / Levenshtein distance—much harder!)
2. Can you optimize this if the strings were massive (e.g., millions of base pairs)? (Process in chunks, potentially multithreading or using bitwise operations if encoded compactly).

---

## 🧮 Self-Score Checklist

```
📅 2026-10-08 | DO3 | 20 min (Pre-Exam Mode) | 🎯 Google / Microsoft India
CODING /6:
  [ ] Understood the problem without hints
  [ ] Coded optimal solution
  [ ] Handled edge cases
  [ ] Within 15 min time limit
  [ ] Explained complexity correctly
  [ ] Considered Bio+CS follow-up twist
```

---

## 📚 Tonight's True Priority: Math CT1 Revision
Spend the rest of the night reviewing:
- Calculus fundamentals (limits, continuity, derivatives, integration).
- Any matrices or sequences topics covered in your syllabus.
- **Do not pull an all-nighter.** You have morning classes tomorrow before the 12:30 PM exam.

---

## 👀 Tomorrow's Preview
**Date:** 2026-10-09
**DO:** DO4 (Heavy)
**Session Length:** 45 min
**Company:** Flipkart / Amazon India

## 💪 Closing Note
Thanvish, your unique blend of Computational Biology and strict CS fundamentals gives you an edge few candidates have. Protect your GPA tomorrow—crush that Mathematics CT1, and we'll pick up the heavy engineering prep once the exam is behind you. Good luck!
