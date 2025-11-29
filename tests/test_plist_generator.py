"""Unit tests for the plist_generator module.

Tests for environment variable handling in plist generation and parsing.
"""

from den.plist_generator import TaskConfig, generate_plist, parse_plist


def test_generate_plist_with_env_vars():
    """Test generating a plist with environment variables."""
    config = TaskConfig(
        label="com.example.test",
        program_arguments=["/bin/echo", "hello"],
        environment_variables={"PATH": "/usr/bin:/bin", "TEST_VAR": "value"},
    )

    plist_xml = generate_plist(config)

    assert "<key>EnvironmentVariables</key>" in plist_xml
    assert "<key>PATH</key>" in plist_xml
    assert "<string>/usr/bin:/bin</string>" in plist_xml
    assert "<key>TEST_VAR</key>" in plist_xml
    assert "<string>value</string>" in plist_xml


def test_generate_plist_without_env_vars():
    """Test generating a plist without environment variables."""
    config = TaskConfig(
        label="com.example.test",
        program_arguments=["/bin/echo", "hello"],
        environment_variables=None,
    )

    plist_xml = generate_plist(config)

    assert "<key>EnvironmentVariables</key>" not in plist_xml


def test_parse_plist_with_env_vars():
    """Test parsing a plist with environment variables."""
    plist_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.test</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/echo</string>
        <string>hello</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/bin:/bin</string>
        <key>TEST_VAR</key>
        <string>value</string>
    </dict>
</dict>
</plist>
"""
    config = parse_plist(plist_xml)

    assert config.environment_variables is not None
    assert config.environment_variables["PATH"] == "/usr/bin:/bin"
    assert config.environment_variables["TEST_VAR"] == "value"


def test_parse_plist_without_env_vars():
    """Test parsing a plist without environment variables."""
    plist_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.test</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/echo</string>
        <string>hello</string>
    </array>
</dict>
</plist>
"""
    config = parse_plist(plist_xml)

    assert config.environment_variables is None
