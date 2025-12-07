# Design: Brew Backup Command

## Overview

The `den brew upgrade` command automates Homebrew maintenance and backup. It executes `brew upgrade` to update packages, generates a Brewfile snapshot, uses Anthropic's API to add documentation and categorization, and backs up the result to a GitHub Gist. The system uses content hashing to detect changes and avoid unnecessary API calls when the Brewfile hasn't changed.

## Architecture

The brew backup system follows a pipeline architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         den brew upgrade                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Brew    │  │ Brewfile │  │ Anthropic│  │  GitHub  │  │    State     │  │
│  │ Upgrade  │──│Generator │──│Formatter │──│  Gist    │──│   Storage    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
│       │              │              │             │              │          │
│       └──────────────┴──────────────┴─────────────┴──────────────┘          │
│                                    │                                         │
│                              ┌─────┴─────┐                                   │
│                              │  Logger   │                                   │
│                              └───────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Components

### Brew Command Group (`src/den/commands/brew.py`)
A Typer command group for Homebrew-related commands.

### Brew Runner (`src/den/brew_runner.py`)
Handles execution of Homebrew commands.

### Brewfile Formatter (`src/den/brewfile_formatter.py`)
Handles Anthropic API integration for formatting.

### GitHub Gist Client (`src/den/gist_client.py`)
Handles GitHub Gist API operations.

### State Storage (`src/den/state_storage.py`)
Handles reading and writing application state.

### Hash Utility (`src/den/hash_utils.py`)
Utility for computing content hashes.

### Brew Logger (`src/den/brew_logger.py`)
Configures logging for the brew upgrade process.

## Data Models

### State File (`~/.config/den/state.json`)

```json
{
  "brew": {
    "brewfile_hash": "sha256:abc123...",
    "gist_id": "abc123def456"
  }
}
```

### Log Entry Format

```
2025-01-15 10:30:45 INFO: Updating Homebrew dependencies...
2025-01-15 10:31:02 INFO: Creating Brewfile...
2025-01-15 10:31:03 ERROR: Failed to connect to Anthropic API
```

## Correctness Properties

### Property 1: Hash computation consistency
For any string content, computing the SHA-256 hash multiple times SHALL produce the same hash value.

### Property 2: State merge preserves existing keys
For any existing state.json content and any new brew state being saved, the save operation SHALL preserve all existing keys while adding or updating the "brew" key.

### Property 3: State serialization round-trip
For any valid brew state dictionary, serializing to JSON and deserializing back SHALL produce an equivalent dictionary.

### Property 4: Log entry format compliance
For any log entry written by the brew logger, the entry SHALL contain a timestamp and a log level (INFO, ERROR, or WARNING).

## Error Handling

| Error Condition | Handling Strategy |
|----------------|-------------------|
| `brew upgrade` fails | Log error, display message, exit with code 1 |
| `brew bundle dump` fails | Log error, display message, exit with code 1 |
| Anthropic API key missing | Display "Run `den auth login` to configure Anthropic", exit with code 1 |
| Anthropic API call fails | Log error with details, display message, exit with code 1 |
| GitHub token missing | Display "Configure GitHub authentication", exit with code 1 |
| GitHub API call fails | Log error with details, display message, exit with code 1 |
| Cannot create log directory | Display error with path, exit with code 1 |
| Cannot write state.json | Log error, display message, exit with code 1 |
| Invalid JSON in state.json | Log error, treat as empty state, continue |
