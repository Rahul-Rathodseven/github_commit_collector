# GitHub Commit Data Collector

A robust, production-ready Python backend system for collecting and structuring commit-level data from GitHub repositories. This tool fetches detailed commit information including file changes, author details, team mapping, and comprehensive statistics.

## Features

**GitHub API Integration**
- Personal Access Token (PAT) authentication
- Automatic rate limit handling with intelligent backoff
- Retry logic for failed requests
- Support for both REST API endpoints

**Comprehensive Data Collection**
- Repository metadata
- Commit SHA, message, date, and URL
- Author name, GitHub username, and email
- Team mapping (configurable)
- File-level changes (additions, deletions, modifications)
- Line-by-line change tracking
- Branch information

**Flexible Filtering**
- Date range filtering
- Author filtering
- Team filtering
- Branch selection
- Repository-specific configurations

**Multiple Output Formats**
- JSON (structured, hierarchical)
- CSV (flat, spreadsheet-ready)
- Separate file for detailed file changes
- Collection metadata and statistics

**Team Management**
- Map GitHub users to teams via YAML configuration
- Support for multiple teams
- Default team for unmapped users
- Repository-specific team configurations

**Production Features**
- Structured logging with color output
- Configuration via environment variables and YAML
- Modular, maintainable architecture
- Comprehensive error handling
- Progress tracking and status updates

---

## Quick Start

### 1. Installation

```bash
# Clone or extract the project
cd github_commit_collector

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

#### Set up GitHub Token

Copy the example environment file and add your GitHub token:

```bash
cp .env.example .env
```

Edit `.env` and add your GitHub Personal Access Token:

```env
GITHUB_TOKEN=ghp_your_token_here
```

**How to get a GitHub Token:**
1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate new token (classic)
3. Select scopes: `repo` (for private repos) or `public_repo` (for public only)
4. Copy the token to your `.env` file

#### Configure Repositories

Edit `config/repositories.yaml`:

```yaml
repositories:
  - url: https://github.com/owner/repo1
    branch: main
    enabled: true
  
  - url: https://github.com/owner/repo2
    branch: develop
    enabled: true

filters:
  date_from: 2024-01-01  # Optional: ISO 8601 date
  date_to: 2024-12-31    # Optional: ISO 8601 date
```

#### Configure Team Mapping

Edit `config/teams.yaml`:

```yaml
teams:
  backend:
    - alice
    - bob
  
  frontend:
    - charlie
    - diana
  
  devops:
    - eve

default_team: unassigned
```

### 3. Run the Collector

**Test connection first:**
```bash
python src/main.py --test-connection
```

**Collect from configured repositories:**
```bash
python src/main.py
```

**Collect from a specific repository:**
```bash
python src/main.py --repo https://github.com/owner/repo --branch main
```

---

## Usage Examples

### Basic Collection

```bash
# Collect from all configured repositories
python src/main.py

# Collect from a specific repository
python src/main.py --repo https://github.com/torvalds/linux

# Collect from a specific branch
python src/main.py --repo https://github.com/owner/repo --branch develop
```

### Filtering Data

```bash
# Filter by date range
python src/main.py --date-from 2024-01-01 --date-to 2024-12-31

# Filter by author
python src/main.py --author octocat

# Filter by team (after collection)
python src/main.py --team backend

# Combine filters
python src/main.py --date-from 2024-06-01 --author alice --team backend
```

### Output Formats

```bash
# JSON output (default)
python src/main.py --format json

# CSV output
python src/main.py --format csv

# Both formats
python src/main.py --format both

# Include detailed file changes in CSV
python src/main.py --format csv --include-file-details

# Include patch/diff content in JSON
python src/main.py --format json --include-patch
```

### Advanced Options

```bash
# Custom output directory
python src/main.py --output-dir /path/to/output

# Debug logging
python src/main.py --log-level DEBUG

# Skip detailed commit data (faster, but no file-level changes)
python src/main.py --no-detailed-commits

# Use custom config directory
python src/main.py --config-dir /path/to/config
```

---

## Architecture

### Project Structure

```
github_commit_collector/
├── src/
│   ├── main.py              # CLI entry point
│   ├── config_manager.py    # Configuration handling
│   ├── github_client.py     # GitHub API client
│   ├── team_mapper.py       # Team mapping logic
│   ├── commit_processor.py  # Data processing
│   ├── data_collector.py    # Collection orchestrator
│   ├── data_exporter.py     # Export to JSON/CSV
│   ├── models.py            # Data models
│   └── logger.py            # Logging utilities
├── config/
│   ├── repositories.yaml    # Repository configuration
│   └── teams.yaml          # Team mappings
├── output/                  # Generated output files
│   └── SCHEMA.md           # Output schema documentation
├── logs/                    # Application logs
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Core Components

1. **ConfigManager**: Loads and validates configuration from `.env` and YAML files
2. **GitHubAPIClient**: Handles GitHub API authentication and requests with rate limiting
3. **TeamMapper**: Maps GitHub usernames to team names
4. **CommitProcessor**: Transforms raw API data into structured models
5. **DataCollector**: Orchestrates the collection process
6. **DataExporter**: Exports data to JSON and CSV formats

### Data Flow

```
Configuration → GitHub API → Raw Commits → Processing → Structured Models → Export
```

---

## Output Files

The collector generates several output files:

### JSON Files

