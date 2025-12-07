# Plist Environment Variables

This feature adds environment variable support to the LaunchAgent plist generator within the `den` CLI application. LaunchAgents run in a minimal environment without the user's shell PATH, causing commands like `brew` to fail when executed as scheduled tasks. This feature enables users to configure environment variables (particularly PATH) in generated plist files, ensuring scheduled commands can locate required executables.

## Requirements

### Requirement: Environment Variable Configuration

The system SHALL support specifying environment variables for LaunchAgents.

#### Scenario: EnvironmentVariables in plist
- **WHEN** generating a plist with environment variables configured
- **THEN** the system SHALL include an EnvironmentVariables dict in the plist output

#### Scenario: Key-value pairs
- **WHEN** environment variables are provided
- **THEN** the system SHALL include each variable as a key-value pair within the EnvironmentVariables dict

#### Scenario: Omit when empty
- **WHEN** no environment variables are configured
- **THEN** the system SHALL omit the EnvironmentVariables key from the plist output

#### Scenario: Parse EnvironmentVariables
- **WHEN** parsing a plist containing EnvironmentVariables
- **THEN** the system SHALL extract the environment variables into the TaskConfig

### Requirement: Automatic PATH Capture

The system SHALL automatically capture the current PATH environment variable.

#### Scenario: Capture current PATH
- **WHEN** a user runs `den launchctl install`
- **THEN** the system SHALL capture the current shell PATH environment variable

#### Scenario: Include PATH in plist
- **WHEN** generating the plist
- **THEN** the system SHALL include the captured PATH in the EnvironmentVariables dict

#### Scenario: PATH not available
- **WHEN** the PATH environment variable is not available
- **THEN** the system SHALL proceed without setting PATH in the plist

### Requirement: Environment Variables Round-Trip

The system SHALL preserve environment variables through plist round-trip operations.

#### Scenario: Round-trip consistency
- **WHEN** a plist with EnvironmentVariables is parsed and regenerated
- **THEN** the system SHALL produce equivalent EnvironmentVariables content

#### Scenario: Special character preservation
- **WHEN** environment variables contain special characters
- **THEN** the system SHALL preserve those characters through the round-trip
