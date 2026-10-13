@echo off
REM minx - Setup Windows (Fixed)
echo ========================================
echo minx - Setup Windows (Laptop 4GB RAM)
echo ========================================
echo.

python --version
python -m pip --version

echo [INFO] Upgrade pip...
python -m pip install --upgrade pip

echo [INFO] Install PyTorch CPU-only...
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu

echo [INFO] Install requirements...
python -m pip install -r requirements.txt

echo [INFO] Install prebuilt llama-cpp-python without compilation...
python -m pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

echo.
echo ========================================
echo SETUP SELESAI
echo ========================================
pause