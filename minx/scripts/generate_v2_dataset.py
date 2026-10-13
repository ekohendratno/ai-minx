"""
minx - Generator dataset versi 2
Standar baru berdasarkan referensi ROBIN (Instruction Following Indonesia)
dan Text2SQL Indonesia.

Output: data/raw/robin_indonesia.jsonl
        data/raw/text2sql_indonesia.jsonl
        data/raw/coding_mixed_lang.jsonl
"""

import json
import os
import random

OUT_DIR = "data/raw"
os.makedirs(OUT_DIR, exist_ok=True)

# =============================================================
# ROBIN STYLE: Instruksi campur Indonesia & Inggris (formal, sopan, langsung)
# =============================================================
robin_style = [
    ("Tolong buatkan function untuk menghitung faktorial di javascript",
     """function factorial(n) {
    if (n < 0) return undefined;
    if (n === 0 || n === 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

console.log(factorial(5)); // 120
"""),
    ("Bisa bantu bikin REST API CRUD sederhana pakai PHP native?",
     """<?php
header('Content-Type: application/json');
$pdo = new PDO('mysql:host=localhost;dbname=test', 'root', '');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$method = $_SERVER['REQUEST_METHOD'];
$id = $_GET['id'] ?? null;

switch ($method) {
    case 'GET':
        $stmt = $id ? $pdo->prepare('SELECT * FROM users WHERE id = ?') : $pdo->query('SELECT * FROM users');
        if ($id) $stmt->execute([$id]);
        echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
        break;
    case 'POST':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $pdo->prepare('INSERT INTO users (name, email) VALUES (?, ?)');
        $stmt->execute([$data['name'], $data['email']]);
        echo json_encode(['id' => $pdo->lastInsertId()]);
        break;
    case 'PUT':
        parse_str(file_get_contents('php://input'), $data);
        $stmt = $pdo->prepare('UPDATE users SET name = ?, email = ? WHERE id = ?');
        $stmt->execute([$data['name'], $data['email'], $id]);
        echo json_encode(['affected' => $stmt->rowCount()]);
        break;
    case 'DELETE':
        $stmt = $pdo->prepare('DELETE FROM users WHERE id = ?');
        $stmt->execute([$id]);
        echo json_encode(['deleted' => $stmt->rowCount()]);
        break;
}
?>"""),
    ("Halo minx, tolong dong kasih saya snippet code Flutter widget buat Bottom Navigation Bar",
     """import 'package:flutter/material.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});
  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _index = 0;
  final _pages = const [HomeView(), SearchView(), ProfileView()];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.search), label: 'Search'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}"""),
    ("Buatkan cara validasi form realtime pakai react hooks, dong",
     """import { useState } from 'react';

function useFormValidation(initialState, validate) {
    const [values, setValues] = useState(initialState);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setValues({ ...values, [name]: value });
        if (touched[name]) {
            setErrors({ ...errors, [name]: validate(name, value) });
        }
    };

    const handleBlur = (e) => {
        const { name } = e.target;
        setTouched({ ...touched, [name]: true });
        setErrors({ ...errors, [name]: validate(name, values[name]) });
    };

    return { values, errors, touched, handleChange, handleBlur };
}

// Usage:
const { values, errors, touched, handleChange, handleBlur } = useFormValidation(
    { email: '', password: '' },
    (name, value) => {
        if (name === 'email' && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(value)) return 'Email invalid';
        if (name === 'password' && value.length < 8) return 'Min 8 karakter';
        return '';
    }
);"""),
]

