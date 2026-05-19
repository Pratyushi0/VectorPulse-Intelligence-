import oqs # Open Quantum Safe library
import base64

def generate_node_identity(node_name):
    # ML-DSA-65 is the finalized Dilithium standard
    sig = oqs.Signature('ML-DSA-65')
    public_key = sig.generate_keypair()
    private_key = sig.export_secret_key()
    
    with open(f"{node_name}_vultar.pub", "wb") as f:
        f.write(public_key)
    
    # In a real grid, this private key is stored in a Hardware Security Module (HSM)
    print(f"✅ Identity created for {node_name}")
    print(f"Public Key (Truncated): {base64.b64encode(public_key[:16]).decode()}...")

for node in ["NYC-01", "LA-01", "CHI-01"]:
    generate_node_identity(node)