# RISC-V UDB Code Generation Pipeline

This project implements a complete code generation pipeline for the RISC-V Unified Database (UDB), as requested in the coding challenge.

## Overview

The pipeline converts RISC-V instruction definitions from YAML format to C headers, then back to YAML, demonstrating a complete round-trip code generation process.

## Files

- `yaml_to_c_converter.py` - Python program that reads UDB YAML files and generates C headers
- `c_to_yaml_converter.c` - C program that reads C header data and outputs YAML
- `pipeline.py` - Complete pipeline automation script
- `Makefile` - Build automation

## Pipeline Steps

1. **YAML → C Header**: Read RISC-V instruction YAML files and generate C header/implementation
2. **C Compilation**: Compile C program that includes the generated header
3. **C → YAML**: Run C program to emit instruction data as YAML
4. **Round-trip Verification**: Use generated YAML as input and verify consistency

## Usage

### Quick Start
```bash
make run-pipeline
```

This will automatically:
- Install Python dependencies (PyYAML)
- Process YAML files from the UDB
- Generate C headers
- Compile and run C programs
- Verify round-trip conversion

### Manual Steps

1. Convert YAML to C header:
```bash
python yaml_to_c_converter.py spec/std/isa/inst/I/add.yaml spec/std/isa/inst/I/addi.yaml -o riscv_instructions.h
```

2. Compile C program:
```bash
gcc -o c_to_yaml_converter c_to_yaml_converter.c riscv_instructions.c
```

3. Generate YAML from C:
```bash
./c_to_yaml_converter generated_instructions.yaml
```

## Features

### YAML to C Converter
- Parses UDB YAML instruction format
- Generates C struct definitions
- Handles encoding, access permissions, and operation descriptions
- Creates both header (.h) and implementation (.c) files

### C to YAML Converter
- Reads compiled instruction data
- Outputs valid YAML format
- Handles string escaping and formatting
- Maintains instruction structure

### Pipeline Automation
- Automatic dependency management
- Complete round-trip verification
- Error handling and reporting
- File existence validation

## Data Structure

The C representation uses this structure:
```c
typedef struct {
    const char* name;
    const char* long_name;
    const char* description;
    const char* defined_by;
    const char* assembly;
    const char* encoding_match;
    const char* variables;
    bool access_s;
    bool access_u;
    bool access_vs;
    bool access_vu;
    bool data_independent_timing;
    const char* operation;
} riscv_instruction_t;
```

## Example

Input YAML (add.yaml):
```yaml
kind: instruction
name: add
long_name: Integer add
description: Add the value in xs1 to xs2, and store the result in xd
definedBy: I
assembly: xd, xs1, xs2
encoding:
  match: 0000000----------000-----0110011
```

Generated C:
```c
{
    .name = "add",
    .long_name = "Integer add",
    .description = "Add the value in xs1 to xs2, and store the result in xd",
    .defined_by = "I",
    .assembly = "xd, xs1, xs2",
    .encoding_match = "0000000----------000-----0110011",
    // ... other fields
}
```

Output YAML:
```yaml
kind: instruction
name: add
long_name: "Integer add"
description: "Add the value in xs1 to xs2, and store the result in xd"
definedBy: I
assembly: xd, xs1, xs2
encoding:
  match: 0000000----------000-----0110011
```

## Requirements

- Python 3.7+ with PyYAML
- GCC compiler
- RISC-V Unified Database files

## Verification

The pipeline includes round-trip verification:
1. Original YAML → C Header₁ → YAML₁
2. YAML₁ → C Header₂ → YAML₂
3. Compare YAML₁ and YAML₂ for structural consistency

## Clean Up

```bash
make clean
```

This removes all generated files including headers, compiled programs, and output YAML files.
