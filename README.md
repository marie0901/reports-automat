# Report Automation System v2

Automated report generation system with plugin architecture for marketing campaign analytics.

## Installation

```bash
pip install -e .
```

## Quick Start

### 1. Casino-Ret Report ✅

Processes casino and retention campaigns with week replacement support.

**Generate new report:**
```bash
python3 -m report_automation generate \
  "test_ret1_metrics.csv,test_ret2_metrics.csv,test_ab_metrics.csv" \
  output/casino_ret_report.xlsx \
  --report-type casino-ret
```

**Replace week in existing Excel:**
```bash
python3 -m report_automation generate \
  "test_ret1_metrics.csv,test_ret2_metrics.csv,test_ab_metrics.csv" \
  output/casino_ret_report.xlsx \
  --report-type casino-ret \
  --existing-excel "existing_report.xlsx" \
  --replace-week 05
```

**Template Mapping:**
```
CSV Templates              → Target Excel Names
─────────────────────────────────────────────────
[C] 10 min casino basic wp → "10 min"
[C] 1h casino basic wp     → "1h"
[C] 1d casino basic wp     → "1d"
[C] 3d casino basic wp     → "3d"
[C] 7d casino basic wp     → "7d"
[C] 14d casino basic wp    → "14d"
```

**Target Sheet:** `WP Chains Sport`  
**Metrics per block:** 6 (Sent, Delivered, Opened, Clicked, Converted, Unsubscribed)  
**Week replacement:** ✅ Supported (90 values copied)

---

### 2. AWOL Report ✅

Processes inactive user campaigns with formula preservation and week replacement support.

**Generate new report:**
```bash
python3 -m report_automation generate \
  "test_inactive7j19-31.csv,test_inactive14j12-31.csv,test_inactive22j5-31.csv,test_inactive31jx-31.csv" \
  output/awol_report.xlsx \
  --report-type awol
```

**Replace week in existing Excel:**
```bash
python3 -m report_automation generate \
  "test_inactive7j19-31.csv,test_inactive14j12-31.csv,test_inactive22j5-31.csv,test_inactive31jx-31.csv" \
  output/awol_report.xlsx \
  --report-type awol \
  --existing-excel "existing_report.xlsx" \
  --replace-week 05
```

**Template Mapping:**
```
CSV Templates    → Target Excel Names
──────────────────────────────────────
Day 1 inactive   → "1d"
Day 3 inactive   → "3d"
Day 7 inactive   → "7d"
Day 14 inactive  → "14d"
Day 22 inactive  → "22d"
Day 31+ inactive → "31d"
```

**Target Sheet:** `AWOL Chains Sport`  
**Metrics per block:** 8 (Sent, Delivered, Opened, Clicked, Converted, Unsubscribed, + 4 percentage formulas)  
**Week replacement:** ✅ Supported (60 values copied, formulas preserved)

---

### 3. A-B Report ✅

Processes sport A/B testing campaigns with time-based aggregation.

**Generate new report:**
```bash
python3 -m report_automation generate \
  "test_week5/test_ab_metrics.csv" \
  output/ab_report.xlsx \
  --report-type a-b-report
```

**Template Mapping:**
```
CSV Templates                              → Target Time Period
────────────────────────────────────────────────────────────────
[S] 10 min sport basic wp                  → "10m"
[S] 1h sport basic wp                      → "1h"
[S] 1d 2 BLOCKS (basic wp + highroller)    → "1d"
[S] 3d casino 1st dep total wp             → "3d"
[S] 5d casino 1st dep                      → "5d"
[S] 7d 2 BLOCKS SPORT + CAS                → "7d"
[S] 10d A: freebet + 100fs                 → "9d"
[S] 10d b: 150%sport + 100fs               → "9d"
[S] 12d A: freebet + 100fs                 → "12d"
[S] 12d b: 150%sport + 100fs               → "12d"
```

**Target Sheet:** New Excel (Sheet1)  
**Time periods:** 8 (10m, 1h, 1d, 3d, 5d, 7d, 9d, 12d)  
**Metrics per block:** 10 (Sent, Delivered, Opened, Clicked, Converted, Unsubscribed, + 4 percentages)  
**Week replacement:** ❌ Not supported (generates new Excel only)

