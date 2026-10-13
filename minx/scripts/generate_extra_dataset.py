"""
minx - Generator dataset tambahan
Tulis contoh coding + Q&A umum ke data/raw/ untuk digabung prepare_dataset.py

Output: data/raw/extra_001.jsonl s/d data/raw/extra_004.jsonl
Total: sekitar 120 contoh (HTML, CSS, JS, PHP, React, Vue, Flutter, RN + Q&A)
"""

import json
import os
import random

OUT_DIR = "data/raw"
os.makedirs(OUT_DIR, exist_ok=True)

# ============================ HTML ============================
html_samples = [
    ("Buatkan halaman HTML contact form lengkap",
     """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kontak Kami</title>
</head>
<body>
    <section class="contact">
        <h1>Hubungi Kami</h1>
        <form action="/submit-contact" method="POST">
            <div>
                <label for="nama">Nama Lengkap</label>
                <input type="text" id="nama" name="nama" placeholder="Nama Anda" required>
            </div>
            <div>
                <label for="email">Email</label>
                <input type="email" id="email" name="email" placeholder="email@contoh.com" required>
            </div>
            <div>
                <label for="subjek">Subjek</label>
                <input type="text" id="subjek" name="subjek" required>
            </div>
            <div>
                <label for="pesan">Pesan</label>
                <textarea id="pesan" name="pesan" rows="5" required></textarea>
            </div>
            <button type="submit">Kirim Pesan</button>
        </form>
    </section>
</body>
</html>"""),

    ("Buatkan tabel data pengguna dengan HTML",
     """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Data Pengguna</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f2f2f2; }
        tr:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Daftar Pengguna</h1>
    <table>
        <thead>
            <tr><th>No</th><th>Nama</th><th>Email</th><th>Role</th></tr>
        </thead>
        <tbody>
            <tr><td>1</td><td>Budi Santoso</td><td>budi@email.com</td><td>Admin</td></tr>
            <tr><td>2</td><td>Siti Aminah</td><td>siti@email.com</td><td>User</td></tr>
            <tr><td>3</td><td>Agus Wijaya</td><td>agus@email.com</td><td>User</td></tr>
        </tbody>
    </table>
</body>
</html>"""),

    ("Buatkan HTML halaman profil dengan avatar dan info pengguna",
     """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profil Pengguna</title>
    <link rel="stylesheet" href="profil.css">
</head>
<body>
    <main class="profile-card">
        <img src="avatar.jpg" alt="Foto Profil" class="avatar">
        <h2>Rina Kartika</h2>
        <p class="bio">Full-stack developer, pecinta teknologi dan kopi.</p>
        <ul class="info">
            <li><strong>Lokasi:</strong> Jakarta, Indonesia</li>
            <li><strong>Website:</strong> rina.dev</li>
            <li><strong>Bergabung:</strong> 2020</li>
        </ul>
        <div class="social">
            <a href="#github">GitHub</a>
            <a href="#linkedin">LinkedIn</a>
            <a href="#twitter">Twitter</a>
        </div>
    </main>
</body>
</html>"""),

    ("Buatkan halaman landing page dengan hero section",
     """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Startup Kami</title>
    <link rel="stylesheet" href="landing.css">
</head>
<body>
    <header class="navbar">
        <div class="logo">StartupKu</div>
        <nav>
            <a href="#fitur">Fitur</a>
            <a href="#harga">Harga</a>
            <a href="#kontak">Kontak</a>
        </nav>
        <a href="#daftar" class="btn-nav">Daftar</a>
    </header>

    <main>
        <section class="hero">
            <h1>Tumbuhkan Bisnismu Lebih Cepat</h1>
            <p>Platform digital untuk mengelola bisnis UMKM secara mudah dan otomatis.</p>
            <div class="hero-cta">
                <a href="#daftar" class="btn-primary">Coba Gratis</a>
                <a href="#video" class="btn-secondary">Lihat Demo</a>
            </div>
        </section>

        <section id="fitur" class="fitur">
            <h2>Fitur Unggulan</h2>
            <div class="fitur-grid">
                <div class="fitur-item"><h3>POS Kasir</h3><p>Kelola penjualan real-time.</p></div>
                <div class="fitur-item"><h3>Stok Barang</h3><p>Pantau stok otomatis.</p></div>
                <div class="fitur-item"><h3>Laporan</h3><p>Analisa penjualan bulanan.</p></div>
            </div>
        </section>
    </main>

    <footer>© 2025 StartupKu</footer>
</body>
</html>"""),

    ("Buatkan HTML dengan tag semantic utama",
     """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Semantic HTML</title>
</head>
<body>
    <header>
        <h1>Blog Teknologi</h1>
        <nav>
            <ul>
                <li><a href="#beranda">Beranda</a></li>
                <li><a href="#artikel">Artikel</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <article>
            <h2>Tips Belajar Coding</h2>
            <p>Mulai dari dasar, konsisten, dan banyak latihan.</p>
        </article>
        <aside>
            <h3>Artikel Populer</h3>
            <ul>
                <li><a href="#">React vs Vue</a></li>
                <li><a href="#">Flutter untuk Pemula</a></li>
            </ul>
        </aside>
    </main>
    <section>
        <h2>Berlangganan</h2>
        <form>
            <input type="email" placeholder="Email Anda">
            <button type="submit">Langganan</button>
        </form>
    </section>
    <footer>
        <p>© 2025 Blog Teknologi</p>
    </footer>
</body>
</html>"""),
]

