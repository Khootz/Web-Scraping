import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time 
# Suppress only the specific InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup
import re
from rapidfuzz import fuzz

# ---------------------------
# 0. HELPER FUNCTIONS
# ---------------------------

def normalize_text(text):
    """
    Convert text to lowercase, remove punctuation, and collapse extra spaces.
    (Used for fuzzy matching purposes)
    """
    text = text.lower()
    # Remove punctuation (non-alphanumeric or whitespace)
    text = re.sub(r'[^\w\s]', '', text)
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_near_duplicate(text_a, text_b, threshold=90):
    """
    Compare two normalized strings using RapidFuzz's fuzz.ratio().
    Return True if similarity >= threshold.
    """
    similarity_score = fuzz.ratio(text_a, text_b)
    return similarity_score >= threshold

def sanitize_output(text):
    """
    Remove ANY non-ASCII characters (like emojis or weird symbols),
    allowing only letters, digits, and whitespace.
    """
    # Encode to ASCII, ignoring non-ASCII chars, then decode back to ASCII
    text_ascii = text.encode("ascii", errors="ignore").decode("ascii")
    # If you also want to remove punctuation from the ASCII text, you can do:
    text_ascii = re.sub(r'[^a-zA-Z0-9\s]', '', text_ascii)
    # Now strip extra spaces
    text_ascii = re.sub(r'\s+', ' ', text_ascii).strip()
    return text_ascii

# ---------------------------
# 1. SCRAPE HKUST ANNOUNCEMENTS
# ---------------------------
hkust_url = 'https://bmundergrad.hkust.edu.hk/announcement'
page_1 = requests.get(hkust_url, verify=False)
soup_1 = BeautifulSoup(page_1.text, 'html.parser')

keywords = ['Case', 'Challenge', 'Competition', 'Hackathon', 'Datathon']

hkust_entries = []
announcements = soup_1.find_all('tr')
for row in announcements:
    titles = row.find_all('h3')
    for title in titles:
        title_text = title.get_text(strip=True)
        # Check if any keyword is in the title
        if any(keyword.lower() in title_text.lower() for keyword in keywords):
            # Append title with (UST)
            hkust_entries.append(title_text + " [UST]")

# ---------------------------
# 2. SCRAPE HKU COMPETITIONS
# ---------------------------
hku_url = 'https://ug.hkubs.hku.hk/competition'
page_2 = requests.get(hku_url)
soup_2 = BeautifulSoup(page_2.text, 'html.parser')

hku_entries = []
comp_cards = soup_2.find_all('a', class_='card-blk__item')
for card in comp_cards:
    text_found = card.find('p', class_='card-blk__title')
    if text_found:
        # Append title with (HKU)
        hku_entries.append(text_found.text.strip() + " [HKU]")

# ---------------------------
# 3. COMBINE INTO ONE LIST WITH INDEX
# ---------------------------
combined_entries = hkust_entries + hku_entries
indexed_entries = list(enumerate(combined_entries))

# ---------------------------
# 4. FUZZY DEDUPLICATION
# ---------------------------
unique_entries = []  # (original_index, original_text, normalized_text)

for idx, original_text in indexed_entries:
    norm_text = normalize_text(original_text)

    duplicate_found = False
    for (existing_idx, existing_orig, existing_norm) in unique_entries:
        if is_near_duplicate(norm_text, existing_norm):
            duplicate_found = True
            break

    if not duplicate_found:
        unique_entries.append((idx, original_text, norm_text))

# ---------------------------
# 5. PRINT RESULTS
# ---------------------------
for (index_in_list, original_title, normalized_version) in unique_entries:
    # Remove weird symbols and only keep letters, digits, and whitespace
    cleaned_output = sanitize_output(original_title)
    print(cleaned_output)

time.sleep(10)
