"""
minx - Step 6: Test Model
Uji model minx (GGUF atau HuggingFace) untuk coding web+mobile.

```
python scripts/test.py
```

Test akan mengukur:
- RAM usage
- Tokens per second
- Kualitas jawaban
"""

import os
import sys
import time
import psutil
import torch
from datetime import datetime

# ============ Test Prompts ============

TEST_CASES = [
    {
        "category": "HTML",
        "prompt": "Buatkan HTML form pendaftaran sederhana",
        "keywords": ["<form", "<input", "<label", "submit"],
    },
    {
        "category": "CSS",
        "prompt": "Buatkan CSS flexbox untuk navbar",
        "keywords": ["display", "flex", "justify-content", "align-items"],
    },
    {
        "category": "JavaScript",
        "prompt": "Buatkan function JavaScript untuk fetch data dari API",
        "keywords": ["fetch", "async", "await", "response"],
    },
    {
        "category": "React",
        "prompt": "Buatkan React component untuk button counter",
        "keywords": ["useState", "onClick", "return", "className"],
    },
    {
        "category": "Flutter",
        "prompt": "Buatkan widget Flutter untuk card menu",
        "keywords": ["StatelessWidget", "build", "Card", "column"],
    },
    {
        "category": "React Native",
        "prompt": "Buatkan screen login dengan React Native",
        "keywords": ["useState", "TextInput", "TouchableOpacity", "StyleSheet"],
    },
    {
        "category": "HTML",
        "prompt": "Buatkan form login responsif dengan HTML & CSS",
        "keywords": ["form", "input", "login", "responsive"],
    },
    {
        "category": "JavaScript",
        "prompt": "Cara buat async function di JavaScript",
        "keywords": ["async", "function", "promise", "await"],
    },
    {
        "category": "Debug",
        "prompt": "Kenapa useState saya tidak update value?",
        "keywords": ["setState", "functional update", "immutable", "closure"],
    },
    {
        "category": "Architecture",
        "prompt": "Apa perbedaan REST API dan GraphQL?",
        "keywords": ["REST", "GraphQL", "endpoint", "query"],
    },
]


def get_ram_usage():
    """Dapatkan RAM usage MB."""
    proc = psutil.Process(os.getpid())
    return proc.memory_info().rss / 1024 / 1024


