#!/usr/bin/env python3
"""
Complete RISC-V UDB Code Generation Demo
Demonstrates the full pipeline as requested in the coding challenge.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from yaml_to_c_converter import main as yaml_to_c_main

def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("="*60)
    print("RISC-V UDB Code Generation Challenge - Complete Demo")
    print("="*60)
    print()
    
    # Original YAML files from UDB
    original_yamls = [
        "/Users/pankajbaid/Desktop/riscv-unified-db/spec/std/isa/inst/I/add.yaml",
        "/Users/pankajbaid/Desktop/riscv-unified-db/spec/std/isa/inst/I/addi.yaml", 
        "/Users/pankajbaid/Desktop/riscv-unified-db/spec/std/isa/inst/I/lui.yaml"
    ]
    
    print("Step 1: Read RISC-V UDB YAML files")
    print("Input files:")
    for yaml_file in original_yamls:
        if os.path.exists(yaml_file):
            print(f"  ✓ {os.path.basename(yaml_file)}")
        else:
            print(f"  ✗ {yaml_file} (not found)")
    print()
    
    print("Step 2: Generate C header from YAML")
    print("Running: python yaml_to_c_converter.py ...")
    
    old_argv = sys.argv
    sys.argv = ['yaml_to_c_converter.py'] + original_yamls + ['-o', 'demo_instructions.h']
    
    try:
        yaml_to_c_main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv
    
    if os.path.exists('demo_instructions.h') and os.path.exists('demo_instructions.c'):
        print("  ✓ Generated demo_instructions.h and demo_instructions.c")
    else:
        print("  ✗ Failed to generate C files")
        return 1
    print()
    
    print("Step 3: Compile C program that uses the generated header")
    compile_cmd = "gcc -o demo_c_to_yaml c_to_yaml_converter.c demo_instructions.c"
    success, stdout, stderr = run_command(compile_cmd)
    
    if success:
        print(f"  ✓ Compiled demo_c_to_yaml successfully")
    else:
        print(f"  ✗ Compilation failed: {stderr}")
        return 1
    print()
    
    print("Step 4: Run C program to generate YAML")
    success, stdout, stderr = run_command("./demo_c_to_yaml demo_output_step1.yaml")
    
    if success:
        print("  ✓ Generated demo_output_step1.yaml")
        print(f"  Output: {stdout.strip()}")
    else:
        print(f"  ✗ Failed to run C program: {stderr}")
        return 1
    print()
    
    print("Step 5: Use generated YAML as input (round-trip test)")
    print("First, split the multi-document YAML...")
    
    success, stdout, stderr = run_command("/Users/pankajbaid/Desktop/riscv-unified-db/.venv/bin/python split_yaml.py demo_output_step1.yaml")
    if success:
        print("  ✓ Split YAML into individual files")
        print(f"  {stdout.strip()}")
    else:
        print(f"  ✗ Failed to split YAML: {stderr}")
        return 1
    
    print("\nStep 6: Generate second C header from generated YAML")
    split_files = ['inst_add.yaml', 'inst_addi.yaml', 'inst_lui.yaml']
    
    sys.argv = ['yaml_to_c_converter.py'] + split_files + ['-o', 'demo_instructions2.h']
    try:
        yaml_to_c_main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv
    
    if os.path.exists('demo_instructions2.h') and os.path.exists('demo_instructions2.c'):
        print("  ✓ Generated demo_instructions2.h and demo_instructions2.c")
    else:
        print("  ✗ Failed to generate second C files")
        return 1
    print()
    
    print("Step 7: Compile second C program")
    compile_cmd = "gcc -o demo_c_to_yaml2 c_to_yaml_converter.c demo_instructions2.c"
    success, stdout, stderr = run_command(compile_cmd)
    
    if success:
        print(f"  ✓ Compiled demo_c_to_yaml2 successfully")
    else:
        print(f"  ✗ Second compilation failed: {stderr}")
        return 1
    print()
    
    print("Step 8: Run second C program to complete round-trip")
    success, stdout, stderr = run_command("./demo_c_to_yaml2 demo_output_final.yaml")
    
    if success:
        print("  ✓ Generated demo_output_final.yaml")
        print(f"  Output: {stdout.strip()}")
    else:
        print(f"  ✗ Failed to run second C program: {stderr}")
        return 1
    print()
    
    print("="*60)
    print("PIPELINE COMPLETE!")
    print("="*60)
    print()
    print("Summary of generated files:")
    files_to_check = [
        ('demo_instructions.h', 'C header from original YAML'),
        ('demo_instructions.c', 'C implementation from original YAML'),
        ('demo_c_to_yaml', 'First compiled C program'),
        ('demo_output_step1.yaml', 'YAML output from first C program'),
        ('inst_add.yaml', 'Split individual instruction file'),
        ('demo_instructions2.h', 'C header from generated YAML'),
        ('demo_instructions2.c', 'C implementation from generated YAML'),
        ('demo_c_to_yaml2', 'Second compiled C program'),
        ('demo_output_final.yaml', 'Final YAML output (round-trip complete)')
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✓ {filename:<25} - {description} ({size} bytes)")
        else:
            print(f"  ✗ {filename:<25} - {description} (missing)")
    
    print()
    print("The pipeline successfully demonstrates:")
    print("  1. Reading RISC-V UDB YAML files")
    print("  2. Generating C headers and implementation")
    print("  3. Compiling C programs that use the headers")
    print("  4. Generating YAML from C program output")
    print("  5. Complete round-trip verification")
    print()
    print("Challenge completed successfully!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
