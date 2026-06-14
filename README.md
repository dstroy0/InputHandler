[![Alt text](https://github.com/dstroy0/InputHandler/blob/main/docs/img/_Logolarge.png?raw=true)](https://github.com/dstroy0/InputHandler)

# InputHandler

A lightweight, feature-rich C++ command parser library designed for microcontrollers (Arduino, ESP32, Teensy, etc.). It enables complex command tree structures with subcommands, type-safe argument parsing, and wildcard support—all while maintaining a minimal memory footprint.

[**Quick Start Guide**](https://github.com/dstroy0/InputHandler/blob/main/examples/all_platforms/basic/GetCommandFromStream/GetCommandFromStream.ino) | [**View Examples**](https://github.com/dstroy0/InputHandler/tree/main/examples) | [**API Documentation**](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html)

---

## Core Features

- **Hierarchical Command Trees:** Organize commands with nested subcommands (e.g., `LED ON RED`).
- **Type-Safe Arguments:** Automatic validation for `int16_t`, `uint16_t`, `float`, `char`, and specialized sequences.
- **Wildcard Support:** Match dynamic patterns in command strings (e.g., `SET*`).
- **Zero Delimiter Commands (ZDC):** Handle commands fused with data (e.g., `Z123`).
- **Minimal RAM Usage:** Command structures live in `PROGMEM`. Non-wildcard commands use 8 bytes or less of SRAM (AVR).
- **Platform Agnostic:** Compatible with any `Stream`-based interface (Serial, WiFi, etc.) or raw buffers.

---

## Technical Overview

InputHandler uses [C++11 Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) for `ih::Parameters` and `ih::InputParameters` structs.

### Basic Initialization

```cpp
#include <InputHandler.h>
using namespace ih;

// Initialize with an optional output buffer for human-readable feedback
char output_buffer[512];
Input inputHandler(output_buffer, sizeof(output_buffer));

void setup() {
    // Register commands and call begin()
    inputHandler.begin();
}
```

### Advanced Configuration

Aspects of `InputParameters` such as delimiters, line endings, and control characters are fully customizable:

```cpp
const PROGMEM DelimiterSequences process_delimseq = {
  2,          // Number of sequences
  {1, 1},     // Lengths
  {" ", ","}  // Delimiters: space or comma
};

const PROGMEM InputParameters input_prm[1] = {
  &process_name, &process_eol, &process_ccseq, &process_wcc, &process_delimseq, &process_ststpseq
};
```

---

## Unit Testing & Verification

The library includes a robust cross-platform test suite to ensure stability across updates.

### Test Structure
- **`tests/cases/`**: Unit tests covering argument parsing, nesting, wildcards, and boundary limits.
- **`tests/mocks/`**: Hardware abstraction layer (HAL) mocks for non-embedded environments.
- **`tools/`**: Automated test runners.

### Running Tests
You can run the full suite from the project root or the `tools/` directory.

**Windows (PowerShell):**
```powershell
./tools/run_tests.ps1
```

**Linux/Ubuntu (Bash):**
```bash
./tools/run_tests.sh
```

### Coverage Highlights
- **`test_args`**: Verifies type-safe extraction of signed/unsigned integers and floats.
- **`test_limits`**: Stress tests maximum argument counts (32+), command lengths, and input overflows.
- **`test_nested`**: Validates deep command tree traversal and hierarchical parent-child matching.
- **`test_wildcards`**: Ensures complex wildcard patterns match correctly while excluding invalid inputs.

---

## Design Goals

- **Efficiency:** Low memory overhead and optimized string matching.
- **Flexibility:** Parse `uint8_t` raw buffers or standard `Stream` objects.
- **Safety:** Enforce strict type checking for all command arguments.
- **Clarity:** Provide detailed diagnostic output when debug flags are enabled.

---

## Supported Platforms

The library is extensively tested on the following architectures:
- **AVR:** Arduino Uno, Mega, Leonardo, etc.
- **SAMD:** Arduino Zero, Adafruit Feather M0/M4.
- **ESP32 / ESP8266:** All variants.
- **Teensy:** 3.x and 4.x.
- **MBED:** Arduino Nano 33 BLE, etc.

*Note: ATTiny85 and ATMegaNG are not currently supported due to flash/RAM constraints.*

---

## Bug Reporting

Please report issues via [bug_report.md](https://github.com/dstroy0/InputHandler/blob/main/src/bug_report.md) or join the discussion at the [Bug Report Forum](https://github.com/dstroy0/InputHandler/discussions/60).

---

## Build Status

| Platform | Status |
| :--- | :--- |
| **Adafruit** | [![Adafruit](https://github.com/dstroy0/InputHandler/actions/workflows/adafruit_platforms.yml/badge.svg)](...) |
| **Arduino** | [![Arduino](https://github.com/dstroy0/InputHandler/actions/workflows/arduino_platforms.yml/badge.svg)](...) |
| **ESP32/8266** | [![ESP](https://github.com/dstroy0/InputHandler/actions/workflows/esp32_platforms.yml/badge.svg)](...) |
| **Teensy** | [![Teensy](https://github.com/dstroy0/InputHandler/actions/workflows/teensyduino_platforms.yml/badge.svg)](...) |
| **Docs/Lint** | [![Docs](https://github.com/dstroy0/InputHandler/actions/workflows/docs.yml/badge.svg)](...) |

---

## Changelog

*See [Releases](https://github.com/dstroy0/InputHandler/releases) for full history.*

**v0.0.12 (2023-11-03)**
- Improved wildcard matching performance.
- Fixed subcommand traversal edge cases.
- Added comprehensive unit testing infrastructure.