# ============================ CSS ============================
css_samples = [
    ("Buatkan CSS modern button dengan efek hover",
     """.btn-modern {
    display: inline-block;
    padding: 12px 32px;
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    text-decoration: none;
}

.btn-modern:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.btn-modern:active {
    transform: translateY(-1px);
}"""),

    ("Buatkan CSS untuk membuat hero section yang menarik",
     """.hero {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 100vh;
    padding: 0 20px;
    background: linear-gradient(160deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
}

.hero h1 {
    font-size: clamp(2rem, 5vw, 4rem);
    margin-bottom: 20px;
    line-height: 1.2;
}

.hero p {
    font-size: 1.2rem;
    max-width: 600px;
    color: #a8b2d1;
    margin-bottom: 30px;
}

.hero .cta-buttons {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
}"""),

    ("Buatkan CSS untuk membuat tabel data yang rapi",
     """/* Tabel rapi dan mudah dibaca */
.table-container {
    overflow-x: auto;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

table.data-table {
    width: 100%;
    border-collapse: collapse;
    background: #fff;
    font-size: 14px;
}

.data-table thead th {
    background: #2d3436;
    color: #fff;
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    position: sticky;
    top: 0;
}

.data-table tbody tr {
    border-bottom: 1px solid #eee;
    transition: background 0.2s;
}

.data-table tbody tr:hover {
    background: #f8f9fa;
}

.data-table td {
    padding: 12px 16px;
    color: #333;
}

.data-table tbody tr:last-child {
    border-bottom: none;
}

/* Badge status */
.status {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.status-aktif { background: #d4edda; color: #155724; }
.status-nonaktif { background: #f8d7da; color: #721c24; }"""),

    ("Buatkan CSS responsive untuk grid produk e-commerce",
     """.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
    padding: 20px;
}

.product-card {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    background: #fff;
    transition: box-shadow 0.3s;
}

.product-card:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.product-image {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
}

.product-info {
    padding: 15px;
}

.product-name {
    font-weight: 600;
    margin-bottom: 5px;
}

.product-price {
    color: #e74c3c;
    font-weight: 700;
    font-size: 1.1rem;
}

.product-old-price {
    color: #999;
    text-decoration: line-through;
    font-size: 0.9rem;
}

.btn-beli {
    width: 100%;
    padding: 10px;
    background: #27ae60;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 10px;
}

@media (max-width: 600px) {
    .product-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        padding: 10px;
    }
}"""),

    ("Buatkan CSS untuk membuat sidebar navigasi",
     """.sidebar {
    width: 250px;
    min-height: 100vh;
    background: #2c3e50;
    color: #ecf0f1;
    position: fixed;
    top: 0;
    left: 0;
    padding: 20px 0;
}

.sidebar-logo {
    padding: 0 20px;
    font-size: 1.4rem;
    font-weight: bold;
    margin-bottom: 30px;
    color: #fff;
}

.sidebar-menu {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar-menu li a {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 20px;
    color: #bdc3c7;
    text-decoration: none;
    transition: all 0.2s;
}

.sidebar-menu li a:hover,
.sidebar-menu li.active a {
    background: #34495e;
    color: #fff;
    border-left: 4px solid #3498db;
}

.main-content {
    margin-left: 250px;
    padding: 20px;
}"""),
]

# ============================ JavaScript ============================
js_samples = [
    ("Buatkan JavaScript untuk toggle menu mobile",
     """const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    hamburger.classList.toggle('is-active');
});

// Tutup menu saat klik salah satu link
document.querySelectorAll('#navLinks a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        hamburger.classList.remove('is-active');
    });
});

// Tutup menu saat resize ke desktop
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        navLinks.classList.remove('active');
    }
});"""),

    ("Buatkan JavaScript untuk tombol kembali ke atas",
     """const backToTop = document.getElementById('backToTop');

// Tampilkan setelah scroll 400px
window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
        backToTop.style.display = 'block';
    } else {
        backToTop.style.display = 'none';
    }
});

// Klik = scroll ke atas dengan animasi
backToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});"""),

    ("Buatkan JavaScript untuk validasi password dan konfirmasi password",
     """function validatePassword() {
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirmPassword').value;
    const error = document.getElementById('passwordError');

    // Reset error
    error.textContent = '';

    if (password !== confirm) {
        error.textContent = 'Password dan konfirmasi tidak cocok';
        return false;
    }

    if (password.length < 8) {
        error.textContent = 'Password minimal 8 karakter';
        return false;
    }

    if (!/[A-Z]/.test(password)) {
        error.textContent = 'Password harus mengandung huruf kapital';
        return false;
    }

    if (!/[0-9]/.test(password)) {
        error.textContent = 'Password harus mengandung angka';
        return false;
    }

    return true;
}

document.getElementById('registForm')
    .addEventListener('submit', (e) => {
        if (!validatePassword()) {
            e.preventDefault();
        }
    });"""),

    ("Buatkan JavaScript untuk menghitung total belanja keranjang",
     """function hitungTotal() {
    const items = document.querySelectorAll('.cart-item');
    let totalHarga = 0;

    items.forEach(item => {
        const harga = parseFloat(item.dataset.harga);
        const qty = parseInt(item.querySelector('.qty-input').value);
        const subtotal = harga * qty;

        item.querySelector('.subtotal').textContent =
            'Rp ' + subtotal.toLocaleString('id-ID');

        totalHarga += subtotal;
    });

    // Tampilkan total
    const diskon = 0; // bisa diisi logika diskon
    const ongkir = totalHarga > 500000 ? 0 : 25000;
    const grandTotal = totalHarga + ongkir - diskon;

    document.getElementById('subtotal').textContent =
        'Rp ' + totalHarga.toLocaleString('id-ID');
    document.getElementById('ongkir').textContent =
        'Rp ' + ongkir.toLocaleString('id-ID');
    document.getElementById('total').textContent =
        'Rp ' + grandTotal.toLocaleString('id-ID');

    return grandTotal;
}

// Event listener pada qty
document.querySelectorAll('.qty-input').forEach(input => {
    input.addEventListener('change', hitungTotal);
});

// Hitung awal
hitungTotal();"""),

    ("Buatkan JavaScript fetch data dari API dan tampilkan ke tabel",
     """async function loadPengguna() {
    const tableBody = document.getElementById('penggunaBody');
    tableBody.innerHTML = '<tr><td colspan="4">Memuat...</td></tr>';

    try {
        const res = await fetch('/api/pengguna');
        if (!res.ok) throw new Error('Gagal mengambil data');

        const data = await res.json();

        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4">Belum ada data</td></tr>';
            return;
        }

        tableBody.innerHTML = data.map((p, idx) => `
            <tr>
                <td>${idx + 1}</td>
                <td>${p.nama}</td>
                <td>${p.email}</td>
                <td><span class="status status-${p.aktif ? 'aktif' : 'nonaktif'}">
                    ${p.aktif ? 'Aktif' : 'Nonaktif'}</span></td>
            </tr>
        `).join('');

    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="4">Error: ${err.message}</td></tr>`;
    }
}

// Load saat pertama kali
document.addEventListener('DOMContentLoaded', loadPengguna);

// Refresh tiap 30 detik
setInterval(loadPengguna, 30000);"""),

    ("Buatkan JavaScript untuk filter dan search list item",
     """const searchInput = document.getElementById('searchInput');
const itemList = document.getElementById('itemList');
const emptyMessage = document.getElementById('emptyMessage');

searchInput.addEventListener('input', filterItems);

function filterItems() {
    const query = searchInput.value.toLowerCase().trim();
    const items = itemList.querySelectorAll('.item');
    let visibleCount = 0;

    items.forEach(item => {
        const title = item.querySelector('.item-title').textContent.toLowerCase();
        const match = title.includes(query);
        item.style.display = match ? '' : 'none';
        if (match) visibleCount++;
    });

    emptyMessage.style.display = visibleCount === 0 ? 'block' : 'none';
}

// Reset filter
document.getElementById('clearFilter').addEventListener('click', () => {
    searchInput.value = '';
    filterItems();
    searchInput.focus();
});"""),
]

