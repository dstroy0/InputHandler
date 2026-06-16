#!/bin/bash

# Test runner script for Linux (Ubuntu)
# Standard location: tools/run_tests.sh

testFiles=../tests/cases/*.cpp
failed=0
passed=0

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Ensure we are running from the tools directory or the project root
if [ -d "tools" ]; then
    cd tools
fi

for file in $testFiles; do
    name=$(basename "$file" .cpp)
    echo -e "${CYAN}Compiling $name...${NC}"
    
    # Compile with g++
    # Note: Updated include paths for reorganization
    g++ -std=c++11 -I../tests/mocks -I../src "$file" -o "$name"
    
    if [ $? -eq 0 ]; then
        echo -e "${CYAN}Running $name...${NC}"
        "./$name"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}$name PASSED${NC}"
            ((passed++))
        else
            echo -e "${RED}$name FAILED${NC}"
            ((failed++))
        fi
        
        # Cleanup executable
        rm "$name"
    else
        echo -e "${RED}Compilation of $name FAILED${NC}"
        ((failed++))
    fi
    echo "----------------------------------------"
done

echo -e "${WHITE}\nTest Summary:${NC}"
echo -e "${GREEN}Passed: $passed${NC}"
echo -e "${RED}Failed: $failed${NC}"

if [ $failed -gt 0 ]; then
    exit 1
else
    exit 0
fi
