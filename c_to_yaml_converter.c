#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "riscv_instructions.h"

/**
 * C program that reads the generated C header file data and outputs it as YAML
 */

void escape_yaml_string(const char* input, char* output, size_t max_len) {
    size_t i = 0, j = 0;
    
    while (input[i] != '\0' && j < max_len - 1) {
        if (input[i] == '"') {
            if (j < max_len - 2) {
                output[j++] = '\\';
                output[j++] = '"';
            }
        } else if (input[i] == '\\' && input[i+1] == 'n') {
            // Convert \n back to actual newline for multi-line strings
            output[j++] = '\n';
            i++; // Skip the 'n' 
        } else if (input[i] == '\\' && input[i+1] == '\\') {
            if (j < max_len - 2) {
                output[j++] = '\\';
                output[j++] = '\\';
            }
            i++; // Skip the second backslash
        } else {
            output[j++] = input[i];
        }
        i++;
    }
    output[j] = '\0';
}

void print_yaml_instruction(const riscv_instruction_t* inst) {
    char escaped_desc[4096];
    char escaped_op[4096];
    
    escape_yaml_string(inst->description, escaped_desc, sizeof(escaped_desc));
    escape_yaml_string(inst->operation, escaped_op, sizeof(escaped_op));
    
    printf("---\n");
    printf("kind: instruction\n");
    printf("name: %s\n", inst->name);
    printf("long_name: \"%s\"\n", inst->long_name);
    
    if (strlen(escaped_desc) > 0) {
        if (strchr(escaped_desc, '\n') != NULL) {
            printf("description: |\n");
            // Split long descriptions into multiple lines
            char* desc_copy = strdup(escaped_desc);
            char* line = strtok(desc_copy, "\n");
            while (line != NULL) {
                printf("  %s\n", line);
                line = strtok(NULL, "\n");
            }
            free(desc_copy);
        } else if (strlen(escaped_desc) > 60) {
            printf("description: |\n");
            printf("  %s\n", escaped_desc);
        } else {
            printf("description: \"%s\"\n", escaped_desc);
        }
    }
    
    printf("definedBy: %s\n", inst->defined_by);
    printf("assembly: %s\n", inst->assembly);
    
    if (strlen(inst->encoding_match) > 0) {
        printf("encoding:\n");
        printf("  match: %s\n", inst->encoding_match);
        
        if (strlen(inst->variables) > 0) {
            printf("  variables:\n");
            // Parse variables string (simplified for this demo)
            printf("    # Variables: %s\n", inst->variables);
        }
    }
    
    printf("access:\n");
    printf("  s: %s\n", inst->access_s ? "always" : "never");
    printf("  u: %s\n", inst->access_u ? "always" : "never");
    printf("  vs: %s\n", inst->access_vs ? "always" : "never");
    printf("  vu: %s\n", inst->access_vu ? "always" : "never");
    
    printf("data_independent_timing: %s\n", inst->data_independent_timing ? "true" : "false");
    
    if (strlen(escaped_op) > 0) {
        printf("operation(): %s\n", escaped_op);
    }
}

int main(int argc, char* argv[]) {
    const char* output_file = "generated_instructions.yaml";
    
    if (argc > 1) {
        output_file = argv[1];
    }
    
    FILE* fp = fopen(output_file, "w");
    if (!fp) {
        fprintf(stderr, "Error: Could not open %s for writing\n", output_file);
        return 1;
    }
    
    // Redirect stdout to file
    FILE* old_stdout = stdout;
    stdout = fp;
    
    printf("# Generated YAML from C header data\n");
    printf("# Total instructions: %d\n", RISCV_INSTRUCTION_COUNT);
    printf("\n");
    
    for (int i = 0; i < RISCV_INSTRUCTION_COUNT; i++) {
        print_yaml_instruction(&riscv_instructions[i]);
        if (i < RISCV_INSTRUCTION_COUNT - 1) {
            printf("\n");
        }
    }
    
    // Restore stdout
    stdout = old_stdout;
    fclose(fp);
    
    printf("Generated YAML file: %s\n", output_file);
    printf("Processed %d instructions\n", RISCV_INSTRUCTION_COUNT);
    
    return 0;
}