# ============================ PHP + MySQL ============================
php_samples = [
    ("Buatkan koneksi MySQL dengan PDO dan prepared statement",
     """<?php
// Koneksi database dengan PDO
$host = 'localhost';
$dbname = 'belajar_db';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    echo "Koneksi berhasil";
} catch (PDOException $e) {
    die("Koneksi gagal: " . $e->getMessage());
}

// Contoh insert dengan prepared statement (aman dari SQL injection)
$sql = "INSERT INTO pengguna (nama, email, password) VALUES (:nama, :email, :password)";
$stmt = $pdo->prepare($sql);
$stmt->execute([
    ':nama'     => $nama,
    ':email'    => $email,
    ':password' => password_hash($passInput, PASSWORD_DEFAULT),
]);

// Contoh select
$stmt = $pdo->query("SELECT * FROM pengguna WHERE aktif = 1");
$users = $stmt->fetchAll();
foreach ($users as $user) {
    echo $user['nama'] . ' - ' . $user['email'] . '<br>';
}
?>"""),

    ("Buatkan kode PHP untuk login sederhana dengan session",
     """<?php
session_start();
require_once 'koneksi.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email']);
    $password = $_POST['password'];

    // Cek user di database
    $stmt = $pdo->prepare("SELECT * FROM pengguna WHERE email = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password'])) {
        // Login berhasil
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['nama'];
        header('Location: dashboard.php');
        exit;
    } else {
        $error = "Email atau password salah";
    }
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <?php if (isset($error)): ?>
        <p style="color:red"><?= $error ?></p>
    <?php endif; ?>
    <form method="POST">
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Masuk</button>
    </form>
</body>
</html>"""),

    ("Buatkan kode PHP untuk upload file dengan validasi",
     """<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];
    $targetDir = 'uploads/';
    $maxSize = 5 * 1024 * 1024; // 5MB

    // Validasi ukuran
    if ($file['size'] > $maxSize) {
        die("File terlalu besar, maksimal 5MB");
    }

    // Validasi tipe file (cek extension)
    $allowedTypes = ['jpg', 'jpeg', 'png', 'gif', 'pdf'];
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (!in_array($ext, $allowedTypes)) {
        die("Tipe file tidak diizinkan");
    }

    // Buat nama unik
    $newName = date('Ymd_His') . '_' . uniqid() . '.' . $ext;
    $targetPath = $targetDir . $newName;

    // Pindahkan file
    if (move_uploaded_file($file['tmp_name'], $targetPath)) {
        echo "File berhasil diupload: " . $newName;
        // Simpan nama file ke database di sini
    } else {
        echo "Gagal upload file";
    }
}
?>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
</form>"""),

    ("Buatkan kode PHP menampilkan data dari MySQL dalam tabel",
     """<?php
require_once 'koneksi.php';

// Query dengan pencarian opsional
$search = isset($_GET['search']) ? trim($_GET['search']) : '';
$sql = "SELECT * FROM produk";
if ($search !== '') {
    $sql .= " WHERE nama LIKE :search";
}
$sql .= " ORDER BY id DESC";

$stmt = $pdo->prepare($sql);
if ($search !== '') {
    $stmt->execute([':search' => "%$search%"]);
} else {
    $stmt->execute();
}
$produkList = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Daftar Produk</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
    </style>
</head>
<body>
    <h1>Daftar Produk</h1>
    <form method="GET">
        <input type="text" name="search" value="<?= htmlspecialchars($search) ?>"
               placeholder="Cari produk...">
        <button type="submit">Cari</button>
    </form>
    <table>
        <thead>
            <tr><th>ID</th><th>Nama</th><th>Harga</th><th>Stok</th></tr>
        </thead>
        <tbody>
        <?php foreach ($produkList as $p): ?>
            <tr>
                <td><?= $p['id'] ?></td>
                <td><?= htmlspecialchars($p['nama']) ?></td>
                <td>Rp <?= number_format($p['harga'], 0, ',', '.') ?></td>
                <td><?= $p['stok'] ?></td>
            </tr>
        <?php endforeach; ?>
        </tbody>
    </table>
</body>
</html>"""),

    ("Buatkan kode PHP untuk REST API sederhana dengan JSON",
     """<?php
header('Content-Type: application/json');
require_once 'koneksi.php';

// Ambil method request
$method = $_SERVER['REQUEST_METHOD'];
$path = $_GET['route'] ?? '';
$id = $_GET['id'] ?? null;

switch ($method) {
    case 'GET':
        if ($id) {
            // Get single
            $stmt = $pdo->prepare("SELECT * FROM pengguna WHERE id = ?");
            $stmt->execute([$id]);
            $result = $stmt->fetch();
            echo json_encode($result ?: ['error' => 'Data tidak ditemukan']);
        } else {
            // Get all
            $stmt = $pdo->query("SELECT id, nama, email FROM pengguna");
            echo json_encode($stmt->fetchAll());
        }
        break;

    case 'POST':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $pdo->prepare("INSERT INTO pengguna (nama, email) VALUES (?, ?)");
        $stmt->execute([$data['nama'], $data['email']]);
        echo json_encode(['success' => true, 'id' => $pdo->lastInsertId()]);
        break;

    case 'DELETE':
        $stmt = $pdo->prepare("DELETE FROM pengguna WHERE id = ?");
        $stmt->execute([$id]);
        echo json_encode(['success' => $stmt->rowCount() > 0]);
        break;

    default:
        http_response_code(405);
        echo json_encode(['error' => 'Method tidak diizinkan']);
}
?>"""),

    ("Buatkan kode PHP untuk pagination data",
     """<?php
require_once 'koneksi.php';

$perPage = 10;            // Jumlah data per halaman
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$page = max(1, $page);
$offset = ($page - 1) * $perPage;

// Hitung total data
$totalData = $pdo->query("SELECT COUNT(*) FROM artikel")->fetchColumn();
$totalPages = (int)ceil($totalData / $perPage);

// Ambil data per halaman
$stmt = $pdo->prepare("SELECT * FROM artikel ORDER BY tanggal DESC LIMIT :limit OFFSET :offset");
$stmt->bindValue(':limit', $perPage, PDO::PARAM_INT);
$stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
$stmt->execute();
$artikels = $stmt->fetchAll();
?>

<?php foreach ($artikels as $artikel): ?>
    <h2><?= htmlspecialchars($artikel['judul']) ?></h2>
    <p><?= htmlspecialchars($artikel['isi']) ?></p>
<?php endforeach; ?>

<div class="pagination">
    <?php if ($page > 1): ?>
        <a href="?page=<?= $page - 1 ?>">Prev</a>
    <?php endif; ?>

    <?php for ($i = 1; $i <= $totalPages; $i++): ?>
        <a href="?page=<?= $i ?>" class="<?= $i == $page ? 'active' : '' ?>">
            <?= $i ?>
        </a>
    <?php endfor; ?>

    <?php if ($page < $totalPages): ?>
        <a href="?page=<?= $page + 1 ?>">Next</a>
    <?php endif; ?>
</div>"""),
]

