# Security Requirements Generation System

A multi-agent system built with CrewAI that automatically translates high-level product requirements into comprehensive, standards-aligned security requirements.

## Overview

This system uses 5 specialized AI agents orchestrated through CrewAI Flows to generate security requirements from product manager inputs:

1. **Requirements Analysis Agent** - Parses high-level requirements and identifies security implications
2. **Domain Security Agent** - Maps requirements to OWASP, NIST, and ISO 27001 controls
3. **LLM Security Specialist** - Identifies AI/ML components and adds specialized security controls
4. **Compliance Agent** - Ensures regulatory alignment (GDPR, HIPAA, PCI-DSS, etc.)
5. **Validation Agent** - Validates completeness and consistency with self-evaluation loop

### Key Features

- 📋 **Standards-Based**: Leverages OWASP ASVS, NIST CSF, and ISO 27001
- 🤖 **AI-Aware**: Specialized handling of LLM and ML security threats
- ✅ **Self-Evaluating**: Automatic validation with iterative refinement
- 🗄️ **Vector Search**: Semantic search over security standards using Weaviate
- 📊 **Comprehensive Output**: JSON and Markdown reports with validation scores

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Product Manager Input                     │
│                   (High-level Requirements)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Requirements Analysis Agent                    │
│         (Extract security-relevant features)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Domain    │ │  LLM/AI     │ │ Compliance  │
│  Security   │ │  Security   │ │   Agent     │
│   Agent     │ │  Specialist │ │             │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
         ┌─────────────────────────┐
         │   Weaviate Vector DB     │
         │ (Security Standards)     │
         └─────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │   Validation Agent       │
         │ (Self-Evaluation)        │
         └──────────┬───────────────┘
                    │
         ┌──────────┴──────────┐
         │ Score < 0.8?        │
         │ Iterations < 3?     │
         └──────┬──────────┬───┘
                │          │
             Yes│          │No
                │          │
         ┌──────▼──────┐   │
         │   Refine    │   │
         │Requirements │   │
         └──────┬──────┘   │
                │          │
                └────┬─────┘
                     ▼
         ┌─────────────────────────┐
         │  Final Security         │
         │  Requirements Output    │
         └─────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.10-3.13
- Docker and Docker Compose (for Weaviate)
- OpenAI API key

### Setup Steps

1. **Clone and navigate to the project**:
   ```bash
   cd security_requirements_system
   ```

2. **Configure environment variables**:
   ```bash
   cp env.template .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Install dependencies using pnpm** (as per [[memory:5156816]]):
   ```bash
   pnpm install
   ```
   
   Or if you prefer the CrewAI CLI:
   ```bash
   crewai install
   ```

4. **Start Weaviate database**:
   ```bash
   docker-compose up -d
   ```
   
   Wait ~30 seconds for Weaviate to initialize.

5. **Prepare security standards data**:
   ```bash
   python -m security_requirements_system.data.prepare_owasp_asvs
   python -m security_requirements_system.data.prepare_nist
   python -m security_requirements_system.data.prepare_iso27001
   ```

6. **Initialize Weaviate with security standards**:
   ```bash
   python -m security_requirements_system.tools.weaviate_setup
   ```

## Usage

### Running the System

**Option 1: Use default input file** (`inputs/sample_taskmgmt.txt`):
```bash
crewai run
```

**Option 2: Specify a custom input file**:
```bash
INPUT_FILE=inputs/sample_ecommerce.txt crewai run
```

**Option 3: Run directly with Python**:
```bash
python -m security_requirements_system.main
```

### Sample Inputs

Two sample requirement files are provided:

- `inputs/sample_ecommerce.txt` - E-commerce platform requirements
- `inputs/sample_healthcare.txt` - Telemedicine platform requirements

Create your own by placing a text file in the `inputs/` directory with your product requirements.

### Output

The system generates two files in the `outputs/` directory:

1. **security_requirements.json** - Complete structured output with all agent analyses
2. **security_requirements.md** - Human-readable markdown summary

Example output structure:
```json
{
  "metadata": {
    "validation_score": 0.85,
    "validation_passed": true,
    "iterations": 1
  },
  "original_requirements": "...",
  "requirements_analysis": "...",
  "security_controls": "...",
  "ai_ml_security": "...",
  "compliance_requirements": "...",
  "validation_report": "..."
}
```

## Flow Behavior

### Self-Evaluation Loop

The system implements automatic quality assurance:

1. **Initial Generation**: All 5 agents process the requirements
2. **Validation**: Validation agent scores the output (0-1) across 5 dimensions:
   - Completeness
   - Consistency
   - Correctness
   - Implementability
   - Alignment
3. **Decision**:
   - If score ≥ 0.8 → Generate final output ✅
   - If score < 0.8 and iterations < 3 → Refine with feedback 🔄
   - If max iterations reached → Accept current version ⚠️

### Configuration

Adjust thresholds in `src/security_requirements_system/main.py`:

```python
MAX_ITERATIONS = 3  # Maximum refinement loops
VALIDATION_THRESHOLD = 0.8  # Minimum score to pass
```

## Project Structure

```
security_requirements_system/
├── src/
│   └── security_requirements_system/
│       ├── crews/                    # 5 agent crews
│       │   ├── requirements_analysis_crew/
│       │   ├── domain_security_crew/
│       │   ├── llm_security_crew/
│       │   ├── compliance_crew/
│       │   └── validation_crew/
│       ├── tools/                    # Custom tools
│       │   ├── weaviate_tool.py     # Vector DB query tool
│       │   └── weaviate_setup.py    # DB initialization
│       ├── data/                     # Security standards
│       │   ├── prepared/            # Processed JSON
│       │   ├── prepare_owasp_asvs.py
│       │   ├── prepare_nist.py
│       │   └── prepare_iso27001.py
│       └── main.py                  # Flow orchestration
├── inputs/                          # Input requirements
├── outputs/                         # Generated requirements
├── docker-compose.yml              # Weaviate setup
└── pyproject.toml                  # Dependencies

