# 📅 2026-10-06 | 🏫 DO1 | ⏱️ 20 min | 🎯 TCS / Infosys
**Student:** Machireddy Venkata Thanvish Reddy (RA2611027010109)
**Profile Focus:** CS, CompBio, AI/ML, Full-stack 

⚠️ **EXAM ALERT**: Chemistry exam on Oct 7 at 12:30–02:10 PM. Prioritize revision tonight. 
*Session reduced to minimum 20 min (1 easy problem) to maximize exam prep.*

---

## 💻 QUICK CODING WARM-UP: Push Zeros to End (TCS NQT Favorite)

**Problem Statement:**
Given an integer array `nums`, move all `0`s to the end of it while maintaining the relative order of the non-zero elements. You must do this in-place without making a copy of the array.

**Constraints:**
- 1 <= nums.length <= 10^4
- -2^31 <= nums[i] <= 2^31 - 1

### Examples
1. `Input: nums = [4, 5, 0, 1, 9, 0, 5, 0] -> Output: [4, 5, 1, 9, 5, 0, 0, 0]`
2. `Input: nums = [0] -> Output: [0]`
3. `Input: nums = [0, 0, 1] -> Output: [1, 0, 0]`

### Progressive Hints
1. Instead of thinking about moving the zeros, focus on moving the non-zero elements forward.
2. Keep a pointer (let's call it `insertPos`) that tracks where the next non-zero element should be written.
3. Iterate through the array. Whenever you see a non-zero element, place it at `insertPos` and increment `insertPos`. Finally, fill all remaining indices from `insertPos` to the end with `0`.

### Solutions

**Brute Force Approach** (Time: O(N), Space: O(N)):
Create a new array. Iterate through the original array and copy all non-zero elements to the new array. Fill the rest with zeros. Then copy the new array back to the original array. (Violates in-place constraint).

**Optimal Approach (Two-Pointer)** (Time: O(N), Space: O(1)):

*Python:*
```python
def moveZeroes(nums):
    insert_pos = 0
    # Move non-zero elements forward
    for num in nums:
        if num != 0:
            nums[insert_pos] = num
            insert_pos += 1
            
    # Fill remaining spaces with zeroes
    for i in range(insert_pos, len(nums)):
        nums[i] = 0
```

*JavaScript:*
```javascript
function moveZeroes(nums) {
    let insertPos = 0;
    
    // Move all the non-zero elements to the front
    for (let i = 0; i < nums.length; i++) {
        if (nums[i] !== 0) {
            nums[insertPos] = nums[i];
            insertPos++;
        }
    }
    
    // Fill the rest with zeros
    for (let i = insertPos; i < nums.length; i++) {
        nums[i] = 0;
    }
}
```

**Common Mistakes:**
- Swapping every element (doing an O(N^2) bubble-sort style shift).
- Modifying the array size while iterating in languages like Python.
- Forgetting to maintain relative order of non-zero elements.

**Follow-up Question:** 
Can you optimize the total number of operations if the array has very few non-zero elements? *(Hint: use swapping instead of separate fill step)*.

---

## 🧪 CHEMISTRY CT1 EXAM REVISION (High-Yield Cheatsheet)

Since your CT1 is tomorrow at 12:30 PM, focus entirely on these typical Engineering Chemistry modules:

**1. Water Technology**
- **Hardness:** Temporary (Bicarbonates of Ca/Mg) vs Permanent (Chlorides/Sulfates of Ca/Mg).
- **Units:** 1 ppm = 1 mg/L = 0.1 °Fr = 0.07 °Cl.
- **EDTA Method:** Know the indicator (Eriochrome Black-T) and the color change (Wine Red to Steel Blue) at pH 9-10 (Buffer: NH4Cl + NH4OH).
- **Boiler Troubles:** Scales & Sludges (prevent via Calgon conditioning), Priming & Foaming, Caustic Embrittlement (NaOH attacks grain boundaries).
- **Water Softening:** Ion Exchange (Demineralization using cation/anion resins), Zeolite process.
- **Reverse Osmosis:** Pushing solvent from high conc. to low conc. using external pressure > osmotic pressure.

**2. Polymers**
- **Addition vs Condensation polymerization**
- **Thermoplastics (PVC, Teflon) vs Thermosetting (Bakelite, Epoxy resin)**
- **Conducting Polymers:** Structure of Polyacetylene / Polyaniline. Doping creates charge carriers.

**3. Phase Rule**
- **Formula:** F = C - P + 2
- **Water System:** 
  - Areas (F=2): Ice, Water, Vapor.
  - Curves (F=1): Melting, Sublimation, Vaporization. 
  - Triple Point (F=0): T=0.0098°C, P=4.58mm Hg (Ice, water, vapor exist in equilibrium).

*Review past SRM chemistry question papers tonight and ensure your calculator is packed.*

---

## ✅ SELF-SCORE CHECKLIST

```text
📅 2026-10-06 | DO1 | 20 min | 🎯 TCS / Infosys
CODING /6: [ ]
EXAM REVISION /4: [ ]
```

---

### 🔮 TOMORROW'S PREVIEW
**Date:** 2026-10-07 | **Day Order:** DO2
**Schedule:** NSS block + **Chemistry Exam (12:30 PM)** + CompBio.
**Session Mode:** Post-exam recovery standard session (60 min) focused on Wipro / HCL problems.

*Good luck tomorrow, Thanvish! Between computationally crunching DNA and writing full-stack ML code, balancing a chemistry exam is just another optimization problem you're fully capable of solving. Crush it!*