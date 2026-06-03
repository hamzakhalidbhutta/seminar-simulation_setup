import random
import urllib.parse

# --- THEORY 3.3: THE MUTATION ENGINE ---
def mutate_request(payload):
    """Simulates an attacker disguising a 'SQL Injection'"""
    mutations = [
        lambda p: p, # Clean version
        lambda p: urllib.parse.quote(p), # URL Encoded mutation
        lambda p: p.replace(" ", "/**/"), # SQL Comment mutation
        lambda p: "".join(reversed(p))    # Character reordering
    ]
    return random.choice(mutations)(payload)

# --- THEORY 3.5: EARLY-EXIT INFERENCE ---
def early_exit_classifier(request_text):
    """Simulates a model checking the request layer by layer"""
    malicious_keywords = ["SELECT", "DROP", "OR 1=1", "SCRIPT"]
    
    # Layer 1: Quick check (Early Exit)
    if any(word in request_text.upper() for word in malicious_keywords):
        return "BLOCKED (Layer 1 - High Confidence)"
    
    # Layer 2: Deeper check (Simulating the AI 'un-mutating' things)
    decoded = urllib.parse.unquote(request_text.upper())
    if any(word in decoded for word in malicious_keywords):
        return "BLOCKED (Layer 2 - Deep Inspection)"
        
    return "ALLOWED (Safe Traffic)"

# --- THE SIMULATION ---
def run_sim():
    print("--- Starting AI Security Simulation ---\n")
    attack = "SELECT * FROM users"
    
    for i in range(5):
        # 1. Create a mutated attack
        disguised_attack = mutate_request(attack)
        print(f"Incoming Request: {disguised_attack}")
        
        # 2. Run the detection logic
        result = early_exit_classifier(disguised_attack)
        print(f"AI Decision:      {result}\n")

if __name__ == "__main__":
    run_sim()