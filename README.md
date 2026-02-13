# Real Estate Deal Pipeline

A tool that extracts deal information from real estate news articles and broker PDFs, then saves it to Excel files for easy tracking.

**Works with:** Sweden, Denmark, and Finland real estate deals

---

# Viktor's Setup Guide

This guide gives you the exact commands to copy and paste. No thinking required.

---

## How This Tool Works

**Two processes, one output file:**

| Process | Input | Output Sheet |
|---------|-------|--------------|
| Process 1 | PDFs (IMs, Teasers) | "Deal list" |
| Process 2 | News article URLs | "Sweden" / "Denmark" / "Finland" |

Everything goes into **one file**: `output/deals.xlsx`

Each time you run a command, the new deal gets **added** to the existing file. By Friday, all your deals are collected!

---

## One-Time Setup (Do This First)

### Step 1: Install Python

1. Go to: **https://www.python.org/downloads/**
2. Click the yellow **"Download Python"** button
3. Run the installer
4. **IMPORTANT:** Check the box **"Add Python to PATH"** at the bottom
5. Click **"Install Now"**

### Step 2: Get an Anthropic API Key

1. Go to: **https://console.anthropic.com/**
2. Create an account and log in
3. Click **"API Keys"** → **"Create Key"**
4. Copy the key (starts with `sk-ant-`)
5. Save it somewhere (you'll need it every time)

### Step 3: Install Required Packages

1. Press **Windows key**, type **cmd**, press **Enter**
2. Copy and paste this command:

```
cd C:\Users\vilu\Desktop\real-estate-deal-pipeline && pip install -r requirements.txt
```

3. Press **Enter** and wait for it to finish

---

## Every Time You Use the Tool

### Step 1: Open Command Prompt in the Program Folder

1. Press **Windows key**
2. Type **cmd**
3. Press **Enter**
4. Copy and paste this command:

```
cd C:\Users\vilu\Desktop\real-estate-deal-pipeline
```

5. Press **Enter**

### Step 2: Set Your API Key

Copy and paste this command (replace `YOUR-KEY-HERE` with your actual API key):

```
set ANTHROPIC_API_KEY=YOUR-KEY-HERE
```

**Example (not a real key):**
```
set ANTHROPIC_API_KEY=sk-ant-api03-ABC123xyz456DEF789
```

---

## Process 1: Extract from PDFs (Incoming Deals)

### Option A: Process ONE PDF

Copy and paste this command (change the PDF path to your actual file):

```
python -m src.cli process-pdf-file --input "C:\Users\vilu\Desktop\your_file.pdf"
```

**Result:** Added to "Deal list" sheet in `output/deals.xlsx`

---

### Option B: Process MULTIPLE PDFs at Once (Batch)

This is the easiest way to process many PDFs. Follow these steps exactly:

#### Step 1: Create a folder for your PDFs

1. Go to your Desktop
2. Right-click → **New** → **Folder**
3. Name it exactly: **PDFs**

So now you have a folder at: `C:\Users\vilu\Desktop\PDFs`

#### Step 2: Put your PDF files in that folder

1. Copy all the PDFs you want to process
2. Paste them into `C:\Users\vilu\Desktop\PDFs`

#### Step 3: Open Command Prompt and go to the program folder

1. Press **Windows key**
2. Type **cmd**
3. Press **Enter**
4. Copy and paste:

```
cd C:\Users\vilu\Desktop\real-estate-deal-pipeline
```

5. Press **Enter**

#### Step 4: Set your API key

Copy and paste (use your real key):

```
set ANTHROPIC_API_KEY=sk-ant-api03-YOUR-ACTUAL-KEY-HERE
```

Press **Enter**

#### Step 5: Run the batch command

Copy and paste this exact command:

```
python -m src.cli process-pdf-folder --folder "C:\Users\vilu\Desktop\PDFs"
```

Press **Enter**

#### What happens:

- The program will show progress like: `[1/5] document1.pdf ... OK`
- When done, you'll see: `Added to sheet 'Deal list' in output/deals.xlsx`
- All your deals are now in the Excel file!

#### Optional: Set a date for all PDFs

If you want to set a "date received" for all the PDFs:

```
python -m src.cli process-pdf-folder --folder "C:\Users\vilu\Desktop\PDFs" --date "2024/02/12"
```

---

## Process 2: Extract from Article URLs (Transactions)

For each article you want to process, copy and paste this command (change the URL):

```
python -m src.cli process-url --url "https://www.fastighetsvarlden.se/notiser/YOUR-ARTICLE-URL/"
```

**Result:** Added to "Sweden" (or Denmark/Finland) sheet in `output/deals.xlsx`

**Processing multiple articles:** Just run the command again with a different URL. Each one gets added to the file.

---

## Finding Your Output

Your Excel file is here:

```
C:\Users\vilu\Desktop\real-estate-deal-pipeline\output\deals.xlsx
```

**To open it:**
1. Open File Explorer
2. Go to: Desktop → real-estate-deal-pipeline → output
3. Double-click `deals.xlsx`

---

## The Output File Has 4 Sheets

```
deals.xlsx
├── Deal list   ← All PDFs go here
├── Sweden      ← Swedish articles go here
├── Denmark     ← Danish articles go here
└── Finland     ← Finnish articles go here
```

---

## Quick Reference (Copy-Paste Commands)

**Go to program folder:**
```
cd C:\Users\vilu\Desktop\real-estate-deal-pipeline
```

**Set API key:**
```
set ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
```

**Process one PDF:**
```
python -m src.cli process-pdf-file --input "C:\Users\vilu\Desktop\your_file.pdf"
```

**Process all PDFs in a folder:**
```
python -m src.cli process-pdf-folder --folder "C:\Users\vilu\Desktop\PDFs"
```

**Process an article URL:**
```
python -m src.cli process-url --url "https://example.com/article"
```

---

## Weekly Workflow

### Throughout the week:

**When you get a PDF from a broker:**
1. Put it in `C:\Users\vilu\Desktop\PDFs`
2. Run the batch command (or process individually)

**When you see a transaction article:**
1. Copy the URL
2. Run the process-url command

### On Friday:

1. Open `output/deals.xlsx`
2. Everything is organized into the correct sheets
3. Copy-paste into your presentation

---

## Troubleshooting

### "python is not recognized"
Reinstall Python and check "Add Python to PATH"

### "No module named src"
You're not in the right folder. Run:
```
cd C:\Users\vilu\Desktop\real-estate-deal-pipeline
```

### "ANTHROPIC_API_KEY not set"
Run this again (with your real key):
```
set ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
```

### "File not found"
Check the file path is correct. You can drag and drop files into Command Prompt to paste their path.

### Starting fresh with a new file
Delete the old file and run any command:
```
del output\deals.xlsx
```

---

## What Gets Extracted

### From PDFs (Deal list sheet):
- Date received, Week number
- Project Name, Type (IM/Teaser)
- Country, Location, Address
- Property type, Area
- NOI, Yield, Occupancy, WAULT
- Deal value, Comments

### From Articles (Country sheets):
- Date, Buyer, Seller
- Country, Location
- Property type, Area
- Price (in millions), Price per sqm
- Yield, Comments, Source URL

---

## Output Details

- **Price is in millions** — 743 MSEK shows as "743"
- **Week number is auto-calculated** from the date
- **Price per sqm is auto-calculated** from price and area
- **Property types are normalized** — "warehouse" becomes "Logistics"
- **Cities are translated** — Göteborg → Gothenburg
