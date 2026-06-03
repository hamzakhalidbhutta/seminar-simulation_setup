from scapy.all import sniff
from scapy.layers.http import HTTPRequest

def process_packet(packet):
    """
    This function acts as the 'Gateway'. Every time a packet arrives, 
    Scapy sends it here.
    """
    # We only care about HTTP Requests (like the GET request you made)
    if packet.haslayer(HTTPRequest):
        
        # Extract the Host (e.g., neverssl.com)
        host = packet[HTTPRequest].Host.decode('utf-8') if packet[HTTPRequest].Host else ""
        
        # Extract the Path/Query (e.g., /?id=1'%20OR%20'1'='1)
        path = packet[HTTPRequest].Path.decode('utf-8') if packet[HTTPRequest].Path else ""
        
        # Combine them to recreate the exact string your AI model needs
        full_uri = f"{host}{path}"
        method = packet[HTTPRequest].Method.decode('utf-8') if packet[HTTPRequest].Method else ""

        print("-" * 50)
        print(f"[+] INCOMING {method} REQUEST DETECTED")
        print(f"[!] AI Input Signature: {full_uri}")
        
        # ---------------------------------------------------------
        # FUTURE THESIS STEP:
        # Here is where you will pass 'full_uri' to your DistilBERT 
        # model for Early-Exit classification!
        #
        # if caed_http_model.predict(full_uri) == "Malicious":
        #     print("BLOCKING PACKET!")
        # ---------------------------------------------------------

print("Starting Neural-Edge Gateway Sniffer...")
print("Listening for HTTP traffic on port 80. Press Ctrl+C to stop.")

# sniff() captures the traffic. 
# filter="tcp port 80" ensures we only catch unencrypted web traffic.
# prn=process_packet tells it to send every caught packet to our function.
# store=False keeps it fast so it doesn't eat up your RAM.
sniff(filter="tcp port 80", prn=process_packet, store=False)