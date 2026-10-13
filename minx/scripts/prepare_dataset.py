"""
minx - Step 2: Prepare Dataset
Siapkan dataset coding web + mobile app untuk fine-tuning minx.

Input : data/raw/*.jsonl (opsional, jika kosong gunakan template bawaan)
Output: data/processed/minx_train.jsonl

Format tiap baris:
{
  "instruction": "...",
  "output": "...",
  "input": "..." (opsional)
}

Fokus: HTML, CSS, JavaScript, React, Vue, Flutter, React Native
"""

import json
import os
import random
import sys

# ============ Template Data Bawaan ============
# 50 contoh dasar coding web + mobile (fallback jika raw kosong)
BUILTIN_DATA = [
    # === HTML ===
    {
        "instruction": "Buatkan struktur HTML dasar untuk halaman login sederhana",
        "output": """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <main class="login-container">
        <h1>Masuk</h1>
        <form action="/login" method="post">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required>

            <label for="password">Password</label>
            <input type="password" id="password" name="password" required>

            <button type="submit">Login</button>
        </form>
    </main>
</body>
</html>"""
    },
    {
        "instruction": "Buatkan HTML responsive dengan navbar dan konten utama",
        "output": """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Responsive</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="logo">Logo</div>
        <ul class="nav-links">
            <li><a href="#home">Beranda</a></li>
            <li><a href="#about">Tentang</a></li>
            <li><a href="#contact">Kontak</a></li>
        </ul>
    </nav>
    <main>
        <section id="home" class="hero">
            <h1>Selamat Datang</h1>
            <p>Ini adalah website responsive sederhana</p>
        </section>
        <section id="about" class="content">
            <h2>Tentang Kami</h2>
            <p>Konten bagian tentang</p>
        </section>
    </main>
    <footer>© 2024 Website Responsive</footer>
</body>
</html>"""
    },

    # === CSS ===
    {
        "instruction": "Buatkan CSS untuk membuat layout card horizontal yang responsif",
        "output": """.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
}

.card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.3s ease;
}

@media (hover: hover) {
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
}

.card-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.card-body {
    padding: 1.5rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.card-text {
    color: #666;
    line-height: 1.6;
}

.card-button {
    display: inline-block;
    padding: 0.5rem 1.5rem;
    background: #2563eb;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}"""
    },
    {
        "instruction": "Buatkan CSS flexbox untuk membuat navbar yang responsive dengan hamburger menu",
        "output": """/* Styling dasar navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #1e293b;
    color: #fff;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-links {
    display: flex;
    gap: 2rem;
    list-style: none;
}

.nav-links a {
    color: #e2e8f0;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #60a5fa;
}

/* Hamburger - default hidden di desktop */
.hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
}

.hamburger span {
    width: 25px;
    height: 3px;
    background: #fff;
    border-radius: 3px;
}

/* Responsive: mobile */
@media (max-width: 768px) {
    .hamburger {
        display: flex;
    }

    .nav-links {
        position: fixed;
        top: 60px;
        right: -100%;
        flex-direction: column;
        background: #1e293b;
        width: 100%;
        text-align: center;
        gap: 0;
        transition: right 0.3s ease;
    }

    .nav-links.active {
        right: 0;
    }

    .nav-links li {
        padding: 1rem;
        border-top: 1px solid #334155;
    }
}"""
    },

    # === JavaScript ===
    {
        "instruction": "Buatkan JavaScript untuk validasi form login sebelum submit",
        "output": """function validateLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    // Reset error
    document.querySelectorAll('.error').forEach(el => el.remove());

    let isValid = true;

    // Validasi email
    if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        showError('email', 'Email tidak valid');
        isValid = false;
    }

    // Validasi password minimal 8 karakter
    if (!password || password.length < 8) {
        showError('password', 'Password minimal 8 karakter');
        isValid = false;
    }

    if (isValid) {
        // Submit ke server
        loginUser(email, password);
    }

    return isValid;
}

function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const error = document.createElement('span');
    error.className = 'error';
    error.style.color = 'red';
    error.style.fontSize = '0.85rem';
    error.textContent = message;
    field.parentElement.appendChild(error);
}

async function loginUser(email, password) {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) throw new Error('Login gagal');

        const data = await response.json();
        localStorage.setItem('token', data.token);
        window.location.href = '/dashboard';
    } catch (error) {
        alert('Terjadi kesalahan: ' + error.message);
    }
}

// Event listener
document.getElementById('loginForm').addEventListener('submit', validateLogin);"""
    },
    {
        "instruction": "Buatkan JavaScript untuk mengambil data dari API dan menampilkannya sebagai list",
        "output": """// Ambil data dari API
async function fetchUsers() {
    try {
        const response = await fetch('https://api.example.com/users', {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        });

        if (!response.ok) throw new Error('Gagal mengambil data');

        const users = await response.json();
        renderUserList(users);
    } catch (error) {
        showError(error.message);
    }
}

// Render list user
function renderUserList(users) {
    const container = document.getElementById('userList');
    container.innerHTML = '';

    users.forEach(user => {
        const item = document.createElement('div');
        item.className = 'user-item';

        item.innerHTML = `
            <div class="user-avatar">${user.name.charAt(0).toUpperCase()}</div>
            <div class="user-info">
                <h3>${user.name}</h3>
                <p>${user.email}</p>
            </div>
            <button class="btn-delete" onclick="deleteUser('${user.id}')">Hapus</button>
        `;

        container.appendChild(item);
    });
}

// Hapus user
async function deleteUser(id) {
    if (!confirm('Yakin ingin menghapus user ini?')) return;

    try {
        const response = await fetch(`https://api.example.com/users/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        });

        if (!response.ok) throw new Error('Gagal menghapus');

        // Refresh list
        fetchUsers();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Init
document.addEventListener('DOMContentLoaded', fetchUsers);"""
    },

    # === React ===
    {
        "instruction": "Buatkan component React functional untuk counter dengan hooks",
        "output": """import React, { useState } from 'react';

export default function Counter() {
    const [count, setCount] = useState(0);

    const increment = () => setCount(prev => prev + 1);
    const decrement = () => setCount(prev => prev - 1);
    const reset = () => setCount(0);

    return (
        <div className="counter">
            <h2>Counter: {count}</h2>
            <div className="counter-buttons">
                <button onClick={decrement} disabled={count === 0}>-</button>
                <button onClick={increment}>+</button>
                <button onClick={reset}>Reset</button>
            </div>
        </div>
    );
}"""
    },
    {
        "instruction": "Buatkan component React untuk form input dengan state management sederhana",
        "output": """import React, { useState } from 'react';

export default function UserForm({ onSubmit }) {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        role: 'user'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Validasi sederhana
        if (!formData.name || !formData.email) {
            alert('Semua field wajib diisi');
            return;
        }
        onSubmit(formData);
        setFormData({ name: '', email: '', role: 'user' });
    };

    return (
        <form onSubmit={handleSubmit} className="user-form">
            <div className="form-group">
                <label>Nama:</label>
                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Nama lengkap"
                />
            </div>

            <div className="form-group">
                <label>Email:</label>
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="email@example.com"
                />
            </div>

            <div className="form-group">
                <label>Role:</label>
                <select name="role" value={formData.role} onChange={handleChange}>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                    <option value="moderator">Moderator</option>
                </select>
            </div>

            <button type="submit" className="btn-primary">Simpan</button>
        </form>
    );
}"""
    },

    # === Vue ===
    {
        "instruction": "Buatkan component Vue 3 dengan Composition API untuk todo list",
        "output": """<template>
  <div class="todo-app">
    <h1>Todo List</h1>
    <form @submit.prevent="addTodo">
      <input
        v-model="newTodo"
        type="text"
        placeholder="Tambahkan tugas..."
        class="todo-input"
      />
      <button type="submit" class="btn-add">Tambah</button>
    </form>

    <ul class="todo-list">
      <li
        v-for="todo in todos"
        :key="todo.id"
        :class="{ done: todo.completed }"
      >
        <input
          type="checkbox"
          :checked="todo.completed"
          @change="toggleTodo(todo.id)"
        />
        <span>{{ todo.text }}</span>
        <button @click="deleteTodo(todo.id)" class="btn-delete">X</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newTodo = ref('');
const todos = ref([]);

const addTodo = () => {
  if (!newTodo.value.trim()) return;

  todos.value.push({
    id: Date.now(),
    text: newTodo.value.trim(),
    completed: false
  });

  newTodo.value = '';
};

const toggleTodo = (id) => {
  const todo = todos.value.find(t => t.id === id);
  if (todo) todo.completed = !todo.completed;
};

const deleteTodo = (id) => {
  todos.value = todos.value.filter(t => t.id !== id);
};
</script>

<style scoped>
.todo-app {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1rem;
}

.todo-list {
  list-style: none;
  padding: 0;
}

.todo-list li {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}

.todo-list li.done span {
  text-decoration: line-through;
  color: #999;
}
</style>"""
    },

    # === Flutter ===
    {
        "instruction": "Buatkan widget Flutter sederhana untuk login form",
        "output": """import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _login() {
    if (_formKey.currentState?.validate() ?? false) {
      // TODO: panggil API login
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Login berhasil')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  prefixIcon: Icon(Icons.email),
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Email wajib diisi';
                  }
                  if (!value.contains('@')) {
                    return 'Email tidak valid';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                obscureText: _obscurePassword,
                decoration: InputDecoration(
                  labelText: 'Password',
                  prefixIcon: const Icon(Icons.lock),
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword
                          ? Icons.visibility
                          : Icons.visibility_off,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscurePassword = !_obscurePassword;
                      });
                    },
                  ),
                ),
                validator: (value) {
                  if (value == null || value.length < 8) {
                    return 'Password minimal 8 karakter';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _login,
                  child: const Text('Masuk'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}"""
    },
    {
        "instruction": "Buatkan widget Flutter untuk menampilkan list data dari API",
        "output": """import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class UserListPage extends StatefulWidget {
  const UserListPage({super.key});

  @override
  State<UserListPage> createState() => _UserListPageState();
}

class _UserListPageState extends State<UserListPage> {
  List<dynamic> _users = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchUsers();
  }

  Future<void> _fetchUsers() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final response = await http.get(
        Uri.parse('https://api.example.com/users'),
      );

      if (response.statusCode == 200) {
        setState(() {
          _users = jsonDecode(response.body);
          _loading = false;
        });
      } else {
        throw Exception('Gagal memuat data');
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Daftar User')),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Error: $_error'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _fetchUsers,
              child: const Text('Coba Lagi'),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _fetchUsers,
      child: ListView.builder(
        itemCount: _users.length,
        itemBuilder: (context, index) {
          final user = _users[index];
          return ListTile(
            leading: CircleAvatar(
              child: Text(user['name'][0].toUpperCase()),
            ),
            title: Text(user['name']),
            subtitle: Text(user['email']),
            trailing: IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () {
                // TODO: hapus user
                setState(() {
                  _users.removeAt(index);
                });
              },
            ),
          );
        },
      ),
    );
  }
}"""
    },

    # === React Native ===
    {
        "instruction": "Buatkan komponen React Native untuk login screen menggunakan hooks",
        "output": """import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    // Validasi
    if (!email || !password) {
      Alert.alert('Error', 'Email dan password wajib diisi');
      return;
    }

    setLoading(true);
    try {
      // TODO: panggil API login
      // const res = await api.post('/login', { email, password });
      setLoading(false);
      navigation.navigate('Home');
    } catch (error) {
      setLoading(false);
      Alert.alert('Login Gagal', error.message);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={styles.form}>
        <Text style={styles.title}>Masuk</Text>

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
          onPress={handleLogin}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'Memuat...' : 'Masuk'}
          </Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  form: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
    color: '#1e293b',
  },
  input: {
    height: 50,
    backgroundColor: '#fff',
    borderRadius: 8,
    paddingHorizontal: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  button: {
    height: 50,
    backgroundColor: '#2563eb',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});"""
    },

    # === Instalasi & Penyiapan Project ===
    {
        "instruction": "Perintah untuk membuat project React baru dengan Vite",
        "output": """## Instalasi

# Buat project dengan Vite
npm create vite@latest my-app -- --template react

# Masuk folder
cd my-app

# Install dependencies
npm install

# Jalankan development server
npm run dev

# Build untuk production
npm run build

# Struktur project yang dihasilkan
my-app/
├── node_modules/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
└── README.md"""
    },
    {
        "instruction": "Perintah untuk membuat project Flutter baru",
        "output": """## Membuat Project Flutter Baru

# Buat project baru
flutter create my_app

# Masuk folder project
cd my_app

# Jalankan di Chrome (web)
flutter run -d chrome

# Jalankan di Android emulator
flutter run -d android

# Build APK release
flutter build apk --release

# Struktur project yang dihasilkan
my_app/
├── android/
├── ios/
├── lib/
│   └── main.dart
├── test/
├── pubspec.yaml
└── README.md"""
    },
    {
        "instruction": "Perintah untuk setup project React Native dengan Expo",
        "output": """## Membuat Project React Native dengan Expo

# Install Expo CLI (jika belum ada)
npm install -g expo-cli

# Buat project baru
npx create-expo-app my-app

# Masuk folder
cd my-app

# Jalankan development server
npx expo start

# Jalankan di Android
npx expo start --android

# Jalankan di iOS
npx expo start --ios

# Build APK
expo build:android"""
    },

    # === Bug Fixes & Best Practices ===
    {
        "instruction": "Apa cara terbaik untuk mengelola state global di React?",
        "output": """## State Global di React

### 1. Context API (untuk state kecil)
```javascript
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth harus dipakai dalam AuthProvider');
  }
  return context;
}
```

### 2. Zustand (untuk state menengah, ringan)
```bash
npm install zustand
```

```javascript
import { create } from 'zustand';

const useStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));

// Penggunaan di komponen
const user = useStore((state) => state.user);
const setUser = useStore((state) => state.setUser);
```

### 3. Redux Toolkit (untuk state kompleks skala besar)
```bash
npm install @reduxjs/toolkit react-redux
```

```javascript
import { configureStore, createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null },
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
    },
  },
});

export const { setUser } = authSlice.actions;
export default configureStore({
  reducer: {
    auth: authSlice.reducer,
  },
});
```

### Rekomendasi
- **State kecil**: Context API
- **State menengah**: Zustand (ringan, mudah)
- **State besar/kompleks**: Redux Toolkit"""
    },
]