def get_system_ram():
    """Info RAM sistem."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total / 1024 / 1024 / 1024,
        "used": mem.used / 1024 / 1024 / 1024,
        "free": mem.available / 1024 / 1024 / 1024,
        "percent": mem.percent,
    }


def check_answer(prompt, response, keywords):
    """Cek apakah jawaban mengandung keyword-keyword."""
    response_lower = response.lower()
    hits = []
    misses = []
    for kw in keywords:
        if kw.lower() in response_lower:
            hits.append(kw)
        else:
            misses.append(kw)

    score = len(hits) / len(keywords) * 100 if keywords else 0
    return score, hits, misses


def test_with_hf_model(model_name, cases):
    """Test menggunakan HuggingFace transformers."""
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    if torch.cuda.is_available():
        device_map = "auto"
        dtype = torch.float16
        device_name = torch.cuda.get_device_name(0)
    else:
        device_map = "cpu"
        dtype = torch.float32
        device_name = "CPU"

    print(f"  Device : {device_name}")
    print(f"  Model  : {model_name}")

    ram_before = get_ram_usage()
    sys_ram_before = get_system_ram()
    print(f"\n  [Load model]")
    start = time.time()

    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
            device_map=device_map,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except MemoryError:
        print("[ERROR] OOM - model terlalu besar untuk RAM tersedia")
        print("[SOLUSI] Tutup aplikasi lain atau gunakan model lebih kecil")
        return None

    load_time = time.time() - start
    ram_after = get_ram_usage()
    sys_ram_after = get_system_ram()

    print(f"  Waktu load : {load_time:.1f}s")
    print(f"  RAM proses : {ram_before:.0f}MB -> {ram_after:.0f}MB (+{ram_after-ram_before:.0f}MB)")
    print(f"  RAM sistem : {sys_ram_before['used']:.1f}/{sys_ram_before['total']:.1f}GB "
          f"({sys_ram_before['percent']}%)")

    print(f"\n  [Inference test] ({len(cases)} test cases)")
    results = []
    total_tokens = 0
    total_inference_time = 0

    for i, case in enumerate(cases, 1):
        print(f"\n  Test {i}: {case['category']}")
        print(f"  Prompt: {case['prompt'][:80]}...")

        messages = [
            {"role": "system", "content": "Anda adalah minx, asisten coding untuk pemrograman web dan aplikasi mobile. Berikan jawaban dalam kode yang dapat langsung digunakan."},
            {"role": "user", "content": case['prompt']},
        ]

        # Format chat
        try:
            text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        except Exception:
            text = f"### Instruction:\n{case['prompt']}\n### Response:\n"

        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)

        start = time.time()
        try:
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                )
        except MemoryError:
            print("[ERROR] OOM saat inference")
            results.append({"category": case['category'], "score": 0, "tokens_per_sec": 0})
            continue

        inference_time = time.time() - start
        response_ids = outputs[0][inputs['input_ids'].shape[-1]:]
        response = tokenizer.decode(response_ids, skip_special_tokens=True)
        response_len = len(response_ids)

        tokens_per_sec = response_len / inference_time if inference_time > 0 else 0
        total_tokens += response_len
        total_inference_time += inference_time

        # Skor kualitas
        score, hits, misses = check_answer(case['prompt'], response, case['keywords'])
        print(f"  Tokens    : {response_len} ({tokens_per_sec:.1f} tok/s)")
        print(f"  Score     : {score:.0f}% ({len(hits)}/{len(case['keywords'])} keyword)")
        if misses:
            print(f"  Missing   : {', '.join(misses)}")

        results.append({
            "category": case['category'],
            "score": score,
            "tokens_per_sec": tokens_per_sec,
        })

    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN TEST")
    print("=" * 60)
    print(f"  Total test     : {len(results)}")
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    avg_tps = sum(r['tokens_per_sec'] for r in results) / len(results) if results else 0
    print(f"  Skor rata-rata : {avg_score:.1f}%")
    print(f"  Tokens/second  : {avg_tps:.1f}")

    # Distribusi per kategori
    categories = {}
    for r in results:
        cat = r['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    print(f"\n  Per kategori:")
    for cat, cat_results in categories.items():
        cat_avg = sum(r['score'] for r in cat_results) / len(cat_results)
        cat_tps = sum(r['tokens_per_sec'] for r in cat_results) / len(cat_results)
        print(f"    {cat:20s}: score {cat_avg:5.1f}% | {cat_tps:.1f} tok/s")

    # Verdict
    print()
    if avg_score >= 80:
        print("  ✅ VERDICT: BAGUS - model cukup memahami coding web+mobile")
    elif avg_score >= 60:
        print("  ⚠️  VERDICT: CUKUP - model dasar memahami, perlu lebih banyak training")
    elif avg_score >= 40:
        print("  ⚠️  VERDICT: LEMAH - jawaban ada tapi kurang tepat")
    else:
        print("  ❌ VERDICT: GAGAL - perlu perbaikan signifikan")

    return results


def test_with_gguf(model_path, cases):
    """Test menggunakan llama-cpp-python."""
    try:
        from llama_cpp import Llama
    except ImportError:
        print("[ERROR] llama-cpp-python belum terinstall.")
        print("       Jalankan: pip install llama-cpp-python")
        return None

    if not os.path.exists(model_path):
        print(f"[ERROR] GGUF model tidak ditemukan: {model_path}")
        print("[INFO] Jalankan dulu: python scripts/quantize.py")
        return None

    print(f"  Device : CPU (llama.cpp)")
    print(f"  Model  : {model_path}")

    ram_before = get_ram_usage()

    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=2,  # kecil hemat RAM
            verbose=False,
        )
    except MemoryError:
        print("[ERROR] OOM saat load GGUF model")
        return None

    ram_after = get_ram_usage()

    print(f"  RAM load : {ram_before:.0f}MB -> {ram_after:.0f}MB (+{ram_after-ram_before:.0f}MB)")
    print(f"\n  [Inference test] ({len(cases)} test cases)")

    results = []
    total_tokens = 0
    total_inference_time = 0

    for i, case in enumerate(cases, 1):
        print(f"\n  Test {i}: {case['category']}")
        print(f"  Prompt: {case['prompt'][:80]}...")

        prompt = (
            f"### Instruction:\n{case['prompt']}\n\n"
            f"### Response:\n"
        )

        start = time.time()
        try:
            output = llm(
                prompt,
                max_tokens=256,
                temperature=0.7,
                top_p=0.9,
                repeat_penalty=1.1,
                stop=["###", "### Instruction"],
            )
        except Exception as e:
            print(f"[ERROR] Inference gagal: {e}")
            results.append({"category": case['category'], "score": 0, "tokens_per_sec": 0})
            continue

        inference_time = time.time() - start
        response = output['choices'][0]['text']
        tokens_per_sec = output['usage']['completion_tokens'] / inference_time if inference_time > 0 else 0
        total_tokens += output['usage']['completion_tokens']
        total_inference_time += inference_time

        score, hits, misses = check_answer(case['prompt'], response, case['keywords'])
        print(f"  Tokens    : {output['usage']['completion_tokens']} ({tokens_per_sec:.1f} tok/s)")
        print(f"  Score     : {score:.0f}% ({len(hits)}/{len(case['keywords'])} keyword)")
        if misses:
            print(f"  Missing   : {', '.join(misses)}")

        results.append({
            "category": case['category'],
            "score": score,
            "tokens_per_sec": tokens_per_sec,
        })

    # Ringkasan
    print("\n" + "=" * 60)
    print("RINGKASAN TEST (GGUF)")
    print("=" * 60)
    print(f"  Total test     : {len(results)}")
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    avg_tps = sum(r['tokens_per_sec'] for r in results) / len(results) if results else 0
    print(f"  Skor rata-rata : {avg_score:.1f}%")
    print(f"  Tokens/second  : {avg_tps:.1f}")

    return results


def main():
    print("=" * 60)
    print("minx - Step 6: Test Model")
    print("=" * 60)

    # Determine model path
    gguf_path = "models/minx-gguf/minx-q4_k_m.gguf"
    hf_path = "models/minx-merged"

    use_gguf = False
    use_hf = False

    if os.path.exists(gguf_path):
        print(f"[INFO] Ditemukan GGUF model: {gguf_path}")
        print("       Menggunakan llama-cpp-python untuk test")
        use_gguf = True
    elif os.path.isdir(hf_path):
        print(f"[INFO] Ditemukan HuggingFace model: {hf_path}")
        print("       Menggunakan transformers untuk test")
        use_hf = True
    else:
        print("[INFO] Tidak ada model yang ditemukan.")
        print("       Jalankan dulu salah satu:")
        print("         Step 4: python scripts/merge_export.py")
        print("         Step 5: python scripts/quantize.py")
        print()
        print("       Atau download model TinyLlama untuk test cepat...")
        use_hf = True
        hf_path = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        print(f"       Test dengan base model: {hf_path}")

    print(f"\n  Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sys_ram = get_system_ram()
    print(f"  RAM sistem: {sys_ram['free']:.1f}GB tersisa dari {sys_ram['total']:.1f}GB")

    if use_gguf:
        results = test_with_gguf(gguf_path, TEST_CASES)
    else:
        results = test_with_hf_model(hf_path, TEST_CASES)

    if results:
        print("\n" + "=" * 60)
        print("TEST SELESAI")
        print("=" * 60)


if __name__ == "__main__":
    main()
