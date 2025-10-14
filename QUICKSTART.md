# Quick Start Guide

Get up and running with the Security Requirements System in 5 minutes.

## Prerequisites

- Docker Desktop running
- OpenAI API key
- Python 3.10+

## Installation

### 1. Run Setup Script

```bash
./setup.sh
```

This will:
- Create `.env` file from template
- Install dependencies
- Start Weaviate database
- Prepare security standards data
- Ingest data into Weaviate

**Important**: When prompted, edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Alternative: Manual Setup

If you prefer manual setup:

```bash
# 1. Configure environment
cp env.template .env
# Edit .env with your OPENAI_API_KEY

# 2. Install dependencies
crewai install
# or: pnpm install

# 3. Start Weaviate
docker-compose up -d
sleep 30

# 4. Prepare data
python -m security_requirements_system.data.prepare_owasp_asvs
python -m security_requirements_system.data.prepare_nist
python -m security_requirements_system.data.prepare_iso27001

# 5. Initialize Weaviate
python -m security_requirements_system.tools.weaviate_setup
```

## Running the System

### Using Sample Inputs

Try one of the included examples:

**E-Commerce Platform:**
```bash
INPUT_FILE=inputs/sample_ecommerce.txt crewai run
```

**Healthcare Platform:**
```bash
INPUT_FILE=inputs/sample_healthcare.txt crewai run
```

**Task Management App (default):**
```bash
crewai run
```

### Using Your Own Requirements

1. Create a text file in `inputs/` directory:
   ```bash
   nano inputs/my_app.txt
   ```

2. Write your high-level requirements in plain English

3. Run the system:
   ```bash
   INPUT_FILE=inputs/my_app.txt crewai run
   ```

## Viewing Results

After the flow completes (typically 5-15 minutes), check the `outputs/` directory:

- **security_requirements.json** - Complete structured output
- **security_requirements.md** - Markdown summary

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

## What Happens During Execution?

The system runs through 8 steps:

1. **Load Requirements** - Reads your input file
2. **Analyze Requirements** - Identifies security-relevant features
3. **Map Security Controls** - Queries OWASP, NIST, ISO 27001 standards
4. **Identify AI/ML Security** - Detects and addresses AI-specific threats
5. **Assess Compliance** - Identifies regulatory requirements (GDPR, HIPAA, etc.)
6. **Validate Requirements** - Scores output on 5 dimensions
7. **Self-Evaluation Decision** - Decides if refinement needed
8. **Generate Final Output** - Creates JSON and Markdown reports

### Self-Evaluation Loop

The validation agent scores the output:
- ✅ **Score ≥ 0.8**: Validation passed → Generate output
- 🔄 **Score < 0.8**: Refinement needed → Loop back with feedback (max 3 iterations)

## Troubleshooting

### Weaviate Not Connecting

```bash
# Check if Weaviate is running
docker-compose ps

# Restart if needed
docker-compose restart

# View logs
docker-compose logs weaviate
```

### OpenAI API Errors

- Verify API key in `.env`
- Check quota at platform.openai.com
- Ensure billing is active

### No Security Controls Found

This means Weaviate may not be populated:
```bash
python -m security_requirements_system.tools.weaviate_setup
```

## Next Steps

1. **Review the README.md** for detailed documentation
2. **Customize agents** by editing YAML configs in `src/security_requirements_system/crews/*/config/`
3. **Add more standards** by creating new preparation scripts
4. **Adjust validation thresholds** in `main.py`

## Tips for Better Results

### Writing Good Requirements

✅ **Do:**
- Describe features and functionality clearly
- Mention data types (personal data, health data, payment info)
- Specify user roles and access patterns
- Include integrations and third-party services
- Note any AI/ML features

❌ **Don't:**
- Be too vague or high-level
- Skip important features
- Assume implicit security requirements

### Example: Good vs. Bad Requirements

**Bad:**
```
Build an app with user login.
```

**Good:**
```
User Management System:
- User registration with email and password
- Social login (Google, Facebook)
- User profiles storing personal information (name, email, phone)
- Role-based access (Admin, User, Guest)
- Password reset via email
- Store user activity logs
```

## Support

For issues or questions about this thesis project, refer to the main README.md or contact the author.

---

**Ready to start?** Run `./setup.sh` and then `crewai run`!

