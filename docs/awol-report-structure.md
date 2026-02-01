# AWOL Report Structure Documentation

## Command
```bash
python3 -m report_automation generate \
  "test_week5/test_inactive7j19-31.csv,test_week5/test_inactive14j12-31.csv,test_week5/test_inactive22j5-31.csv,test_week5/test_inactive31jx-31.csv" \
  output/test_awol_week_replace.xlsx \
  --report-type awol \
  --existing-excel test_week5/test_Beonbet_Chains.xlsx \
  --replace-week 05
```

## Report Type Configuration

### Sheet Mapping
The `awol` report type updates the **"AWOL Chains Sport"** sheet in the existing Excel file.

```python
SHEET_MAPPINGS = {
    'awol': 'AWOL Chains Sport'
}
```

## Overview
This document explains how the `awol` report type processes CSV files for inactive user campaigns and generates the Excel output.

## Data Flow Architecture

```mermaid
graph TB
    subgraph "Input CSV Files"
        CSV1[test_inactive7j19-31.csv]
        CSV2[test_inactive14j12-31.csv]
        CSV3[test_inactive22j5-31.csv]
        CSV4[test_inactive31jx-31.csv]
    end
    
    subgraph "Processing"
        P1[CSV Reader]
        P2[Template Mapper]
        P3[Weekly Aggregator]
        P4[Excel Generator]
    end
    
    subgraph "Output Excel"
        E1[output/test_awol_week_replace.xlsx]
    end
    
    CSV1 --> P1
    CSV2 --> P1
    CSV3 --> P1
    CSV4 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> E1
```

## CSV to Excel Mapping

### File 1: test_inactive7j19-31.csv

```mermaid
flowchart LR
    subgraph CSV["test_inactive7j19-31.csv"]
        direction TB
        C0["campaign_name: Inactive 7"]
        T0["Templates:<br/>- Day 1"]
        D0["Date Range:<br/>2026-01-19 to 2026-01-30"]
    end
    
    subgraph Mapping["AWOL_MAPPINGS"]
        M0["Day 1 to 1d"]
    end
    
    subgraph Excel["Excel Output"]
        E0["Row 3: Campaign Header<br/>inactive 7"]
        E00["Rows 3-10: 1d block"]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

### File 2: test_inactive14j12-31.csv

```mermaid
flowchart LR
    subgraph CSV["test_inactive14j12-31.csv"]
        direction TB
        C1["campaign_name: Inactive 14"]
        T1["Templates:<br/>- Day 1<br/>- Day 3"]
        D1["Date Range:<br/>2026-01-12 to 2026-01-30"]
    end
    
    subgraph Mapping["Template Mapping"]
        M1["Day 1 to 1d<br/>Day 3 to 3d"]
    end
    
    subgraph Excel["Excel Output"]
        E1["Row 11: Campaign Header<br/>inactive 14"]
        E2["Rows 11-18: 1d block<br/>Rows 19-26: 3d block"]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

### File 3: test_inactive22j5-31.csv

```mermaid
flowchart LR
    subgraph CSV["test_inactive22j5-31.csv"]
        direction TB
        C2["campaign_name: Inactive 22"]
        T2["Templates:<br/>- Day 1<br/>- Day 5"]
        D2["Date Range:<br/>2026-01-05 to 2026-01-30"]
    end
    
    subgraph Mapping["Template Mapping"]
        M2["Day 1 to 1d<br/>Day 5 to 5d"]
    end
    
    subgraph Excel["Excel Output"]
        E3["Row 27: Campaign Header<br/>inactive 22"]
        E4["Rows 27-34: 1d block<br/>Rows 35-42: 5d block"]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

### File 4: test_inactive31jx-31.csv

```mermaid
flowchart LR
    subgraph CSV["test_inactive31jx-31.csv"]
        direction TB
        C3["campaign_name: Inactive 31+"]
        T3["Templates:<br/>- Day 1<br/>- Day 5<br/>- Day 10<br/>- Day 15<br/>- Day 20<br/>- Day 30<br/>- Day 40"]
        D3["Date Range:<br/>2026-01-19 to 2026-01-30"]
    end
    
    subgraph Mapping["Template Mapping"]
        M3["Day 1 to 1d<br/>Day 5 to 5d<br/>Day 10 to 10d<br/>etc."]
    end
    
    subgraph Excel["Excel Output"]
        E5["Row 43: Campaign Header<br/>inactive 31+"]
        E6["Rows 43-50: 1d block<br/>Rows 51-58: 5d block<br/>etc."]
    end
    
    CSV --> Mapping
    Mapping --> Excel
