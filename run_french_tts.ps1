# French TTS Runner Script
# Run this in PowerShell to start generating French speech
# Usage: .\run_french_tts.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  French TTS — Coqui TTS (Docker)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure required folders exist
New-Item -ItemType Directory -Force -Path "french_audio_output" | Out-Null
New-Item -ItemType Directory -Force -Path "voice_samples" | Out-Null

# Check if image already built
$imageExists = docker images french-tts:local -q 2>$null

if (-not $imageExists) {
    Write-Host 'Building Docker image (first run only, may take 5-10 min)...' -ForegroundColor Yellow
    Write-Host 'This downloads Python 3.11, TTS library, and ML dependencies.' -ForegroundColor Yellow
    Write-Host ""
    docker build -f Dockerfile.french-cpu -t french-tts:local .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build failed. Check the error above." -ForegroundColor Red
        exit 1
    }
    Write-Host ""
    Write-Host "Image built successfully!" -ForegroundColor Green
} else {
    Write-Host "Docker image already built. Skipping build step." -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting French TTS container..." -ForegroundColor Yellow
Write-Host "Your WAV files will appear in: french_audio_output\" -ForegroundColor Green
Write-Host "Put voice sample WAVs in:       voice_samples\" -ForegroundColor Green
Write-Host ""

# Run non-interactively — mode and speaker are set in generate_french_speech.py
docker run --rm `
    -v "${PWD}/generate_french_speech.py:/app/generate_french_speech.py" `
    -v "${PWD}/french_audio_output:/app/french_audio_output" `
    -v "${PWD}/voice_samples:/app/voice_samples" `
    -v "tts_models_cache:/app/models" `
    -e COQUI_TOS_AGREED=1 `
    -e TTS_HOME=/app/models `
    french-tts:local `
    python generate_french_speech.py

Write-Host ""
Write-Host "Done! Check the 'french_audio_output' folder for your WAV files." -ForegroundColor Green
