import json
import time
import requests

# Test suite untuk menguji kemampuan minx (Qwen2.5-1.5B via Ollama)
test_questions = [
    {
        "id": 1,
        "category": "Identitas & Bahasa Indonesia",
        "prompt": "Siapa kamu dan apa keahlian utamamu?"
    },
    {
        "id": 2,
        "category": "HTML / CSS",
        "prompt": "Buatkan CSS flexbox untuk membuat card produk yang responsif lengkap dengan efek hover."
    },
    {
        "id": 3,
        "category": "JavaScript Modern",
        "prompt": "Bagaimana cara melakukan fetch data dari API publik menggunakan async/await di JavaScript dan menangani error-nya?"
    },
    {
        "id": 4,
        "category": "Backend PHP / MySQL",
        "prompt": "Buatkan script PHP PDO aman untuk menyimpan data user (nama, email, password terenkripsi) ke database MySQL."
    },
    {
        "id": 5,
        "category": "Mobile Dev (Flutter / React Native)",
        "prompt": "Buatkan komponen/widget form login sederhana dengan validasi input untuk Flutter atau React Native."
    },
    {
        "id": 6,
        "category": "Penalaran & Debugging Kode",
        "prompt": "Jelaskan mengapa kode JavaScript ini bisa error dan berikan solusinya:\nconst users = [];\nusers.forEach(async (u) => await fetch(u.url));\nconsole.log('Selesai');"
    }
]

print("==================================================")
print("MINX COMPREHENSIVE BENCHMARK TEST (via Ollama API)")
print("==================================================\n")

total_tokens = 0
total_time = 0

for test in test_questions:
    print(f"--- TEST {test['id']}: [{test['category']}] ---")
    print(f"PROMPT: {test['prompt']}\n")
    
    start_time = time.time()
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "minx",
            "prompt": test['prompt'],
            "stream": False
        }, timeout=120)
        
        elapsed = time.time() - start_time
        if res.status_code == 200:
            data = res.json()
            response_text = data.get("response", "")
            eval_count = data.get("eval_count", 0)
            eval_duration = data.get("eval_duration", 1) / 1e9
            
            tps = eval_count / eval_duration if eval_duration > 0 else 0
            total_tokens += eval_count
            total_time += elapsed
            
            print("RESPONSE MINX:")
            print(response_text.strip())
            print(f"\n[Metrik: {eval_count} token | {elapsed:.2f}s | Speed: {tps:.1f} tok/s]\n")
        else:
            print(f"ERROR: HTTP {res.status_code}\n")
    except Exception as e:
        print(f"ERROR API: {e}\n")

print("==================================================")
print(f"RINGKASAN BENCHMARK:")
print(f"Total Token Generated : {total_tokens}")
print(f"Total Waktu Response  : {total_time:.2f}s")
if total_time > 0:
    print(f"Rata-rata Kecepatan   : {total_tokens / total_time:.1f} tok/s")
print("==================================================")
