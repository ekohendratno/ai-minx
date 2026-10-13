"""
minx - Step 5: Quantize Model ke GGUF
Konversi merged model ke format GGUF Q4_K_M untuk inference CPU.

Output: models/minx-gguf/minx-q4_k_m.gguf
"""

import os
import sys
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_CONFIG = {
    "export": {
        "output_dir": "models/minx-merged",
        "gguf_dir": "models/minx-gguf",
        "quant_method": "q4_k_m",
    }
}


def load_config():
    path = "configs/train_config.yaml"
    if yaml and os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            pass
    return {}


def main():
    print("=" * 60)
    print("minx - Step 5: Quantize ke GGUF (Q4_K_M)")
    print("=" * 60)

    cfg = load_config()
    exp = cfg.get("export", DEFAULT_CONFIG["export"])
    merged_dir = Path(exp.get("output_dir", DEFAULT_CONFIG["export"]["output_dir"]))
    gguf_dir = Path(exp.get("gguf_dir", DEFAULT_CONFIG["export"]["gguf_dir"]))
    quant_method = exp.get("quant_method", "q4_k_m")
    gguf_file = gguf_dir / f"minx-{quant_method}.gguf"

    print(f"\n[1] Merged model : {merged_dir}")
    print(f"    Output GGUF  : {gguf_file}")
    print(f"    Quant method : {quant_method}")

    if not merged_dir.is_dir():
        print(f"[ERROR] Merged model tidak ditemukan: {merged_dir}")
        print("[INFO] Jalankan dulu: python scripts/merge_export.py")
        sys.exit(1)

    config_file = merged_dir / "config.json"
    if not config_file.exists():
        print(f"[ERROR] config.json tidak ada di {merged_dir}")
        sys.exit(1)

    os.makedirs(gguf_dir, exist_ok=True)

    # ---- Metode 1: llama.cpp CLI (jika ada) ----
    print("\n[2] Mencoba metode konversi...")

    # Cek llama.cpp repo di folder saat ini
    llama_cpp_dir = Path("llama.cpp")
    convert_script = llama_cpp_dir / "convert_hf_to_gguf.py"
    quantize_exe = llama_cpp_dir / "build" / "bin" / "Release" / "llama-quantize.exe"

    use_cli = False
    if llama_cpp_dir.is_dir() and convert_script.exists():
        print(f"[2a] Ditemukan llama.cpp di: {llama_cpp_dir}")
        use_cli = True

    if use_cli:
        # Clone llama.cpp jika belum ada
        if not llama_cpp_dir.is_dir():
            print("[INFO] Clone llama.cpp...")
            subprocess.run(
                ["git", "clone", "--depth", "1", "https://github.com/ggerganov/llama.cpp"],
                check=True,
            )

        # Build jika perlu
        build_dir = llama_cpp_dir / "build"
        if not quantize_exe.exists():
            print("[INFO] Build llama.cpp (butuh CMake)...")
            build_dir.mkdir(exist_ok=True)
            subprocess.run(
                ["cmake", "-B", str(build_dir), "-S", str(llama_cpp_dir)],
                check=True,
            )
            subprocess.run(
                ["cmake", "--build", str(build_dir), "--config", "Release"],
                check=True,
            )

        # Convert HF -> GGUF FP16
        fp16_file = gguf_dir / "minx-fp16.gguf"
        print(f"\n[3] Konversi HuggingFace -> GGUF FP16...")
        cmd = [
            sys.executable, str(convert_script),
            str(merged_dir),
            "--outfile", str(fp16_file),
            "--outtype", "f16",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] Konversi gagal:\n{result.stderr}")
            use_cli = False
        else:
            # Quantize FP16 -> Q4_K_M
            print(f"\n[4] Quantize FP16 -> {quant_method}...")
            cmd = [str(quantize_exe), str(fp16_file), str(gguf_file), quant_method]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[ERROR] Quantize gagal:\n{result.stderr}")
                use_cli = False
            else:
                # Bersih FP16
                if fp16_file.exists():
                    fp16_file.unlink()

    # ---- Metode 2: HuggingFace transformers + manual GGUF ----
    if not use_cli or not gguf_file.exists():
        print("\n[3] Metode CLI gagal atau tidak tersedia.")
        print("    Gunakan metode Python (llama-cpp-python)...")

        try:
            from llama_cpp import Llama
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch

            print("    Load merged model...")
            model = AutoModelForCausalLM.from_pretrained(
                str(merged_dir),
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                device_map="cpu",
            )
            tokenizer = AutoTokenizer.from_pretrained(str(merged_dir))

            # Save sebagai safetensors untuk llama.cpp convert
            temp_dir = gguf_dir / "temp_hf"
            print(f"    Simpan ke format HF: {temp_dir}")
            model.save_pretrained(temp_dir)
            tokenizer.save_pretrained(temp_dir)

            print("\n[INFO] Konversi ke GGUF butuh llama.cpp convert_hf_to_gguf.py")
            print("       Clone llama.cpp dan jalankan convert manual:")
            print()
            print("  git clone --depth 1 https://github.com/ggerganov/llama.cpp")
            print("  cd llama.cpp")
            print("  pip install -r requirements.txt")
            print(f"  python convert_hf_to_gguf.py ..\\{temp_dir} --outfile ..\\{gguf_file}")
            print()
            print("  Atau download pre-built binary dari:")
            print("  https://github.com/ggerganov/llama.cpp/releases")

        except Exception as e:
            print(f"[ERROR] Gagal: {e}")
            print("\n[SOLUSI ALTERNATIF]")
            print("1. Download llama.cpp Windows binary dari:")
            print("   https://github.com/ggerganov/llama.cpp/releases")
            print("2. Extract ke folder llama.cpp/")
            print("3. Jalankan ulang script ini")
            sys.exit(1)

    # ---- Verifikasi ----
    if gguf_file.exists():
        size_mb = os.path.getsize(gguf_file) / 1024 / 1024
        print(f"\n[5] Selesai!")
        print(f"    File GGUF  : {gguf_file}")
        print(f"    Ukuran     : {size_mb:.1f} MB")
        print(f"    Format     : GGUF Q4_K_M (CPU-ready)")
        print("\nLanjut ke Step 6: test.py (uji model)")
    else:
        print(f"\n[WARNING] File GGUF tidak ditemukan: {gguf_file}")
        print("[INFO] Gunakan model HuggingFace langsung untuk test:")
        print(f"       python scripts/test.py --model {merged_dir}")


if __name__ == "__main__":
    main()
