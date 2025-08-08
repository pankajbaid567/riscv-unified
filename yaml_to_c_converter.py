#!/usr/bin/env python3
"""
RISC-V UDB YAML to C Header Converter
Reads RISC-V instruction YAML files and converts them to C header format.
"""

import yaml
import os
import sys
from typing import Dict, List, Any
import argparse

class RiscVInstruction:
    """Represents a RISC-V instruction from UDB YAML format"""
    
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get('name', '')
        self.long_name = data.get('long_name', '')
        self.description = data.get('description', '')
        self.defined_by = data.get('definedBy', '')
        self.assembly = data.get('assembly', '')
        self.encoding = data.get('encoding', {})
        self.access = data.get('access', {})
        self.data_independent_timing = data.get('data_independent_timing', False)
        self.operation = data.get('operation()', '')
        self.pseudoinstructions = data.get('pseudoinstructions', [])
        
    def to_c_struct_init(self) -> str:
        """Convert instruction to C struct initialization"""
        # Clean up strings for C
        name = self.name.replace('-', '_')
        long_name = self.long_name.replace('"', '\\"')
        description = self.description.replace('"', '\\"').replace('\n', '\\n')
        operation = self.operation.replace('"', '\\"').replace('\n', '\\n')
        
        # Handle encoding
        encoding_match = self.encoding.get('match', '') if self.encoding else ''
        
        # Handle variables
        variables_str = ''
        if self.encoding and 'variables' in self.encoding and self.encoding['variables'] is not None:
            if isinstance(self.encoding['variables'], list):
                vars_list = []
                for var in self.encoding['variables']:
                    var_name = var.get('name', '')
                    var_location = var.get('location', '')
                    left_shift = var.get('left_shift', 0)
                    vars_list.append(f'{{{{\\"name\\": \\"{var_name}\\", \\"location\\": \\"{var_location}\\", \\"left_shift\\": {left_shift}}}')
                variables_str = ', '.join(vars_list)
        elif hasattr(self, 'variables_str') and self.variables_str:
            # Handle pre-parsed variables string from generated YAML
            variables_str = self.variables_str
        
        # Access permissions
        access_s = 'true' if self.access.get('s') == 'always' else 'false'
        access_u = 'true' if self.access.get('u') == 'always' else 'false'
        access_vs = 'true' if self.access.get('vs') == 'always' else 'false'
        access_vu = 'true' if self.access.get('vu') == 'always' else 'false'
        
        timing_str = 'true' if self.data_independent_timing else 'false'
        
        return f'''    {{
        .name = "{name}",
        .long_name = "{long_name}",
        .description = "{description}",
        .defined_by = "{self.defined_by}",
        .assembly = "{self.assembly}",
        .encoding_match = "{encoding_match}",
        .variables = "{variables_str}",
        .access_s = {access_s},
        .access_u = {access_u},
        .access_vs = {access_vs},
        .access_vu = {access_vu},
        .data_independent_timing = {timing_str},
        .operation = "{operation}"
    }}'''

def load_yaml_file(file_path: str) -> List[Dict[str, Any]]:
    """Load and parse a YAML file, handling multiple documents"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Handle multiple YAML documents
            documents = list(yaml.safe_load_all(f))
            return [doc for doc in documents if doc is not None]
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def generate_c_header(instructions: List[RiscVInstruction], output_file: str):
    """Generate C header file from instructions"""
    header_guard = "RISCV_INSTRUCTIONS_H"
    
    header_content = f"""#ifndef {header_guard}
#define {header_guard}

#include <stdbool.h>

/**
 * RISC-V Instruction Definition
 * Generated from RISC-V Unified Database YAML files
 */
typedef struct {{
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
}} riscv_instruction_t;

#define RISCV_INSTRUCTION_COUNT {len(instructions)}

extern const riscv_instruction_t riscv_instructions[RISCV_INSTRUCTION_COUNT];

// Individual instruction definitions
"""
    
    for i, inst in enumerate(instructions):
        header_content += f"#define INST_{inst.name.upper().replace('-', '_')}_IDX {i}\n"
    
    header_content += f"""
#endif // {header_guard}
"""
    
    # Generate implementation file
    impl_content = f"""#include "{os.path.basename(output_file)}"

const riscv_instruction_t riscv_instructions[RISCV_INSTRUCTION_COUNT] = {{
"""
    
    for i, inst in enumerate(instructions):
        impl_content += inst.to_c_struct_init()
        if i < len(instructions) - 1:
            impl_content += ","
        impl_content += "\n"
    
    impl_content += "};\n"
    
    # Write header file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header_content)
    
    # Write implementation file
    impl_file = output_file.replace('.h', '.c')
    with open(impl_file, 'w', encoding='utf-8') as f:
        f.write(impl_content)
    
    print(f"Generated {output_file} and {impl_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert RISC-V UDB YAML to C header')
    parser.add_argument('input_files', nargs='+', help='Input YAML files')
    parser.add_argument('-o', '--output', default='riscv_instructions.h', 
                       help='Output C header file (default: riscv_instructions.h)')
    
    args = parser.parse_args()
    
    instructions = []
    
    for yaml_file in args.input_files:
        if not os.path.exists(yaml_file):
            print(f"File not found: {yaml_file}")
            continue
            
        print(f"Processing {yaml_file}")
        yaml_documents = load_yaml_file(yaml_file)
        
        for yaml_data in yaml_documents:
            if yaml_data and yaml_data.get('kind') == 'instruction':
                inst = RiscVInstruction(yaml_data)
                instructions.append(inst)
        
        if not yaml_documents:
            print(f"Warning: {yaml_file} contains no valid documents")
    
    if not instructions:
        print("No valid instructions found!")
        return 1
    
    print(f"Found {len(instructions)} instructions")
    generate_c_header(instructions, args.output)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
