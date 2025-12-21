from flask import Flask, render_template, jsonify, request
import random

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
        
        # Pick a random starting word from corpus
        start_words = [tweet.split()[0] for tweet in self.corpus]
        current_word = random.choice(start_words)
        sentence = [current_word]

        for _ in range(20): # Max 20 words
            if current_word in self.chain:
                next_word = random.choice(self.chain[current_word])
                sentence.append(next_word)
                current_word = next_word
            else:
                break 
        
        return " ".join(sentence)

# --- Data: Expanded Topics ---
topics_data = {
  "tech": [
    "Python is easy for developers", "Python is great for automation", "Python is widely used in industry",
    "Coding improves logical thinking", "Coding daily builds discipline", "AI is transforming technology",
    "AI powers modern applications", "Machine learning learns from data", "Deep learning handles complex problems",
    "Data science extracts insights", "Data analysis drives decisions", "Cloud computing enables scalability",
    "Cloud services reduce infrastructure cost", "Web development is in high demand", "Backend development powers applications",
    "Frontend focuses on user experience", "React simplifies UI development", "JavaScript runs everywhere",
    "APIs connect software systems", "Databases store critical information", "SQL manages structured data",
    "NoSQL handles unstructured data", "Cybersecurity protects digital assets", "Encryption secures communication",
    "Networking connects devices globally", "Operating systems manage hardware", "Linux is popular among developers",
    "Open source drives innovation", "Git tracks code changes", "Version control improves collaboration",
    "DevOps speeds up deployment", "Automation reduces manual effort", "Testing improves software quality",
    "Debugging improves understanding", "Clean code improves readability", "Algorithms optimize performance",
    "Data structures organize data", "Problem solving is essential", "Tech skills need continuous learning",
    "Innovation fuels growth", "AI models require training data", "Model accuracy depends on data",
    "Edge computing reduces latency", "IoT connects smart devices", "Blockchain ensures transparency",
    "Smartphones drive mobile computing", "Apps improve productivity", "Virtualization improves efficiency",
    "Containers simplify deployment", "Technology evolves rapidly", "Learning tech is a lifelong process",
    "Coding turns ideas into reality", "Tech careers reward consistency", "Digital transformation changes businesses",
    "Automation boosts productivity", "AI enhances decision making", "Software solves real problems",
    "Tech empowers innovation", "Programming improves creativity", "Developers build the future",
    "Data drives the digital world", "Technology shapes modern life", "AI requires ethical responsibility",
    "Systems must be scalable", "Performance matters in software", "Reliability builds trust",
    "Security is a top priority", "Technology connects the world", "Innovation starts with ideas",
    "Technology enables progress", "Coding is both skill and art", "Tech education opens opportunities",
    "Digital skills are essential", "Future depends on technology", "AI accelerates innovation",
    "Tech simplifies complex tasks", "Engineering solves challenges", "Software impacts society",
    "Tech is constantly evolving", "Learning tech requires patience", "Technology fuels the future",
    "Code powers the digital age"
  ],
  "business": [
    "Business is about value creation", "Profit is essential for sustainability", "Markets react to information",
    "Investing requires patience", "Risk management is crucial", "Entrepreneurship drives innovation",
    "Startups solve real problems", "Strategy defines direction", "Leadership inspires teams",
    "Execution determines success", "Cash flow keeps businesses alive", "Revenue growth attracts investors",
    "Customer satisfaction builds loyalty", "Brand trust drives sales", "Marketing creates awareness",
    "Sales convert opportunities", "Pricing affects demand", "Competition drives improvement",
    "Innovation creates advantage", "Business decisions use data", "Finance measures performance",
    "Accounting tracks transactions", "Economics studies resource allocation", "Supply chains enable production",
    "Logistics ensures delivery", "Globalization expands markets", "Digital business scales faster",
    "Ecommerce reshapes retail", "Startups face uncertainty", "Investors seek returns",
    "Valuation reflects expectations", "Product market fit is critical", "Growth requires focus",
    "Cost control improves margins", "Efficiency increases profitability", "Time is money",
    "Networking creates opportunities", "Negotiation builds agreements", "Business ethics matter",
    "Trust sustains relationships", "Risk brings reward", "Failure teaches lessons",
    "Adaptability ensures survival", "Innovation disrupts industries", "Technology enables scalability",
    "Vision guides organizations", "Culture shapes behavior", "Leadership drives performance",
    "Decision making defines outcomes", "Market trends influence strategy", "Economic cycles affect businesses",
    "Inflation impacts purchasing power", "Interest rates influence investment", "Trade enables growth",
    "Exports boost economies", "Imports meet demand", "Corporate governance ensures accountability",
    "Regulation protects markets", "Entrepreneurial mindset creates value", "Business planning reduces risk",
    "Execution beats ideas", "Scalability attracts investors", "Innovation fuels growth",
    "Sustainability matters long term", "Brand equity builds advantage", "Customer retention improves profits",
    "Quality drives reputation", "Operations ensure efficiency", "Supply meets demand",
    "Market research reduces uncertainty", "Competitive advantage ensures success", "Growth requires investment",
    "Capital enables expansion", "Business success needs discipline", "Money is a medium of exchange",
    "Wealth creation takes time", "Patience rewards investors", "Smart decisions compound returns",
    "Long term thinking wins", "Business builds economies", "Trade connects nations",
    "Enterprise drives employment", "Innovation creates wealth", "Business shapes society"
  ],
  "philosophy": [
    "Life is a journey", "Happiness comes from within", "Meaning gives life direction", "Wisdom grows with experience",
    "Time is precious", "Silence brings clarity", "Change is inevitable", "Acceptance brings peace",
    "Self awareness leads to growth", "Knowledge shapes understanding", "Truth requires reflection",
    "Purpose guides actions", "Suffering teaches resilience", "Freedom comes with responsibility",
    "Mindfulness improves clarity", "Thoughts shape reality", "Perspective changes meaning",
    "Patience brings understanding", "Humility leads to wisdom", "Ego clouds judgment",
    "Compassion builds connection", "Ethics guide behavior", "Virtue leads to fulfillment",
    "Balance creates harmony", "Desire causes suffering", "Detachment brings peace",
    "Inner peace is valuable", "Reflection deepens understanding", "Wisdom transcends knowledge",
    "Character defines identity", "Values shape choices", "Simplicity brings clarity",
    "Truth requires courage", "Meaning evolves with time", "Purpose gives motivation",
    "Awareness leads to insight", "Thought precedes action", "Being matters more than having",
    "Understanding reduces conflict", "Perspective shapes experience", "Curiosity fuels wisdom",
    "Self control builds strength", "Patience cultivates growth", "Reflection reveals truth",
    "Acceptance reduces suffering", "Compassion heals wounds", "Mind guides experience",
    "Peace begins within", "Wisdom requires humility", "Learning never ends", "Questions lead to insight",
    "Knowledge without wisdom is empty", "Time reveals truth", "Experience teaches lessons",
    "Purpose defines meaning", "Ethics shape society", "Truth seeks understanding",
    "Silence reveals clarity", "Calm mind sees clearly", "Simplicity is powerful", "Inner growth matters",
    "Values guide decisions", "Meaning drives fulfillment", "Reflection builds awareness",
    "Philosophy questions existence", "Life seeks meaning", "Wisdom brings peace",
    "Understanding brings harmony", "Self knowledge is power", "Balance creates stability",
    "Thought creates perception", "Awareness brings freedom", "Compassion creates unity",
    "Truth transcends belief", "Mindfulness shapes reality", "Purpose fuels action",
    "Peace is internal", "Wisdom grows silently", "Existence invites inquiry",
    "Life is impermanent", "Acceptance brings clarity"
  ],
  "physics": [
    "Physics studies the laws of nature", "Motion follows physical laws", "Force causes acceleration",
    "Energy cannot be created", "Energy transforms forms", "Gravity attracts masses",
    "Newton defined classical mechanics", "Relativity explains spacetime", "Light has wave properties",
    "Light also behaves as particles", "Quantum mechanics studies the micro world", "Uncertainty is fundamental",
    "Electrons exist as probabilities", "Matter is made of atoms", "Atoms contain subatomic particles",
    "Protons carry positive charge", "Electrons carry negative charge", "Neutrons have no charge",
    "Electricity powers modern life", "Magnetism influences charges", "Electromagnetism unifies forces",
    "Thermodynamics studies heat", "Entropy measures disorder", "Temperature measures energy",
    "Pressure depends on force", "Waves transfer energy", "Sound is a mechanical wave",
    "Frequency determines pitch", "Optics studies light behavior", "Refraction bends light",
    "Reflection changes direction", "Speed of light is constant", "Mass relates to energy",
    "E equals mc squared", "Fields describe interactions", "Quantum states evolve",
    "Particles exhibit duality", "Physics explains reality", "Models approximate nature",
    "Experiments test theories", "Measurements have uncertainty", "Constants define nature",
    "Space and time are linked", "Momentum is conserved", "Angular momentum is conserved",
    "Forces cause interactions", "Physics drives technology", "Semiconductors enable electronics",
    "Lasers use quantum effects", "Nuclear physics studies nuclei", "Fusion powers stars",
    "Fission releases energy", "Radiation carries energy", "Physics underpins engineering",
    "Classical physics explains macroscales", "Modern physics explores extremes", "Cosmology studies the universe",
    "Dark matter affects galaxies", "Dark energy accelerates expansion", "Physics reveals patterns",
    "Mathematics describes physics", "Theories predict observations", "Physics seeks simplicity",
    "Symmetry guides laws", "Nature follows consistency", "Physics enables innovation",
    "Technology applies physics", "Understanding physics explains nature", "Physics inspires curiosity",
    "Discovery drives progress", "Physics bridges theory and reality", "Observation guides understanding",
    "Physics explains motion", "Forces shape the universe", "Energy drives change",
    "Physics reveals hidden rules", "Science seeks truth", "Physics connects phenomena",
    "Knowledge expands understanding"
  ],
  "astronomy": [
    "Astronomy studies celestial objects", "Stars produce energy", "The sun is a star",
    "Planets orbit stars", "Gravity shapes orbits", "The universe is expanding",
    "Galaxies contain billions of stars", "The Milky Way is our galaxy", "Black holes bend spacetime",
    "Light travels vast distances", "Telescopes observe distant objects", "Astronomy explores the cosmos",
    "Stars form from gas clouds", "Supernovae create heavy elements", "Planets form from disks",
    "Moons orbit planets", "Asteroids orbit the sun", "Comets have icy tails", "Space is mostly empty",
    "Distances are measured in light years", "The universe began with a big bang",
    "Cosmic background radiation exists", "Dark matter influences galaxies", "Dark energy drives expansion",
    "Nebulae birth stars", "Constellations map the sky", "Earth rotates daily", "Earth orbits the sun",
    "Seasons result from tilt", "Eclipses align celestial bodies", "Astronomy relies on physics",
    "Spectra reveal composition", "Redshift indicates motion", "Exoplanets orbit other stars",
    "Some planets may support life", "Life beyond Earth is questioned", "Space missions explore planets",
    "Satellites orbit Earth", "Astronomy inspires wonder", "Observations test theories",
    "Time scales are immense", "Stars evolve over billions of years", "Galaxies collide and merge",
    "The universe has structure", "Cosmic dust exists", "Starlight carries information",
    "Gravity governs cosmic motion", "Space exploration expands knowledge", "Telescopes detect faint signals",
    "Radio astronomy observes waves", "X rays reveal energetic events", "Astronomy uses advanced technology",
    "Cosmic rays travel fast", "The universe is vast", "Scale challenges imagination",
    "Astronomy answers fundamental questions", "Human curiosity drives exploration", "Space is dynamic",
    "Stars are born and die", "Astronomy studies origins", "Planets vary widely",
    "Cosmos follows physical laws", "Time began with the universe", "Astronomy connects science and wonder",
    "Exploration fuels discovery", "Observation expands understanding", "Space inspires humanity",
    "Astronomy seeks cosmic truth", "Universe holds mysteries", "Knowledge grows with observation",
    "Astronomy reveals our place", "Cosmos invites curiosity", "Stars guide navigation",
    "Night sky tells stories", "Astronomy studies infinity", "Universe evolves continuously"
  ],
  "geopolitics": [
    "Geopolitics studies global power", "Nations pursue strategic interests", "Geography influences politics",
    "Borders shape conflicts", "Resources drive competition", "Energy security matters",
    "Trade routes influence power", "Alliances balance strength", "Diplomacy prevents conflict",
    "Military power deters aggression", "Soft power influences nations", "Economics shapes foreign policy",
    "Globalization connects states", "National security guides decisions", "Sanctions influence behavior",
    "Technology affects warfare", "Cybersecurity impacts geopolitics", "Information warfare shapes narratives",
    "Media influences perception", "Public opinion affects policy", "Leadership shapes direction",
    "History influences geopolitics", "Colonial legacies remain", "Power shifts over time",
    "Multipolar world is emerging", "Unipolar dominance fades", "International law regulates states",
    "Sovereignty defines authority", "Territory matters in disputes", "Maritime routes are strategic",
    "Arctic geopolitics is rising", "Indo Pacific is important", "Global institutions mediate disputes",
    "United Nations coordinates diplomacy", "NATO ensures collective defense", "Regional blocs influence policy",
    "Economic blocs shape trade", "Currency power influences markets", "Energy pipelines affect relations",
    "Climate change affects geopolitics", "Migration influences stability", "Population impacts power",
    "Demographics shape future", "Technology shifts balance", "Artificial intelligence impacts warfare",
    "Space is a strategic domain", "Satellites support security", "Intelligence gathering guides policy",
    "Espionage affects relations", "Diplomatic talks reduce tensions", "Conflicts reshape borders",
    "Peace requires negotiation", "War has economic costs", "Defense spending reflects priorities",
    "Strategic depth matters", "Buffer states reduce risk", "Sea power enables trade",
    "Land power controls territory", "Air power ensures reach", "Nuclear deterrence prevents war",
    "Arms control reduces risk", "Treaties stabilize relations", "Trust is fragile",
    "Power requires legitimacy", "Influence depends on perception", "Global order is changing",
    "Rivalries shape alliances", "Security dilemmas create tension", "Geopolitics affects markets",
    "Political stability attracts investment", "Sanctions impact economies", "Energy prices influence policy",
    "Strategic autonomy is valued", "National interest guides actions", "Power projection defines status",
    "Geopolitics shapes the future", "Global balance is dynamic", "Diplomacy is essential"
  ]
}

# --- Initialize Generators (Efficiency) ---
generators = {}
for topic, data in topics_data.items():
    generators[topic] = TweetGenerator(data)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_tweet', methods=['GET'])
def get_tweet():
    topic = request.args.get('topic', 'tech')
    generator = generators.get(topic, generators['tech'])
    tweet = generator.generate()
    return jsonify({'tweet': tweet})

if __name__ == '__main__':
    app.run(debug=True)