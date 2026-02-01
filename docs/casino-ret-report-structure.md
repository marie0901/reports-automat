# Casino-Ret Report Structure Documentation

## Command
```bash
python3 -m report_automation generate \
  "test_week5/test_ret1_metrics.csv,test_week5/test_ret2_metrics.csv,test_week5/test_ab_metrics.csv" \
  output/test_week_replace.xlsx \
  --report-type casino-ret \
  --existing-excel test_week5/test_Beonbet_Chains.xlsx \
  --replace-week 05
```

## Report Type Configuration

### Sheet Mapping
The `casino-ret` report type updates the **"WP Chains Sport"** sheet in the existing Excel file.

```python
SHEET_MAPPINGS = {
    'casino-ret': 'WP Chains Sport'
}
```

## Overview
This document explains how the `casino-ret` report type processes CSV files and generates the Excel output.

## Data Flow Architecture

```mermaid
graph TB
    subgraph "Input CSV Files"
        CSV1[test_ret1_metrics.csv]
        CSV2[test_ret2_metrics.csv]
        CSV3[test_ab_metrics.csv]
    end
    
    subgraph "Processing"
        P1[CSV Reader]
        P2[Template Mapper]
        P3[Weekly Aggregator]
        P4[Excel Generator]
    end
    
    subgraph "Output Excel"
        E1[output/test_week_replace.xlsx]
    end
    
    CSV1 --> P1
    CSV2 --> P1
    CSV3 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> E1
```

## CSV to Excel Mapping

### File 1: test_ab_metrics.csv ✅ IMPLEMENTED

```mermaid
flowchart LR
    subgraph CSV["test_ab_metrics.csv"]
        direction TB
        C0["campaign_name: casino+sport A/B Reg_No_Dep"]
        T0["Templates:<br/>- [S] 10 min sport basic wp<br/>- [S] 1h sport basic wp<br/>- [S] 1d 2 BLOCKS<br/>- [S] 3d casino 1st dep total wp<br/>- [S] 5d casino 1st dep<br/>- [S] 7d 2 BLOCKS SPORT + CAS<br/>- [S] 10d A/B<br/>- [S] 12d A/B"]
        D0["Date Range:<br/>2026-01-12 to 2026-01-31"]
    end
    
    subgraph Mapping["CASINOSPORT_MAPPINGS"]
        M0["[S] 10 min sport basic wp to 10min<br/>[S] 1h sport basic wp to 1h<br/>[S] 1d 2 BLOCKS to 1d<br/>[S] 3d casino 1st dep total wp to 4d<br/>[S] 5d casino 1st dep to 6d<br/>[S] 7d 2 BLOCKS SPORT + CAS to 8d<br/>[S] 10d A/B to 10d<br/>[S] 12d A/B to 12d"]
    end
    
    subgraph Excel["Excel Output"]
        E0["Row 3: Campaign Header<br/>casino+sport A/B Reg_No_Dep"]
        E00["Rows 3-8: 10min block<br/>Rows 9-14: 1h block<br/>Rows 15-20: 1d block<br/>Rows 27-32: 4d block<br/>Rows 33-38: 6d block<br/>Rows 39-44: 8d block<br/>Rows 45-50: 10d block<br/>Rows 51-56: 12d block"]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

### File 2: test_ret1_metrics.csv

```mermaid
flowchart LR
    subgraph CSV["test_ret1_metrics.csv"]
        direction TB
        C1["campaign_name: Ret 1 dep SPORT"]
        T1["Templates:<br/>- Day 3<br/>- Day 4<br/>- Day 6<br/>- Day 8<br/>- Day 10"]
        D1["Date Range:<br/>2026-01-12 to 2026-01-31"]
    end
    
    subgraph Mapping["Template Mapping"]
        M1["Day 3 to 3d<br/>Day 4 to 4d<br/>Day 6 to 6d<br/>Day 8 to 8d<br/>Day 10 to 10d"]
    end
    
    subgraph Excel["Excel Output"]
        E1["Row 75: Campaign Header<br/>Ret 1 dep SPORT"]
        E2["Rows 93-98: 3d block<br/>Rows 99-104: 4d block<br/>Rows 105-110: 6d block<br/>Rows 111-116: 8d block<br/>Rows 117-122: 10d block"]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

