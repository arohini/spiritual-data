import re


def clean_sanskrit(text):
    corrections = {
        "  ": " ",     # Remove double spaces
        "|": "।",       # Fix vertical bars to Purna Virama
        "||": "॥"       # Fix double bars
    }
    for old, new in corrections.items():
        text = text.replace(old, new)
        text = re.sub(r'\d+', '', text)
    return text

# clean up the text by removing non-IAST characters and extra spaces
def clean_text(text):
    # Remove non-IAST characters (keep only letters, spaces, and common punctuation)
    cleaned_text = re.sub(r'[^a-zA-ZāīūṛḷṃḥñṭḍṇśṣĀĪŪṚḶṂḤÑṬḌṆŚṢ\s.,;!?-]', '', text)
    
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    cleaned_text = clean_sanskrit(cleaned_text)
    
    return cleaned_text

def find_iast_words(text):
    # Regex pattern to match Sanskrit words in IAST format
    # Includes standard letters + diacritics used in IAST
    iast_pattern = r'\b[a-zA-ZāīūṛḷṃḥñṭḍṇśṣĀĪŪṚḶṂḤÑṬḌṆŚṢ]+\b'
    
    # Find all matches
    words = re.findall(iast_pattern, text)
    if len(words) == 0:pass
    return words

input_file_path = "spiritual-data/holywalls/lord-ganesha/sri_ganesha_sahasranamam.txt"


def stotram_from_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
            
    # Split into lines and filter out empty lines
    lines = [clean_text(line.strip()) for line in text.splitlines() if line.strip() and find_iast_words(line.strip())]
    
    # Assuming each line is a verse, we can return the list of verses
    return lines

print(stotram_from_text_file(input_file_path))