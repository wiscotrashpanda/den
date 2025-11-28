# Requirements Document

## Introduction

This document specifies the requirements for a LaunchCtl helper command within the `den` CLI application. The feature simplifies the creation and management of macOS LaunchAgent plist files, providing an interactive experience for users to define scheduled background tasks without manually writing XML plist files. The generated files are stored in the standard `~/Library/LaunchAgents/` directory.

## Glossary

- **LaunchAgent**: A macOS mechanism for scheduling user-level background tasks via plist configuration files
- **Plist**: Property list file in XML format used by macOS to configure LaunchAgents
- **Domain**: A reverse-DNS style identifier prefix for plist files (e.g., `com.example`)
- **Task Name**: A user-provided identifier for the scheduled task
- **Den CLI**: The parent command-line application that hosts the launchctl subcommand
- **Config File**: The JSON configuration file located at `~/.config/den/config.json`

## Requirements

### Requirement 1

**User Story:** As a user, I want to install a new LaunchAgent through an interactive prompt, so that I can schedule background tasks without writing XML plist files manually.

#### Acceptance Criteria

1. WHEN a user runs `den launchctl install` THEN the Den CLI SHALL prompt the user for a task name
2. WHEN a user provides a task name THEN the Den CLI SHALL prompt the user for the command to execute
3. WHEN a user provides a command THEN the Den CLI SHALL prompt the user for scheduling options (interval in seconds or calendar-based schedule)
4. WHEN a user selects interval-based scheduling THEN the Den CLI SHALL prompt for the interval duration in seconds
5. WHEN a user selects calendar-based scheduling THEN the Den CLI SHALL prompt for hour and minute values
6. WHEN all prompts are completed THEN the Den CLI SHALL generate a valid plist XML file with the provided configuration

### Requirement 2

**User Story:** As a user, I want the plist file to be named according to a domain and task convention, so that my LaunchAgents are organized and identifiable.

#### Acceptance Criteria

1. WHEN generating a plist file THEN the Den CLI SHALL read the domain value from `~/.config/den/config.json`
2. WHEN the config file exists and contains a domain key THEN the Den CLI SHALL use that domain value as the plist name prefix
3. WHEN the config file does not exist or lacks a domain key THEN the Den CLI SHALL use `com.example` as the default domain
4. WHEN creating the plist filename THEN the Den CLI SHALL format it as `[domain].[task].plist`
5. WHEN the Den CLI writes the plist file THEN the Den CLI SHALL store it in `~/Library/LaunchAgents/`

### Requirement 3

**User Story:** As a user, I want the LaunchAgent to be loaded automatically after installation, so that my scheduled task starts running immediately.

#### Acceptance Criteria

1. WHEN the plist file is successfully written THEN the Den CLI SHALL execute `launchctl load` with the plist path
2. WHEN `launchctl load` succeeds THEN the Den CLI SHALL display a success message with the plist path
3. IF `launchctl load` fails THEN the Den CLI SHALL display an error message and exit with a non-zero status code

### Requirement 4

**User Story:** As a user, I want to uninstall a LaunchAgent by selecting from my existing tasks, so that I can stop and remove scheduled tasks I no longer need.

#### Acceptance Criteria

1. WHEN a user runs `den launchctl uninstall` THEN the Den CLI SHALL scan `~/Library/LaunchAgents/` for plist files matching the configured domain prefix
2. WHEN matching plist files are found THEN the Den CLI SHALL display a numbered list of available tasks for selection
3. WHEN the user selects a task from the list THEN the Den CLI SHALL execute `launchctl unload` with the selected plist path
4. WHEN `launchctl unload` succeeds THEN the Den CLI SHALL delete the plist file from disk
5. WHEN the plist file is deleted THEN the Den CLI SHALL display a success message
6. IF no matching plist files are found THEN the Den CLI SHALL display a message indicating no tasks exist for the configured domain

### Requirement 5

**User Story:** As a user, I want the generated plist to contain valid XML structure, so that macOS can properly parse and execute my scheduled tasks.

#### Acceptance Criteria

1. WHEN generating a plist THEN the Den CLI SHALL produce well-formed XML with the proper plist DOCTYPE declaration
2. WHEN generating a plist THEN the Den CLI SHALL include the Label key set to `[domain].[task].plist`
3. WHEN generating a plist THEN the Den CLI SHALL include the ProgramArguments array with the user-specified command
4. WHEN interval scheduling is selected THEN the Den CLI SHALL include the StartInterval key with the specified seconds value
5. WHEN calendar scheduling is selected THEN the Den CLI SHALL include the StartCalendarInterval dict with Hour and Minute keys
6. WHEN generating a plist THEN the Den CLI SHALL include RunAtLoad set to true
7. WHEN generating a plist THEN the Den CLI SHALL produce output that can be round-tripped through a plist parser and pretty-printer to yield equivalent content

### Requirement 6

**User Story:** As a user, I want input validation on my task configuration, so that I don't create invalid LaunchAgents.

#### Acceptance Criteria

1. WHEN a user provides an empty task name THEN the Den CLI SHALL reject the input and re-prompt
2. WHEN a user provides a task name with invalid characters (spaces, slashes, or special characters other than hyphens and underscores) THEN the Den CLI SHALL reject the input and re-prompt
3. WHEN a user provides an empty command THEN the Den CLI SHALL reject the input and re-prompt
4. WHEN a user provides a non-positive interval value THEN the Den CLI SHALL reject the input and re-prompt
5. WHEN a user provides an hour value outside 0-23 THEN the Den CLI SHALL reject the input and re-prompt
6. WHEN a user provides a minute value outside 0-59 THEN the Den CLI SHALL reject the input and re-prompt
