@echo off
setlocal
cd /d C:\ai\minx
set HF_HUB_DISABLE_XET=1

echo ================================================
echo PIPELINE MINX OTOMATIS
echo ================================================

echo.
echo [STEP 3/6] Training LoRA...
python scripts\train_lora.py
if %errorlevel% neq 0 goto :fail

echo.
echo [STEP 4/6] Merge LoRA...
python scripts\merge_export.py
if %errorlevel% neq 0 goto :fail

echo.
echo [STEP 5a/6] Convert GGUF F16...
cd llama.cpp
python convert_hf_to_gguf.py ..\models\minx-merged --outfile ..\models\minx-gguf\minx-f16.gguf --outtype f16
if %errorlevel% neq 0 goto :fail
cd ..

echo.
echo [STEP 5b/6] Quantize Q4_K_M...
python scripts\quantize_f16_to_q4.py
if %errorlevel% neq 0 goto :fail

echo.
echo [STEP 6/6] Buat model Ollama...
ollama create minx -f Modelfile
if %errorlevel% neq 0 goto :fail

echo.
echo ================================================
echo SELESAI - minx siap pakai lewat Ollama
echo ================================================
echo.
echo Tes manual: ollama run minx
echo.
goto :eof

:fail
echo.
echo [GAGAL] Pipeline berhenti di langkah di atas.
pause