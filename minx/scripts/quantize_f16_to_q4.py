"""
minx - Step 5b: Quantize F16 to Q4_K_M via llama_cpp C API
"""
import os, sys, ctypes
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_EXPORT = {"gguf_dir": "models/minx-gguf", "quant_method": "q4_k_m"}

def load_config():
    path = "configs/train_config.yaml"
    if yaml and os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f).get("export", DEFAULT_EXPORT)
        except Exception:
            pass
    return DEFAULT_EXPORT

def main():
    print("=" * 60)
    print("minx - Quantize F16 ke Q4_K_M")
    print("=" * 60)

    cfg = load_config()
    gguf_dir = Path(cfg.get("gguf_dir", DEFAULT_EXPORT["gguf_dir"]))
    quant_method = cfg.get("quant_method", DEFAULT_EXPORT["quant_method"])
    fp16_file = gguf_dir / "minx-f16.gguf"
    out_file  = gguf_dir / f"minx-{quant_method}.gguf"

    if not fp16_file.exists():
        print(f"[ERROR] File F16 tidak ditemukan: {fp16_file}")
        print("        Jalankan Step 5a terlebih dahulu.")
        sys.exit(1)

    print(f"[1] Input  : {fp16_file} ({os.path.getsize(fp16_file)/1024/1024:.0f} MB)")
    print(f"[2] Output : {out_file}")
    print(f"[3] Method : {quant_method}")

    import llama_cpp
    ftype_map = {
        "q4_0":    llama_cpp.LLAMA_FTYPE_MOSTLY_Q4_0,
        "q4_1":    llama_cpp.LLAMA_FTYPE_MOSTLY_Q4_1,
        "q4_k_s":  llama_cpp.LLAMA_FTYPE_MOSTLY_Q4_K_S,
        "q4_k_m":  llama_cpp.LLAMA_FTYPE_MOSTLY_Q4_K_M,
        "q5_0":    llama_cpp.LLAMA_FTYPE_MOSTLY_Q5_0,
        "q5_1":    llama_cpp.LLAMA_FTYPE_MOSTLY_Q5_1,
        "q5_k_s":  llama_cpp.LLAMA_FTYPE_MOSTLY_Q5_K_S,
        "q5_k_m":  llama_cpp.LLAMA_FTYPE_MOSTLY_Q5_K_M,
        "q6_k":    llama_cpp.LLAMA_FTYPE_MOSTLY_Q6_K,
        "q8_0":    llama_cpp.LLAMA_FTYPE_MOSTLY_Q8_0,
    }

    ftype = ftype_map.get(quant_method.lower())
    if ftype is None:
        print(f"[ERROR] Quant method tidak dikenal: {quant_method}")
        sys.exit(1)

    print(f"[4] FTYPE  : {ftype}")

    params = llama_cpp.llama_model_quantize_default_params()
    print(f"[5] Quantize params: nthread={params.nthread}")

    print("[6] Jalankan quantize (butuh waktu beberapa menit)...")
    c_in  = ctypes.c_char_p(str(fp16_file).encode("utf-8"))
    c_out = ctypes.c_char_p(str(out_file).encode("utf-8"))
    c_ftype = ctypes.c_int(ftype)
    c_params = ctypes.pointer(params)

    result = llama_cpp.llama_model_quantize(c_in, c_out, c_params)

    if result != 0:
        print(f"[ERROR] Quantize gagal dengan kode: {result}")
        sys.exit(1)

    if out_file.exists():
        size_mb = os.path.getsize(out_file) / 1024 / 1024
        print(f"\n[SELESAI] File GGUF Q4_K_M berhasil dibuat!")
        print(f"  File : {out_file}")
        print(f"  Ukuran: {size_mb:.0f} MB")
        print(f"  Hapus F16: {fp16_file}")
        fp16_file.unlink()
        print("\nLangkah selanjutnya: python scripts/test.py")
    else:
        print(f"[ERROR] File output tidak ditemukan: {out_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()