### File 3: test_ret2_metrics.csv

```mermaid
flowchart LR
    subgraph CSV["test_ret2_metrics.csv"]
        direction TB
        C2["campaign_name: Ret 2 dep SPORT"]
        T2["Templates:<br/>- Day 3<br/>- Day 4<br/>- Day 6<br/>- Day 8<br/>- Day 10"]
        D2["Date Range:<br/>2026-01-12 to 2026-01-31"]
    end
    
    subgraph Mapping["Template Mapping"]
        M2["Day 3 to 3d<br/>Day 4 to 4d<br/>Day 6 to 6d<br/>Day 8 to 8d<br/>Day 10 to 10d"]
    end
    
    subgraph Excel["Excel Output"]
        E3["Row 123: Campaign Header<br/>Ret 2 dep SPORT"]
        E4["Rows 141-146: 3d block<br/>Rows 147-152: 4d block<br/>Rows 153-158: 6d block<br/>Rows 159-164: 8d block<br/>Rows 165-170: 10d block"]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

## Excel Output Structure

```mermaid
graph TD
    subgraph "Excel: output/test_week_replace.xlsx"
        H[Row 1: Week Headers]
        
        subgraph "Section 1: Signed up Row 3"
            S1["Row 3: casino+sport A/B Reg_No_Dep<br/>Data from test_ab_metrics.csv"]
        end
        
        subgraph "Section 2: deposits_quantity is 1 Row 75"
            C1["Row 75: Ret 1 dep SPORT"]
            B1[Rows 93-122: Template Blocks]
        end
        
        subgraph "Section 3: deposits_quantity is 2 Row 123"
            C2["Row 123: Ret 2 dep SPORT"]
            B2[Rows 141-170: Template Blocks]
        end
    end
    
    H --> S1
    S1 --> C1
    C1 --> B1
    B1 --> C2
    C2 --> B2
```

## Template Block Structure

Each template block contains 6 rows of metrics:

```mermaid
graph LR
    subgraph "Template Block Example: 3d at Row 93"
        R1[Row 93: Sent]
        R2[Row 94: Delivered]
        R3[Row 95: Opened]
        R4[Row 96: Clicked]
        R5[Row 97: Unsubscribed]
        R6[Row 98: Pct Delivered]
    end
    
    R1 --> R2 --> R3 --> R4 --> R5 --> R6
```

## Week Column Mapping

```mermaid
graph LR
    subgraph "Week Columns"
        W6[Column E: Week 6<br/>02.02]
        W5[Column F: Week 5<br/>26.01]
        W4[Column G: Week 4<br/>19.01]
        W3[Column H: Week 3<br/>12.01]
        W2[Column I: Week 2<br/>05.01]
        W1[Column J: Week 1<br/>29.12]
    end
```

## Data Aggregation by Week

```mermaid
flowchart TB
    subgraph "CSV Data Processing"
        D1["Raw CSV Data<br/>(timestamp, template_name, metrics)"]
        D2["Convert timestamp to datetime"]
        D3["Filter by weekly boundaries"]
        D4["Group by template_name"]
        D5["Sum metrics"]
    end
    
    subgraph "Weekly Boundaries"
        W1["Week 1: 2025-12-29 to 2026-01-04"]
        W2["Week 2: 2026-01-05 to 2026-01-11"]
        W3["Week 3: 2026-01-12 to 2026-01-18"]
        W4["Week 4: 2026-01-19 to 2026-01-25"]
        W5["Week 5: 2026-01-26 to 2026-02-01"]
        W6["Week 6: 2026-02-02 to 2026-02-08"]
    end
    
    D1 --> D2 --> D3 --> D4 --> D5
    D3 -.-> W1
    D3 -.-> W2
    D3 -.-> W3
    D3 -.-> W4
    D3 -.-> W5
    D3 -.-> W6
