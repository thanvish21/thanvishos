---
title: Interview Prep Session — 2026-10-10
date: 2026-10-10
tags: [interview-prep, coding, exam-alert, pps, c-programming, holiday, bioinformatics, zoho, strings]
status: draft
---

# 🎯 Evening Interview Prep — 2026-10-10

```
DATE: 2026-10-10 | DAY: Saturday | DO: HOLIDAY | SESSION MODE: 20 min (Pre-Exam Mode)
```

---

## ⚠️ EXAM ALERT
**PPS (Programming for Problem Solving / C Programming) exam on Oct 12 at 08:00–09:40 AM. Prioritize revision tonight.**

With your CT1 PPS exam arriving first thing Monday morning (followed by Japanese on Oct 13 and Biology on Oct 14), tonight's weekend session is streamlined into a **20-minute high-impact warm-up**. Behavioral questions and System Design are intentionally deferred to guard your bandwidth. Tonight's coding problem is tailored to bridge core linear string traversal (a classic in Zoho / Product technical rounds) with essential C array logic directly tested in Monday's PPS exam!

---

## 🏢 Company of the Day (Weekend / Product Track)
**Zoho / Chennai Tech Startups / Product Engineering Track**
*(Full company deep-dive deferred during CT1 exam week.)*

---

## 🧩 Coding Problem — Easy Warm-Up (Bio+CS Twist)

### Problem: Genomic Run-Length Encoding (DNA Compression)
**Difficulty:** Easy | **Topic:** Strings, Two-Pointer / Linear Scan, C Fundamentals | **Time target:** 15 min

**Problem Statement:**
Given a DNA sequence string `s` composed solely of nucleotide characters (`'A'`, `'C'`, `'G'`, and `'T'`), compress the string using **Run-Length Encoding (RLE)**. 

Run-Length Encoding replaces each consecutive run of identical characters with the character itself followed by the integer count of its consecutive occurrences.

**Constraints:**
- `1 <= s.length <= 10^5`
- `s` consists only of uppercase English letters `'A'`, `'C'`, `'G'`, and `'T'`.

**Examples:**
```
Input:  s = "AAACCGGTTTT"
Output: "A3C2G2T4"

Input:  s = "A"
Output: "A1"

Input:  s = "ACGT"
Output: "A1C1G1T1"
```

---

### 💡 Hints (try before reading)
1. **Linear Pass:** Traverse the string while keeping track of the current character and a running count of consecutive duplicates.
2. **Boundary Check:** A run ends either when `s[i] != s[i+1]` or when you reach the end of the string (`i == len(s) - 1`).
3. **Memory Efficiency:** Avoid repetitive string concatenation in a loop (which can cause $O(N^2)$ overhead due to string immutability). Use a list/array buffer to collect chunks, then join them.

---

### 🐢 Brute Force & ⚡ Optimal Solutions

#### Python 3 (Optimal Linear Scan):
```python
def encode_dna(s: str) -> str:
    if not s:
        return ""
    
    encoded_parts = []
    count = 1
    n = len(s)
    
    for i in range(n):
        # Check if we are at the end of the string or the next char differs
        if i + 1 < n and s[i] == s[i + 1]:
            count += 1
        else:
            encoded_parts.append(f"{s[i]}{count}")
            count = 1
            
    return "".join(encoded_parts)


# Test Cases
print(encode_dna("AAACCGGTTTT"))  # "A3C2G2T4"
print(encode_dna("A"))            # "A1"
print(encode_dna("ACGT"))         # "A1C1G1T1"
```

#### JavaScript (ES6):
```javascript
function encodeDNA(s) {
    if (!s || s.length === 0) return "";
    
    const result = [];
    let count = 1;
    const n = s.length;
    
    for (let i = 0; i < n; i++) {
        if (i + 1 < n && s[i] === s[i + 1]) {
            count++;
        } else {
            result.push(`${s[i]}${count}`);
            count = 1;
        }
    }
    
    return result.join("");
}

// Test Cases
console.log(encodeDNA("AAACCGGTTTT")); // "A3C2G2T4"
console.log(encodeDNA("A"));           // "A1"
console.log(encodeDNA("ACGT"));        // "A1C1G1T1"
```

#### 🎯 Bonus: C Implementation (Direct PPS CT1 Revision):
```c
#include <stdio.h>
#include <string.h>

void runLengthEncode(const char *s, char *output) {
    int n = strlen(s);
    if (n == 0) {
        output[0] = '\0';
        return;
    }
    
    int outIdx = 0;
    int count = 1;
    
    for (int i = 0; i < n; i++) {
        if (i + 1 < n && s[i] == s[i + 1]) {
            count++;
        } else {
            // Write character followed by count into the output buffer
            outIdx += sprintf(&output[outIdx], "%c%d", s[i], count);
            count = 1;
        }
    }
}

int main(void) {
    char dna[] = "AAACCGGTTTT";
    char result[256];
    
    runLengthEncode(dna, result);
    printf("Original: %s\nEncoded:  %s\n", dna, result); // A3C2G2T4
    return 0;
}
```

