# /sniffer/ai_gateway_sniffer.py
import time
import torch
from scapy.all import sniff
from scapy.layers.http import HTTPRequest
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print("Loading Neural-Edge AI Gateway...")

# 1. Load the Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# 2. Load the Classifier (The "Brain")
# For the prototype, we use a basic pre-trained model. 
# For your thesis, you will replace "distilbert-base-uncased" with your custom CAED-HTTP weights.
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
model.eval() # Set model to evaluation mode (faster, no training)

print("[SUCCESS] DistilBERT loaded. Ready for live traffic.")

def process_packet(packet):
    """
    The Gateway Pipeline: Sniff -> Tokenize -> Predict -> Act
    """
    if packet.haslayer(HTTPRequest):
        host = packet[HTTPRequest].Host.decode('utf-8') if packet[HTTPRequest].Host else ""
        path = packet[HTTPRequest].Path.decode('utf-8') if packet[HTTPRequest].Path else ""
        full_uri = f"{host}{path}"
        method = packet[HTTPRequest].Method.decode('utf-8') if packet[HTTPRequest].Method else ""

        print("\n" + "=" * 60)
        print(f"[+] RAW INCOMING: {full_uri}")
        
        # Start the latency timer (Crucial for your HAIMM Aviation benchmark)
        start_time = time.time()

        # ---------------------------------------------------------
        # THE INFERENCE ENGINE
        # ---------------------------------------------------------
        # 1. Convert the raw string into PyTorch tensors
        inputs = tokenizer(full_uri, return_tensors="pt", truncation=True, max_length=128)
        
        # 2. Feed the tensors into DistilBERT without calculating gradients (saves memory)
        with torch.no_grad():
            outputs = model(**inputs)
            
        # 3. Extract the prediction (0 = Safe, 1 = Malicious/Anomaly)
        prediction = torch.argmax(outputs.logits, dim=-1).item()
        
        # End the latency timer
        inference_time = (time.time() - start_time) * 1000 # Convert to milliseconds

        if prediction == 1:
            print(f"[🚨] ACTION: MALICIOUS PAYLOAD DETECTED! CONNECTION DROPPED.")
        else:
            print(f"[✅] ACTION: SAFE TRAFFIC. FORWARDING TO SERVER.")
            
        print(f"[⏱️] AI Processing Time: {inference_time:.2f} ms")
        print("=" * 60)

print("Listening for HTTP traffic on port 80. Press Ctrl+C to stop.")
sniff(filter="tcp port 80", prn=process_packet, store=False)
