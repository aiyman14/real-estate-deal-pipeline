# Real Estate Deal Pipeline

Extracts deal information from PDFs and news articles into Excel.

---

# Viktor's Instructions

Follow these steps exactly. Do not skip any step.

---

## PART 1: ONE-TIME SETUP

### Step 1: Install Python

1. Open your web browser
2. Go to: **https://www.python.org/downloads/**
3. Click the yellow **"Download Python"** button
4. When the download finishes, open the downloaded file
5. **IMPORTANT:** Check the box at the bottom that says **"Add Python to PATH"**
6. Click **"Install Now"**
7. Wait for it to finish
8. Click **"Close"**

---

### Step 2: Download This Program

1. On this GitHub page, click the green **"Code"** button
2. Click **"Download ZIP"**
3. The file will download to your OneDrive Downloads folder

---

### Step 3: Extract the ZIP File

1. Open File Explorer
2. Go to: **This PC → Downloads** (or check your OneDrive → Downloads)
3. Find the file called **nordics-real-estate-automation-main.zip**
4. Right-click it → **Extract All...**
5. Click **Extract**
6. You now have a folder called **nordics-real-estate-automation-main**
7. **Leave this folder where it is** (in your Downloads)

---

### Step 4: Find Your Folder Path

1. Open the **nordics-real-estate-automation-main** folder
2. Click in the address bar at the top (where it shows the folder location)
3. The full path will be highlighted - it will look something like:
   ```
   C:\Users\vilu\OneDrive\Downloads\nordics-real-estate-automation-main
   ```
4. **Write this path down** or copy it somewhere - you will need it

---

### Step 5: Install Required Packages

1. Press the **Windows key** on your keyboard
2. Type **cmd**
3. Press **Enter** (this opens Command Prompt - a black window)

4. **First, go to the folder.** Type this command:
   ```
   cd C:\Users\vilu\OneDrive\Downloads\nordics-real-estate-automation-main
   ```
5. Press **Enter**

6. **Check it worked.** Type this command:
   ```
   dir
   ```
7. Press **Enter**
8. You should see a list of files including **requirements.txt** and **src**
   - If you see "The system cannot find the path specified" → your path is wrong, see "HOW TO FIND YOUR EXACT PATH" at the bottom
   - If you see the files → continue to the next step

9. **Now install.** Type this command:
   ```
   pip install -r requirements.txt
   ```
