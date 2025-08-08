#ifndef RISCV_INSTRUCTIONS_H
#define RISCV_INSTRUCTIONS_H

#include <stdbool.h>

/**
 * RISC-V Instruction Definition
 * Generated from RISC-V Unified Database YAML files
 */
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

#define RISCV_INSTRUCTION_COUNT 3

extern const riscv_instruction_t riscv_instructions[RISCV_INSTRUCTION_COUNT];

// Individual instruction definitions
#define INST_ADD_IDX 0
#define INST_ADDI_IDX 1
#define INST_LUI_IDX 2

#endif // RISCV_INSTRUCTIONS_H
