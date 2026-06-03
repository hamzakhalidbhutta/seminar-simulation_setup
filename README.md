# Neural-Edge Security Gateway: HAIMM Architecture Prototype

## Project Overview

This repository contains the simulation environment, data generation pipeline, and live inference codebase for a domain-agnostic, AI-driven network gateway.

Designed to address the **Robustness-Efficiency Paradox** in high-stakes edge computing, this prototype replaces traditional static Web Application Firewalls (WAF) with a dynamically fine-tuned DistilBERT classification head. The current iteration utilizes an Aviation Management (HAIMM) dataset as a proof-of-concept for securing critical infrastructure APIs against mutated adversarial payloads.

---

## Directory Structure

```text
simulation_setup/
│
├── main.py                                      # Theoretical Simulation Engine (Mutation & Early-Exit)
├── README.md                                    # Project documentation
│
└── source_code/
    ├── datasets/
    │   └── create_ai_haimm_dataset.py           # Synthetic API & Adversarial Payload Generator
    │
    ├── models/
    │   └── train.py                             # Deep Learning Fine-Tuning Pipeline (Hugging Face)
    │
    └── sniffer/
        ├── sniffer_transformer.py               # Tokenization Intercept Prototype
        └── ai_gateway_sniffer.py                # Live PyTorch Inference & Latency Benchmarking
```
# RUNNING_PROJECT.md

# Running the Neural-Edge Security Gateway

This document provides the exact steps required to execute the project and reproduce the results presented in the research report.

---

## Step 1: Install Dependencies

Install all required Python libraries:

```bash
pip install torch transformers scapy pandas datasets scikit-learn accelerate
```

---

## Step 2: Generate the Training Dataset

Run the dataset generation script:

```bash
python source_code/datasets/create_ai_haimm_dataset.py
```

Expected Output:

```text
haimm_training_data.csv generated successfully
```

This script creates a synthetic aviation-security dataset containing both legitimate API requests and adversarial payloads.

---

## Step 3: Train the DistilBERT Model

Run:

```bash
python source_code/models/train.py
```

The script will:

* Load the generated dataset
* Tokenize the requests
* Fine-tune DistilBERT
* Save the trained model

Expected Output:

```text
Training Complete
Model Saved Successfully
```

---

## Step 4: Observe Transformer Tokenization

Start the token inspection sniffer:

```bash
sudo python source_code/sniffer/sniffer_transformer.py
```

This component:

* Captures HTTP traffic
* Extracts Request URIs
* Passes requests through the DistilBERT tokenizer
* Displays WordPiece tokenization output

---

## Step 5: Start the AI Gateway

Run:

```bash
sudo python source_code/sniffer/ai_gateway_sniffer.py
```

This launches the Neural-Edge Security Gateway and begins monitoring live traffic.

The gateway will:

* Capture packets
* Extract requests
* Convert text to tensors
* Execute DistilBERT inference
* Display classifications
* Measure latency

---

## Step 6: Generate Test Traffic

Open a new terminal and execute:

```bash
curl "http://neverssl.com/?id=1%27%20OR%20%271%27%3D%271"
```

Decoded Payload:

```text
?id=1' OR '1'='1
```

This simulates a URL-encoded SQL Injection attack.

---

## Expected Results

The gateway should detect the malicious payload and output something similar to:

```text
Captured Request:
http://neverssl.com/?id=1%27%20OR%20%271%27%3D%271

Prediction:
MALICIOUS

Inference Time:
~100ms
```

---

## Project Workflow

```text
Generate Dataset
       │
       ▼
Train DistilBERT
       │
       ▼
Start Packet Sniffer
       │
       ▼
Launch AI Gateway
       │
       ▼
Generate Test Traffic
       │
       ▼
Capture Request
       │
       ▼
Tokenization
       │
       ▼
Inference
       │
       ▼
Threat Classification
```

---

## Notes

* Administrator/root privileges are required for packet capture.
* Internet connectivity is required to generate test traffic using the provided URL.
* The current implementation serves as a proof-of-concept for the proposed Neural-Edge Security Gateway architecture.

---

## Module Breakdown & Execution Flow

### 1. The Theoretical Simulation (`main.py`)

This script serves as the foundational proof-of-concept for the core theories proposed in this research:

#### Theory 3.3 – The Mutation Engine

Simulates how attackers obfuscate malicious payloads using techniques such as:

* URL Encoding
* SQL Comment Injection (`/**/`)
* Character Permutation
* Payload Mutation

These transformations demonstrate how adversaries attempt to bypass traditional signature-based and rule-based WAF systems.

#### Theory 3.5 – Early-Exit Inference

Demonstrates a multi-layer classification architecture:

* **Layer 1:** Lightweight high-confidence threat detection.
* **Layer 2:** Deep semantic analysis for heavily mutated payloads.

This approach reduces computational overhead while maintaining detection accuracy, making it suitable for edge deployment scenarios.

---

### 2. Domain-Specific Data Engineering (`source_code/datasets/`)

#### `create_ai_haimm_dataset.py`

Programmatically generates a synthetic cybersecurity dataset (`haimm_training_data.csv`) containing:

* Legitimate aviation-related API requests
* SQL Injection (SQLi) attacks
* Cross-Site Scripting (XSS) attacks
* Path Traversal attempts
* URL-encoded malicious payloads

The resulting dataset provides explicit safe-versus-malicious labels required for supervised machine learning and cybersecurity classification tasks.

---

### 3. Model Fine-Tuning (`source_code/models/`)

#### `train.py`

Implements the training pipeline using:

* Hugging Face Transformers
* Hugging Face Datasets
* PyTorch Backend

The script fine-tunes:

```text
distilbert-base-uncased
```

for malicious payload classification.

Key responsibilities:

* Dataset loading and preprocessing
* Tokenization
* Train/validation split
* Model fine-tuning
* Classification weight initialization
* Performance evaluation

The resulting model learns semantic representations of both normal API traffic and mutated cyber threats.

---

### 4. Real-Time Network Interception (`source_code/sniffer/`)

This module transitions the project from offline experimentation to live network traffic analysis.

#### `sniffer_transformer.py`

A packet interception prototype that:

1. Captures HTTP traffic using Scapy.
2. Extracts Request URIs.
3. Passes incoming payloads through the DistilBERT tokenizer.
4. Displays WordPiece token fragmentation.

This component provides visibility into how transformer-based architectures interpret network payloads.

---

#### `ai_gateway_sniffer.py`

The fully integrated Neural-Edge Security Gateway.

Core functionality:

* Live packet interception
* URI extraction
* Tokenization
* Tensor generation
* PyTorch inference
* Real-time classification
* Latency benchmarking

Inference is executed using:

```python
torch.no_grad()
```

to minimize computational overhead during deployment.

Example output:

```text
Request: /api/passenger/list
Prediction: SAFE

Request: /api/login?id=' OR 1=1 --
Prediction: MALICIOUS
```

---

### Research Benchmark

Current testing establishes an approximate inference latency of:

```text
~100ms per packet
```

on standard CPU hardware.

This benchmark highlights the practical motivation behind the proposed:

* Fuzzy-Logic Early-Exit Framework
* Multi-layer Inference Architecture
* Edge-AI Optimization Strategy

for future research iterations.

---

## End-to-End Workflow

```text
Dataset Generation
        │
        ▼
HAIMM Training Dataset
        │
        ▼
DistilBERT Fine-Tuning
        │
        ▼
Trained Classification Model
        │
        ▼
Live Packet Capture (Scapy)
        │
        ▼
Tokenizer Processing
        │
        ▼
PyTorch Inference
        │
        ▼
Threat Classification
        │
        ▼
Latency Measurement
```

---

## Prerequisites

Python 3.10+ is recommended.

Required libraries:

```bash
pip install torch transformers scapy pandas datasets scikit-learn accelerate
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd simulation_setup
```

Install dependencies:

```bash
pip install torch transformers scapy pandas datasets scikit-learn accelerate
```

---

## Running the Project

### Generate the Dataset

```bash
python source_code/datasets/create_ai_haimm_dataset.py
```

### Train the DistilBERT Model

```bash
python source_code/models/train.py
```

### Run the Tokenization Sniffer

```bash
sudo python source_code/sniffer/sniffer_transformer.py
```

### Run the AI Gateway

```bash
sudo python source_code/sniffer/ai_gateway_sniffer.py
```

---

## Security Notice

The network interception modules require elevated privileges because packet capture occurs directly at the network interface level.

Linux/macOS:

```bash
sudo python ai_gateway_sniffer.py
```

Windows:

```powershell
Run PowerShell as Administrator
```

---

## Research Contributions

This prototype demonstrates the feasibility of:

* AI-driven Web Application Firewall replacement
* Adversarial payload mutation resilience
* Transformer-based cybersecurity classification
* Edge-AI deployment strategies
* Early-exit inference architectures
* Latency-aware threat detection

The HAIMM implementation serves as a proof-of-concept for extending these techniques to critical infrastructure domains such as aviation, healthcare, industrial control systems, and smart-city deployments.

---

## Author

**Hamza Khalid Bhutta**

MSc Artificial Intelligence Researcher

Research Focus:

* Edge AI
* Cybersecurity
* Transformer Architectures
* Adversarial Machine Learning
* Intelligent Network Security Systems