# ============ Logika Utama ============

def load_raw_data(raw_dir="data/raw"):
    """Muat data dari file raw jika ada."""
    raw_data = []
    if os.path.isdir(raw_dir):
        for fname in sorted(os.listdir(raw_dir)):
            if fname.endswith('.jsonl'):
                fpath = os.path.join(raw_dir, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                raw_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                print(f"  [skip] baris tidak valid: {line[:50]}...")
    return raw_data


def format_for_training(example):
    """Format contoh jadi format training (instruction/output)."""
    if 'instruction' in example and 'output' in example:
        return example
    # Jika raw punya 'prompt'/'completion' (format lama)
    if 'prompt' in example and 'completion' in example:
        return {
            "instruction": example["prompt"],
            "output": example["completion"]
        }
    return None


def build_chat_format(instruction, output):
    """Bangun format chat untuk model TinyLlama."""
    return {
        "prompt": f"### Instruction:\n{instruction}\n\n### Response:\n",
        "completion": output,
        "chosen": output,
        "rejected": "",
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": output}
        ]
    }


def main():
    print("=" * 60)
    print("minx - Step 2: Prepare Dataset")
    print("=" * 60)

    raw_dir = "data/raw"
    processed_dir = "data/processed"
    out_path = os.path.join(processed_dir, "minx_train.jsonl")

    os.makedirs(processed_dir, exist_ok=True)

    # 1. Muat raw data (jika ada)
    raw_data = load_raw_data(raw_dir)
    print(f"\n[1] Raw data dari files: {len(raw_data)} contoh")
    if not raw_data:
        print("    (kosong, akan pakai template bawaan)")

    # 2. Gabungkan dengan builtin template
    combined = list(BUILTIN_DATA)
    for item in raw_data:
        formatted = format_for_training(item)
        if formatted:
            combined.append(formatted)

    print(f"\n[2] Total data setelah gabung: {len(combined)} contoh")

    # 3. Format & random shuffle
    train_examples = []
    for ex in combined:
        formatted = build_chat_format(ex['instruction'], ex['output'])
        train_examples.append(formatted)

    random.seed(42)
    random.shuffle(train_examples)

    # 4. Tulis ke JSONL
    with open(out_path, 'w', encoding='utf-8') as f:
        for ex in train_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')

    print(f"\n[3] Dataset tersimpan: {out_path}")
    print(f"    Total baris: {len(train_examples)}")

    # 5. Ringkasan
    languages = {}
    for ex in combined:
        output = ex['output'].lower()
        if 'flutter' in output or 'dart' in output:
            lang = 'Flutter/Dart'
        elif 'react native' in output:
            lang = 'React Native'
        elif 'react' in output:
            lang = 'React'
        elif 'vue' in output:
            lang = 'Vue'
        elif 'html' in output:
            lang = 'HTML'
        elif 'css' in output or '<style' in output:
            lang = 'CSS'
        elif 'javascript' in output or 'async function' in output:
            lang = 'JavaScript'
        else:
            lang = 'Umum'
        languages[lang] = languages.get(lang, 0) + 1

    print("\n[4] Distribusi dataset:")
    for lang, count in sorted(languages.items(), key=lambda x: -x[1]):
        print(f"    {lang}: {count}")

    print("\nSelesai. Dataset siap untuk training (Step 3).")


if __name__ == "__main__":
    main()