# ============================ React ============================
react_samples = [
    ("Buatkan komponen React untuk accordion/frequently asked questions",
     """import React, { useState } from 'react';

const faqs = [
    {
        q: 'Apakah ada biaya tersembunyi?',
        a: 'Tidak ada. Harga yang tertera sudah final tanpa biaya tersembunyi.'
    },
    {
        q: 'Berapa lama pengiriman?',
        a: 'Pengiriman dalam negeri 2-5 hari kerja.'
    },
    {
        q: 'Apakah bisa refund?',
        a: 'Bisa, dalam 7 hari jika produk belum dipakai.'
    }
];

export default function Accordion() {
    const [openIndex, setOpenIndex] = useState(null);

    return (
        <div className="faq-accordion">
            {faqs.map((faq, idx) => (
                <div className={`faq-item ${openIndex === idx ? 'open' : ''}`} key={idx}>
                    <button
                        className="faq-question"
                        onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
                    >
                        {faq.q}
                        <span className="faq-icon">{openIndex === idx ? '−' : '+'}</span>
                    </button>
                    {openIndex === idx && (
                        <div className="faq-answer">{faq.a}</div>
                    )}
                </div>
            ))}
        </div>
    );
}"""),

    ("Buatkan komponen React untuk search bar dengan debounce",
     """import React, { useState, useEffect } from 'react';

export default function SearchBar({ onSearch, placeholder = 'Cari...' }) {
    const [query, setQuery] = useState('');

    // Debounce: tunggu 500ms setelah user berhenti mengetik
    useEffect(() => {
        const timeout = setTimeout(() => {
            onSearch(query);
        }, 500);

        // Bersihkan timeout saat query berubah atau unmount
        return () => clearTimeout(timeout);
    }, [query]);

    return (
        <div className="search-bar">
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={placeholder}
                className="search-input"
            />
            {query && (
                <button className="search-clear" onClick={() => setQuery('')}>
                    ✕
                </button>
            )}
        </div>
    );
}"""),

    ("Buatkan komponen React untuk tabel data dengan sorting",
     """import React, { useState, useMemo } from 'react';

export default function DataTable({ data, columns }) {
    const [sortKey, setSortKey] = useState(null);
    const [sortAsc, setSortAsc] = useState(true);

    const sorted = useMemo(() => {
        if (!sortKey) return data;
        return [...data].sort((a, b) => {
            const va = a[sortKey];
            const vb = b[sortKey];
            if (typeof va === 'number' && typeof vb === 'number') {
                return sortAsc ? va - vb : vb - va;
            }
            return sortAsc
                ? String(va).localeCompare(String(vb))
                : String(vb).localeCompare(String(va));
        });
    }, [data, sortKey, sortAsc]);

    const handleSort = (key) => {
        if (sortKey === key) {
            setSortAsc(!sortAsc);
        } else {
            setSortKey(key);
            setSortAsc(true);
        }
    };

    return (
        <table className="data-table">
            <thead>
                <tr>
                    {columns.map(col => (
                        <th key={col.key} onClick={() => handleSort(col.key)}>
                            {col.label}
                            {sortKey === col.key && (
                                <span>{sortAsc ? ' ▲' : ' ▼'}</span>
                            )}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {sorted.map((row, i) => (
                    <tr key={i}>
                        {columns.map(col => (
                            <td key={col.key}>{row[col.key]}</td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
}"""),

    ("Buatkan komponen React dengan localStorage untuk menyimpan data",
     """import React, { useState, useEffect } from 'react';

// Custom hook untuk localStorage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        try {
            const stored = localStorage.getItem(key);
            return stored ? JSON.parse(stored) : initialValue;
        } catch {
            return initialValue;
        }
    });

    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);

    return [value, setValue];
}

export default function CatatanApp() {
    const [catatan, setCatatan] = useLocalStorage('catatan', []);
    const [text, setText] = useState('');

    const tambah = () => {
        if (!text.trim()) return;
        setCatatan([
            ...catatan,
            { id: Date.now(), isi: text.trim(), waktu: new Date().toLocaleString() }
        ]);
        setText('');
    };

    const hapus = (id) => {
        setCatatan(catatan.filter(c => c.id !== id));
    };

    return (
        <div className="catatan-app">
            <h2>Catatan Saya</h2>
            <div className="input-row">
                <input
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Tulis catatan..."
                    onKeyPress={(e) => e.key === 'Enter' && tambah()}
                />
                <button onClick={tambah}>Tambah</button>
            </div>
            <ul>
                {catatan.map(c => (
                    <li key={c.id}>
                        <p>{c.isi}</p>
                        <small>{c.waktu}</small>
                        <button onClick={() => hapus(c.id)}>Hapus</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}"""),

    ("Buatkan komponen React untuk modals",
     """import React, { useState } from 'react';

export default function Modal({ trigger, title, children }) {
    const [open, setOpen] = useState(false);

    useEffect(() => {
        // Kunci scroll saat modal terbuka
        document.body.style.overflow = open ? 'hidden' : '';
        return () => { document.body.style.overflow = ''; };
    }, [open]);

    // Tutup dengan tombol Esc
    useEffect(() => {
        const handler = (e) => e.key === 'Escape' && setOpen(false);
        window.addEventListener('keydown', handler);
        return () => window.removeEventListener('keydown', handler);
    }, []);

    return (
        <>
            {/* Trigger untuk membuka */}
            {React.cloneElement(trigger, { onClick: () => setOpen(true) })}

            {open && (
                <div className="modal-overlay" onClick={() => setOpen(false)}>
                    <div className="modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>{title}</h3>
                            <button className="modal-close" onClick={() => setOpen(false)}>
                                ✕
                            </button>
                        </div>
                        <div className="modal-body">
                            {children}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

// Penggunaan:
// <Modal
//     title="Konfirmasi"
//     trigger={<button>Hapus Data</button>}
// >
//     <p>Yakin ingin menghapus data ini?</p>
//     <button onClick={handleDelete}>Ya, Hapus</button>
// </Modal>"""),
]

