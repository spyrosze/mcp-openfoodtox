[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/spyrosze-mcp-openfoodtox-badge.png)](https://mseep.ai/app/spyrosze-mcp-openfoodtox)

# 🧪 MCP OpenFoodTox

## Accessing EFSA's Chemical Hazards Database using natural language

A Model Context Protocol (MCP) providing access to EFSA's comprehensive OpenFoodTox database containing 8,006 chemical substances, 45,582 alternative names, and 54,621 study records from 2,437 scientific assessments across 8 interconnected data tables with over 138,000 entries.

This OpenFoodTox MCP server uses the latest EFSA dataset (updated 14 September 2023) ([OpenFoodTox](https://www.efsa.europa.eu/en/microstrategy/openfoodtox), [data report](https://www.efsa.europa.eu/en/data-report/chemical-hazards-database-openfoodtox), [Zenodo](https://zenodo.org/records/8120114)) and addresses the critical need for accessible chemical safety data by consolidating EFSA's authoritative risk assessments of regulated food products, contaminants, pesticides, and feed additives. Unlike hard to use toxicological databases and spreadsheets scattered across various sources, OpenFoodTox provides structured hazard characterization data—including 11,357 risk assessments (ADI/TDI values), 11,698 toxicity endpoints (NOAEL, LD50), and 246 genotoxicity studies. This MCP makes EFSA's scientifically validated safety assessments readily available through natural language queries (via a large language model such as Claude Deesktop) for scientists, regulators, food manufacturers, and public health stakeholders.

## 🛠️ Tools

- **Search Substance** - Find substances by name, E-number, or description. Answers: "What is [substance]?"
- **Get Substance Safety Assessment** - Get safety flags (mutagenic, genotoxic, carcinogenic) for a substance. Answers: "Is [substance] safe?"
- **Get Toxicity Endpoints** - Get toxicity study data including NOAEL, LD50, and target organs. Answers: "What are the toxicity effects of [substance]?"
- **Get Risk Assessments** - Get safe intake limits (ADI/TDI values) and safety factors. Answers: "How much [substance] is safe daily?"
- **Get Genotoxicity Details** - Get detailed genotoxicity study information including test guidelines and results. Answers: "Is [substance] genotoxic?"
- **Get Opinions** - Retrieve EFSA opinion documents with publication dates, DOIs, and regulation information. Answers: "What EFSA opinions exist for [substance]?"
- **List Substances by Class and Safety** - Filter substances by category (food additive, pesticide, etc.) and safety criteria. Answers: "List all [category] substances" or "Show me carcinogenic food additives"
- **List Substances by Assessment** - Find substances matching specific risk assessment criteria (ADI/TDI ranges, assessment types, population groups). Answers: "List substances with ADI > 5 mg/kg" or "Find substances assessed for children"

## 🧾 Data Attribution

This project uses data from EFSA OpenFoodTox, the European Food Safety Authority’s chemical hazards database.
Data source:

European Food Safety Authority (EFSA). OpenFoodTox – The EFSA Chemical Hazards Database. Zenodo, DOI: 10.5281/zenodo.8120114
.
© European Food Safety Authority. Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0)
.

Official EFSA dataset page: https://www.efsa.europa.eu/en/data-report/chemical-hazards-database-openfoodtox

Disclaimer:
OpenFoodTox compiles toxicological reference values and hazard data extracted from EFSA’s scientific opinions.
The dataset is provided for transparency and research purposes; for regulatory or legal use, always consult the original EFSA scientific outputs.

## 📋 Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager  
- [More details](#prerequisites-installation-details)

## ⚡ Quick Installation in 2 steps

1. Create virtual environment, install dependencies and setup the database (required on first run)

```bash
make setup
```
_No virtual environment **activation** is required_

2. Install MCP server in Claude Desktop (optional)

```bash
# Automated installation
make claude
```

If you prefer to install _manually_, add to Claude Desktop user -> settings -> Developer -> Local MCP servers -> Edit Config:

```json
{
  "mcp-openfoodtox": {
    "command": "absolute/path/to/mcp-openfoodtox/.venv/bin/python",
    "args": ["absolute/path/to/mcp-openfoodtox/main.py"]
  }
}
```

The config file location:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

## 📦 Prerequisites Installation Details

### 📦 Install uv

Mac/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via HomeBrew (Mac)
```bash
brew install uv
```

Windows
```bash
winget install astral-sh.uv
```

### 🐍 Install Python 3.12+

```bash
uv python install 3.12
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ©️ Copyright

Copyright (c) 2025 Spyros Zevelakis, [Phoebe AI Limited](https://www.phoebeai.com)

This software is open source and available under the MIT License.

