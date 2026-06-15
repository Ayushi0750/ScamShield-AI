import re


def preprocess_text(text: str) -> str:
    """
    Clean and normalize job text while PRESERVING scam signal keywords.
    
    Key changes from original:
    - Keep currency symbols (₹, $, €) - scam indicator
    - Keep numbers with context - important for amounts/fees
    - Keep common scam emojis (, , , )
    - Keep urgency words (limited, expire, immediate, today)
    - Only remove truly noisy characters
    """
    
    # Preserve currency symbols by replacing with tokens
    currency_map = {
        '₹': 'RUPEES',
        '$': 'DOLLARS', 
        '€': 'EUROS',
        '£': 'POUNDS'
    }
    
    for symbol, word in currency_map.items():
        text = text.replace(symbol, ' ' + word + ' ')
    
    # Preserve scam-indicator emojis by converting to text
    emoji_map = {
        '🎯': 'TARGET',
        '✅': 'CHECK',
        '⚡': 'LIGHTNING',
        '💰': 'MONEY',
        '🚀': 'ROCKET',
        '🔥': 'FIRE'
    }
    
    for emoji, word in emoji_map.items():
        text = text.replace(emoji, ' ' + word + ' ')
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs (still noise)
    text = re.sub(r"http\S+|www\S+", "", text)
    
    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)
    
    # Remove HTML entities and markup
    text = re.sub(r"&\w+;|<[^>]+>", "", text)
    
    # Keep alphanumeric, spaces, and hyphens (important for "no-interview", "work-from-home")
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()


#test
if __name__ == "__main__":
    test_texts = [
        "pay a registration fee of ₹4999 immediately",
        "🎯 INSTANT CASH - NO INTERVIEW 🎯\nEarn ₹2000-5000 DAILY",
        "Limited-time offer expires today! $50 registration required",
        "Congratulations! Guaranteed Google internship. Limited slots!",
    ]
    
    print("=" * 80)
    print("PREPROCESSING TEST")
    print("=" * 80)
    
    for text in test_texts:
        print(f"\n Original:\n{text}")
        print(f"\n🔧 Preprocessed:\n{preprocess_text(text)}")
        print("-" * 80)