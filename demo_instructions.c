#include "demo_instructions.h"

const riscv_instruction_t riscv_instructions[RISCV_INSTRUCTION_COUNT] = {
    {
        .name = "add",
        .long_name = "Integer add",
        .description = "Add the value in xs1 to xs2, and store the result in xd.\nAny overflow is thrown away.\n",
        .defined_by = "I",
        .assembly = "xd, xs1, xs2",
        .encoding_match = "0000000----------000-----0110011",
        .variables = "{{\"name\": \"xs2\", \"location\": \"24-20\", \"left_shift\": 0}, {{\"name\": \"xs1\", \"location\": \"19-15\", \"left_shift\": 0}, {{\"name\": \"xd\", \"location\": \"11-7\", \"left_shift\": 0}",
        .access_s = true,
        .access_u = true,
        .access_vs = true,
        .access_vu = true,
        .data_independent_timing = true,
        .operation = "X[xd] = X[xs1] + X[xs2];"
    },
    {
        .name = "addi",
        .long_name = "Add immediate",
        .description = "Adds an immediate value to the value in xs1, and store the result in xd",
        .defined_by = "I",
        .assembly = "xd, xs1, imm",
        .encoding_match = "-----------------000-----0010011",
        .variables = "{{\"name\": \"imm\", \"location\": \"31-20\", \"left_shift\": 0}, {{\"name\": \"xs1\", \"location\": \"19-15\", \"left_shift\": 0}, {{\"name\": \"xd\", \"location\": \"11-7\", \"left_shift\": 0}",
        .access_s = true,
        .access_u = true,
        .access_vs = true,
        .access_vu = true,
        .data_independent_timing = true,
        .operation = "X[xd] = X[xs1] + $signed(imm);"
    },
    {
        .name = "lui",
        .long_name = "Load upper immediate",
        .description = "Load the zero-extended imm into xd.",
        .defined_by = "I",
        .assembly = "xd, imm",
        .encoding_match = "-------------------------0110111",
        .variables = "{{\"name\": \"imm\", \"location\": \"31-12\", \"left_shift\": 12}, {{\"name\": \"xd\", \"location\": \"11-7\", \"left_shift\": 0}",
        .access_s = true,
        .access_u = true,
        .access_vs = true,
        .access_vu = true,
        .data_independent_timing = true,
        .operation = "X[xd] = imm;"
    }
};
