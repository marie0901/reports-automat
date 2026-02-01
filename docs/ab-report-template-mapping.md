# A-B Report Template Mapping

## Overview

This document defines the correct template mapping for the `a-b-report` plugin based on:
- **Source**: `/test_week5/test_ab_metrics.csv`
- **Target**: `/test_week5/test_ab_target.xlsx` (Sheet1, columns G-H)

## Target Excel Structure

The target Excel expects **8 time period blocks** in merged cells G-H:

| Row | Time Period | Description |
|-----|-------------|-------------|
| 2   | 10m         | 10 minutes  |
| 14  | 1h          | 1 hour      |
| 26  | 1d          | 1 day       |
| 38  | 3d          | 3 days      |
| 50  | 5d          | 5 days      |
| 62  | 7d          | 7 days      |
| 74  | 9d          | 9 days      |
| 86  | 12d         | 12 days     |

## CSV Templates Available

The CSV contains **10 [S] templates** (Sport campaigns):

```
[S] 10 min sport basic wp
[S] 1h sport basic wp
[S] 1d 2 BLOCKS (basic wp + highroller)
[S] 3d casino 1st dep total wp
[S] 5d casino 1st dep
[S] 7d 2 BLOCKS SPORT + CAS
[S] 10d A: freebet + 100fs
[S] 10d b: 150%sport + 100fs
[S] 12d A: freebet + 100fs
[S] 12d b: 150%sport + 100fs
```

## Correct Template Mapping

### Python Dictionary Format

```python
TEMPLATE_MAPPING = {
    # 10 minutes
    "[S] 10 min sport basic wp": "10m",
    
    # 1 hour
    "[S] 1h sport basic wp": "1h",
    
    # 1 day
    "[S] 1d 2 BLOCKS (basic wp + highroller)": "1d",
    
    # 3 days
    "[S] 3d casino 1st dep total wp": "3d",
    
    # 5 days
    "[S] 5d casino 1st dep": "5d",
    
    # 7 days
    "[S] 7d 2 BLOCKS SPORT + CAS": "7d",
    
    # 9 days (mapped from 10d templates - likely renamed campaign)
    "[S] 10d A: freebet + 100fs": "9d",
    "[S] 10d b: 150%sport + 100fs": "9d",
    
    # 12 days (two variants: A and B)
    "[S] 12d A: freebet + 100fs": "12d",
    "[S] 12d b: 150%sport + 100fs": "12d",
}
```

## Mapping Notes

### ✅ Complete Coverage
All 8 target time periods have matching templates:
- **10m**: 1 template
- **1h**: 1 template
- **1d**: 1 template
- **3d**: 1 template
- **5d**: 1 template
- **7d**: 1 template
- **9d**: 2 templates (10d A + 10d B)
- **12d**: 2 templates (12d A + 12d B)

### ⚠️ 10d → 9d Mapping
The CSV contains `10d` templates but the target Excel expects `9d`:
- **Decision**: Map `10d` templates → `9d` block
- **Reason**: Likely a campaign rename or the target Excel uses 9d as the canonical name
- **Impact**: Both 10d variants (A and B) will aggregate into the 9d time period

### 📊 Multiple Templates per Period
Some time periods have multiple template variants:
- **9d**: 2 templates (A: freebet, B: 150%sport)
- **12d**: 2 templates (A: freebet, B: 150%sport)

When multiple templates map to the same period, their metrics should be **aggregated** (summed).

## Comparison: Old vs New Mapping

### ❌ Old Mapping (INCORRECT)
```python
TEMPLATE_MAPPING = {
    "[S] 10 min sport basic wp": "10m",
    "[S] 1h sport basic wp": "1h",
    "[S] 2d sport basic wp": "1d",    # ❌ Template doesn't exist
    "[S] 4d sport basic wp": "3d",    # ❌ Template doesn't exist
    "[S] 8d sport basic wp": "7d"     # ❌ Template doesn't exist
}
```

**Problems**:
- Only 2/5 templates exist in CSV
- Missing 5d, 9d, 12d periods
- Uses fictional template names

### ✅ New Mapping (CORRECT)
```python
TEMPLATE_MAPPING = {
    "[S] 10 min sport basic wp": "10m",
    "[S] 1h sport basic wp": "1h",
    "[S] 1d 2 BLOCKS (basic wp + highroller)": "1d",
    "[S] 3d casino 1st dep total wp": "3d",
    "[S] 5d casino 1st dep": "5d",
    "[S] 7d 2 BLOCKS SPORT + CAS": "7d",
    "[S] 10d A: freebet + 100fs": "9d",
    "[S] 10d b: 150%sport + 100fs": "9d",
    "[S] 12d A: freebet + 100fs": "12d",
    "[S] 12d b: 150%sport + 100fs": "12d",
}
```

**Benefits**:
- ✅ All 10 templates mapped
- ✅ All 8 target periods covered
- ✅ Uses actual template names from CSV
- ✅ Handles multiple variants per period

## Implementation

Update `/src/report_automation/plugins/implementations/ab_report.py`:

```python
# Replace the TEMPLATE_MAPPING constant with:
TEMPLATE_MAPPING = {
    "[S] 10 min sport basic wp": "10m",
    "[S] 1h sport basic wp": "1h",
    "[S] 1d 2 BLOCKS (basic wp + highroller)": "1d",
    "[S] 3d casino 1st dep total wp": "3d",
    "[S] 5d casino 1st dep": "5d",
    "[S] 7d 2 BLOCKS SPORT + CAS": "7d",
    "[S] 10d A: freebet + 100fs": "9d",
    "[S] 10d b: 150%sport + 100fs": "9d",
    "[S] 12d A: freebet + 100fs": "12d",
    "[S] 12d b: 150%sport + 100fs": "12d",
}

# Update TIME_PERIODS to include all 8 periods:
TIME_PERIODS = ["10m", "1h", "1d", "3d", "5d", "7d", "9d", "12d"]
```

## Testing

After updating the mapping, test with:

```bash
python3 -m report_automation generate \
  "test_week5/test_ab_metrics.csv" \
  output/ab_report.xlsx \
  --report-type a-b-report
```

Expected result: All 8 time period blocks should have data populated.