**Week Boundaries:**
```
Week 1: 29.12 (2025-12-29 to 2026-01-04)
Week 2: 05.01 (2026-01-05 to 2026-01-11)
Week 3: 12.01 (2026-01-12 to 2026-01-18)
Week 4: 19.01 (2026-01-19 to 2026-01-25)
Week 5: 26.01 (2026-01-26 to 2026-02-01)
```

---

## Report Types Comparison

| Feature | casino-ret | awol | a-b-report |
|---------|------------|------|------------|
| **Status** | ✅ Working | ✅ Working | ✅ Working |
| **Multiple CSV files** | Yes (3) | Yes (4) | No (1) |
| **Week replacement** | ✅ Yes | ✅ Yes | ❌ No |
| **Target sheet** | WP Chains Sport | AWOL Chains Sport | New Excel |
| **Metrics per block** | 6 | 8 | 10 |
| **Formula preservation** | No | Yes | N/A |
| **Template variants** | 6 | 6 | 10 |

---

## Project Structure

```
src/report_automation/
├── domain/              # Core business logic & models
│   ├── models.py        # Data models (CampaignMetrics, ReportData)
│   └── aggregator.py    # Aggregation logic
├── infrastructure/      # External integrations
│   ├── csv_reader.py    # CSV file processing
│   ├── excel_writer.py  # Excel generation
│   └── config.py        # Configuration management
├── plugins/             # Extensible report type system
│   ├── base.py          # Plugin abstractions
│   └── implementations/
│       ├── casino_ret.py  # Casino & retention campaigns
│       ├── awol.py        # Inactive user campaigns
│       └── ab_report.py   # A/B testing campaigns
└── cli/                 # Command-line interface
    └── main.py          # CLI entry point
```

---

## Week Replacement Feature

Week replacement allows updating specific week columns in existing Excel reports without regenerating the entire file.

**Supported report types:**
- ✅ `casino-ret` - Replaces data in 'WP Chains Sport' sheet
- ✅ `awol` - Replaces data in 'AWOL Chains Sport' sheet with formula preservation
- ❌ `a-b-report` - Not supported (generates new Excel only)

**How it works:**
1. Reads existing Excel file
2. Identifies target week column (e.g., Week 5 → column BB)
3. Copies new data from generated report
4. Preserves formulas in target cells (AWOL only)
5. Saves updated Excel file

**Example:**
```bash
# Replace Week 5 data in existing report
python3 -m report_automation generate \
  "data.csv" \
  output.xlsx \
  --report-type casino-ret \
  --existing-excel "existing_report.xlsx" \
  --replace-week 05
```

---

## Documentation

Detailed documentation available in `/docs`:

- `casino-ret-report-structure.md` - Casino-ret report structure and mappings
- `awol-report-structure.md` - AWOL report structure and formula preservation
- `ab-report-template-mapping.md` - A-B report template mappings
- `week-replacement-analysis.md` - Week replacement implementation details
- `report-types-summary.md` - Complete comparison of all report types

---

## Testing

Test data available in `/test_week5`:
- `test_ab_metrics.csv` - A/B testing data
- `test_ret1_metrics.csv` - Retention 1 deposit data
- `test_ret2_metrics.csv` - Retention 2 deposit data
- `test_inactive*.csv` - Inactive user campaign data
- `test_ab_target.xlsx` - Target Excel structure for A/B reports

---

## Development

### Adding a New Report Type

1. Create plugin in `src/report_automation/plugins/implementations/`
2. Inherit from `BaseReportPlugin`
3. Implement required methods:
   - `process_csv()` - Read and parse CSV
   - `transform_data()` - Transform to report format
   - `generate_excel()` - Generate Excel output
4. Register with `@register_plugin` decorator

Example:
```python
from ..base import BaseReportPlugin, register_plugin

@register_plugin
class MyReportPlugin(BaseReportPlugin):
    name = "my-report"
    supports_multiple_files = False
    
    def process_csv(self, csv_path):
        # Implementation
        pass
```

---

## License

Internal use only.
