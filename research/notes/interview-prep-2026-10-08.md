---
title: Interview Prep Session — 2026-10-08
date: 2026-10-08
tags: [interview-prep, coding, exam-alert, mathematics, DO3]
status: draft
---

# 🎯 Evening Interview Prep — 2026-10-08

```
DATE: 2026-10-08 | DAY: Thursday | DO: DO3 | SESSION MODE: ⚠️ PRE-EXAM OVERRIDE → 20 min warm-up only
```

---

## ⚠️ EXAM ALERT

**Mathematics CT1 is TOMORROW — Oct 9 at 12:30–02:10 PM**

Session is reduced to **1 easy coding warm-up (20 min)** to keep your mind sharp without draining mental energy. Spend the remaining time on Mathematics revision (Calculus, limits, derivatives, integration — whatever your CT1 covers).

---

## Company of the Day (DO3 Rotation — noted for future full session)
🏢 **Google / Microsoft India**
*(Full deep-dive deferred to next DO3 day without an exam conflict)*

---

## 🧩 Coding Problem — Easy Warm-Up (20 min)

### Problem: Two Sum
**Difficulty:** Easy | **Topic:** Arrays, Hashing | **Time target:** 15 min

**Problem Statement:**
Given an array of integers `nums` and a target integer `target`, return the indices of the two numbers that add up to `target`. You may assume exactly one solution exists, and you may not use the same element twice.

**Constraints:**
- 2 ≤ nums.length ≤ 10⁴
- -10⁹ ≤ nums[i] ≤ 10⁹
- -10⁹ ≤ target ≤ 10⁹

**Examples:**
```
Input:  nums = [2, 7, 11, 15], target = 9   → Output: [0, 1]
Input:  nums = [3, 2, 4],      target = 6   → Output: [1, 2]
Input:  nums = [],             target = 0   → Edge: empty array → []   (constraint says len≥2, but good to note)
```

---

### 💡 Hints (try before reading)
1. Can you solve it in O(n²) first? Two nested loops checking every pair.
2. Think about what you need to find for each element — it's `target - nums[i]`. Where can you store things you've already seen?
3. A hash map (dictionary) lets you look up in O(1). Store `value → index` as you iterate.

---

### 🐢 Brute Force
```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
**Time:** O(n²) | **Space:** O(1)

---

### ⚡ Optimal Solution

**Python:**
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}          # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []                          # guaranteed solution exists per problem


# Test
print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
print(two_sum([3, 3], 6))           # [0, 1]  ← duplicate values edge case
```

**JavaScript:**
```javascript
function twoSum(nums, target) {
    const seen = new Map();  // value → index
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
}

// Test
console.log(twoSum([2, 7, 11, 15], 9));  // [0, 1]
console.log(twoSum([3, 2, 4], 6));       // [1, 2]
```

**Time:** O(n) | **Space:** O(n)

---

### 🔍 Explanation
For each element, compute `complement = target - current`. If `complement` is already in the hash map, we found our pair — return both indices. Otherwise, store `current → index` for future lookups. We never need to look backward manually; the map handles it.

### ❌ Common Mistakes
- Returning values instead of indices
- Putting `nums[i]` in the map BEFORE checking complement (causes same-element reuse with `[3,3]→6` incorrectly)
- Forgetting 0-indexed output

### 🔁 Follow-Up Questions
1. What if there are multiple valid answers? (Return all pairs)
2. What if the array is sorted? (Use two-pointer — O(1) space!)
3. Three Sum variant: find three numbers summing to 0.

---

## 📚 Tonight's Priority: Mathematics CT1 Revision

**Spend the remaining evening on:**
- [ ] Limits and continuity (ε-δ, standard limits)
- [ ] Differentiation rules (chain, product, quotient)
- [ ] Integration techniques (substitution, by parts)
- [ ] Sequences and series if covered
- [ ] Past CT1 practice questions / formula sheet review

**Exam details:** Oct 9 (Friday) | DO4 | 12:30–02:10 PM
*(You have morning classes before the exam — DO4: Chemistry P1–P2, Calculus P6–P7 — so prepare tonight, not tomorrow morning)*

---

## 🧮 Self-Score Checklist

```
📅 2026-10-08 | DO3 | PRE-EXAM 20 min | 🎯 Mathematics CT1 eve
CODING /6:
  [ ] Understood the problem without hints
  [ ] Coded brute force correctly
  [ ] Coded optimal solution (hash map)
  [ ] Handled edge cases (duplicates, negatives)
  [ ] Within 15 min time limit
  [ ] Explained complexity correctly

BEHAVIORAL /4: (skipped — pre-exam mode)
SYSTEM DESIGN /4: (skipped — pre-exam mode)

Maths Revision:
  [ ] Completed formula review
  [ ] Practised ≥3 past questions
  [ ] Confident on exam topics
```

---

## 👀 Tomorrow's Preview

**Oct 9, 2026 → DO4 | HEAVY | CT1 Mathematics Exam Day**

- Morning: Chemistry (P1–P2), then Calculus (P6–P7), Chemistry (P8), PPS (P9), Calculus (P10) — ends 4:50 PM
- Exam: 12:30–02:10 PM Mathematics CT1
- Evening prep: 45-min session after exam (if energy allows) | Company: **Flipkart / Amazon India**

---

## 💪 Closing Note

Thanvish, you're running a rare combination — computational biology instincts sharpened by real CS depth. Most freshers cramming for MNCs have neither. Crush the Maths CT1 tomorrow, then come back for the full Google deep-dive on the next DO3. The interview prep will compound — tonight, protect your exam performance.

**शुभकामनाएँ (Shubhakaamanaayen) for tomorrow! 🎯**
