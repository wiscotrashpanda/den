# Requirements Document

## Introduction

This document specifies the requirements for adding environment variable support to the LaunchAgent plist generator within the `den` CLI application. LaunchAgents run in a minimal environment without the user's shell PATH, causing commands like `brew` to fail when executed as scheduled tasks. This feature enables users to configure environment variables (particularly PATH) in generated plist files, ensuring scheduled commands can locate required executables.

## Glossary

- **LaunchAgent**: A macOS mechanism for scheduling user-level background tasks via plist configuration files
- **Plist**: Property list file in XML format used by macOS to configure LaunchAgents
- **EnvironmentVariables**: A plist key that specifies environment variables to set when the LaunchAgent executes
- **PATH**: An environment variable containing directories where the system searches for executable commands
- **TaskConfig**: The dataclass used to configure LaunchAgent task parameters
- **Den CLI**: The parent command-line application that hosts the launchctl subcommand

## Requirements

### Requirement 1

**User Story:** As a user, I want to specify environment variables for my LaunchAgent, so that scheduled commands can find executables that require a specific PATH.

#### Acceptance Criteria

1. WHEN generating a plist with environment variables configured THEN the Den CLI SHALL include an EnvironmentVariables dict in the plist output
2. WHEN environment variables are provided THEN the Den CLI SHALL include each variable as a key-value pair within the EnvironmentVariables dict
3. WHEN no environment variables are configured THEN the Den CLI SHALL omit the EnvironmentVariables key from the plist output
4. WHEN parsing a plist containing EnvironmentVariables THEN the Den CLI SHALL extract the environment variables into the TaskConfig

### Requirement 2

**User Story:** As a user, I want the launchctl install command to automatically include my current PATH, so that scheduled commands work without manual configuration.

#### Acceptance Criteria

1. WHEN a user runs `den launchctl install` THEN the Den CLI SHALL capture the current shell PATH environment variable
2. WHEN generating the plist THEN the Den CLI SHALL include the captured PATH in the EnvironmentVariables dict
3. WHEN the PATH environment variable is not available THEN the Den CLI SHALL proceed without setting PATH in the plist

### Requirement 3

**User Story:** As a user, I want the plist round-trip to preserve environment variables, so that parsing and regenerating a plist maintains all configuration.

#### Acceptance Criteria

1. WHEN a plist with EnvironmentVariables is parsed and regenerated THEN the Den CLI SHALL produce equivalent EnvironmentVariables content
2. WHEN environment variables contain special characters THEN the Den CLI SHALL preserve those characters through the round-trip

