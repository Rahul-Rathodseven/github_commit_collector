# Setup and Configuration Guide

## Initial Setup

### 1. System Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning)
- Internet connection for GitHub API access

### 2. Installation Steps

```bash
# Navigate to project directory
cd github_commit_collector

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. GitHub Token Setup

#### Creating a Personal Access Token

1. **Navigate to GitHub Settings**
   - Go to https://github.com/settings/tokens
   - Or: GitHub Profile → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Give it a descriptive name (e.g., "Commit Data Collector")

3. **Select Scopes**
   - For **public repositories only**: Select `public_repo`
   - For **private repositories**: Select `repo` (full control)
   - Recommended: Also select `read:org` if collecting from organization repos

4. **Copy Token**
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again!)

#### Configure Token in Project

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor

# Add your token
GITHUB_TOKEN=ghp_your_actual_token_here
```

### 4. Configure Repositories

Edit `config/repositories.yaml`:

```yaml
repositories:
  # Example: Public repository
  - url: https://github.com/torvalds/linux
    branch: master
    enabled: true
  
  # Example: Your organization's repo
  - url: https://github.com/your-org/your-repo
    branch: main
    enabled: true
  
  # Example: Disabled repository (won't be collected)
  - url: https://github.com/old-org/legacy-repo
    branch: main
    enabled: false

# Optional global filters
filters:
  date_from: "2024-01-01"  # ISO 8601 format
  date_to: "2024-12-31"
  authors: []              # Leave empty for all authors
  teams: []                # Leave empty for all teams
```

### 5. Configure Team Mapping

Edit `config/teams.yaml`:

```yaml
teams:
  # Team name: list of GitHub usernames
  backend:
    - alice
    - bob
    - charlie
  
  frontend:
    - david
    - eve
  
  devops:
    - frank
    - grace
  
  data:
    - henry
    - iris

# Default team for users not in any team above
default_team: unassigned

# Optional: Repository-specific teams
# This is useful if certain repos are owned by specific teams
repository_teams:
  your-org/backend-api:
    - backend
    - devops
  your-org/frontend-app:
    - frontend
```

#### Finding Team Members

**Method 1: From GitHub UI**
1. Navigate to your organization on GitHub
2. Go to Teams tab
3. Click on each team to see members
4. Note the GitHub usernames

**Method 2: If you don't have teams**
- Just list individual contributors by their GitHub usernames
- Group them logically (backend, frontend, etc.)
- The tool doesn't require actual GitHub teams; it's just a mapping

### 6. Test Your Configuration

```bash
# Test GitHub API connection
python src/main.py --test-connection

# Expected output:
# ✓ Successfully authenticated as: your-username
# ✓ Connection test successful!
```

### 7. First Data Collection Run

```bash
# Dry run: Collect from a small, known public repo first
python src/main.py --repo https://github.com/octocat/Hello-World --log-level DEBUG

# Check the output
ls -lh output/

# View the collected data
cat output/commits_*.json | head -50
```

## Configuration Tips

### Repository Selection

**Option 1: Configuration File (Recommended for multiple repos)**
- Edit `config/repositories.yaml`
- Run: `python src/main.py`

**Option 2: Command Line (For ad-hoc collection)**
- Run: `python src/main.py --repo <url> --branch <branch>`

### Filtering Strategies

**By Date:**
```bash
# Last month's commits
python src/main.py --date-from 2024-01-01 --date-to 2024-01-31

# All commits this year
python src/main.py --date-from 2024-01-01
```

**By Author:**
```bash
# Single author
python src/main.py --author octocat

# Multiple authors (use config file)
# In repositories.yaml:
filters:
  authors: ["alice", "bob"]
```

**By Team:**
```bash
# Collect all, then filter by team
python src/main.py --team backend
```

### Output Organization

**Default Structure:**
```
output/
├── commits_20240129_103045.json
├── commits_20240129_103045.csv
├── collection_summary_20240129_103045.json
├── team_summary_20240129_103045.json
└── repository_stats_20240129_103045.json
```

