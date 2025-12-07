# Design: Auth Login Command

## Overview

The `den auth login` command provides a user-friendly way to configure API credentials for external services. The initial implementation supports Anthropic authentication, with an extensible architecture to add more providers. Credentials are stored in a JSON file at `~/.config/den/auth.json`.

## Architecture

The auth system follows a modular design with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    den auth login                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Provider   │  │ Credential  │  │   Auth Storage      │  │
│  │  Selector   │──│   Input     │──│   (auth.json)       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Auth Command Group (`src/den/commands/auth.py`)

A Typer command group that organizes authentication-related commands.

### Provider Registry

A simple registry pattern for managing available providers:

```python
@dataclass
class Provider:
    name: str
    key_name: str  # Key used in auth.json (e.g., "anthropic_api_key")
    prompt_text: str  # Text shown when prompting for credentials
```

### Auth Storage (`src/den/auth_storage.py`)

Handles reading and writing credentials to the auth.json file.

## Data Models

### Auth Configuration File (`~/.config/den/auth.json`)

```json
{
  "anthropic_api_key": "sk-ant-...",
  "future_provider_key": "..."
}
```

## Error Handling

| Error Condition | Handling Strategy |
|----------------|-------------------|
| User cancels provider selection | Exit with code 0, no changes |
| User cancels API key input | Exit with code 0, no changes |
| Empty API key entered | Display error, re-prompt |
| Cannot create config directory | Display error with path, exit with code 1 |
| Cannot write auth.json | Display error with details, exit with code 1 |
| Invalid JSON in existing auth.json | Display error, suggest manual fix, exit with code 1 |

## Correctness Properties

### Property 1: Non-empty API key acceptance
For any non-empty string provided as an API key, the validation function SHALL accept it as valid input.

### Property 2: Credential merge preserves existing keys
For any existing auth.json content and any new credential being saved, the save operation SHALL preserve all existing keys while adding or updating the new key.

### Property 3: Credential serialization round-trip
For any valid credentials dictionary, serializing to JSON and deserializing back SHALL produce an equivalent dictionary.

### Property 4: Credential read/write consistency
For any credential key-value pair that is saved, reading that key from storage SHALL return the same value that was saved.
