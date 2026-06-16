# Test runner script for Windows (PowerShell)
# Standard location: tools/run_tests.ps1

# Set the location to the directory where the script is located
Set-Location $PSScriptRoot

$testFiles = Get-ChildItem -Path ../tests/cases/*.cpp

$failed = 0
$passed = 0

foreach ($file in $testFiles) {
    $name = $file.BaseName
    Write-Host "Compiling $name..." -ForegroundColor Cyan
    # Note: Updated include paths for reorganization
    & g++ -std=c++11 -I../tests/mocks -I../src $file.FullName -o "$name.exe"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Running $name..." -ForegroundColor Cyan
        & "./$name.exe"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "$name PASSED" -ForegroundColor Green
            $passed++
        } else {
            Write-Host "$name FAILED" -ForegroundColor Red
            $failed++
        }
        
        # Cleanup executable
        Remove-Item "$name.exe"
    } else {
        Write-Host "Compilation of $name FAILED" -ForegroundColor Red
        $failed++
    }
    Write-Host "----------------------------------------"
}

Write-Host "`nTest Summary:" -ForegroundColor White
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red

if ($failed -gt 0) { exit 1 }
