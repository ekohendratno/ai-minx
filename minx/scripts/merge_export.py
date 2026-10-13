"""
minx - Step 4: Merge LoRA & Export Model
Gabungkan adapter LoRA ke base model, lalu export sebagai model lengkap.

```
python scripts/merge_export.py
```

Output: models/minx-merged/ (HuggingFace model)
"""

import os
import sys
import yaml
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

DEFAULT_OUTPUT = "models/minx-merged"
DEFAULT_LORA_DIR = "models/minx-lora"
DEFAULT_BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


def load_config():
    """Muat config, fallback ke default."""
    path = "configs/train_config.yaml"
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            pass
    return {}


def main():
    print("=" * 60)
    print("minx - Step 4: Merge LoRA & Export")
    print("=" * 60)

    # Cek file adanya
    lora_dir = DEFAULT_LORA_DIR
    output_dir = DEFAULT_OUTPUT
    base_model = DEFAULT_BASE_MODEL

    cfg = load_config()
    if cfg:
        base_model = cfg.get('base_model', base_model)
        lora_dir = cfg.get('training', {}).get('output_dir', lora_dir)
        output_dir = cfg.get('export', {}).get('output_dir', output_dir)

    # Cek adapter exists
    if not os.path.isdir(lora_dir):
        print(f"[ERROR] LoRA adapter tidak ditemukan: {lora_dir}")
        print("[INFO] Jalankan dulu: python scripts/train_lora.py")
        sys.exit(1)

    adapter_config = os.path.join(lora_dir, "adapter_config.json")
    if not os.path.exists(adapter_config):
        print(f"[ERROR] adapter_config.json tidak ada di {lora_dir}")
        print("[INFO] Jalankan dulu: python scripts/train_lora.py")
        sys.exit(1)

    print(f"\n[1] Base model : {base_model}")
    print(f"    LoRA dir   : {lora_dir}")
    print(f"    Output dir : {output_dir}")

    # ---- Cek GPU ----
    if torch.cuda.is_available():
        device_map = "auto"
        dtype = torch.float16
        print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")
    else:
        device_map = "cpu"
        dtype = torch.float32
        print("[INFO] CPU mode")

    # ---- Load base model ----
    print(f"\n[2] Load base model: {base_model}")
    base_model_obj = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        device_map=device_map,
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token

    # ---- Load & apply LoRA ----
    print("[3] Load LoRA adapter...")
    try:
        from peft import PeftModel
    except ImportError:
        print("[ERROR] peft belum terinstall.")
        print("       Jalankan: pip install peft")
        sys.exit(1)

    lora_model = PeftModel.from_pretrained(
        base_model_obj,
        lora_dir,
    )

    # ---- Merge weights ----
    print("[4] Merge LoRA weights ke base model...")
    merged_model = lora_model.merge_and_unload()

    # ---- Save merged model ----
    print(f"[5] Simpan merged model ke: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    merged_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    # ---- Verifikasi ----
    size_mb = sum(
        os.path.getsize(os.path.join(output_dir, f))
        for f in os.listdir(output_dir)
        if os.path.isfile(os.path.join(output_dir, f))
    ) / 1024 / 1024

    print(f"\n[6] Selesai!")
    print(f"    Ukuran merged model: {size_mb:.1f} MB")
    print(f"    Lokasi: {output_dir}")
    print(f"    Files: {os.listdir(output_dir)}")
    print("\nLanjut ke Step 5: quantize.py")


if __name__ == "__main__":
    main()