# =============================================================
# Indonesian Text-to-SQL: 30 contoh query dari bahasa natural
# =============================================================
text2sql = [
    ("Tampilkan semua data siswa",
     "SELECT * FROM siswa;"),
    ("Tampilkan 10 siswa dengan nilai tertinggi",
     "SELECT * FROM siswa ORDER BY nilai DESC LIMIT 10;"),
    ("Tampilkan nama siswa yang aktif",
     "SELECT nama FROM siswa WHERE status = 'aktif';"),
    ("Berapa jumlah total siswa?",
     "SELECT COUNT(*) AS total_siswa FROM siswa;"),
    ("Tampilkan siswa dari kelas 10A",
     "SELECT * FROM siswa WHERE kelas = '10A';"),
    ("Tampilkan rata-rata nilai per kelas",
     "SELECT kelas, AVG(nilai) AS rata_rata FROM siswa GROUP BY kelas;"),
    ("Siswa apa saja yang nilainya di atas 80?",
     "SELECT * FROM siswa WHERE nilai > 80;"),
    ("Tampilkan 3 produk termahal",
     "SELECT * FROM produk ORDER BY harga DESC LIMIT 3;"),
    ("Hapus user dengan id 5",
     "DELETE FROM users WHERE id = 5;"),
    ("Update email user dengan id 10 menjadi baru@mail.com",
     "UPDATE users SET email = 'baru@mail.com' WHERE id = 10;"),
    ("Tampilkan pesanan yang dibuat minggu ini",
     "SELECT * FROM pesanan WHERE tanggal >= DATE_SUB(NOW(), INTERVAL 7 DAY);"),
    ("Tampilkan produk yang stoknya kurang dari 10",
     "SELECT * FROM produk WHERE stok < 10;"),
    ("Siswa yang nilai matematika di atas 75 dan bahasa Indonesia di atas 80",
     "SELECT * FROM siswa WHERE matematika > 75 AND bahasa_indonesia > 80;"),
    ("Tampilkan pesanan dengan total lebih dari 100000 diurutkan dari yang terbaru",
     "SELECT * FROM pesanan WHERE total > 100000 ORDER BY tanggal DESC;"),
    ("Hitung total penjualan per kategori produk",
     "SELECT kategori, SUM(total) AS total_penjualan FROM pesanan GROUP BY kategori;"),
    ("Tampilkan produk yang paling laris (paling banyak dipesan)",
     "SELECT produk_id, COUNT(*) AS jumlah FROM pesanan_detail GROUP BY produk_id ORDER BY jumlah DESC;"),
    ("Tampilkan customer yang pernah belanja lebih dari 5 kali",
     "SELECT customer_id, COUNT(*) AS jumlah_transaksi FROM pesanan GROUP BY customer_id HAVING COUNT(*) > 5;"),
    ("Gabungkan data siswa dengan data kelasnya",
     "SELECT s.*, k.nama_kelas FROM siswa s JOIN kelas k ON s.kelas_id = k.id;"),
    ("Tampilkan nama siswa dan nilai rata-rata dari semua mata pelajaran",
     "SELECT s.nama, AVG(n.nilai) AS rata_rata FROM siswa s JOIN nilai n ON s.id = n.siswa_id GROUP BY s.id;"),
    ("Tampilkan artikel yang dipublikasikan bulan ini",
     "SELECT * FROM artikel WHERE MONTH(tanggal_publikasi) = MONTH(CURDATE()) AND YEAR(tanggal_publikasi) = YEAR(CURDATE());"),
    ("Insert data karyawan baru: nama Andi, gaji 5000000",
     "INSERT INTO karyawan (nama, gaji) VALUES ('Andi', 5000000);"),
    ("Hapus semua log yang lebih lama dari 30 hari",
     "DELETE FROM logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);"),
    ("Tampilkan user yang login dalam 24 jam terakhir",
     "SELECT * FROM users WHERE last_login >= DATE_SUB(NOW(), INTERVAL 1 DAY);"),
    ("Hitung total revenue bulan ini",
     "SELECT SUM(total) AS revenue FROM pesanan WHERE MONTH(tanggal) = MONTH(CURDATE());"),
    ("Tampilkan produk yang belum pernah dipesan",
     "SELECT * FROM produk WHERE id NOT IN (SELECT DISTINCT produk_id FROM pesanan_detail);"),
    ("Update stok produk berkurang 1 untuk produk dengan id 7",
     "UPDATE produk SET stok = stok - 1 WHERE id = 7;"),
    ("Tampilkan 5 customer dengan total belanja terbesar",
     "SELECT customer_id, SUM(total) AS total_belanja FROM pesanan GROUP BY customer_id ORDER BY total_belanja DESC LIMIT 5;"),
    ("Tampilkan jumlah siswa per jenis kelamin",
     "SELECT jenis_kelamin, COUNT(*) AS jumlah FROM siswa GROUP BY jenis_kelamin;"),
    ("Tampilkan transaksi dengan status pending yang lebih dari 1 hari",
     "SELECT * FROM pesanan WHERE status = 'pending' AND tanggal < DATE_SUB(NOW(), INTERVAL 1 DAY);"),
    ("Cari user dengan nama mengandung 'budi'",
     "SELECT * FROM users WHERE nama LIKE '%budi%';"),
]

