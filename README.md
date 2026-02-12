# Real Estate Deal Pipeline

A tool that extracts deal information from real estate news articles and broker PDFs, then saves it to Excel files for easy tracking.

**Works with:** Sweden, Denmark, and Finland real estate deals

---

# Complete Setup Guide for Viktor's monkey brain

This guide will walk you through every step to get this program running on your Windows computer. Follow each step carefully.

---

## How This Tool Works (Overview)

This tool handles **two separate processes** that match your Friday presentation workflow:

### Process 1: Incoming Deals (PDFs)
- **Input:** PDF documents from brokers (IMs, Teasers)
- **Output:** Goes to the **"Deal list"** sheet
- **Use case:** Tracking deals that are being marketed but haven't closed yet

### Process 2: Completed Transactions (Articles)
- **Input:** News articles about completed deals
- **Output:** Goes to country-specific sheets: **"Sweden"**, **"Denmark"**, or **"Finland"**
- **Use case:** Tracking transactions that have already happened

**One file, four sheets:**
```
output/deals.xlsx
├── Deal list   (Process 1 - all your PDFs go here)
├── Sweden      (Process 2 - Swedish article deals)
├── Denmark     (Process 2 - Danish article deals)
└── Finland     (Process 2 - Finnish article deals)
```

**The magic:** Each time you run a command, the new deal is **added** to the correct sheet in the same file. Run it throughout the week, and by Friday everything is collected in one place!

---

## Step 1: Install Python

Python is the programming language this tool uses. You need to install it first.

### 1.1 Download Python

1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow button that says **"Download Python 3.x.x"** (any version 3.9 or higher is fine)
3. Save the file to your Downloads folder

### 1.2 Install Python

1. Open your Downloads folder
2. Double-click the file you just downloaded (it will be named something like `python-3.12.x-amd64.exe`)
3. **IMPORTANT:** On the first screen, check the box that says **"Add Python to PATH"** at the bottom
4. Click **"Install Now"**
5. Wait for the installation to complete
6. Click **"Close"**

### 1.3 Verify Python is Installed

1. Press the **Windows key** on your keyboard
2. Type **cmd** and press Enter (this opens Command Prompt)
3. Type the following and press Enter:

```
python --version
```

You should see something like `Python 3.12.4`. If you see this, Python is installed correctly.

**If you see an error:** Close Command Prompt, restart your computer, and try again.

---

## Step 2: Get an Anthropic API Key

This tool uses Claude AI to read and understand the documents. You need an API key to use it.