# ============================ Vue ============================
vue_samples = [
    ("Buatkan komponen Vue 3 untuk counter dengan Composition API",
     """<script setup>
import { ref, computed } from 'vue';

const count = ref(0);
const isEven = computed(() => count.value % 2 === 0);

const increment = () => count.value++;
const decrement = () => count.value--;
const reset = () => (count.value = 0);
</script>

<template>
    <div class="counter">
        <h2>Nilai: {{ count }}</h2>
        <p class="indicator">{{ isEven ? 'Genap' : 'Ganjil' }}</p>
        <div class="buttons">
            <button @click="decrement" :disabled="count === 0">-</button>
            <button @click="increment">+</button>
            <button @click="reset">Reset</button>
        </div>
    </div>
</template>

<style scoped>
.counter { text-align: center; padding: 20px; }
.buttons { display: flex; gap: 10px; justify-content: center; }
.buttons button {
    padding: 10px 20px; border: none;
    background: #42b883; color: white;
    border-radius: 6px; cursor: pointer;
}
</style>"""),

    ("Buatkan komponen Vue untuk form validasi",
     """<script setup>
import { reactive, ref } from 'vue';

const form = reactive({
    nama: '',
    email: '',
    umur: ''
});

const errors = ref({});
const sukses = ref(false);

function validate() {
    const err = {};

    if (!form.nama.trim()) {
        err.nama = 'Nama wajib diisi';
    }
    if (!form.email.trim()) {
        err.email = 'Email wajib diisi';
    } else if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(form.email)) {
        err.email = 'Format email tidak valid';
    }
    if (!form.umur || Number(form.umur) < 17) {
        err.umur = 'Umur minimal 17 tahun';
    }

    errors.value = err;
    return Object.keys(err).length === 0;
}

function submit() {
    sukses.value = false;
    if (validate()) {
        // Kirim ke API
        console.log('Data valid:', form);
        sukses.value = true;
    }
}
</script>

<template>
    <form @submit.prevent="submit" class="form">
        <div class="field">
            <label>Nama</label>
            <input v-model="form.nama" />
            <small v-if="errors.nama" class="error">{{ errors.nama }}</small>
        </div>

        <div class="field">
            <label>Email</label>
            <input v-model="form.email" type="email" />
            <small v-if="errors.email" class="error">{{ errors.email }}</small>
        </div>

        <div class="field">
            <label>Umur</label>
            <input v-model="form.umur" type="number" />
            <small v-if="errors.umur" class="error">{{ errors.umur }}</small>
        </div>

        <button type="submit">Simpan</button>
        <p v-if="sukses" class="sukses">Data berhasil disimpan!</p>
    </form>
</template>"""),
]

# ============================ Flutter ============================
flutter_samples = [
    ("Buatkan widget Flutter untuk bottom navigation",
     """import 'package:flutter/material.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  final List<Widget> _pages = const [
    HomePage(),
    SearchPage(),
    CartPage(),
    ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _pages,
      ),
      bottomNavigationBar: NavigationBar(
        currentIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() => _currentIndex = index);
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Beranda',
          ),
          NavigationDestination(
            icon: Icon(Icons.search),
            label: 'Cari',
          ),
          NavigationDestination(
            icon: Icon(Icons.shopping_cart_outlined),
            selectedIcon: Icon(Icons.shopping_cart),
            label: 'Keranjang',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Profil',
          ),
        ],
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});
  @override
  Widget build(BuildContext context) =>
      const Center(child: Text('Halaman Beranda'));
}

class SearchPage extends StatelessWidget {
  const SearchPage({super.key});
  @override
  Widget build(BuildContext context) =>
      const Center(child: Text('Halaman Pencarian'));
}

class CartPage extends StatelessWidget {
  const CartPage({super.key});
  @override
  Widget build(BuildContext context) =>
      const Center(child: Text('Keranjang Belanja'));
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});
  @override
  Widget build(BuildContext context) =>
      const Center(child: Text('Profil Saya'));
}"""),

    ("Buatkan widget Flutter untuk menampilkan form pendaftaran",
     """import 'package:flutter/material.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _nama = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _showPassword = false;

  @override
  void dispose() {
    _nama.dispose();
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  void _daftar() {
    if (_formKey.currentState?.validate() ?? false) {
      // Panggil API register
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Pendaftaran berhasil!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Daftar Akun')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nama,
                decoration: const InputDecoration(
                  labelText: 'Nama Lengkap',
                  prefixIcon: Icon(Icons.person),
                  border: OutlineInputBorder(),
                ),
                validator: (v) =>
                    (v == null || v.isEmpty) ? 'Nama wajib diisi' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _email,
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  prefixIcon: Icon(Icons.email),
                  border: OutlineInputBorder(),
                ),
                validator: (v) {
                  if (v == null || v.isEmpty) return 'Email wajib diisi';
                  if (!v.contains('@')) return 'Email tidak valid';
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _password,
                obscureText: !_showPassword,
                decoration: InputDecoration(
                  labelText: 'Password',
                  prefixIcon: const Icon(Icons.lock),
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(_showPassword
                        ? Icons.visibility_off
                        : Icons.visibility),
                    onPressed: () =>
                        setState(() => _showPassword = !_showPassword),
                  ),
                ),
                validator: (v) => (v == null || v.length < 8)
                    ? 'Minimal 8 karakter'
                    : null,
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _daftar,
                  child: const Text('Daftar Sekarang'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}"""),

    ("Buatkan widget Flutter untuk menampilkan dialog konfirmasi",
     """import 'package:flutter/material.dart';

// Contoh pemakaian dialog konfirmasi
Future<void> showConfirmDialog(BuildContext context) async {
  final result = await showDialog<bool>(
    context: context,
    builder: (context) => AlertDialog(
      title: const Text('Konfirmasi Hapus'),
      content: const Text('Yakin ingin menghapus data ini?\nAksi tidak bisa dibatalkan.'),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: const Text('Batal'),
        ),
        TextButton(
          onPressed: () => Navigator.pop(context, true),
          style: TextButton.styleFrom(foregroundColor: Colors.red),
          child: const Text('Hapus'),
        ),
      ],
    ),
  );

  if (result == true) {
    // Lakukan aksi hapus
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Data dihapus')),
    );
  }
}

// Widget tombol yang memanggil dialog
class DeleteButton extends StatelessWidget {
  const DeleteButton({super.key});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.delete, color: Colors.red),
      onPressed: () => showConfirmDialog(context),
    );
  }
}"""),

    ("Buatkan widget Flutter untuk dark mode toggle",
     """import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool _darkMode = false;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      themeMode: _darkMode ? ThemeMode.dark : ThemeMode.light,
      theme: ThemeData.light(useMaterial3: true),
      darkTheme: ThemeData.dark(useMaterial3: true),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Mode Gelap'),
          actions: [
            IconButton(
              icon: Icon(_darkMode ? Icons.light_mode : Icons.dark_mode),
              onPressed: () => setState(() => _darkMode = !_darkMode),
            ),
          ],
        ),
        body: Center(
          child: Text(
            _darkMode ? 'Mode gelap aktif' : 'Mode terang aktif',
            style: const TextStyle(fontSize: 18),
          ),
        ),
      ),
    );
  }
}"""),
]

