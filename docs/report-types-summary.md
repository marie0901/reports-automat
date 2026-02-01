# Report Types Summary

## Available Report Types

### 1. `casino-ret` ✅ FULLY FUNCTIONAL
**Plugin**: `CasinoRetPlugin`  
**File**: `casino_ret.py`  
**Purpose**: Casino and retention campaigns report

**Processes**:
- Casino/Sport A/B campaigns (test_ab_metrics.csv)
- Retention 1 deposit campaigns (test_ret1_metrics.csv)
- Retention 2 deposit campaigns (test_ret2_metrics.csv)

**Target Sheet**: `WP Chains Sport`

**Command**:
```bash
python3 -m report_automation generate \
  "test_ret1_metrics.csv,test_ret2_metrics.csv,test_ab_metrics.csv" \
  output/report.xlsx \
  --report-type casino-ret \
  --existing-excel existing.xlsx \
  --replace-week 05
```

**Status**: ✅ Working (90 values copied)

---

### 2. `awol` ✅ FULLY FUNCTIONAL
**Plugin**: `AWOLPlugin`  
**File**: `awol.py`  
**Purpose**: Inactive users campaigns report (AWOL = Absent Without Leave)

**Processes**:
- Inactive 7 days campaigns (test_inactive7j19-31.csv)
- Inactive 14 days campaigns (test_inactive14j12-31.csv)
- Inactive 22 days campaigns (test_inactive22j5-31.csv)
- Inactive 31+ days campaigns (test_inactive31jx-31.csv)

**Target Sheet**: `AWOL Chains Sport`

**Command**:
```bash
python3 -m report_automation generate \
  "test_inactive7j19-31.csv,test_inactive14j12-31.csv,test_inactive22j5-31.csv,test_inactive31jx-31.csv" \
  output/report.xlsx \
  --report-type awol \
  --existing-excel existing.xlsx \
  --replace-week 05
```

**Status**: ✅ Working (60 values copied, formulas preserved)

---

### 3. `a-b-report` ⚠️ EXISTS BUT NOT TESTED
**Plugin**: `ABReportPlugin`  
**File**: `ab_report.py`  
**Purpose**: A/B testing report (V3 specification)

**Processes**:
- Sport A/B campaigns with specific templates
- Time-based aggregation (10m, 1h, 1d, 3d, 7d)

**Template Mapping**:
```python
{
    "[S] 10 min sport basic wp": "10m",
    "[S] 1h sport basic wp": "1h",
    "[S] 2d sport basic wp": "1d",
    "[S] 4d sport basic wp": "3d",
    "[S] 8d sport basic wp": "7d"
}
```

**Target Sheet**: Not specified (generates new Excel)

**Command**:
```bash
python3 -m report_automation generate \
  "ab_test_metrics.csv" \
  output/ab_report.xlsx \
  --report-type a-b-report
```

**Status**: ⚠️ Not tested, no week replacement support

---

## Report Type Naming Analysis

### Current Names
1. `casino-ret` - Descriptive, clear purpose
2. `awol` - Acronym, industry-specific
3. `a-b-report` - Descriptive with hyphen

### Recommendation for A/B Report Type

**Current name**: `a-b-report`  
**Alternative names**:
- `ab-test` - Shorter, common industry term
- `ab-report` - Consistent with current name, no hyphens in "ab"
- `sport-ab` - More specific to sport campaigns
- `ab-sport` - Emphasizes A/B testing for sport

**Recommendation**: Keep `a-b-report` as is, because:
1. ✅ Already registered in code
2. ✅ Clear and descriptive
3. ✅ Follows pattern of being explicit
4. ✅ Hyphen separates "a-b" from "report" for clarity

---

## Comparison Table

| Feature | casino-ret | awol | a-b-report |
|---------|------------|------|------------|
| **Status** | ✅ Working | ✅ Working | ⚠️ Untested |
| **Multiple files** | Yes (3) | Yes (4) | No (1) |
| **Week replacement** | Yes | Yes | No |
| **Target sheet** | WP Chains Sport | AWOL Chains Sport | N/A |
| **Metrics per block** | 6 | 8 | 10 |
| **Formula preservation** | No | Yes | N/A |
| **Documentation** | ✅ Complete | ✅ Complete | ❌ Missing |

---

## Registered Plugins

From `__init__.py`:
```python
from .ab_report import ABReportPlugin
from .casino_ret import CasinoRetPlugin
from .awol import AWOLPlugin

__all__ = ["ABReportPlugin", "CasinoRetPlugin", "AWOLPlugin"]
```

All three plugins are properly registered and available.

---

## Usage Summary

### For Casino/Retention campaigns:
```bash
--report-type casino-ret
```

### For Inactive user campaigns:
```bash
--report-type awol
```

### For A/B testing (V3 spec):
```bash
--report-type a-b-report
```

---

## Conclusion

**We have 3 report types**:
1. ✅ `casino-ret` - Fully functional
2. ✅ `awol` - Fully functional  
3. ⚠️ `a-b-report` - Exists but untested

**The A/B report type should be called**: `a-b-report` (keep current name)