```

## Actual Data in Output

### Casino Section (Row 3): casino+sport A/B Reg_No_Dep

| Template | Metric | Week 5 (F) | Week 4 (G) | Week 3 (H) |
|----------|--------|------------|------------|------------|
| **10min** | Sent | 733 | - | - |
| | Delivered | 701 | - | - |
| | Opened | 89 | - | - |
| | Clicked | 18 | - | - |
| | Unsubscribed | 1 | - | - |
| **1h** | Sent | 661 | - | - |
| | Delivered | 631 | - | - |
| | Opened | 150 | - | - |
| **1d** | Sent | 661 | - | - |
| | Delivered | 631 | - | - |
| **4d** | Sent | 693 | - | - |
| | Delivered | 663 | - | - |
| **6d** | Sent | 660 | - | - |
| | Delivered | 632 | - | - |
| **8d** | Sent | 557 | - | - |
| | Delivered | 527 | - | - |
| **10d** | Sent | 277 | - | - |
| | Delivered | 263 | - | - |

### Retention Section 1 (Row 75): Ret 1 dep [SPORT] ⚽️

| Template | Metric | Week 5 (F) | Week 4 (G) | Week 3 (H) |
|----------|--------|------------|------------|------------|
| **3d** | Sent | 147 | 146 | 131 |
| | Delivered | 146 | 146 | 128 |
| | Opened | 44 | 43 | 31 |
| | Clicked | 4 | 3 | 2 |
| | Unsubscribed | 3 | 4 | 1 |
| **4d** | Sent | 132 | 145 | 122 |
| | Delivered | 132 | 145 | 121 |
| | Opened | 29 | 29 | 23 |
| **6d** | Sent | 132 | 128 | 107 |
| | Delivered | 132 | 128 | 107 |
| | Opened | 30 | 35 | 28 |
| **8d** | Sent | 105 | 129 | 102 |
| | Delivered | 105 | 129 | 102 |
| | Opened | 24 | 28 | 22 |
| **10d** | Sent | 115 | 109 | 129 |
| | Delivered | 115 | 109 | 129 |
| | Opened | 20 | 21 | 26 |

## Template Mapping Reference

### Casino Templates (CASINOSPORT_MAPPINGS)

```mermaid
graph LR
    subgraph "CSV Template Names"
        C1["[S] 10 min sport basic wp"]
        C2["[S] 1h sport basic wp"]
        C3["[S] 1d 2 BLOCKS"]
        C4["[S] 3d casino 1st dep total wp"]
        C5["[S] 5d casino 1st dep"]
        C6["[S] 7d 2 BLOCKS SPORT + CAS"]
        C7["[S] 10d A/B"]
        C8["[S] 12d A/B"]
    end
    
    subgraph "Generated Excel Names"
        G1["10min"]
        G2["1h"]
        G3["1d"]
        G4["4d"]
        G5["6d"]
        G6["8d"]
        G7["10d"]
        G8["12d"]
    end
    
    subgraph "Existing Excel Names"
        E1["10 min (Cyrillic)"]
        E2["1 h"]
        E3["2 d"]
        E4["4 d"]
        E5["6 d"]
        E6["8 d"]
        E7["10 d"]
        E8["12d"]
    end
    
    C1 --> G1 --> E1
    C2 --> G2 --> E2
    C3 --> G3 --> E3
    C4 --> G4 --> E4
    C5 --> G5 --> E5
    C6 --> G6 --> E6
    C7 --> G7 --> E7
    C8 --> G8 --> E8
```

### Retention Templates (RETENTION_MAPPINGS)

```mermaid
graph LR
    subgraph "CSV Template Names"
        T1["Day 3"]
        T2["Day 4"]
        T3["Day 6"]
        T4["Day 8"]
        T5["Day 10"]
    end
    
    subgraph "Excel Template Names"
        E1["3d"]
        E2["4d"]
        E3["6d"]
        E4["8d"]
        E5["10d"]
    end
    
    T1 --> E1
    T2 --> E2
    T3 --> E3
    T4 --> E4
    T5 --> E5