# ============================ React Native ============================
reactnative_samples = [
    ("Buatkan komponen React Native untuk form pendaftaran",
     """import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  StyleSheet, Alert, ScrollView, KeyboardAvoidingView, Platform,
} from 'react-native';

export default function RegisterScreen() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!name || !email || !password) {
      Alert.alert('Error', 'Semua field wajib diisi');
      return;
    }
    if (password.length < 8) {
      Alert.alert('Error', 'Password minimal 8 karakter');
      return;
    }

    setLoading(true);
    try {
      // Panggil API register
      // const res = await api.post('/register', { name, email, password });
      setLoading(false);
      Alert.alert('Sukses', 'Akun berhasil dibuat!');
    } catch (error) {
      setLoading(false);
      Alert.alert('Gagal', error.message);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Buat Akun</Text>
        <TextInput
          style={styles.input}
          placeholder="Nama Lengkap"
          value={name}
          onChangeText={setName}
        />
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <TouchableOpacity
          style={styles.button}
          onPress={handleRegister}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'Memuat...' : 'Daftar'}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f9f9f9' },
  content: { padding: 24, flexGrow: 1, justifyContent: 'center' },
  title: {
    fontSize: 28, fontWeight: 'bold',
    textAlign: 'center', marginBottom: 32, color: '#333',
  },
  input: {
    backgroundColor: '#fff', borderRadius: 8, padding: 14,
    fontSize: 16, marginBottom: 16,
    borderWidth: 1, borderColor: '#ddd',
  },
  button: {
    backgroundColor: '#2563eb', borderRadius: 8,
    padding: 16, alignItems: 'center', marginTop: 8,
  },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
});"""),

    ("Buatkan komponen React Native untuk slide toggle pengaturan",
     """import React, { useState } from 'react';
import { View, Text, Switch, StyleSheet } from 'react-native';

export default function SettingsScreen() {
  const [notif, setNotif] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [location, setLocation] = useState(false);

  const settings = [
    {
      label: 'Notifikasi Push',
      desc: 'Terima notifikasi dari aplikasi',
      value: notif,
      onValueChange: setNotif,
    },
    {
      label: 'Mode Gelap',
      desc: 'Tampilan dengan tema gelap',
      value: darkMode,
      onValueChange: setDarkMode,
    },
    {
      label: 'Akses Lokasi',
      desc: 'Gunakan lokasi untuk fitur terdekat',
      value: location,
      onValueChange: setLocation,
    },
  ];

  return (
    <View style={styles.container}>
      {settings.map((item, idx) => (
        <View key={idx} style={styles.row}>
          <View style={styles.info}>
            <Text style={styles.label}>{item.label}</Text>
            <Text style={styles.desc}>{item.desc}</Text>
          </View>
          <Switch
            value={item.value}
            onValueChange={item.onValueChange}
            trackColor={{ true: '#2563eb' }}
          />
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  row: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', paddingVertical: 16,
    borderBottomWidth: 1, borderBottomColor: '#eee',
  },
  info: { flex: 1, marginRight: 16 },
  label: { fontSize: 16, fontWeight: '600', color: '#333' },
  desc: { fontSize: 13, color: '#888', marginTop: 4 },
});"""),

    ("Buatkan komponen React Native untuk daftar vertical produk",
     """import React, { useState, useEffect } from 'react';
import {
  View, Text, FlatList, ActivityIndicator,
  TouchableOpacity, StyleSheet, Image, RefreshControl,
} from 'react-native';

export default function ProductList({ navigation }) {
  const [produk, setProduk] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const res = await fetch('https://api.contoh.com/produk');
      const data = await res.json();
      setProduk(data);
      setError(null);
    } catch (err) {
      setError('Gagal memuat data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('Detail', { id: item.id })}
    >
      <Image
        source={{ uri: item.gambar }}
        style={styles.image}
        resizeMode="cover"
      />
      <View style={styles.cardBody}>
        <Text style={styles.nama}>{item.nama}</Text>
        <Text style={styles.harga}>
          Rp {Number(item.harga).toLocaleString('id-ID')}
        </Text>
        <Text style={styles.stok} numberOfLines={1}>
          Stok: {item.stok}
        </Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#2563eb" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={styles.error}>{error}</Text>
        <TouchableOpacity onPress={fetchData} style={styles.retry}>
          <Text style={styles.retryText}>Coba Lagi</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <FlatList
      data={produk}
      keyExtractor={(item) => String(item.id)}
      renderItem={renderItem}
      contentContainerStyle={styles.list}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
      ListEmptyComponent={
        <Text style={styles.empty}>Belum ada produk</Text>
      }
    />
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  list: { padding: 16 },
  card: {
    backgroundColor: '#fff', borderRadius: 10, marginBottom: 16,
    overflow: 'hidden', shadowColor: '#000', shadowOpacity: 0.1,
    shadowRadius: 4, elevation: 3,
  },
  image: { width: '100%', height: 180 },
  cardBody: { padding: 12 },
  nama: { fontSize: 16, fontWeight: '600' },
  harga: { color: '#2563eb', fontWeight: '700', marginTop: 4 },
  stok: { color: '#888', fontSize: 13, marginTop: 2 },
  error: { color: '#e74c3c', fontSize: 16 },
  retry: { marginTop: 16, padding: 12, backgroundColor: '#2563eb', borderRadius: 8 },
  retryText: { color: '#fff' },
  empty: { textAlign: 'center', marginTop: 40, color: '#888' },
});"""),
]

