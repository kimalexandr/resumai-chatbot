Write-Host "Starting ResumAI Chatbot..." -ForegroundColor Green
Write-Host ""

# Проверяем наличие Python
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt
        Write-Host ""
        Write-Host "Starting application..." -ForegroundColor Green
        python run.py
    }
} catch {
    try {
        $pythonVersion = py --version 2>$null
        if ($pythonVersion) {
            Write-Host "Python found: $pythonVersion" -ForegroundColor Green
            Write-Host "Installing dependencies..." -ForegroundColor Yellow
            py -m pip install -r requirements.txt
            Write-Host ""
            Write-Host "Starting application..." -ForegroundColor Green
            py run.py
        }
    } catch {
        Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
        Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
        Read-Host "Press Enter to continue"
        exit 1
    }
}