```

## Excel Output Structure

```mermaid
graph TD
    subgraph "Excel: output/test_awol_week_replace.xlsx"
        H[Row 1: Week Headers]
        
        subgraph "Section 1: Inactive 7 Row 3"
            S1["Row 3: inactive 7<br/>Data from test_inactive7j19-31.csv"]
        end
        
        subgraph "Section 2: Inactive 14 Row 11"
            C1["Row 11: inactive 14"]
            B1[Rows 11-26: Template Blocks]
        end
        
        subgraph "Section 3: Inactive 22 Row 27"
            C2["Row 27: inactive 22"]
            B2[Rows 27-42: Template Blocks]
        end
        
        subgraph "Section 4: Inactive 31+ Row 43"
            C3["Row 43: inactive 31+"]
            B3[Rows 43+: Template Blocks]
        end
    end
    
    H --> S1
    S1 --> C1
    C1 --> B1
    B1 --> C2
    C2 --> B2
    B2 --> C3
    C3 --> B3
```

## Template Block Structure

Each template block contains **8 rows** of metrics:

```mermaid
graph LR
    subgraph "Template Block Example: 1d at Row 3"
        R1[Row 3: Sent]
        R2[Row 4: Delivered]
        R3[Row 5: Opened]
        R4[Row 6: Clicked]
        R5[Row 7: Unsubscribed]
        R6[Row 8: % Delivered FORMULA]
        R7[Row 9: % Open FORMULA]
        R8[Row 10: % Click FORMULA]
    end
    
    R1 --> R2 --> R3 --> R4 --> R5 --> R6 --> R7 --> R8
```

**Important**: Rows 6-8 contain FORMULAS in the target Excel, not values.

## Week Column Mapping

```mermaid
graph LR
    subgraph "Week Columns"
        W6[Column F: Week 6<br/>02.02]
        W5[Column G: Week 5<br/>26.01]
        W4[Column H: Week 4<br/>19.01]
        W3[Column I: Week 3<br/>12.01]
        W2[Column J: Week 2<br/>05.01]
        W1[Column K: Week 1<br/>29.12]
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

### Inactive 7 Section (Row 3): inactive 7

| Template | Metric | Week 5 (G) | Week 4 (H) | Week 3 (I) |
|----------|--------|------------|------------|------------|
| **1d** | Sent | 25 | 49 | - |
| | Delivered | 25 | 49 | - |
| | Opened | 5 | 25 | - |
| | Clicked | 2 | 7 | - |
| | Unsubscribed | 0 | 0 | - |
| | % Delivered | =BB4/BB3 | =BC4/BC3 | - |
| | % Open | =BB5/BB4 | =BC5/BC4 | - |
| | % Click | =BB6/BB4 | =BC6/BC4 | - |

### Inactive 14 Section (Row 11): inactive 14

| Template | Metric | Week 5 (G) | Week 4 (H) | Week 3 (I) |
|----------|--------|------------|------------|------------|
| **1d** | Sent | 26 | 32 | 85 |
| | Delivered | 26 | 31 | 85 |
| | Opened | 10 | 11 | 33 |
| | Clicked | 2 | 2 | 3 |
| **3d** | Sent | 19 | 51 | 65 |
| | Delivered | 19 | 51 | 65 |
| | Opened | 8 | 17 | 19 |

### Inactive 22 Section (Row 27): inactive 22

| Template | Metric | Week 5 (G) | Week 4 (H) | Week 3 (I) | Week 2 (J) |
|----------|--------|------------|------------|------------|------------|
| **1d** | Sent | 22 | 79 | 40 | 38 |
| | Delivered | 22 | 79 | 36 | 37 |
| | Opened | 6 | 24 | 13 | 8 |
| **5d** | Sent | 56 | 41 | 40 | 18 |
| | Delivered | 56 | 41 | 40 | 18 |
| | Opened | 11 | 11 | 6 | 3 |

