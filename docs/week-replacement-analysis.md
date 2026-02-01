# Week Replacement Analysis: Week 5 Data Update - ACTUAL STATE

## Executive Summary

**STATUS: ❌ PARTIAL FAILURE - Only 15 out of 40 expected values were copied**

The week replacement process successfully copied data for:
- ✅ **12d template** (5 values) - casino+sport campaign  
- ✅ **3d template** (5 values each) - Ret 1 dep and Ret 2 dep campaigns

But **FAILED** to copy data for:
- ❌ **10min** - NOT copied (template matching failed)
- ❌ **1h** - NOT copied (row offset issue)
- ❌ **1d** - NOT copied (row offset issue)
- ❌ **4d** - NOT copied (row offset issue)
- ❌ **6d** - NOT copied (row offset issue)
- ❌ **8d** - NOT copied (row offset issue)
- ❌ **10d** - NOT copied (row offset issue)

## Critical Issues Identified

### Issue 1: Template "10min" Matching Failed

**Problem**: Row 3 in 'WP Chains Sport' has "10 min" (Latin, with space) but code expects "10 мин" (Cyrillic).

**Evidence**:
```python
# Code has:
template_map = {"10min": "10 мин"}  # Cyrillic

# Excel has:
Row 3, Column D: "10 min\n#2250\n#2269..."  # Latin with space
```

**Result**: Template not found, no values copied for 10min.

### Issue 2: Template Matching Failures

**Problem**: The `_find_target_row()` function has incorrect template mappings that don't match the actual Excel values.

**Actual structure in 'WP Chains Sport'**:
```
Row 3:  B=campaign, C=All Mail, D=10 min, E=Sent
Row 4:  E=Delivered
Row 5:  E=Opened
...

Row 11: D=1h, E=Sent
Row 12: E=Delivered
Row 13: E=Opened
```

**Key insight**: 
- Column D: Template name
- Column E: Metric name  
- Template and first metric ("Sent") are on the SAME row
- Row offset calculation `row + 0` for "Sent" is CORRECT ✅

**Template Mismatches**:

| Template | Code Expects | Excel Has | Match? |
|----------|--------------|-----------|--------|
| 10min | "10 мин" (Cyrillic) | "10 min" (Latin) | ❌ NO |
| 1h | "1 h" (with space) | "1h" (no space) | ❌ NO |
| 1d | "2 d" | "1d" | ❌ NO |
| 4d | "4 d" (with space) | "4d" (no space) | ❌ NO |
| 6d | "6 d" (with space) | "6d" (no space) | ❌ NO |
| 8d | "8 d" (with space) | "8d" (no space) | ❌ NO |
| 10d | "10 d" (with space) | "10d" (no space) | ❌ NO |
| 12d | "12d" | "12d" | ✅ YES |

## Missing Mappings

### Templates NOT Being Copied (35 values)

| Template | Source Row | Target Row | Expected Value | Actual Value | Reason |
|----------|------------|------------|----------------|--------------|--------|
| **10min** | 3 | 3-7 | 733, 701, 89, 18, 1 | None | Template mismatch: "10 мин" vs "10 min" |
| **1h** | 9 | 11-15 | 661, 631, 150, 30, 4 | None | Template mismatch: "1 h" vs "1h" |
| **1d** | 15 | 19-23 | 661, 626, 122, 13, 5 | None | Template mismatch: "2 d" vs "1d" |
| **4d** | 27 | 27-31 | 693, 665, 83, 5, 1 | None | Template mismatch: "4 d" vs "4d" |
| **6d** | 33 | 35-39 | 660, 632, 50, 9, 1 | None | Template mismatch: "6 d" vs "6d" |
| **8d** | 39 | 43-47 | 557, 527, 60, 4, 0 | None | Template mismatch: "8 d" vs "8d" |
| **10d** | 45 | 51-55 | 277, 263, 31, 0, 2 | None | Template mismatch: "10 d" vs "10d" |

### Templates Successfully Copied (15 values)

| Template | Source Row | Target Row | Expected Value | Actual Value | Status |
|----------|------------|------------|----------------|--------------|--------|
| **12d** | 51 | 59-63 | 313, 302, 49, 1, 2 | 313, 302, 49, 1, 2 | ✅ COPIED |
| **3d (Ret1)** | 93 | 75-79 | 147, 146, 44, 4, 3 | 147, 146, 44, 4, 3 | ✅ COPIED |
| **3d (Ret2)** | 141 | 123-127 | 18, 18, 3, 1, 0 | 18, 18, 3, 1, 0 | ✅ COPIED |

## Root Cause Analysis

### Why Only 12d and 3d Were Copied

Looking at the code's `_find_target_row()` function:

