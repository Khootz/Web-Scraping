# Web Scraping for Business Competitions

This project uses web scraping to automatically gather announcements related to business case competitions, student competitions, hackathons, and datathons from the websites of HKUST and HKU. As an engineering student, I noticed that I was not being notified of business competitions, an area I am passionate about. To address this, I created a solution to save time and effort by automating the process of finding and filtering relevant competitions.

The web scraper extracts competition details from both the HKUST and HKU websites, filters them by keywords (Case, Challenge, Competition, Hackathon, Datathon), and removes any duplicates using fuzzy matching.

## Features
- **Web Scraping**: Extracts relevant business competition data from the HKUST and HKU websites.
- **Keyword Filtering**: Filters the scraped content by specific keywords such as "Case," "Challenge," "Competition," "Hackathon," and "Datathon."
- **Fuzzy Deduplication**: Removes near-duplicates from the scraped entries using RapidFuzz's fuzzy matching capabilities.
- **Text Sanitization**: Cleans up the output by removing non-ASCII characters and unwanted symbols.
- **Efficient and Automated**: Saves time by automating the process of finding and organizing competitions.

## Code Overview

The script consists of several parts, as outlined below:

### 1. Helper Functions:
- **normalize_text()**: Converts text to lowercase, removes punctuation, and collapses extra spaces to standardize text for comparison.
- **is_near_duplicate()**: Compares two normalized strings and returns `True` if they are similar enough (based on a similarity threshold).
- **sanitize_output()**: Removes non-ASCII characters (e.g., emojis) and other unwanted symbols, leaving only letters, digits, and whitespace.

### 2. Scraping HKUST Announcements:
- The script sends a request to the HKUST announcements page and parses the HTML content.
- It filters for titles containing keywords like "Case," "Challenge," "Competition," "Hackathon," and "Datathon."
- The relevant announcements are stored in the `hkust_entries` list.

### 3. Scraping HKU Competitions:
- The script sends a request to the HKU competition page and parses the HTML content.
- It extracts the competition titles and appends them to the `hku_entries` list.

### 4. Combine and Deduplicate:
- The results from both HKU and HKUST are combined into one list, `combined_entries`.
- The script uses fuzzy matching to remove duplicates and ensure each entry is unique.
- The `unique_entries` list holds the final results after deduplication.

### 5. Output:
- The final, cleaned list of unique competition titles is printed, with special characters removed.

## How It Works
1. The script scrapes the web pages of HKUST and HKU.
2. It filters out titles that contain the specified keywords.
3. It removes any duplicate titles using fuzzy string matching.
4. The final list of unique competitions is printed with unnecessary symbols removed.