**Custom Output Directory:**
```bash
python src/main.py --output-dir /path/to/custom/output
```

## Common Workflows

### Workflow 1: Monthly Team Report

```bash
# Collect last month's commits
python src/main.py \
  --date-from 2024-01-01 \
  --date-to 2024-01-31 \
  --format both \
  --include-file-details

# Output files will include:
# - commits_*.csv (for spreadsheets)
# - team_summary_*.json (team statistics)
```

### Workflow 2: Repository Audit

```bash
# Full repository history
python src/main.py \
  --repo https://github.com/org/repo \
  --format json \
  --include-patch

# Analyze specific files, authors, or patterns
```

### Workflow 3: Continuous Collection

```bash
# Create a script to run daily
#!/bin/bash
cd /path/to/github_commit_collector
source venv/bin/activate

# Yesterday's commits
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)

python src/main.py \
  --date-from $YESTERDAY \
  --date-to $TODAY \
  --format both

# Move to archive
mv output/commits_*.* /archive/$(date +%Y-%m)/
```

## Advanced Configuration

### Custom API Settings

In `.env`:

```env
# Increase timeout for slow connections
GITHUB_API_TIMEOUT=60

# More aggressive rate limit buffer
RATE_LIMIT_BUFFER=50

# Maximum retries for failed requests
MAX_RETRIES=5
```

### Multiple GitHub Accounts

Create separate environment files:

```bash
# .env.work
GITHUB_TOKEN=ghp_work_token_here

# .env.personal
GITHUB_TOKEN=ghp_personal_token_here

# Use specific env file
python src/main.py --env-file .env.work
```

### Performance Tuning

**For Large Repositories:**
```bash
# Skip detailed commit data (faster)
python src/main.py --no-detailed-commits

# Use specific date ranges
python src/main.py --date-from 2024-01-01 --date-to 2024-01-31

# Collect during off-peak hours (less rate limiting)
```

**Rate Limit Management:**
- Default: 5,000 requests/hour
- Each detailed commit = 1 request
- Plan accordingly for large repos

## Troubleshooting Setup

### Python Version Issues

```bash
# Check Python version
python --version

# If < 3.8, install newer version or use python3
python3 --version
python3 -m venv venv
```

### Dependency Installation Errors

```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Try system packages if virtual env fails
sudo apt-get install python3-dev  # Linux
```

### Permission Errors

```bash
# Make sure output directories are writable
chmod -R 755 output logs

# Check .env file permissions (should be restricted)
chmod 600 .env
```

### YAML Parsing Errors

```yaml
# Common mistakes in YAML:

# WRONG: Missing quotes around dates
date_from: 2024-01-01

# CORRECT:
date_from: "2024-01-01"

# WRONG: Inconsistent indentation
teams:
  backend:
  - alice  # Wrong indent
    - bob  # Wrong indent

# CORRECT:
teams:
  backend:
    - alice
    - bob
```

## Security Best Practices

1. **Never commit `.env` file**
   - It's already in `.gitignore`
   - Use `.env.example` for sharing

2. **Rotate tokens regularly**
   - Generate new tokens every 90 days
   - Revoke old tokens after rotation

3. **Use minimal permissions**
   - Only `public_repo` for public repos
   - Only `repo` if you need private access

4. **Secure storage**
   - Keep `.env` file permissions restricted: `chmod 600 .env`
   - Don't share tokens in chat, email, or tickets

## Next Steps

After setup is complete:

1. Run test connection
2. Collect from a small test repository
3. Verify output files
4. Configure your actual repositories
5. Set up team mappings
6. Run full collection
7. Review output schema documentation
8. Integrate with your analysis workflow

## Getting Help

If you encounter issues:

1. Check logs in `logs/collector_*.log`
2. Run with `--log-level DEBUG`
3. Verify GitHub token has correct permissions
4. Check GitHub API status: https://www.githubstatus.com/
5. Review README.md troubleshooting section