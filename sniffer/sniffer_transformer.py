# /sniffer/sniffer_transformer.py
from scapy.all import sniff
from scapy.layers.http import HTTPRequest
from transformers import AutoTokenizer

# Load the "brain" - DistilBERT's exact tokenizer
print("Loading DistilBERT Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def process_packet(packet):
    """
    The Gateway Pipeline: Sniff -> Extract -> Tokenize
    """
    if packet.haslayer(HTTPRequest):
        host = packet[HTTPRequest].Host.decode('utf-8') if packet[HTTPRequest].Host else ""
        path = packet[HTTPRequest].Path.decode('utf-8') if packet[HTTPRequest].Path else ""
        full_uri = f"{host}{path}"
        method = packet[HTTPRequest].Method.decode('utf-8') if packet[HTTPRequest].Method else ""

        print("\n" + "=" * 60)
        print(f"[+] RAW INCOMING: {full_uri}")
        
        # ---------------------------------------------------------
        # THE AI INTEGRATION
        # We chop the raw string into the mathematical tokens 
        # the model actually uses for classification.
        # ---------------------------------------------------------
        tokens = tokenizer.tokenize(full_uri)
        print(f"[!] AI TOKEN VIEW: {tokens}")
        print("=" * 60)

print("Neural-Edge Gateway Sniffer Active.")
print("Listening for HTTP traffic on port 80. Press Ctrl+C to stop.")

# Capture the traffic
sniff(filter="tcp port 80", prn=process_packet, store=False)