**Already have an API key?** Skip to [Step 3](#step-3-download-this-program).

### 2.1 Create an Anthropic Account

1. Go to: **https://console.anthropic.com/**
2. Click **"Sign Up"** and create an account (you can use your email or Google account)
3. Verify your email if required

### 2.2 Get Your API Key

1. After logging in, click on **"API Keys"** in the left menu
2. Click **"Create Key"**
3. Give it a name like "Deal Pipeline" and click **"Create Key"**
4. **IMPORTANT:** Copy the key that appears. It starts with `sk-ant-` and is very long
5. Save this key somewhere safe (like a text file or password manager). You will need it later.

**Note:** You will need to add payment information to your Anthropic account. Each document processed costs a few cents.

---

## Step 3: Download This Program

### Option A: Download as ZIP (Easiest)

1. On this GitHub page, click the green **"Code"** button near the top
2. Click **"Download ZIP"**
3. Save the file to your Downloads folder
4. Open your Downloads folder
5. Right-click the ZIP file and select **"Extract All..."**
6. Choose a location you'll remember, like your Desktop or Documents folder
7. Click **"Extract"**

You now have a folder called `nordics-real-estate-automation-main` (or similar).

### Option B: Using Git (Advanced)

If you have Git installed, open Command Prompt and run:

```
cd %USERPROFILE%\Documents
git clone https://github.com/YOUR-USERNAME/nordics-real-estate-automation.git
```

---

## Step 4: Open Command Prompt in the Program Folder

1. Open the folder where you extracted the program (for example: `Documents\nordics-real-estate-automation-main`)
2. Click in the address bar at the top of the File Explorer window (where it shows the folder path)
3. Type **cmd** and press Enter

This opens Command Prompt directly in the program folder.

**Alternative method:**
1. Press the Windows key
2. Type **cmd** and press Enter
3. Type the following (adjust the path to match where you saved the folder):

```
cd %USERPROFILE%\Documents\nordics-real-estate-automation-main
```

---

## Step 5: Install Required Packages

With Command Prompt open in the program folder, type the following and press Enter:

```
pip install -r requirements.txt
```

Wait for everything to install. You'll see a lot of text scrolling. When it's done, you'll see the blinking cursor again.

**If you see an error about pip:** Try running:
```
python -m pip install -r requirements.txt
```

---

## Step 6: Set Up Your API Key

You need to tell the program your Anthropic API key. Type the following command, replacing `YOUR-API-KEY-HERE` with the key you saved in Step 2:

```
set ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Important Notes:**
- Do NOT put quotes around the key
- Do NOT put spaces around the `=` sign
- The key should start with `sk-ant-`
- You need to run this command every time you open a new Command Prompt window

**Example (not a real key):**
```
set ANTHROPIC_API_KEY=sk-ant-api03-ABC123xyz456DEF789ghi012JKL345mno678PQR901stu234VWX567yza890
```

---

## Step 7: Run the Program

Now you're ready to use the program! There are three main ways to use it:

---

### Option 1: Process a News Article URL (Process 2 - Transactions)

Use this to extract deal information from a real estate news article on the web.

**Important:**
- This processes ONE article at a time
- The deal will be automatically added to the correct country sheet (Sweden/Denmark/Finland)
- Each run **adds** to the existing file (it doesn't overwrite previous deals)

**Command format:**
```
python -m src.cli process-url --url "PASTE-ARTICLE-URL-HERE"
```

**Example with a real URL:**
```
python -m src.cli process-url --url "https://www.fastighetsvarlden.se/notiser/heimstaden-saljer-for-en-miljard/"
```

**What happens:**
1. The program reads the article
2. Extracts deal information (buyer, seller, price, location, property type, etc.)
3. Figures out which country it's for (Sweden, Denmark, or Finland)
4. **Adds** it to the correct sheet in `output/deals.xlsx`

**After it runs:** You'll see something like:
```
Done. Added to sheet 'Sweden' in output/deals.xlsx
```

**Processing multiple articles:** Just run the command again with a different URL. Each deal gets added to the same file!

```
python -m src.cli process-url --url "https://example.com/article1"
python -m src.cli process-url --url "https://example.com/article2"
python -m src.cli process-url --url "https://example.com/article3"
```

All three deals will be in `output/deals.xlsx`, each on the correct country sheet.

---

### Option 2: Process a Single PDF (Process 1 - Incoming Deals)

Use this to extract deal information from a PDF document (like a broker teaser or IM).

**Important:**
- PDFs go to the **"Deal list"** sheet (not the country sheets)
- Each run **adds** to the existing file (it doesn't overwrite previous deals)

**Command format:**
```
python -m src.cli process-pdf-file --input "PATH-TO-YOUR-PDF"
```

**Example (if your PDF is on the Desktop):**
```
python -m src.cli process-pdf-file --input "%USERPROFILE%\Desktop\property_teaser.pdf"
```

**Example (if your PDF is in Documents):**
```
python -m src.cli process-pdf-file --input "%USERPROFILE%\Documents\broker_im.pdf"
```

**What happens:**
1. The program reads the PDF text
2. Extracts deal information (property name, location, NOI, yield, area, etc.)
3. **Adds** it to the "Deal list" sheet in `output/deals.xlsx`

**After it runs:** You'll see:
```
Done. Added to sheet 'Deal list' in output/deals.xlsx
```

**Tip:** You can drag and drop a PDF file into the Command Prompt window to paste its full path.

**Optional: Set a "date received":**
```
python -m src.cli process-pdf-file --input "path\to\file.pdf" --date "2024/01/15"
```

---

### Option 3: Process Multiple PDFs at Once (Batch)

Use this to process all PDF files in a folder at once.

**Command format:**
```
python -m src.cli process-pdf-folder --folder "PATH-TO-FOLDER"
```

**Example (if your PDFs are in a folder called "PDFs" on your Desktop):**
```
python -m src.cli process-pdf-folder --folder "%USERPROFILE%\Desktop\PDFs"
```

**Example (if your PDFs are in Documents):**
```
python -m src.cli process-pdf-folder --folder "%USERPROFILE%\Documents\Deal_PDFs"
```

**What happens:**
1. The program finds all PDF files in the folder
2. Processes each one (showing progress as it goes)
3. **Adds** all deals to the "Deal list" sheet in `output/deals.xlsx`

**After it runs:** You'll see:
```
Processed 5 PDFs: 5 success, 0 failed
Added to sheet 'Deal list' in output/deals.xlsx
```

**Optional settings:**
- `--max 10` — Only process the first 10 PDFs (default is 20)
- `--date "2024/01/15"` — Set a "date received" for all deals

**Example with options:**
```
python -m src.cli process-pdf-folder --folder "%USERPROFILE%\Desktop\PDFs" --max 10 --date "2024/02/01"
```

---

## The Output File Structure

Everything goes into **one Excel file** with **four sheets**:

```
output/deals.xlsx
│
├── Deal list    ← All PDFs go here (Process 1 - Incoming deals)
│                  This matches your purple "Deal list" sheet
│
├── Sweden       ← Swedish articles go here (Process 2)
│                  Columns: Country, Date, Buyer, Seller, Location,
│                           Property type, Price (MSEK), Area, Yield, etc.
│
├── Denmark      ← Danish articles go here (Process 2)
│                  Columns: Country, Date, Buyer, Seller, Location,
│                           Property type, Price (MDKK), Area, etc.
│
└── Finland      ← Finnish articles go here (Process 2)
                   Columns: Source, Country, Date, Buyer, Seller,
                            Location, Property type, Price (MEUR), etc.
```

**Important notes about the output:**

1. **Column order matches your Excel sheets** — You can copy-paste directly into your presentation

2. **Each country has its own column layout** — Sweden uses MSEK, Denmark uses MDKK, Finland uses MEUR

3. **Price is in millions** — A 743 million SEK deal shows as "743" (not "743000000")

4. **Week number is auto-calculated** — Based on the date

5. **Price per sqm is auto-calculated** — Based on price and area

6. **Property types are normalized** — "warehouse", "lager", "logistics" all become "Logistics"

7. **City names are translated** — Göteborg → Gothenburg, København → Copenhagen

---

## Finding Your Output Files

All your deals are saved in the `output` folder inside the program folder.

**To open your output:**
1. Open File Explorer
2. Navigate to the program folder (e.g., `Documents\nordics-real-estate-automation-main`)
3. Open the `output` folder
4. Double-click `deals.xlsx` to open it in Excel

**First time running?** The file will be created automatically when you process your first deal.

**Starting fresh?** If you want to start over with a new file, simply delete `output/deals.xlsx` and run any command again.

---

## Typical Weekly Workflow

Here's how to use this tool for your Friday presentation:

### Throughout the week:

**When you get a new PDF from a broker:**
```
python -m src.cli process-pdf-file --input "path\to\new_im.pdf" --date "2024/02/10"
```
→ Adds to "Deal list" sheet

**When you see a transaction article:**
```
python -m src.cli process-url --url "https://fastighetsvarlden.se/article..."
```
→ Adds to "Sweden" (or Denmark/Finland) sheet

### On Friday:

1. Open `output/deals.xlsx`
2. All your deals are already organized into the correct sheets
3. Copy-paste into your presentation sheets

**That's it!** No more manual data entry.

---

## Troubleshooting

### "python is not recognized as an internal or external command"

**Solution:** Python is not in your PATH. Either:
- Reinstall Python and make sure to check "Add Python to PATH"
- Or use the full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`

### "No module named src" or "ModuleNotFoundError"

**Solution:** You're not in the right folder. Make sure you're in the program folder:
```
cd %USERPROFILE%\Documents\nordics-real-estate-automation-main
```

### "ANTHROPIC_API_KEY not set" or "API key not found"

**Solution:** Set your API key again (you need to do this each time you open Command Prompt):
```
set ANTHROPIC_API_KEY=your-key-here
```

### "Invalid API key" or "Authentication error"

**Solution:** Your API key is incorrect. Double-check you copied it correctly from the Anthropic console. Make sure:
- No extra spaces before or after the key
- No quotation marks around the key
- The key starts with `sk-ant-`

### "File not found" error

**Solution:** The file path is incorrect. Tips:
- Use full paths starting with `%USERPROFILE%` or `C:\Users\YourName\...`
- Drag and drop files into Command Prompt to paste their paths
- Make sure the file exists at that location

### Command Prompt closes immediately

**Solution:** Don't double-click Python files. Always run commands from Command Prompt as shown in this guide.

### The wrong country sheet was used

**Solution:** The tool detects country from the article text. If it guessed wrong:
1. Check if the article mentions the correct country
2. You can manually move the row to the correct sheet in Excel

### I want to start over with a fresh file

**Solution:** Delete the output file and run a command:
```
del output\deals.xlsx
python -m src.cli process-url --url "..."
```

---

## Tips for Best Results

1. **Article URLs:** Works best with Nordic real estate news sites (Fastighetsvarlden, Estate Media, Eiendomswatch, etc.)

2. **PDF quality:** Clear, text-based PDFs work best. Scanned images may not work well.

3. **One article at a time:** The article processor handles one URL per command. Run it multiple times for multiple articles.

4. **Batch PDFs:** Put all related PDFs in one folder for batch processing.

5. **Keep Command Prompt open:** If you're processing multiple items, keep the same Command Prompt window open so you don't have to re-enter your API key.

6. **Don't worry about duplicates:** Each run adds a new row, so if you accidentally process the same article twice, just delete the duplicate row in Excel.

---

## What Gets Extracted

### For Articles (Process 2 - Transactions):

| Field | Description |
|-------|-------------|
| Country | Sweden, Denmark, or Finland |
| Date | Transaction date |
| Buyer | Company buying the property |
| Seller | Company selling the property |
| Location | City name |
| Property type | Office, Residential, Logistics, etc. |
| Price | In millions (MSEK, MDKK, or MEUR) |
| Area | Square meters |
| Price per sqm | Auto-calculated |
| Yield | If mentioned in article |
| Comments | Brief summary of the deal |
| Source | Article URL |

### For PDFs (Process 1 - Incoming Deals):

| Field | Description |
|-------|-------------|
| Date received | When you got the PDF |
| Week nr. | Auto-calculated from date |
| Type | IM or Teaser |
| Project Name | Deal/property name |
| Country | Sweden, Denmark, or Finland |
| Location | City/area |
| Use | Property type (Office, Logistics, etc.) |
| Leasable area | Square meters |
| NOI | Net Operating Income |
| NOI per sqm | Auto-calculated |
| Yield | If stated |
| Deal value | Asking price |
| WAULT | Weighted average lease term |
| Occupancy | Economic occupancy rate |
| Comment | Brief summary |

---

## Quick Reference Card

**Set your API key (do this first, every time):**
```
set ANTHROPIC_API_KEY=your-key-here
```

**Process one article (goes to Sweden/Denmark/Finland sheet):**
```
python -m src.cli process-url --url "https://example.com/article"
```

**Process one PDF (goes to Deal list sheet):**
```
python -m src.cli process-pdf-file --input "C:\path\to\file.pdf"
```

**Process folder of PDFs (all go to Deal list sheet):**
```
python -m src.cli process-pdf-folder --folder "C:\path\to\folder"
```

**All output goes to:** `output/deals.xlsx`

---

## For Developers

See [docs/QUICK_START.md](docs/QUICK_START.md) for the full command reference and [docs/HOW_TO_ADD_MAPPINGS.md](docs/HOW_TO_ADD_MAPPINGS.md) for extending the normalization rules.

**Run tests:**
```
python -m pytest tests/ -v
```

**Project structure:**
```
src/
├── cli.py                  # Command-line interface
├── extract/                # LLM extraction (prompts, API calls)
├── normalize/              # Data normalization (dates, numbers, property types)
├── render/                 # Output rendering (TSV, Excel)
├── pipelines/              # End-to-end workflows
├── fetch/                  # URL and PDF text extraction
└── validate/               # Schema validation

config/
├── schemas/                # Column definitions for each sheet type
│   ├── transactions.schema.json    # Sweden/Denmark/Finland columns
│   └── inbound_purple.schema.json  # Deal list columns
└── mappings/               # Normalization rules
    ├── property_type_map.yml       # "warehouse" → "Logistics"
    └── city_map.yml                # "Göteborg" → "Gothenburg"

tests/                      # Unit tests (164 tests)
output/                     # Generated Excel files go here
```
