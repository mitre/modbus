# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2025-06-19

### Added

- This CHANGELOG.
- Makefile providing targets to build payloads.

### Changed

- Updated fact names to be consistent with other Caldera for OT plugins (#1).
- Bumped `pymodbus` dependency to version 3.9.2.
- Changed Modbus read output for easier parsing.
- Changed ability ATT&CK mappings.
- Updated documentation to reflect all changes.
- Simplified `src/` directory layout.

## [1.1.0] - 2024-09-18

### Added

- Caldera v5 (Magma) GUI.

## [1.0.0] - 2023-07-17

### Added

- Initial stable version of the Modbus plugin, part of 
  [MITRE Caldera™ for OT](https://github.com/mitre/caldera-ot). Provides 10
  unique Caldera adversary emulation abilities specific to the Modbus protocol.

[unreleased]: https://github.com/mitre/modbus/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/mitre/modbus/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/mitre/modbus/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mitre/modbus/releases/tag/v1.0.0