# =============================================================
# Coding campur bahasa Indonesia-Inggris ala ROBIN
# =============================================================
coding_mixed = [
    ("Maksud saya gimana caranya handle error try catch di python",
     """try:
    result = divide(10, 0)
except ZeroDivisionError:
    print("Tidak bisa bagi dengan nol")
except Exception as e:
    print(f"Error: {e}")
else:
    print(f"Hasil: {result}")
finally:
    print("Selesai")
"""),
    ("Kalau mau bikin object oriented programming di PHP gimana caranya",
     """<?php
class User {
    private string $name;
    private string $email;

    public function __construct(string $name, string $email) {
        $this->name = $name;
        $this->email = $email;
    }

    public function getName(): string { return $this->name; }
    public function getEmail(): string { return $this->email; }

    public function toArray(): array {
        return ['name' => $this->name, 'email' => $this->email];
    }
}

$user = new User('Budi', 'budi@mail.com');
print_r($user->toArray());
?>"""),
    ("Tolong jelasin asynchronous programming dong",
     """Asynchronous programming memungkinkan kode berjalan tanpa menunggu operasi lain selesai. Contoh di JavaScript:

// Synchronous: nunggu satu per satu
console.log('1');
console.log('2');
console.log('3');

// Asynchronous: tidak blocking
console.log('1');
setTimeout(() => console.log('2'), 1000);  // delay 1 detik
console.log('3');
// Output: 1, 3, 2 (karena 2 delay)

// Dengan Promise
fetch('/api/users')
    .then(res => res.json())
    .then(data => console.log(data));

// Dengan async/await (lebih readable)
async function getUsers() {
    try {
        const res = await fetch('/api/users');
        const data = await res.json();
        return data;
    } catch (err) {
        console.error('Error:', err);
    }
}
"""),
    ("Buatkan Laravel controller sederhana dong",
     """<?php

namespace App\\Http\\Controllers;

use App\\Models\\Product;
use Illuminate\\Http\\Request;

class ProductController extends Controller
{
    public function index()
    {
        $products = Product::all();
        return response()->json($products);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name'  => 'required|string|max:255',
            'price' => 'required|numeric|min:0',
        ]);

        $product = Product::create($validated);
        return response()->json($product, 201);
    }

    public function show($id)
    {
        $product = Product::findOrFail($id);
        return response()->json($product);
    }

    public function update(Request $request, $id)
    {
        $product = Product::findOrFail($id);
        $product->update($request->all());
        return response()->json($product);
    }

    public function destroy($id)
    {
        Product::destroy($id);
        return response()->json(null, 204);
    }
}
"""),
    ("Gimana cara bikin responsive design pakai CSS Grid?",
     """.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    padding: 1rem;
}

.grid-item {
    background: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Untuk mobile */
@media (max-width: 600px) {
    .grid-container {
        grid-template-columns: 1fr;
    }
}

/* Untuk tablet */
@media (min-width: 601px) and (max-width: 1024px) {
    .grid-container {
        grid-template-columns: repeat(2, 1fr);
    }
}"""),
]

# Simpan semua ke file
def write_jsonl(filename, data):
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"  {filename}: {len(data)} contoh")

write_jsonl('robin_indonesia.jsonl', robin_style)
write_jsonl('text2sql_indonesia.jsonl', text2sql)
write_jsonl('coding_mixed_lang.jsonl', coding_mixed)

print(f"\nTotal: {len(robin_style) + len(text2sql) + len(coding_mixed)} contoh baru")
