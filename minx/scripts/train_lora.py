"""
minx - Step 3: Fine-tuning dengan LoRA
Train model coding web+mobile pada laptop RAM 4GB (CPU-only).

```
python scripts/train_lora.py
```

Output: models/minx-lora/ (adapter LoRA)
"""

import os
import sys
import time
import psutil
import torch
import yaml
from datasets import load_dataset

# ---- Fallback config jika pysaml belum ada ----
DEFAULT_CONFIG = {
    "base_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "dataset_path": "data/processed/minx_train.jsonl",
    "max_seq_length": 512,
    "lora": {
        "r": 16,
        "alpha": 32,
        "dropout": 0.05,
        "bias": "none",
        "task_type": "CAUSAL_LM",
        "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj",
                           "gate_proj", "up_proj", "down_proj"]
    },
    "training": {
        "output_dir": "models/minx-lora",
        "num_train_epochs": 2,
        "per_device_train_batch_size": 1,
        "gradient_accumulation_steps": 8,
        "learning_rate": 2e-4,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.05,
        "weight_decay": 0.01,
        "save_steps": 100,
        "save_total_limit": 2,
        "report_to": []
    },
    "optimization": {
        "max_threads": 2,
        "block_size": 128,
        "gradient_checkpointing": True,
        "max_memory_cpu": "2GB"
    }
}


def load_config(path="configs/train_config.yaml"):
    """Muat config dari YAML, fallback ke default."""
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                loaded = yaml.safe_load(f)
            # Merge dengan default
            cfg = DEFAULT_CONFIG
            cfg.update(loaded)
            for section in ['lora', 'training', 'optimization']:
                if section in loaded:
                    cfg[section].update(loaded[section])
            return cfg
        except Exception as e:
            print(f"[warning] Gagal load config {path}: {e}")
            print("[warning] Pakai config default")
    return DEFAULT_CONFIG


def report_ram(stage):
    """Laporkan penggunaan RAM saat ini."""
    mem = psutil.virtual_memory()
    proc = psutil.Process(os.getpid())
    rss = proc.memory_info().rss / 1024 / 1024
    print(f"[RAM] {stage}: {rss:.0f} MB (proses) | "
          f"{mem.used/1024/1024/1024:.1f}/{mem.total/1024/1024/1024:.1f} GB (sistem)")


def prepare_dataset(cfg):
    """Muat dataset JSONL dan format untuk fine-tuning chat."""
    ds_path = cfg['dataset_path']
    print(f"[2] Muat dataset: {ds_path}")

    if not os.path.exists(ds_path):
        print(f"[ERROR] Dataset tidak ditemukan: {ds_path}")
        print("[INFO] Jalankan dulu: python scripts/prepare_dataset.py")
        sys.exit(1)

    dataset = load_dataset(
        'json',
        data_files=ds_path,
        split='train'
    )
    print(f"    Total contoh: {len(dataset)}")
    return dataset