---

### 📊 Complexity Analysis
- **Time Complexity:** $O(N)$, where $N$ is the length of string `s`. Every character is examined exactly once in a single sequential pass.
- **Space Complexity:** $O(N)$ to hold the encoded output string / character array. Auxiliary space for variables is $O(1)$.

---

### 🔍 Explanation & Edge Cases
1. **Single Pass Counting:** We maintain `count = 1`. As long as the next nucleotide matches the current one, we increment `count`. Once a mismatch is detected (or the string ends), we write `s[i]` and its count to the buffer, then reset `count = 1`.
2. **Edge Cases Handled:**
   - **Single-character sequence (`"A"`):** Loop terminates at `i=0`, properly emitting `"A1"`.
   - **All distinct characters (`"ACGT"`):** Every iteration triggers the flush branch, outputting `"A1C1G1T1"`.
   - **All identical characters (`"AAAAA"`):** Count increments up to 5, flushing once at the last index to produce `"A5"`.

---

### ❌ Common Mistakes
- **Off-by-One / Buffer Overflow:** Forgetting to handle the last run when `i == n - 1`, causing the final run to be dropped or accessing out-of-bounds index `s[i+1]` without `i + 1 < n` check.
- **Quadratic String Concatenation:** Using `result += s[i] + count` inside loops in Python/Java/JS copies the entire string on every iteration, turning an $O(N)$ algorithm into $O(N^2)$.
- **Resetting Count to 0 instead of 1:** When a new run begins, `count` must be initialized to `1`, not `0`.

---

### 🔁 Follow-Up Questions
1. **Inverse Decoder:** How would you implement the decompression algorithm `decode_dna(encoded_str: str) -> str` to handle multi-digit run lengths like `"A12C3"`?
2. **In-place Compression (LeetCode 443):** If given a mutable `char[]` array, how would you compress it in-place using two pointers with $O(1)$ extra space?
3. **Bioinformatics Homopolymers:** In long-read sequencing (e.g., Oxford Nanopore), long homopolymer runs often introduce insertion/deletion errors. How is RLE used to canonicalize genomic alignments against sequencing drift?

---

## 🧮 Self-Score Checklist

```
📅 2026-10-10 | HOLIDAY | 20 min (Pre-Exam Mode) | 🎯 Zoho / Product Track
CODING /6:
  [ ] Understood the problem without hints
  [ ] Coded optimal linear scan solution
  [ ] Handled single-character and boundary edge cases
  [ ] Completed within 15 min time limit
  [ ] Explained time and space complexity accurately
  [ ] Reviewed the C implementation for PPS CT1 readiness
EXAM REVISION /4:
  [ ] C string manipulation / pointer fundamentals reviewed
  [ ] Conditional & looping constructs (for/while/switch) solid
  [ ] Array indexing and boundary handling verified
  [ ] Ready for Monday 8:00 AM PPS CT1 paper
```

---

## 📚 Weekend Priority: PPS CT1 Exam Revision
Use your remaining study blocks this weekend to review:
- **C Basics & Operators:** Precedence, bitwise operators, ternary expressions, `sizeof`.
- **Control Structures:** Nested `if-else`, `switch-case` fallthrough rules, `while` vs `do-while` vs `for`.
- **Arrays & Strings:** 1D/2D array memory layout, null terminator `\0`, `strlen`/`strcpy`/`strcmp` mechanics.
- **Functions & Scope:** Call by value, local vs global vs static variables, basic recursion.

---

## 👀 Tomorrow's Preview
- **Date:** 2026-10-11
- **Day:** Sunday
- **DO:** `HOLIDAY` (Calendar: Oct 10–11→HOLIDAY)
- **Upcoming Day Order:** Oct 12 → DO5 (Heavy | CT1 PPS Exam at 08:00–09:40 AM)
- **Session Length:** 20 min (Final Pre-Exam Polish)
- **Focus:** Quick C Warm-up & Final CT1 PPS Readiness

---

## 💪 Closing Note
Thanvish, your rare combination of Computational Biology and Systems/CS fundamentals gives you an incredible long-term moat. Take care of business on Monday morning with that PPS CT1 paper—keep the code clean, trace your pointers carefully, and set the tone for exam week!