10. Press **Enter**
11. Wait for it to finish (you'll see lots of text scrolling)
12. When it's done, you'll see the blinking cursor again

---

### Step 6: Get Your API Key

1. Go to: **https://console.anthropic.com/**
2. Create an account or log in
3. Click **"API Keys"** on the left
4. Click **"Create Key"**
5. Copy the key (it starts with **sk-ant-**)
6. Save this key somewhere safe - you need it every time you use the program

---

## PART 2: USING THE PROGRAM

Every time you want to use the program, follow these steps:

---

### Step 1: Open Command Prompt

1. Press the **Windows key**
2. Type **cmd**
3. Press **Enter**

---

### Step 2: Go to the Program Folder

Type this command (use YOUR path from the setup):
```
cd C:\Users\vilu\OneDrive\Downloads\nordics-real-estate-automation-main
```
Press **Enter**

---

### Step 3: Set Your API Key

Type this command (replace YOUR-KEY with your actual API key):
```
set ANTHROPIC_API_KEY=YOUR-KEY
```
Press **Enter**

Example (not a real key):
```
set ANTHROPIC_API_KEY=sk-ant-api03-ABC123xyz456DEF789
```

---

## PROCESS PDFS (Incoming Deals)

### To Process Multiple PDFs at Once:

**Step 1: Create a folder for your PDFs**

1. Open File Explorer
2. Go to your Downloads folder
3. Right-click → **New** → **Folder**
4. Name it exactly: **PDFs**

Your PDFs folder is now at:
```
C:\Users\vilu\OneDrive\Downloads\PDFs
```

**Step 2: Put your PDF files in that folder**

Copy all the PDFs you want to process into the **PDFs** folder.

**Step 3: Open Command Prompt and run these commands**

Open Command Prompt (Windows key → type cmd → Enter), then run these 3 commands:

Command 1 - Go to program folder:
```
cd C:\Users\vilu\OneDrive\Downloads\nordics-real-estate-automation-main
```

Command 2 - Set API key:
```
set ANTHROPIC_API_KEY=YOUR-KEY
```

Command 3 - Process all PDFs:
```
python -m src.cli process-pdf-folder --folder "C:\Users\vilu\OneDrive\Downloads\PDFs"
```

**What you'll see:**
```
Processing PDFs in: C:\Users\vilu\OneDrive\Downloads\PDFs
[1/3] document1.pdf ... OK
[2/3] document2.pdf ... OK
[3/3] document3.pdf ... OK
Done. Processed 3 PDFs: 3 success, 0 failed
Added to sheet 'Deal list' in output/deals.xlsx
```

---

### To Process One PDF:

```
python -m src.cli process-pdf-file --input "C:\Users\vilu\OneDrive\Downloads\your_file.pdf"
```

---

## PROCESS ARTICLES (Transactions)

For each article URL, run this command (change the URL):

```
python -m src.cli process-url --url "https://www.fastighetsvarlden.se/notiser/your-article/"
```

Run it once for each article. Each one gets added to the correct country sheet (Sweden/Denmark/Finland).

---

## FIND YOUR OUTPUT FILE

Your Excel file is saved inside the program folder:

1. Open File Explorer
2. Go to: **OneDrive → Downloads → nordics-real-estate-automation-main → output**
3. Open **deals.xlsx**

The file has 4 sheets:
- **Deal list** - all your PDFs go here
- **Sweden** - Swedish articles
- **Denmark** - Danish articles
- **Finland** - Finnish articles

---

## QUICK REFERENCE

Open Command Prompt, then run these commands in order:

**1. Go to folder:**
```
cd C:\Users\vilu\OneDrive\Downloads\nordics-real-estate-automation-main
```

**2. Set API key:**
```
set ANTHROPIC_API_KEY=YOUR-KEY
```

**3. Process PDFs:**
```
python -m src.cli process-pdf-folder --folder "C:\Users\vilu\OneDrive\Downloads\PDFs"
```

**4. Process article:**
```
python -m src.cli process-url --url "https://example.com/article"
```

---

## IF SOMETHING GOES WRONG

### "No such file or directory: requirements.txt"
You're not in the right folder. Do this:
1. Find your folder in File Explorer
2. Click in the address bar to see the full path
3. Copy that path
4. In Command Prompt, type `cd ` (with a space after cd)
5. Right-click to paste your path
6. Press Enter
7. Type `dir` and press Enter to verify you see the files
8. Now run `pip install -r requirements.txt`

### "python is not recognized"
You need to reinstall Python. Make sure to check "Add Python to PATH" during installation.

### "No module named src"
You're not in the right folder. Run the `cd` command again with your correct path.

### "ANTHROPIC_API_KEY not set"
You need to set your API key. Run the `set ANTHROPIC_API_KEY=YOUR-KEY` command again.

### "The system cannot find the path specified"
The folder path is wrong. See "HOW TO FIND YOUR EXACT PATH" below.

### "File not found" or "Not a directory"
The path is wrong. Double-check your folder path by:
1. Open the folder in File Explorer
2. Click in the address bar
3. Copy the exact path shown
4. Use that path in your command

---

## HOW TO FIND YOUR EXACT PATH

If the commands don't work, you need to find your exact folder path:

1. Open File Explorer
2. Navigate to the **nordics-real-estate-automation-main** folder
3. Click once in the address bar at the top
4. The full path will be highlighted and selected
5. Press **Ctrl+C** to copy it
6. Use this path in your commands

The path might look like:
- `C:\Users\vilu\OneDrive\Downloads\nordics-real-estate-automation-main`
- `C:\Users\vilu\Downloads\nordics-real-estate-automation-main`
- Something else depending on your OneDrive setup

Whatever path you see - that's the one to use in all the commands.
