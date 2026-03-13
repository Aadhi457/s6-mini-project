# 🔍 Malware Scanner & Scraper Professional

A powerful, YARA-based malware detection suite featuring a clean Python backend and a modern Flask-powered web dashboard.

## 🚀 Features

- **Robust YARA Scanning**: Pre-compiled rules for high-performance file analysis.
- **Recursive Directory Scan**: Scans nested directories for malicious signatures.
- **Web Dashboard**: Modern, responsive UI for triggering scans and viewing detailed reports.
- **Content Scraper**: Download files directly from URLs and automatically scan them for threats.
- **Extensible Rule Set**: Easy to add new `.yar` rules to the `rules/` directory.

## 🛠️ Tech Stack

- **Backend**: Python 3.11
- **Detection**: [YARA-python](https://github.com/VirusTotal/yara-python)
- **Web Interface**: Flask + Bootstrap 5
- **Scraping**: BeautifulSoup4 + Requests

## 📦 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Scanner (CLI)
```bash
python3 scanner.py
```

### 3. Run the Web Dashboard
```bash
python3 app.py
```
Visit `http://localhost:5000` in your browser.

## 📂 Project Structure

- `app.py`: Flask web application and routes.
- `scanner.py`: Core `MalwareScanner` class for YARA analysis.
- `scraper.py`: `ContentScraper` for fetching remote files.
- `rules/`: Contains YARA rule definitions (`malware_rules.yar`).
- `samples/`: Target directory for scanning (includes test samples).
- `templates/`: HTML layouts for the web dashboard.

## 🛡️ Malware Detection Rules
The system detects various threats including:
- **Process Injection** (VirtualAllocEx, WriteProcessMemory, etc.)
- **Keyloggers** (GetAsyncKeyState, SetWindowsHookEx)
- **Ransomware Indicators** (Bitcoin, Ransom, Encryption strings)
- **Suspicious PowerShell & Scripting** (Encoded commands, base64, etc.)
- **Packed Executables** (UPX, etc.)

---
*Disclaimer: This tool is for educational and security research purposes only.*