```python
def _find_target_row(self, ws, campaign: str, template: str, metric: str) -> int:
    # Find campaign
    campaign_start = ...  # Found at row 3
    
    # Find template in column C or D
    for row in range(campaign_start, ...):
        cell_d = ws[f'D{row}'].value
        if cell_d and target_template.lower() in str(cell_d).lower():
            # Found template at row X
            metric_order = ["Sent", "Delivered", "Opened", "Clicked", "Unsubscribed"]
            return row + metric_order.index(metric)  # ❌ WRONG OFFSET
```

**Why 12d worked**:
- Code looks for: "12d"
- Excel has: "12d" in column D at row 59
- Template found! ✅
- Metric "Sent" at index 0
- Calculated row: 59 + 0 = 59
- Actual "Sent" at E59 ✅
- Values copied successfully

**Why 1h-10d failed**:
- Code looks for: "1 h" (with space), "4 d", "6 d", "8 d", "10 d"
- Excel has: "1h", "4d", "6d", "8d", "10d" (NO spaces)
- Template NOT found ❌
- Function returns None
- No values copied

**Why 10min failed**:
- Code looks for: "10 мин" (Cyrillic)
- Excel has: "10 min" (Latin)
- Template NOT found ❌
- Function returns None
- No values copied

**Why 1d failed**:
- Code looks for: "2 d"
- Excel has: "1d"
- Template NOT found ❌
- Function returns None
- No values copied

## File Structure Analysis

### Source File: `output/test_week_replace_with_ab.xlsx`

```
Column A: Signed up
Column B: casino+sport A/B Reg_No_Dep
Column C: Template (10min, 1h, 1d, 4d, 6d, 8d, 10d, 12d)
Column D: Metric (Sent, Delivered, Opened, Clicked, Unsubscribed)
Column F: Week 5 values

Row 3:  B=casino+sport A/B Reg_No_Dep, C=10min, D=Sent, F=733
Row 4:  D=Delivered, F=701
Row 5:  D=Opened, F=89
Row 6:  D=Clicked, F=18
Row 7:  D=Unsubscribed, F=1
```

### Target File: `test_week5/test_Beonbet_Chains.xlsx`

**Sheet: 'WP Chains Sport'** (CORRECT SHEET ✅)

```
Column B: Campaign
Column C: All Mail (or empty)
Column D: Template OR Metric
Column BB: Week 5 values

Row 3:  B=casino+sport A/B Reg_No_Dep, C=All Mail, D=10 min\n#2250..., BB=None
Row 4:  D=Sent, BB=None
Row 5:  D=Delivered, BB=None
Row 6:  D=Opened, BB=None
Row 7:  D=Clicked, BB=None
Row 8:  D=Unsubscribe, BB=None

Row 11: D=1h, BB=None
Row 12: D=Sent, BB=None
Row 13: D=Delivered, BB=None
...

Row 59: D=12d, BB=None → 313 ✅
Row 60: D=Sent, BB=None → 302 ✅
Row 61: D=Delivered, BB=None → 49 ✅
```

**Key observation**: In 'WP Chains Sport', the template name and first metric are in DIFFERENT rows:
- Row 11: Template "1h"
- Row 12: Metric "Sent"

But for 12d, they happen to be in the SAME row:
- Row 59: Both template "12d" AND metric "Sent"

## Command Executed

```bash
python3 -m report_automation generate \
  "test_week5/test_ret1_metrics.csv,test_week5/test_ret2_metrics.csv,test_week5/test_ab_metrics.csv" \
  output/test_week_replace_with_ab.xlsx \
  --report-type casino-ret \
  --existing-excel test_week5/test_Beonbet_Chains.xlsx \
  --replace-week 05
```

## Actual Results

### Log Output
```
INFO - Copied casino+sport A/B Reg_No_Dep/12d/Sent: 313 to row 59
INFO - Copied casino+sport A/B Reg_No_Dep/12d/Delivered: 302 to row 60
INFO - Copied casino+sport A/B Reg_No_Dep/12d/Opened: 49 to row 61
INFO - Copied casino+sport A/B Reg_No_Dep/12d/Clicked: 1 to row 62
INFO - Copied casino+sport A/B Reg_No_Dep/12d/Unsubscribed: 2 to row 63
INFO - Copied Ret 1 dep [SPORT] ⚽️/3d/Sent: 147 to row 75
INFO - Copied Ret 1 dep [SPORT] ⚽️/3d/Delivered: 146 to row 76
INFO - Copied Ret 1 dep [SPORT] ⚽️/3d/Opened: 44 to row 77
INFO - Copied Ret 1 dep [SPORT] ⚽️/3d/Clicked: 4 to row 78
INFO - Copied Ret 1 dep [SPORT] ⚽️/3d/Unsubscribed: 3 to row 79
INFO - Copied Ret 2 dep [SPORT] ⚽️/3d/Sent: 18 to row 123
INFO - Copied Ret 2 dep [SPORT] ⚽️/3d/Delivered: 18 to row 124
INFO - Copied Ret 2 dep [SPORT] ⚽️/3d/Opened: 3 to row 125
INFO - Copied Ret 2 dep [SPORT] ⚽️/3d/Clicked: 1 to row 126
INFO - Copied Ret 2 dep [SPORT] ⚽️/3d/Unsubscribed: 0 to row 127
INFO - Updated Excel saved: test_week5/updated_test_Beonbet_Chains.xlsx (15 values)
```

