# LaunchCtl Helper

This feature provides a LaunchCtl helper command within the `den` CLI application. The feature simplifies the creation and management of macOS LaunchAgent plist files, providing an interactive experience for users to define scheduled background tasks without manually writing XML plist files. The generated files are stored in the standard `~/Library/LaunchAgents/` directory.

## Requirements

### Requirement: Interactive LaunchAgent Installation

The system SHALL provide an interactive prompt for installing new LaunchAgents.

#### Scenario: Task name prompt
- **WHEN** a user runs `den launchctl install`
- **THEN** the system SHALL prompt the user for a task name

#### Scenario: Command prompt
- **WHEN** a user provides a task name
- **THEN** the system SHALL prompt the user for the command to execute

#### Scenario: Scheduling options
- **WHEN** a user provides a command
- **THEN** the system SHALL prompt the user for scheduling options (interval in seconds or calendar-based schedule)

#### Scenario: Interval scheduling
- **WHEN** a user selects interval-based scheduling
- **THEN** the system SHALL prompt for the interval duration in seconds

#### Scenario: Calendar scheduling
- **WHEN** a user selects calendar-based scheduling
- **THEN** the system SHALL prompt for hour and minute values

#### Scenario: Plist generation
- **WHEN** all prompts are completed
- **THEN** the system SHALL generate a valid plist XML file with the provided configuration

### Requirement: Domain-Based Naming

The system SHALL name plist files according to a domain and task convention.

#### Scenario: Domain from config
- **WHEN** generating a plist file
- **THEN** the system SHALL read the domain value from `~/.config/den/config.json`

#### Scenario: Configured domain
- **WHEN** the config file exists and contains a domain key
- **THEN** the system SHALL use that domain value as the plist name prefix

#### Scenario: Default domain
- **WHEN** the config file does not exist or lacks a domain key
- **THEN** the system SHALL use `com.example` as the default domain

#### Scenario: Filename format
- **WHEN** creating the plist filename
- **THEN** the system SHALL format it as `[domain].[task].plist`

#### Scenario: File location
- **WHEN** the system writes the plist file
- **THEN** the system SHALL store it in `~/Library/LaunchAgents/`

### Requirement: Automatic LaunchAgent Loading

The system SHALL automatically load the LaunchAgent after installation.

#### Scenario: Load after install
- **WHEN** the plist file is successfully written
- **THEN** the system SHALL execute `launchctl load` with the plist path

#### Scenario: Load success
- **WHEN** `launchctl load` succeeds
- **THEN** the system SHALL display a success message with the plist path

#### Scenario: Load failure
- **WHEN** `launchctl load` fails
- **THEN** the system SHALL display an error message and exit with a non-zero status code

### Requirement: LaunchAgent Uninstallation

The system SHALL provide a way to uninstall existing LaunchAgents.

#### Scenario: Scan for agents
- **WHEN** a user runs `den launchctl uninstall`
- **THEN** the system SHALL scan `~/Library/LaunchAgents/` for plist files matching the configured domain prefix

#### Scenario: Display task list
- **WHEN** matching plist files are found
- **THEN** the system SHALL display a numbered list of available tasks for selection

#### Scenario: Unload agent
- **WHEN** the user selects a task from the list
- **THEN** the system SHALL execute `launchctl unload` with the selected plist path

#### Scenario: Delete plist
- **WHEN** `launchctl unload` succeeds
- **THEN** the system SHALL delete the plist file from disk

#### Scenario: Uninstall success
- **WHEN** the plist file is deleted
- **THEN** the system SHALL display a success message

#### Scenario: No agents found
- **WHEN** no matching plist files are found
- **THEN** the system SHALL display a message indicating no tasks exist for the configured domain

### Requirement: Valid Plist XML Structure

The system SHALL generate well-formed plist XML.

#### Scenario: DOCTYPE declaration
- **WHEN** generating a plist
- **THEN** the system SHALL produce well-formed XML with the proper plist DOCTYPE declaration

#### Scenario: Label key
- **WHEN** generating a plist
- **THEN** the system SHALL include the Label key set to `[domain].[task].plist`

#### Scenario: ProgramArguments
- **WHEN** generating a plist
- **THEN** the system SHALL include the ProgramArguments array with the user-specified command

#### Scenario: StartInterval
- **WHEN** interval scheduling is selected
- **THEN** the system SHALL include the StartInterval key with the specified seconds value

#### Scenario: StartCalendarInterval
- **WHEN** calendar scheduling is selected
- **THEN** the system SHALL include the StartCalendarInterval dict with Hour and Minute keys

#### Scenario: RunAtLoad
- **WHEN** generating a plist
- **THEN** the system SHALL include RunAtLoad set to true

#### Scenario: Plist round-trip
- **WHEN** generating a plist and parsing the output
- **THEN** the system SHALL produce output that can be round-tripped through a plist parser to yield equivalent content

### Requirement: Input Validation

The system SHALL validate user input during task configuration.

#### Scenario: Empty task name
- **WHEN** a user provides an empty task name
- **THEN** the system SHALL reject the input and re-prompt

#### Scenario: Invalid task name characters
- **WHEN** a user provides a task name with invalid characters (spaces, slashes, or special characters other than hyphens and underscores)
- **THEN** the system SHALL reject the input and re-prompt

#### Scenario: Empty command
- **WHEN** a user provides an empty command
- **THEN** the system SHALL reject the input and re-prompt

#### Scenario: Non-positive interval
- **WHEN** a user provides a non-positive interval value
- **THEN** the system SHALL reject the input and re-prompt

#### Scenario: Invalid hour
- **WHEN** a user provides an hour value outside 0-23
- **THEN** the system SHALL reject the input and re-prompt

#### Scenario: Invalid minute
- **WHEN** a user provides a minute value outside 0-59
- **THEN** the system SHALL reject the input and re-prompt
