# Paramine Framework

Paramine is an automated web reconnaissance, parameter discovery, fuzzing, and smart vulnerability scanning framework written in Python.

It is designed for:
- bug bounty hunters
- web pentesters
- red teamers
- reconnaissance workflows
- archived parameter mining
- smart payload testing

Uses:
- waybackurls
- gau
- Playwright

---

# Features

## Recon Engine
- Extracts URLs from:
  - Wayback Machine
  - gau
- Filters parameterized URLs
- Finds unique parameters
- Checks alive URLs
- Saves organized outputs

---

## FUZZ Engine
- Replaces parameter values
- Fuzzes one parameter at a time
- Preserves original values of other parameters
- Supports duplicate removal
- Generates ready-to-use FUZZ URLs

---

## Manual Vulnerability Scan
- Uses custom payload files
- Supports:
  - XSS
  - SQLi
  - LFI
  - RFI
- Reflection detection
- Screenshot support

---

## Smart Scan Engine
Automatically selects payloads based on parameter names.

Examples:

| Parameter | Payload Type |
|---|---|
| id | SQLi |
| file | LFI |
| page | LFI |
| q | XSS |
| search | XSS |
| redirect | Open Redirect |

---

## Screenshot Engine
- Automatic browser screenshots
- Uses Chromium
- Auto-heals Playwright environment
- Saves screenshots for:
  - reflections
  - possible vulnerabilities
  - suspicious responses

---

## Resume System
- Resume interrupted scans
- Avoid retesting payloads
- Uses cache system

---

## Workspace System
- Centralized output management
- Multiple projects supported
- Drag & drop paths supported

---

# Project Structure


paramine/
│
├── main.py
├── requirements.txt
│
├── core/
│   ├── alive.py
│   ├── cache.py
│   ├── detector.py
│   ├── filter.py
│   ├── injector.py
│   ├── logger.py
│   ├── mutator.py
│   ├── output.py
│   ├── payloads.py
│   ├── providers.py
│   ├── screenshot.py
│   ├── setup.py
│   └── smart_selector.py
│
└── payloads/

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/whiteseccybersecurity/paramine.git

cd paramine
```

---

# 2. Create Virtual Environment

```bash
python -m venv venv
```

---

# 3. Activate Virtual Environment

## Linux/macOS

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

---

# 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

# 5. Install Go

Required for:

* waybackurls
* gau

Download:

* [https://go.dev/dl/](https://go.dev/dl/)

Verify:

```bash
go version
```

---

# Running Paramine

```bash
python main.py
```

---

# Main Menu

```txt
PARAMINE FRAMEWORK

1. Recon
2. FUZZ
3. Manual Scan
4. Smart Scan
5. Help
```

---

# Recon Mode

Purpose:

* URL extraction
* parameter discovery
* alive checking

---

## Example

```txt
Select: 1

Quiet mode? (y/n): n

Resume previous scan if exists? (y/n): n

1. Single Domain  2. List:
1

Enter domain:
testphp.vulnweb.com

Threads (20):
50
```

---

# Recon Process

Paramine:

1. Runs:

   * waybackurls
   * gau
2. Extracts archived URLs
3. Filters parameter URLs
4. Checks alive endpoints
5. Saves outputs

---

# Recon Output

```bash
workspace/
└── testphp.vulnweb.com/
    ├── all_wayback.txt
    ├── all_params.txt
    ├── alive_params.txt
    ├── unique_params.txt
    ├── param_patterns.txt
    └── .cache.json
```

---

# File Descriptions

| File               | Description                |
| ------------------ | -------------------------- |
| all_wayback.txt    | All extracted URLs         |
| all_params.txt     | URLs containing parameters |
| alive_params.txt   | Alive parameter URLs       |
| unique_params.txt  | Unique parameter names     |
| param_patterns.txt | Parameter patterns         |
| .cache.json        | Resume cache               |

---

# FUZZ Mode

Purpose:

* Replace parameter values
* Generate fuzz-ready URLs

---

## Example

```txt
Select: 2

Drag & drop URL file:
/home/kali/results/alive_params.txt

Project name:
nokia

Value (default FUZZ):
FUZZ

Remove duplicate URLs? (y/n):
y
```

---

# FUZZ Example

## Original

```txt
https://site.com/page?id=1&cat=2
```

## Generated

```txt
https://site.com/page?id=FUZZ&cat=2