```

## Security Standards Coverage

### OWASP ASVS
- Authentication
- Session Management
- Access Control
- Validation, Sanitization and Encoding
- Cryptography
- Error Handling and Logging
- Data Protection
- Communications
- Malicious Code
- Business Logic
- File and Resources
- API and Web Service
- Configuration

### NIST Cybersecurity Framework
- Identify (Asset Management, Risk Assessment, Governance)
- Protect (Access Control, Data Security, Training)
- Detect (Anomalies, Monitoring)
- Respond (Response Planning, Communications, Analysis, Mitigation)
- Recover (Recovery Planning, Improvements)

### ISO 27001:2022 Annex A
- Organizational Controls
- People Controls
- Physical Controls
- Technological Controls

## Extending the System

### Adding New Security Standards

1. Create a preparation script in `src/security_requirements_system/data/`:
   ```python
   # prepare_custom_standard.py
   def prepare_custom_standard():
       controls = [
           {
               "standard_name": "CustomStandard",
               "control_id": "CS-1",
               "title": "Control Title",
               "description": "Control description",
               "category": "Category",
           },
           # ... more controls
       ]
       # Save to prepared/custom_standard.json
   ```

2. Run the preparation script and reingest data:
   ```bash
   python -m security_requirements_system.data.prepare_custom_standard
   python -m security_requirements_system.tools.weaviate_setup
   ```

### Customizing Agents

Edit the YAML configuration files in each crew's `config/` directory:
- `agents.yaml` - Agent roles, goals, and backstories
- `tasks.yaml` - Task descriptions and expected outputs

## Troubleshooting

### Weaviate Connection Issues
```bash
# Check Weaviate is running
docker-compose ps

# View logs
docker-compose logs weaviate

# Restart Weaviate
docker-compose restart
```

### OpenAI API Issues
- Verify your `OPENAI_API_KEY` in `.env`
- Check API quota and billing

### Low Validation Scores
- Review validation feedback in output
- Adjust input requirements to be more specific
- Modify validation thresholds if appropriate

## Research Context

This system was developed as part of a Master's thesis investigating multi-agent approaches to security requirements engineering. The goal is to automate the translation of high-level business requirements into detailed, standards-compliant security specifications.

### Thesis Objectives
- Reduce manual effort in security requirements generation
- Ensure comprehensive coverage of security standards
- Address emerging AI/ML security concerns
- Maintain alignment with regulatory compliance needs

## License

This project is for academic research purposes.

## Contributing

This is a thesis project, but feedback and suggestions are welcome.

## Acknowledgments

- **CrewAI** for the multi-agent orchestration framework
- **Weaviate** for vector database capabilities
- **OpenAI** for LLM infrastructure
- **OWASP, NIST, ISO** for security standards

---

**Note**: This system generates security requirements as recommendations. Always review outputs with qualified security professionals before implementation.