**Result**: Only 15 values copied (12d + Ret campaigns), NOT 40 values.

## Required Fixes

### Fix: Update Template Mappings

**File**: `src/report_automation/plugins/implementations/casino_ret.py` (line 307-317)

Change the entire template_map from:
```python
template_map = {
    "10min": "10 мин",  # ❌ Cyrillic
    "1h": "1 h",        # ❌ Has space
    "1d": "2 d",        # ❌ Wrong number
    "3d": "3d", 
    "4d": "4 d",        # ❌ Has space
    "6d": "6 d",        # ❌ Has space
    "8d": "8 d",        # ❌ Has space
    "10d": "10 d",      # ❌ Has space
    "12d": "12d"
}
```

To:
```python
template_map = {
    "10min": "10 min",  # ✅ Latin with space
    "1h": "1h",         # ✅ No space
    "1d": "1d",         # ✅ Correct number
    "3d": "3d", 
    "4d": "4d",         # ✅ No space
    "6d": "6d",         # ✅ No space
    "8d": "8d",         # ✅ No space
    "10d": "10d",       # ✅ No space
    "12d": "12d"
}
```

**Note**: The row offset calculation is already CORRECT. No changes needed there.

## Expected Results After Fixes

| Template | Target Row | Expected Value | Current Value | After Fix |
|----------|------------|----------------|---------------|-----------|
| 10min | 4 | 733 | None | 733 ✅ |
| 1h | 12 | 661 | None | 661 ✅ |
| 1d | 20 | 661 | None | 661 ✅ |
| 4d | 28 | 693 | None | 693 ✅ |
| 6d | 36 | 660 | None | 660 ✅ |
| 8d | 44 | 557 | None | 557 ✅ |
| 10d | 52 | 277 | None | 277 ✅ |
| 12d | 60 | 302 | 302 | 302 ✅ |

**Total**: 40 values (8 templates × 5 metrics) should be copied to 'WP Chains Sport' sheet.

## Fix Implementation Results

### ✅ FIX SUCCESSFUL - All 90 values copied!

**Command executed**:
```bash
python3 -m report_automation generate \
  "test_week5/test_ret1_metrics.csv,test_week5/test_ret2_metrics.csv,test_week5/test_ab_metrics.csv" \
  output/test_week_replace_FIXED.xlsx \
  --report-type casino-ret \
  --existing-excel test_week5/test_Beonbet_Chains.xlsx \
  --replace-week 05
```

**Results**:
- ✅ **90 values copied** (was 15 before fix)
- ✅ **casino+sport A/B**: All 8 templates × 5 metrics = 40 values
- ✅ **Ret 1 dep**: All 5 templates × 5 metrics = 25 values
- ✅ **Ret 2 dep**: All 5 templates × 5 metrics = 25 values

**Verification**:

| Template | Expected | Actual | Status |
|----------|----------|--------|--------|
| 10min | 733 | 733 | ✅ |
| 1h | 661 | 661 | ✅ |
| 1d | 661 | 661 | ✅ |
| 4d | 693 | 693 | ✅ |
| 6d | 660 | 660 | ✅ |
| 8d | 557 | 557 | ✅ |
| 10d | 277 | 277 | ✅ |
| 12d | 313 | 313 | ✅ |

## Summary

### Current State
- ❌ **15 values copied** (only 12d + Ret campaigns)
- ❌ **25 values missing** (10min through 10d for casino+sport campaign)
- ✅ Correct sheet targeted ('WP Chains Sport')

### Root Cause
**Template mapping mismatches**: The code's template_map has incorrect values that don't match the actual Excel file.

### Solution
Update template_map in `_find_target_row()` function to match exact Excel values:
- "10 мин" → "10 min" (Latin)
- "1 h" → "1h" (remove space)
- "2 d" → "1d" (correct number)
- "4 d" → "4d" (remove space)
- "6 d" → "6d" (remove space)
- "8 d" → "8d" (remove space)
- "10 d" → "10d" (remove space)

### Files Involved

| File | Purpose | Status |
|------|---------|--------|
| `output/test_week_replace_with_ab.xlsx` | Generated report (source) | ✅ Correct |
| `test_week5/test_Beonbet_Chains.xlsx` | Original template | ✅ Correct |
| `test_week5/updated_test_Beonbet_Chains.xlsx` | Updated report | ❌ Partially updated (15/40 values) |
| `src/report_automation/plugins/implementations/casino_ret.py` | Code with bugs | ❌ Needs 3 fixes |