- **`commits_TIMESTAMP.json`**: Complete commit data with metadata
- **`collection_summary_TIMESTAMP.json`**: High-level statistics
- **`team_summary_TIMESTAMP.json`**: Team-level aggregations
- **`repository_stats_TIMESTAMP.json`**: Per-repository statistics

### CSV Files

- **`commits_TIMESTAMP.csv`**: Flat commit data
- **`commits_TIMESTAMP_file_changes.csv`**: Detailed file changes (with `--include-file-details`)

See `output/SCHEMA.md` for detailed schema documentation.

---

## Configuration Reference

### Environment Variables (`.env`)

```env
# Required
GITHUB_TOKEN=your_token_here

# Optional - API Configuration
GITHUB_API_URL=https://api.github.com
GITHUB_API_TIMEOUT=30
MAX_RETRIES=3
RATE_LIMIT_BUFFER=10

# Optional - Collection Settings
DEFAULT_BRANCH=main
MAX_COMMITS_PER_REQUEST=100

# Optional - Output Settings
OUTPUT_FORMAT=json
OUTPUT_DIR=output
LOG_LEVEL=INFO
LOG_DIR=logs
```

### Repository Configuration (`config/repositories.yaml`)

```yaml
repositories:
  - url: https://github.com/owner/repo
    branch: main          # Optional, defaults to 'main'
    enabled: true         # Optional, defaults to true
    filters:              # Optional, repository-specific filters
      date_from: 2024-01-01
      author: alice

filters:  # Global filters (applied to all repositories)
  date_from: null
  date_to: null
  authors: []
  teams: []
```

### Team Mapping (`config/teams.yaml`)

```yaml
teams:
  team_name:
    - username1
    - username2

default_team: unassigned

# Optional: Repository-specific team assignments
repository_teams:
  owner/repo:
    - team1
    - team2
```

---

## Rate Limiting

The collector intelligently handles GitHub API rate limits:

- **Automatic rate limit checking** before requests
- **Configurable buffer** to pause before hitting limit
- **Automatic waiting** when rate limit is reached
- **Detailed logging** of rate limit status

Default GitHub API limits:
- **5,000 requests/hour** for authenticated users
- **60 requests/hour** for unauthenticated users

---

## Error Handling

The system includes comprehensive error handling:

- **API errors**: Logged with context and retry logic
- **Invalid configurations**: Validated on startup
- **Missing data**: Graceful handling with warnings
- **Network issues**: Automatic retry with exponential backoff
- **Keyboard interrupt**: Graceful shutdown

All errors are logged to both console and log files.

---

## Performance Considerations

### Optimizations

- **Batch processing**: Fetches commits in batches of 100
- **Pagination**: Automatically handles paginated responses
- **Rate limit awareness**: Prevents unnecessary API calls
- **Conditional detailed fetching**: Skip with `--no-detailed-commits` for faster collection

### Performance Tips

1. **Use date filters** to limit the number of commits
2. **Skip detailed commits** if you don't need file-level changes
3. **Collect during off-peak hours** to avoid rate limit contention
4. **Use branch filters** to focus on specific development lines

---

## Troubleshooting

### Common Issues

**"GITHUB_TOKEN not found"**
- Ensure `.env` file exists and contains `GITHUB_TOKEN=...`
- Check that `.env` is in the project root directory

**"Rate limit exceeded"**
- Wait for the rate limit to reset (shown in logs)
- Reduce the number of repositories or date range
- Use `--no-detailed-commits` to reduce API calls

**"Repository not found"**
- Verify repository URL is correct
- Ensure your token has access to private repositories (if applicable)
- Check repository exists and you have read permissions

**No commits collected**
- Check date filters aren't too restrictive
- Verify branch name is correct
- Check if repository actually has commits in the specified range

---

## Data Privacy & Security

- **Tokens**: Never commit `.env` file to version control (it's in `.gitignore`)
- **Commit messages**: Stored as-is from GitHub
- **Email addresses**: Collected from commit metadata
- **Patch content**: Only stored if explicitly requested with `--include-patch`

---

## Extensions & Customization

### Adding Custom Team Mapping Logic

Edit `src/team_mapper.py` to implement custom logic:

```python
def get_team(self, username: Optional[str]) -> str:
    # Add custom logic here
    if username and username.endswith("_admin"):
        return "admin"
    return super().get_team(username)
```

### Adding Custom Filters

Edit `src/commit_processor.py` to add filtering logic:

```python
def filter_commits(self, commits: List[CommitData], **kwargs) -> List[CommitData]:
    # Add custom filters
    if kwargs.get("min_changes"):
        commits = [c for c in commits if c.total_changes >= kwargs["min_changes"]]
    return commits
```

### Custom Export Formats

Extend `src/data_exporter.py` to add new export formats:

```python
def export_to_xml(self, commits: List[CommitData]) -> str:
    # Implement XML export
    pass
```

---

## Requirements

- **Python**: 3.8 or higher
- **GitHub Token**: Personal Access Token with appropriate scopes
- **Dependencies**: Listed in `requirements.txt`

---

## License

This project is provided as-is for data collection purposes.

---

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review log files in `logs/` directory
3. Verify configuration files are properly formatted
4. Test GitHub API connection with `--test-connection`

---

## Changelog

### Version 1.0.0
- Initial release
- GitHub API integration
- JSON and CSV export
- Team mapping
- Comprehensive filtering
- Rate limit handling