```

## TIMING_BLOCKS Configuration

The `TIMING_BLOCKS` constant defines where each template's data goes:

```python
TIMING_BLOCKS = {
    "10min": {"casino_rows": [3, 8]},
    "1h": {"casino_rows": [9, 14]},
    "1d": {"casino_rows": [15, 20]},
    "3d": {
        "casino_rows": [21, 26],
        "section_1_rows": [93, 98],   # Ret 1 dep
        "section_2_rows": [141, 146]  # Ret 2 dep
    },
    "4d": {
        "casino_rows": [27, 32],
        "section_1_rows": [99, 104],
        "section_2_rows": [147, 152]
    },
    "6d": {
        "casino_rows": [33, 38],
        "section_1_rows": [105, 110],
        "section_2_rows": [153, 158]
    },
    "8d": {
        "casino_rows": [39, 44],
        "section_1_rows": [111, 116],
        "section_2_rows": [159, 164]
    },
    "10d": {
        "casino_rows": [45, 50],
        "section_1_rows": [117, 122],
        "section_2_rows": [165, 170]
    },
    "12d": {"casino_rows": [51, 56]},
}
```

## Summary

```mermaid
graph TB
    subgraph "Input"
        I0["test_ab_metrics.csv<br/>Campaign: casino+sport A/B<br/>Templates: [S] 10 min, 1h, 1d, 3d, 5d, 7d, 10d, 12d<br/>Dates: Jan 12-31<br/>STATUS: PROCESSED"]
        I1["test_ret1_metrics.csv<br/>Campaign: Ret 1 dep<br/>Templates: Day 3,4,6,8,10<br/>Dates: Jan 12-31"]
        I2["test_ret2_metrics.csv<br/>Campaign: Ret 2 dep<br/>Templates: Day 3,4,6,8,10<br/>Dates: Jan 12-31"]
    end
    
    subgraph "Processing"
        P1["Map templates to timing codes"]
        P2["Aggregate by weeks"]
        P3["Calculate percentages"]
    end
    
    subgraph "Output Structure"
        O0["Row 3: casino+sport section<br/>Rows 3-56: 8 template blocks<br/>Week 5: 733 sent, 701 delivered"]
        O1["Row 75: Ret 1 dep section<br/>Rows 93-122: 5 template blocks<br/>Week 5: 147 sent, 146 delivered"]
        O2["Row 123: Ret 2 dep section<br/>Rows 141-170: 5 template blocks"]
        O3["Columns E-J: Week 6 to Week 1"]
    end
    
    I0 --> P1
    I1 --> P1
    I2 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> O0
    P3 --> O1
    P3 --> O2
    O0 --> O3
    O1 --> O3
    O2 --> O3
```

## Notes

- **Week 5 data is partial**: CSV only contains data through Jan 31, while Week 5 extends to Feb 1
- **Week 1-2 are empty**: CSV data starts from Jan 12 (Week 3)
- **All three files processed successfully**: Casino, Ret 1 dep, and Ret 2 dep sections all populated
- **Each template block**: 6 rows (Sent, Delivered, Opened, Clicked, Unsubscribed, Pct Delivered)

## Implementation Details

### File Detection Logic

The code detects which section to populate using:

1. **Campaign name detection** (primary):
   - Checks `campaign_name` field in CSV for `casino+sport` or `a/b`
   - Maps to casino section (Row 3)

2. **Template content detection** (secondary):
   - Checks template names for `[S]`, `sport`, `casino`, `FS`
   - Maps to casino section (Row 3)

3. **Filename detection** (fallback):
   - `casinosport` or `ab` in filename → casino section
   - `ret` + `1` in filename → Ret 1 dep section (Row 75)
   - `ret` + `2` in filename → Ret 2 dep section (Row 123)

### Week Replacement Results

**Test Run Results:**
- **35 values copied** to existing Excel
- **Source**: Column F (Week 5) from generated Excel
- **Target**: Column BB (Week 5) in existing Excel
- **Campaigns matched**: casino+sport A/B Reg_No_Dep
- **Templates matched**: 10 мин, 1 h, 2 d, 4 d, 6 d, 8 d, 10 d

### Template Name Mapping for Week Replacement

```python
template_map = {
    "10min": "10 мин",  # Cyrillic "min"
    "1h": "1 h",        # Space between number and unit
    "1d": "2 d",        # Note: 1d maps to "2 d" in Excel
    "3d": "3d",
    "4d": "4 d",
    "6d": "6 d",
    "8d": "8 d",
    "10d": "10 d",
    "12d": "12d"
}
```

