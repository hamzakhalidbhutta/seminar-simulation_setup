# datasets/create_ai_haimm_dataset.py
import pandas as pd
import random
import urllib.parse

print("Generating HAIMM Aviation Network Dataset...")

# 1. Clean Aviation API Endpoints (The normal traffic)
clean_endpoints = [
    "/api/v1/passenger/manifest?flight=TK",
    "/api/v2/baggage/routing?tag_id=",
    "/api/telemetry/runway_status?sensor=",
    "/api/auth/crew_login?user=",
    "/api/maintenance/logs?aircraft_tail="
]

# 2. Raw Attack Payloads (SQLi, XSS, Path Traversal)
raw_attacks = [
    "' OR '1'='1",
    "1; DROP TABLE passengers--",
    "<script>alert('xss')</script>",
    "../../../../etc/passwd",
    "' UNION SELECT username, password FROM admin_users--"
]

data = []

# Generate 5,000 Safe Packets
for _ in range(5000):
    endpoint = random.choice(clean_endpoints)
    # Add some random numbers to simulate real IDs (e.g., flight TK1998)
    safe_uri = f"api.ist-airport.local{endpoint}{random.randint(1000, 9999)}"
    data.append({"uri": safe_uri, "label": 0}) # 0 = Safe

# Generate 5,000 Malicious (Mutated) Packets
for _ in range(5000):
    endpoint = random.choice(clean_endpoints)
    attack = random.choice(raw_attacks)
    
    # URL-Encode the attack to simulate the WAF-bypass mutation!
    mutated_attack = urllib.parse.quote(attack)
    
    malicious_uri = f"api.ist-airport.local{endpoint}{mutated_attack}"
    data.append({"uri": malicious_uri, "label": 1}) # 1 = Malicious

# Shuffle and Save
df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True) # Shuffle the data randomly
df.to_csv("haimm_training_data.csv", index=False)

print(f"[SUCCESS] Generated {len(df)} network logs.")
print("Saved to 'haimm_training_data.csv'.")
print("Preview:")
print(df.head())