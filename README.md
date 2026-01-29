# Report Automation System v2

Clean, structured report automation system with plugin architecture.

## Installation

```bash
pip install -e .
```

## Usage

### Casino-Ret Report

Generate casino and retention campaigns report:

```bash
python3 -m report_automation generate \
  "casinosport.csv,ret_1_dep.csv,ret_2_dep.csv" \
  output.xlsx \
  --report-type casino-ret
```

With week replacement:

```bash
python3 -m report_automation generate \
  "casinosport.csv,ret_1_dep.csv,ret_2_dep.csv" \
  output.xlsx \
  --report-type casino-ret \
  --existing-excel "wp_chains.xlsx" \
  --replace-week 04
```

### AWOL Report

Generate inactive users campaigns report:

```bash
python3 -m report_automation generate \
  "inactive7.csv,inactive14.csv,inactive22.csv,inactive31.csv" \
  awol_report.xlsx \
  --report-type awol
```

With week replacement:

```bash
python3 -m report_automation generate \
  "inactive7.csv,inactive14.csv,inactive22.csv,inactive31.csv" \
  awol_report.xlsx \
  --report-type awol \
  --existing-excel "wp_chains.xlsx" \
  --replace-week 04
```

## Project Structure

```
src/report_automation/
├── domain/          # Core business logic & models
├── infrastructure/  # External concerns (CSV, Excel, Config)
├── plugins/         # Extensible report type system
│   ├── base/        # Plugin abstractions
│   └── implementations/
│       ├── ab_report.py
│       ├── casino_ret.py
│       └── awol.py
└── cli/            # Clean CLI interface
```

## Available Report Types

- `ab-report` - A-B testing campaigns
- `casino-ret` - Casino and retention campaigns (multi-file)
- `awol` - Inactive users campaigns (multi-file)