https://site.com/page?id=1&cat=FUZZ
```

Each parameter is fuzzed separately.

---

# FUZZ Output

```bash
workspace/
└── testphp/
    └── fuzzed.txt
```

---

# Manual Scan

Purpose:

* Use custom payload lists
* Manual testing workflow

---

## Example

```txt
Select: 3

Drag & drop URL file:
/home/kali/results/alive_params.txt

Project name:
semrush

Enable screenshots? (y/n):
y

Use payload file? (y/n):
y

Payload file path:
/home/kali/payloads/xss.txt
```

---

# Payload Example

## xss.txt

```txt
<script>alert(1)</script>
"><svg/onload=alert(1)>
```

---

# Smart Scan

Purpose:

* Automatic vulnerability testing
* Smart payload selection
* Parameter-aware testing

---

# Example

```txt
Select: 4

Drag & drop URL file:
/home/kali/results/alive_params.txt

Project name:
nokia

Enable screenshots? (y/n):
y
```

---

# Smart Scan Logic

Paramine automatically:

* analyzes parameter names
* selects payload categories
* mutates payloads
* tests one parameter at a time

---

# Example

## Original URL

```txt
https://site.com/page?id=1&search=test
```

---

## SQLi Test

```txt
https://site.com/page?id='&search=test
```

---

## XSS Test

```txt
https://site.com/page?id=1&search=<script>alert(1)</script>
```

Other parameters remain unchanged.

---

# Detection Engine

Paramine uses heuristic detection.

Supports:

* reflection detection
* possible XSS detection
* SQL error detection
* LFI pattern detection
* RFI reflection detection

---

# Important Note

Current detections are:

```txt
heuristic detections
```

NOT guaranteed exploitation.

Example:

```txt
[POSSIBLE_XSS]
```

means:

* payload reflected
* suspicious response detected

NOT:

* confirmed JavaScript execution

---

# Screenshot System

Screenshots are taken when:

* reflection detected
* possible vulnerability detected

Saved in:

```bash
screenshots/
```

Example:

```bash
workspace/
└── testphp.vulnweb.com/
    └── screenshots/
        ├── 123456789.png
        ├── 987654321.png
```

---

# Resume System

Paramine supports interrupted scan recovery.

Example:

```txt
Resume previous scan if exists? (y/n): y
```

Uses:

```bash
.cache.json
```

Avoids:

* duplicate requests
* retesting payloads
* rescanning finished targets

---

# Quiet Mode

Suppresses verbose logs.

```txt
Quiet mode? (y/n): y
```

Only shows:

* vulnerabilities
* important findings

---

# Workspace System

When starting:

```txt
Enter workspace folder:
```

Example:

```txt
/home/kali/Desktop/results
```

All results stored centrally.

---

# Multi-Domain Recon

Create:

## domains.txt

```txt
example.com
testphp.vulnweb.com
demo.testfire.net
```

Run:

```txt
Select: 1

1. Single Domain  2. List:
2
```

---

# Example Workflow

## Step 1 — Recon

```txt
Select: 1
```

Produces:

```bash
alive_params.txt
```

---

## Step 2 — FUZZ

```txt
Select: 2
```

Use:

```bash
alive_params.txt
```

---

## Step 3 — Smart Scan

```txt
Select: 4
```

Scans:

* XSS
* SQLi
* LFI
* RFI
* reflections

---

# Recommended Targets

Safe testing targets:

* testphp.vulnweb.com
* demo.testfire.net

---

# Performance Notes

Large enterprise targets:

* generate massive URL lists
* increase scan duration
* increase payload combinations

Recommended:

* start with smaller datasets
* use dedupe mode
* use quiet mode for large scans

---

# Current Limitations

Paramine currently does NOT:

* confirm JavaScript execution
* detect DOM XSS
* detect blind XSS
* bypass CSP
* perform browser exploitation
* execute authenticated workflows

Detection is:

```txt
response-based heuristic analysis
```

---

# Future Improvements

Planned:

* real browser XSS confirmation
* DOM XSS engine
* async queue system
* blind XSS support
* custom headers
* proxy support
* Burp integration
* nuclei template support
* JS endpoint extraction
* API endpoint analysis

---

# Legal Disclaimer

Paramine is intended for:

* authorized security testing
* bug bounty programs
* educational use

Do NOT use against systems without permission.