### Inactive 31+ Section (Row 43): inactive 31+

| Template | Metric | Week 5 (G) | Week 4 (H) |
|----------|--------|------------|------------|
| **1d** | Sent | 33 | 41 |
| | Delivered | 29 | 38 |
| | Opened | 7 | 10 |
| | Clicked | 1 | 0 |

## Template Mapping Reference

### AWOL Templates (AWOL_MAPPINGS)

```mermaid
graph LR
    subgraph "CSV Template Names"
        T1["Day 1"]
        T2["Day 3"]
        T3["Day 5"]
        T4["Day 10"]
        T5["Day 15"]
        T6["Day 20"]
        T7["Day 30"]
        T8["Day 40"]
    end
    
    subgraph "Generated Excel Names"
        G1["1d"]
        G2["3d"]
        G3["5d"]
        G4["10d"]
        G5["15d"]
        G6["20d"]
        G7["30d"]
        G8["40d"]
    end
    
    subgraph "Existing Excel Names"
        E1[" Day 1 (Total)"]
        E2["Day 3"]
        E3[" Day 5"]
        E4["Day 10"]
        E5["Day 15"]
        E6["Day 20"]
        E7["Day 30"]
        E8["Day 40"]
    end
    
    T1 --> G1 --> E1
    T2 --> G2 --> E2
    T3 --> G3 --> E3
    T4 --> G4 --> E4
    T5 --> G5 --> E5
    T6 --> G6 --> E6
    T7 --> G7 --> E7
    T8 --> G8 --> E8
```

## Week Replacement Process Details

### Formula Preservation

**Critical**: Percentage rows (5-7 of each block) contain FORMULAS in the target Excel:

```
Row N+5: =BB(N+1)/BB(N)     # % Delivered = Delivered/Sent
Row N+6: =BB(N+2)/BB(N+1)   # % Open = Opened/Delivered  
Row N+7: =BB(N+3)/BB(N+1)   # % Click = Clicked/Delivered
```

**The code SKIPS these cells** to preserve formulas:

```python
# Skip if target cell has a formula
target_cell = existing_ws[f'{target_col}{target_row}']
if isinstance(target_cell.value, str) and target_cell.value.startswith('='):
    continue
```

**Result**: Only 60 values copied (not 96), formulas calculate automatically.

### Replacement Flow Diagram

```mermaid
sequenceDiagram
    participant CSV as test_inactive7j19-31.csv
    participant Gen as Generated Excel (G)
    participant Code as _replace_week()
    participant Exist as Existing Excel (BB)
    participant Update as Updated Excel
    
    CSV->>Gen: Process & aggregate Week 5 data
    Gen->>Code: Read G3 = 25 (Sent)
    Code->>Code: Find campaign "inactive 7"
    Code->>Code: Find template "Day 1"
    Code->>Code: Check BB3 - no formula
    Code->>Exist: Write BB3 = 25
    Code->>Code: Check BB8 - has formula
    Code->>Code: SKIP (preserve formula)
    Exist->>Update: Save as updated file
    
    Note over Update: BB3: None → 25 ✅<br/>BB8: =BB4/BB3 preserved ✅
```

## Key Differences from casino-ret

| Feature | casino-ret | awol |
|---------|------------|------|
| Metrics per block | 6 | 8 |
| Week columns | E-J | F-K |
| Source week column | F (Week 5) | G (Week 5) |
| Target week column | BB (Week 5) | BB (Week 5) |
| Sheet name | WP Chains Sport | AWOL Chains Sport |
| Campaign detection | Template content | Filename pattern |
| Template variations | Consistent | Inconsistent (spaces) |
| Percentage handling | Calculated values | Formulas preserved |
| Values copied (Week 5) | 90 | 60 (skips formulas) |

## Summary Statistics

- **Total files processed**: 4
- **Total campaigns**: 4 (Inactive 7, 14, 22, 31+)
- **Templates per campaign**: 1-7 (varies by campaign)
- **Metrics per template**: 8 (5 values + 3 formulas)
- **Values copied per template**: 5 (formulas skipped)
- **Week replaced**: Week 5 (Column G → Column BB)
- **Success rate**: 100% ✅