def main():
    print("=" * 60)
    print("minx - Step 3: LoRA Fine-tuning")
    print("      Target: Laptop RAM 4GB, CPU-only")
    print("=" * 60)

    # ---- Cek environment ----
    if not torch.cuda.is_available():
        print("[INFO] GPU tidak tersedia -> mode CPU")
        device = "cpu"
    else:
        print(f"[INFO] GPU tersedia: {torch.cuda.get_device_name(0)}")
        device = "cuda"

    report_ram("start")

    # ---- Load config ----
    cfg = load_config()
    base_model_name = cfg['base_model']
    print(f"\n[1] Base model: {base_model_name}")

    # ---- Import berat (lambat, import setelah env check) ----
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        TrainingArguments,
        Trainer,
    )
    from peft import (
        LoraConfig,
        get_peft_model,
        prepare_model_for_kbit_training,
    )

    # ---- Load dataset ----
    dataset = prepare_dataset(cfg)

    # ---- Load tokenizer ----
    print(f"\n[4] Load tokenizer: {base_model_name}")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # ---- Format chat ----
    print(f"[3] Format dataset untuk chat fine-tuning...")

    def format_chat(examples):
        prompts = []
        for msg in examples['messages']:
            user_msg = next((m['content'] for m in msg if m['role'] == 'user'), '')
            asst_msg = next((m['content'] for m in msg if m['role'] == 'assistant'), '')
            
            # Gunakan template bawaan model (kalau ada)
            conv = [
                {"role": "system", "content": "Anda adalah minx, asisten coding pintar berbahasa Indonesia."},
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": asst_msg}
            ]
            try:
                text = tokenizer.apply_chat_template(conv, tokenize=False)
            except Exception:
                text = (
                    f"<|im_start|>system\nAnda adalah minx, asisten coding pintar berbahasa Indonesia.<|im_end|>\n"
                    f"<|im_start|>user\n{user_msg}<|im_end|>\n"
                    f"<|im_start|>assistant\n{asst_msg}<|im_end|>\n"
                )
            prompts.append(text)
        return {"text": prompts}

    dataset = dataset.map(
        format_chat,
        batched=True,
        remove_columns=dataset.column_names,
    )

    # ---- Load model 4-bit (QLoRA) ----
    print(f"[5] Load model {base_model_name} (4-bit quantized)...")
    report_ram("sebelum load model")

    quant_config = None
    if device == "cpu":
        # CPU mode: load fp16/bf16 penuh, kecilkan memory
        model_kwargs = {
            "torch_dtype": torch.float32,
            "low_cpu_mem_usage": True,
        }
    else:
        # GPU mode: 4-bit QLoRA
        from transformers import BitsAndBytesConfig
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        model_kwargs = {
            "quantization_config": quant_config,
            "torch_dtype": torch.float16,
        }

    try:
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            device_map="auto",
            **model_kwargs,
        )
    except MemoryError as e:
        print(f"[ERROR] OOM saat load model: {e}")
        print("[SOLUSI]")
        print("  1. Tutup aplikasi lain")
        print("  2. Gunakan model lebih kecil (Qwen/Qwen2.5-0.5B-Instruct)")
        print("  3. Edit configs/train_config.yaml -> ganti base_model")
        sys.exit(1)

    report_ram("setelah load model")

    if device == "cpu":
        # Non-active: gcd only untuk CPU (sering gagal di Windows)
        print("[INFO] Mode CPU: nonaktifkan 4-bit, pakai float32")
    else:
        model = prepare_model_for_kbit_training(model)

    # ---- Setup LoRA ----
    print(f"\n[6] Setup LoRA (r={cfg['lora']['r']})...")
    lora_cfg = LoraConfig(
        r=cfg['lora']['r'],
        lora_alpha=cfg['lora']['alpha'],
        lora_dropout=cfg['lora']['dropout'],
        bias=cfg['lora']['bias'],
        task_type=cfg['lora']['task_type'],
        target_modules=cfg['lora']['target_modules'],
    )
    model = get_peft_model(model, lora_cfg)

    # ---- Tokenize dataset ----
    print(f"[7] Tokenize dataset (max_seq_length={cfg['max_seq_length']})...")

    def tokenize_function(examples):
        outputs = tokenizer(
            examples["text"],
            truncation=True,
            max_length=cfg['max_seq_length'],
            padding=False,
        )
        outputs["labels"] = [ids.copy() for ids in outputs["input_ids"]]
        return outputs

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names,
    )

    train_test = tokenized_dataset.train_test_split(
        test_size=0.05,
        seed=42,
    )
    train_ds = train_test['train']
    eval_ds = train_test['test']
    print(f"    Train: {len(train_ds)} | Eval: {len(eval_ds)}")

    # ---- Set torch threads (kecilkan utk hemat CPU/RAM) ----
    max_threads = cfg['optimization']['max_threads']
    torch.set_num_threads(max_threads)
    print(f"[8] Threads model: {max_threads}")

    # ---- Training arguments ----
    t = cfg['training']
    # Pastikan numerik (YAML kadang baca sebagai string)
    t['learning_rate'] = float(t['learning_rate'])
    t['warmup_ratio'] = float(t['warmup_ratio'])
    t['weight_decay'] = float(t['weight_decay'])
    t['max_grad_norm'] = float(t.get('max_grad_norm', 0.3))
    try:
        training_args = TrainingArguments(
            output_dir=t['output_dir'],
            num_train_epochs=t['num_train_epochs'],
            per_device_train_batch_size=t['per_device_train_batch_size'],
            gradient_accumulation_steps=t['gradient_accumulation_steps'],
            learning_rate=t['learning_rate'],
            lr_scheduler_type=t['lr_scheduler_type'],
            warmup_ratio=t['warmup_ratio'],
            weight_decay=t['weight_decay'],
            logging_steps=t['logging_steps'],
            save_steps=t['save_steps'],
            save_total_limit=t['save_total_limit'],
            report_to=t['report_to'],
            eval_strategy="steps",
            eval_steps=50,
            fp16=False,
            bf16=False,
            dataloader_pin_memory=False,
            optim="adamw_torch",
            max_grad_norm=0.3,
        )
    except TypeError:
        warmup_steps = int(len(train_ds) * t['warmup_ratio'])
        training_args = TrainingArguments(
            output_dir=t['output_dir'],
            num_train_epochs=t['num_train_epochs'],
            per_device_train_batch_size=t['per_device_train_batch_size'],
            gradient_accumulation_steps=t['gradient_accumulation_steps'],
            learning_rate=t['learning_rate'],
            lr_scheduler_type=t['lr_scheduler_type'],
            warmup_steps=warmup_steps,
            weight_decay=t['weight_decay'],
            logging_steps=t['logging_steps'],
            save_steps=t['save_steps'],
            save_total_limit=t['save_total_limit'],
            eval_strategy="steps",
            eval_steps=50,
            fp16=False,
            bf16=False,
            dataloader_pin_memory=False,
            optim="adamw_torch",
            max_grad_norm=0.3,
        )

    # ---- Trainer ----
    try:
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
            processing_class=tokenizer,
        )
    except TypeError:
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
        )

    # ---- START TRAINING ----
    print("\n" + "=" * 60)
    print("[9] MULAI TRAINING (harap sabar, CPU lambat)...")
    print("=" * 60)
    print(f"    Waktu mulai: {time.strftime('%H:%M:%S')}")
    print(f"    Estimated time: {len(train_ds) * 60} detik (1 sampel ~ 60s utk 1B)")

    start = time.time()
    try:
        trainer.train()
    except MemoryError:
        print("\n[ERROR] OOM selama training.")
        print("[SOLUSI]")
        print("  1. Tutup semua aplikasi lain")
        print("  2. Kurangi gradient_accumulation_steps di config")
        print("  3. Gunakan dataset lebih kecil (edit prepare_dataset.py)")
        print("  4. Ganti base model lebih kecil (Qwen-0.5B)")
        sys.exit(1)

    elapsed = time.time() - start
    print(f"\n[10] Training selesai dalam {elapsed/60:.1f} menit")

    # ---- Save adapter ----
    lora_dir = t['output_dir']
    print(f"[11] Simpan LoRA adapter ke: {lora_dir}")
    os.makedirs(lora_dir, exist_ok=True)
    model.save_pretrained(lora_dir)
    tokenizer.save_pretrained(lora_dir)
    print("    Adapter tersimpan.")

    report_ram("selesai")
    print("\nSelesai! Lanjut ke Step 4: merge_export.py")


if __name__ == "__main__":
    main()