# ============================ Q&A Umum / Penjelasan ============================
qa_samples = [
    ("siapa pembuat kamu",
     "Saya dibuat oleh pengguna yang sedang belajar pengembangan AI lokal. Nama saya minx, model AI kecil yang dirancang untuk membantu pemrograman web dan aplikasi mobile, dipasang dan berjalan sepenuhnya di komputer Anda secara offline."),

    ("apa itu API",
     "API (Application Programming Interface) adalah jembatan yang menghubungkan dua aplikasi agar bisa saling bertukar data. Contoh: aplikasi web memanggil API server untuk mengambil data pengguna dari database. API mengembalikan data dalam format JSON atau XML. Contoh API sederhana: GET /api/pengguna mengembalikan daftar pengguna, POST /api/login mengirim email dan password lalu mengembalikan token."),

    ("apa perbedaan GET dan POST pada HTTP",
     "GET mengirim data lewat URL (query string), contoh: /cari?q=halo. Data terlihat di URL, tidak cocok untuk data sensitif, dan dibatasi panjangnya. POST mengirim data lewat body request, contoh saat submit form login. Data tidak terlihat (lebih aman), bisa berukuran besar, bisa berisi file. Aturan umumnya: GET untuk mengambil data, POST untuk mengirim/membuat data baru, PUT untuk update, DELETE untuk hapus."),

    ("apa itu REST API",
     "REST API adalah gaya arsitektur API yang mengikuti aturan HTTP standar. Konsepnya: setiap data adalah 'resource' yang diakses lewat URL, dan metode HTTP menentukan aksinya. Contoh resource: /pengguna, /produk, /order. GET /pengguna = ambil semua; GET /pengguna/1 = ambil satu; POST /pengguna = buat baru; PUT /pengguna/1 = update; DELETE /pengguna/1 = hapus. Response biasanya JSON. Keuntungan: sederhana, mudah dipahami, stateless (tidak ingat state antar request)."),

    ("apa itu JSON",
     "JSON (JavaScript Object Notation) adalah format teks untuk bertukar data antar aplikasi. Strukturnya mirip objek JavaScript: pasangan key dan value dalam kurung kurawal. Contoh: {\"nama\": \"Budi\", \"umur\": 25, \"hobi\": [\"coding\", \"musik\"]}. JSON mendukung tipe data: string (dalam tanda kutip), number, boolean (true/false), array (dalam kurung siku), object (kurung kurawal), dan null. Hampir semua bahasa pemrograman bisa membaca JSON, sehingga menjadi standar untuk komunikasi API."),

    ("apa itu program CRUD",
     "CRUD adalah empat operasi dasar pada data: Create (tambah), Read (baca/tampilkan), Update (ubah), Delete (hapus). Setiap aplikasi yang menyimpan data pasti butuh CRUD. Pemetaan ke SQL: Create = INSERT, Read = SELECT, Update = UPDATE, Delete = DELETE. Pemetaan ke REST API: Create = POST, Read = GET, Update = PUT/PATCH, Delete = DELETE. Contoh lengkap: aplikasi manajemen pengguna yang bisa menambah pengguna baru, menampilkan daftar, mengubah profil, dan menghapus akun."),

    ("apa itu SQL injection",
     "SQL injection adalah serangan di mana penyerang menyelipkan kode SQL jahat ke input aplikasi. Contoh rentan: $sql = \"SELECT * FROM user WHERE username = '$username'\"; Jika penyerang mengisi username dengan ' OR '1'='1, query menjadi: SELECT * FROM user WHERE username = '' OR '1'='1 — mengembalikan semua data. Pencegahan: 1) gunakan prepared statement/parameterized query (PDO atau mysqli prepare), 2) jangan pernah menggabungkan string SQL langsung dari input user, 3) validasi dan sanitasi input, 4) beri hak akses database seminimal mungkin."),

    ("apa itu framework",
     "Framework adalah kumpulan kode yang sudah jadi untuk mempercepat pengembangan aplikasi. Ibarat rumah jadi tinggal pakai, bukan bangun semua dari nol. Contoh framework web: Laravel (PHP), Django (Python), Next.js (React, JavaScript). Framework mobile: Flutter (Dart), React Native (JavaScript). Keuntungan: cepat, aman (sudah ada solusi untuk masalah umum), rapi (pola terstruktur). Kekurangannya: harus belajar aturan framework, ukuran aplikasi lebih besar."),

    ("apa itu state management",
     "State management adalah cara aplikasi menyimpan dan membagikan data/bagian yang berubah antar komponen. Contoh state: data user yang login, isi keranjang belanja, tema aplikasi. Di React: useState untuk state lokal, Context API atau Zustand untuk state global. Di Flutter: setState untuk state lokal, Provider atau Riverpod untuk global. Intinya: state = data yang menentukan tampilan, dan management = bagaimana data itu dikelola dan dibagikan antar bagian aplikasi."),

    ("kenapa useState saya tidak update",
     "Ini masalah umum di React. Penyebab biasanya: 1) setNilai dipanggil berulang memakai nilai lama — solusi: pakai functional update, setCount(prev => prev + 1). 2) Nilai diganti dengan mutasi langsung seperti state.push() — React tidak mendeteksi. Solusi: buat array baru, setItems([...items, item]). 3) Setelah setState, nilai belum berubah langsung — state async, baca di useEffect. 4) Komponen dirender ulang tapi state di-reset — pastikan state dideklarasi di luar komponen yang unmount."),

    ("apa bedanya var, let, const di JavaScript",
     "var: deklarasi lama, scope-nya function (bukan block), bisa di-assign ulang, hoisted, sering bikin bug. let: scope block {} , bisa di-assign ulang — dipakai bila nilai berubah. const: scope block, tidak bisa di-assign ulang — harus diinisialisasi, dipakai default untuk nilai tetap. Aturan praktis modern: gunakan const sebagai default, let hanya bila nilai pasti berubah, hindari var. Contoh: const nama = \"Budi\"; let umur = 25; umur = 26; // OK . nama = \"Andi\"; // ERROR"),

    ("apa bedanya == dan === di JavaScript",
     "== (loose equality) membandingkan nilai setelah konversi tipe: '5' == 5 menghasilkan true, 0 == false juga true. Ini rentan bug. === (strict equality) membandingkan nilai DAN tipe tanpa konversi: '5' === 5 menghasilkan false, 0 === false false. Aturan: selalu pakai === agar perbandingan prediktabel dan aman. Kecuali khusus saat sengaja mengabaikan tipe (jarang). Contoh: console.log(0 == false) // true ; console.log(0 === false) // false"),

    ("apa itu promise javascript",
     "Promise adalah objek yang mewakili hasil operasi asinkron (yang butuh waktu, seperti fetch data atau baca file). Statusnya: pending (sedang jalan), fulfilled (berhasil), rejected (gagal). Membuat promise: new Promise((resolve, reject) => {...}). Memakai: promise.then(hasil => ...).catch(err => ...) atau kata kunci async/await yang lebih modern: const data = await fetch('url'). Async/await membuat kode terlihat sinkron dan mudah dibaca, tapi harus dibungkus function async."),

    ("bagaimana cara belajar coding untuk pemula",
     "Rekomendasi saya: 1) Pilih satu bahasa dulu dan fokus — misal HTML/CSS/JavaScript untuk web atau Dart untuk mobile. 2) Kerjakan tutorial interaktif lalu langsung praktik bikin proyek kecil (form, to-do list). 3) Pahami konsep dasar: variabel, tipe data, percabangan, perulangan, fungsi, array. 4) Copy kode bukan memalukan, tapi pahami tiap baris lalu modifikasi. 5) Belajar membaca error log. 6) Konsisten: 1 jam tiap hari lebih baik dari 8 jam seminggu sekali. 7) Gabung komunitas dan jangan takut bertanya."),

    ("tools apa saja yang dibutuhkan untuk develop web",
     "Minimal: 1) Code editor — VS Code gratis paling populer. 2) Browser — Chrome/Edge dengan developer tools. 3) Git untuk version control + akun GitHub. 4) Node.js untuk menjalankan JavaScript dan package manager (npm). 5) Untuk database: MySQL atau SQLite untuk lokal. 6) Postman untuk tes API. 7) Mengenal terminal/command line dasar. Untuk deploy nanti: Netlify/Vercel untuk static, atau cPanel/Hosting untuk PHP."),

    ("apa itu git dan github",
     "Git adalah sistem version control: mencatat setiap perubahan kode sehingga bisa kembali ke versi sebelumnya, bekerja timpa, dan melihat siapa mengubah apa. Perintah dasar: git init, git add, git commit, git push. GitHub adalah platform online tempat menyimpan repo Git: kolaborasi, review kode, issue tracking, dan deploy otomatis. Alur umum: buat perubahan → git add . → git commit -m \"pesan\" → git push origin main → lalu buat Pull Request bila ada tim."),

    ("apa itu npm",
     "npm (Node Package Manager) adalah package manager bawaan Node.js untuk menginstal library JavaScript. Perintah umum: npm init -y membuat package.json; npm install nama-package menginstal; npm install -D nama-package untuk devDependency; npm run dev menjalankan script yang didefinisikan di package.json. File package.json menyimpan daftar dependency dan script. Selama project, library tersimpan di folder node_modules. Untuk project baru juga populer memakai Vite: npm create vite@latest."),

    ("apa itu library vs framework",
     "Library adalah kumpulan fungsi yang Anda panggil sesuai kebutuhan — Anda yang mengontrol alur. Contoh: Axios, jQuery, date-fns. Framework menyediakan struktur besar dan mengontrol alur — Anda mengisi bagian yang disediakan. Contoh: Laravel, Next.js, Flutter. Ibarat mobil: library seperti komponen spare part yang Anda pasang sendiri; framework seperti mobil utuh berisi template, tinggal mengemudi. Kalau butuh kontrol penuh dan project kecil: pakai library. Project besar dengan tim: framework memberi konsistensi."),
]

