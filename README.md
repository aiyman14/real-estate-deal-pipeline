# Real Estate Deal Pipeline

A tool that extracts deal information from real estate news articles and broker PDFs, then saves it to Excel files for easy tracking.

**Works with:** Sweden, Denmark, and Finland real estate deals

---

# Complete Setup Guide for Viktors monkey brain

This guide will walk you through every step to get this program running on your Windows computer. Follow each step carefully.

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

Now you're ready to use the program! There are three ways to use it:

---

### Option 1: Process a News Article URL

Use this to extract deal information from a real estate news article on the web.

**Important:** This processes ONE article at a time. Run the command once for each article.

**Command format:**
```
python -m src.cli process-url --url "PASTE-ARTICLE-URL-HERE" --out output/deal.xlsx
```

**Example with a real URL:**
```
python -m src.cli process-url --url "https://www.fastighetsvarlden.se/notiser/heimstaden-saljer-for-en-miljard/" --out output/my_deal.xlsx
```

**What happens:**
- The program reads the article
- Extracts deal information (price, location, property type, etc.)
- Saves it to an Excel file in the `output` folder

**After it runs:** You'll see `Done. Output: output/my_deal.xlsx` when finished.

---

### Option 2: Process a Single PDF

Use this to extract deal information from a PDF document (like a broker teaser or IM).

**Command format:**
```
python -m src.cli process-pdf-file --input "PATH-TO-YOUR-PDF" --out output/deal.xlsx
```

**Example (if your PDF is on the Desktop):**
```
python -m src.cli process-pdf-file --input "%USERPROFILE%\Desktop\property_teaser.pdf" --out output/property_deal.xlsx
```

**Example (if your PDF is in Documents):**
```
python -m src.cli process-pdf-file --input "%USERPROFILE%\Documents\broker_im.pdf" --out output/broker_deal.xlsx
```

**Tip:** You can drag and drop a PDF file into the Command Prompt window to paste its full path.

---

### Option 3: Process Multiple PDFs at Once (Batch)

Use this to process all PDF files in a folder and combine them into one Excel file.

**Command format:**
```
python -m src.cli process-pdf-folder --folder "PATH-TO-FOLDER" --out output/all_deals.xlsx
```

**Example (if your PDFs are in a folder called "PDFs" on your Desktop):**
```
python -m src.cli process-pdf-folder --folder "%USERPROFILE%\Desktop\PDFs" --out output/all_deals.xlsx
```

**Example (if your PDFs are in Documents):**
```
python -m src.cli process-pdf-folder --folder "%USERPROFILE%\Documents\Deal_PDFs" --out output/all_deals.xlsx
```

**Optional settings:**
- `--max 10` — Only process the first 10 PDFs (default is 20)
- `--date "2024/01/15"` — Set a "date received" for all deals

**Example with options:**
```
python -m src.cli process-pdf-folder --folder "%USERPROFILE%\Desktop\PDFs" --out output/all_deals.xlsx --max 10
```

---

## Finding Your Output Files

After running any command, your Excel file is saved in the `output` folder inside the program folder.

**To open your output:**
1. Open File Explorer
2. Navigate to the program folder (e.g., `Documents\nordics-real-estate-automation-main`)
3. Open the `output` folder
4. Double-click your Excel file to open it

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

---

## Tips for Best Results

1. **Article URLs:** Works best with Nordic real estate news sites (Fastighetsvarlden, Estate Media, etc.)

2. **PDF quality:** Clear, text-based PDFs work best. Scanned images may not work well.

3. **One article at a time:** The article processor handles one URL per command. Run the command multiple times for multiple articles.

4. **Batch PDFs:** Put all related PDFs in one folder for batch processing.

5. **Keep Command Prompt open:** If you're processing multiple items, keep the same Command Prompt window open so you don't have to re-enter your API key.

---

## What the Output Looks Like

The Excel file contains one row per deal with these columns:
- Date, Week number
- Property name, Address, Location
- Property type (Office, Residential, Logistics, etc.)
- Area (square meters)
- Price (in local currency)
- Buyer and Seller
- Yield, NOI, Occupancy
- And more...

Numbers are automatically formatted correctly, and Swedish city names are translated to English (e.g., Göteborg → Gothenburg).

---

## Need Help?

If something isn't working:
1. Make sure you followed each step exactly
2. Check the Troubleshooting section above
3. Try closing Command Prompt and starting fresh from Step 4

---

## Quick Reference Card

**Set your API key (do this first, every time):**
```
set ANTHROPIC_API_KEY=your-key-here
```

**Process one article:**
```
python -m src.cli process-url --url "https://example.com/article" --out output/deal.xlsx
```

**Process one PDF:**
```
python -m src.cli process-pdf-file --input "C:\path\to\file.pdf" --out output/deal.xlsx
```

**Process folder of PDFs:**
```
python -m src.cli process-pdf-folder --folder "C:\path\to\folder" --out output/all_deals.xlsx
```

---

## For Developers

See [docs/QUICK_START.md](docs/QUICK_START.md) for the full command reference and [docs/HOW_TO_ADD_MAPPINGS.md](docs/HOW_TO_ADD_MAPPINGS.md) for extending the normalization rules.

**Run tests:**
```
python -m pytest tests/ -v
```
