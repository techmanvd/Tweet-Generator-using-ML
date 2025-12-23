from flask import Flask, render_template, jsonify, request
import random
import json
import os

app = Flask(__name__)

# --- The Logic (Markov Chain) ---
class TweetGenerator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.chain = {}
        self.build_markov_chain()

    def build_markov_chain(self):
        for tweet in self.corpus:
            words = tweet.split()
            for i in range(len(words) - 1):
                current_word = words[i]
                next_word = words[i + 1]
                
                if current_word not in self.chain:
                    self.chain[current_word] = []
                self.chain[current_word].append(next_word)

    def generate(self):
        if not self.chain: return "Error: No data trained."
        
        # Pick a random starting word
        start_words = [tweet.split()[0] for tweet in self.corpus]
        current_word = random.choice(start_words)
        sentence = [current_word]

        # Generate a tweet (Max 15 words for a punchy caption)
        for _ in range(15): 
            if current_word in self.chain:
                next_word = random.choice(self.chain[current_word])
                sentence.append(next_word)
                current_word = next_word
            else:
                break 
        
        return " ".join(sentence)

# --- LOAD DATA FROM FILE ---
def load_captions():
    try:
        with open('captions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: captions.json not found! Please create the file.")
        return {}

captions_data = load_captions()

# --- THE BRAIN: KEYWORD MAPPING ---
# This decides which category to use based on user input
keyword_map = {
    # New Topics
    "tech": ["code", "python", "java", "ai", "ml", "computer", "app", "web", "dev", "tech", "cyber", "linux", "cloud", "data", "robot"],
    "business": ["money", "market", "profit", "startup", "invest", "finance", "ceo", "founder", "sales", "economy", "trade", "bank", "wealth"],
    "philosophy": ["life", "truth", "mind", "think", "wisdom", "soul", "death", "exist", "reason", "ethics", "peace", "calm"],
    "physics": ["energy", "force", "matter", "atom", "quantum", "light", "gravity", "motion", "science", "lab", "nuclear", "tesla"],
    "astronomy": ["space", "star", "moon", "sun", "planet", "galaxy", "universe", "mars", "sky", "telescope", "alien", "cosmos"],
    "geopolitics": ["war", "peace", "country", "nation", "power", "world", "gov", "border", "army", "politic", "law", "treaty", "global"],
    
    # Emotions
    "happy": ["happy", "good", "great", "excited", "fun", "joy", "smile", "awesome", "lit", "win", "blessed"],
    "sad": ["sad", "cry", "lonely", "depressed", "bad", "hurt", "pain", "tears", "upset", "broke", "grief"],
    "sassy": ["angry", "hate", "boss", "cool", "style", "attitude", "fake", "ex", "haters", "queen", "savage"],
    "motivation": ["work", "study", "grind", "goal", "dream", "fail", "tired", "give up", "success", "hustle"],
    "love": ["love", "crush", "bf", "gf", "couple", "date", "heart", "beautiful", "cute", "marriage", "kiss"]
}

# Initialize Generators for ALL categories found in JSON
generators = {}
if captions_data:
    for category, data in captions_data.items():
        generators[category] = TweetGenerator(data)

def determine_category(user_input):
    user_input = user_input.lower()
    
    # Check keywords (Priority: Specific topics first, then emotions)
    for category, keywords in keyword_map.items():
        for word in keywords:
            if word in user_input:
                return category
    
    return "neutral"

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    data = request.json
    user_input = data.get('thought', '')
    
    # 1. Analyze User Input
    category = determine_category(user_input)
    
    # 2. Get the specific generator
    # If category exists in our generators, use it. Otherwise default to neutral.
    generator = generators.get(category, generators.get('neutral'))
    
    if generator:
        caption = generator.generate()
    else:
        caption = "Error: Dataset not loaded correctly."

    return jsonify({
        'caption': caption,
        'detected_mood': category
    })

if __name__ == '__main__':
    app.run(debug=True)

    