# ============================ Bahasa Indonesia coding ============================
qa_indonesia = [
    ("buatkan fungsi php untuk menyimpan data ke database",
     """<?php
function simpanData($pdo, $tabel, $data) {
    // $data berbentuk array asosiatif ['nama' => ..., 'email' => ...]
    $kolom = array_keys($data);
    $koloms = implode(', ', $kolom);
    $placeholder = implode(', ', array_map(fn($k) => ":$k", $kolom));

    $sql = "INSERT INTO $tabel ($koloms) VALUES ($placeholder)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute($data);

    return $pdo->lastInsertId();
}

// Contoh pemakaian:
$pdo = new PDO("mysql:host=localhost;dbname=test", "root", "");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$idBaru = simpanData($pdo, 'pengguna', [
    'nama'  => 'Budi',
    'email' => 'budi@mail.com'
]);

echo "Data tersimpan dengan ID: $idBaru";
?>"""),

    ("buatkan cara menghitung umur dari tanggal lahir di php",
     """<?php
function hitungUmur($tanggalLahir) {
    $lahir = new DateTime($tanggalLahir);
    $sekarang = new DateTime();
    $selisih = $lahir->diff($sekarang);
    return $selisih->y; // tahun
}

function hitungUmurHari($tanggalLahir) {
    $lahir = new DateTime($tanggalLahir);
    $sekarang = new DateTime();
    return $lahir->diff($sekarang)->days; // total hari
}

// Contoh
echo hitungUmur('2000-05-15'); // misal hasil 25
echo ' | ' . hitungUmurHari('2000-05-15') . ' hari';
?>"""),

    ("buatkan random password generator di javascript",
     """function generatePassword(length = 12) {
    const lower = 'abcdefghijklmnopqrstuvwxyz';
    const upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const numbers = '0123456789';
    const symbols = '!@#$%^&*()_+-=';
    const all = lower + upper + numbers + symbols;

    // Butuh random secure
    const rand = () => {
        const arr = new Uint32Array(1);
        crypto.getRandomValues(arr);
        return arr[0] / (0xffffffff + 1);
    };

    let password = '';
    // Pastikan minimal 1 dari tiap kategori
    password += lower[Math.floor(rand() * lower.length)];
    password += upper[Math.floor(rand() * upper.length)];
    password += numbers[Math.floor(rand() * numbers.length)];
    password += symbols[Math.floor(rand() * symbols.length)];

    // Isi sisa panjang
    for (let i = password.length; i < length; i++) {
        password += all[Math.floor(rand() * all.length)];
    }

    // Acak urutan
    return password.split('').sort(() => rand() - 0.5).join('');
}

console.log(generatePassword(16));
// Contoh hasil: "k$7H#mQ2zW!afB9v"
"""),

    ("buatkan kode javascript untuk mengubah angka menjadi format rupiah",
     """function formatRupiah(angka) {
    return 'Rp ' + Math.round(angka)
        .toString()
        .replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
}

// Pakai toLocaleString (cara simpel)
function formatRupiah2(angka) {
    return 'Rp ' + Number(angka).toLocaleString('id-ID');
}

// Parsing balik: hapus Rp, titik, spasi
function parseRupiah(str) {
    const bersih = str.replace(/[^\\d]/g, '');
    return parseInt(bersih || '0', 10);
}

console.log(formatRupiah(1500000));   // Rp 1.500.000
console.log(formatRupiah2(2500000));  // Rp 2.500.000
console.log(parseRupiah('Rp 1.500.000')); // 1500000
"""),

    ("buatkan kode php untuk mencetak bilangan prima",
     """<?php
function cekPrima($n) {
    if ($n < 2) return false;
    for ($i = 2; $i * $i <= $n; $i++) {
        if ($n % $i == 0) return false;
    }
    return true;
}

function ambilPrima($sampai) {
    $hasil = [];
    for ($i = 2; $i <= $sampai; $i++) {
        if (cekPrima($i)) $hasil[] = $i;
    }
    return $hasil;
}

// Cetak prima 1-50
foreach (ambilPrima(50) as $prima) {
    echo $prima . ' '; // 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
}
?>"""),

    ("buatkan fungsi javascript untuk menghitung diskon",
     """function hitungDiskon(harga) {
    let diskon = 0;

    if (harga >= 100000 && harga < 250000) {
        diskon = 5;          // 5%
    } else if (harga >= 250000 && harga < 500000) {
        diskon = 10;         // 10%
    } else if (harga >= 500000) {
        diskon = 15;         // 15%
    }

    const potongan = (harga * diskon) / 100;
    const total = harga - potongan;

    return {
        harga,
        diskon: diskon + '%',
        potongan,
        total,
        keterangan: diskon === 0
            ? 'Belum dapat diskon'
            : `Diskon ${diskon}% = Rp ${potongan.toLocaleString('id-ID')}`
    };
}

console.log(hitungDiskon(600000));
// { harga: 600000, diskon: '15%', potongan: 90000, total: 510000, ... }
"""),
]

# ============================ Gabung semua ============================
all_samples = (
    html_samples
    + css_samples
    + js_samples
    + php_samples
    + react_samples
    + vue_samples
    + flutter_samples
    + reactnative_samples
    + [(q, a) for q, a in qa_samples]
    + [(q, a) for q, a in qa_indonesia]
)

# Acak urutan
random.seed(42)
random.shuffle(all_samples)

# Bagi jadi 4 file
files = {}
for i, (instruction, output) in enumerate(all_samples):
    cat = i % 4 + 1
    files.setdefault(cat, []).append({
        "instruction": instruction,
        "output": output
    })

for cat, items in files.items():
    path = os.path.join(OUT_DIR, f"extra_00{cat}.jsonl")
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"  {path}: {len(items)} contoh")

print(f"\nTotal: {len(all_samples)} contoh ditulis ke data/raw/")