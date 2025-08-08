# Makefile for RISC-V UDB Code Generation Pipeline

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
PYTHON = /Users/pankajbaid/Desktop/riscv-unified-db/.venv/bin/python

# Default target
all: run-pipeline

# Install Python dependencies
install-deps:
	$(PYTHON) -m pip install PyYAML

# Run the complete pipeline
run-pipeline: install-deps
	$(PYTHON) pipeline.py

# Manual steps (for reference)
yaml-to-c:
	$(PYTHON) yaml_to_c_converter.py spec/std/isa/inst/I/add.yaml spec/std/isa/inst/I/addi.yaml spec/std/isa/inst/I/lui.yaml -o riscv_instructions.h

compile-c: riscv_instructions.h riscv_instructions.c
	$(CC) $(CFLAGS) -o c_to_yaml_converter c_to_yaml_converter.c riscv_instructions.c

run-c: c_to_yaml_converter
	./c_to_yaml_converter generated_instructions.yaml

# Clean generated files
clean:
	rm -f *.h *.c riscv_instructions.c c_to_yaml_converter c_to_yaml_converter2
	rm -f *.yaml generated_instructions*.yaml
	rm -f *.exe *.out

# Test with specific YAML files
test-specific:
	$(PYTHON) yaml_to_c_converter.py spec/std/isa/inst/I/add.yaml spec/std/isa/inst/I/addi.yaml -o test_instructions.h
	$(CC) $(CFLAGS) -o test_converter c_to_yaml_converter.c test_instructions.c
	./test_converter test_output.yaml
	@echo "Generated test_output.yaml"

# Help
help:
	@echo "Available targets:"
	@echo "  all, run-pipeline  - Run the complete pipeline"
	@echo "  install-deps       - Install Python dependencies"  
	@echo "  yaml-to-c         - Convert YAML to C header (manual)"
	@echo "  compile-c         - Compile C program (manual)"
	@echo "  run-c             - Run C program (manual)"
	@echo "  test-specific     - Test with specific files"
	@echo "  clean             - Clean generated files"
	@echo "  help              - Show this help"

.PHONY: all run-pipeline install-deps yaml-to-c compile-c run-c clean test-specific help
