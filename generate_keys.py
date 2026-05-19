import oqs
import os

# ML-DSA-65 is the NIST standard for Dilithium Level 3
sig_alg = "ML-DSA-65"

def generate_sentinel_keys():
    print(f"🛠️  Initializing {sig_alg}...")
    
    with oqs.Signature(sig_alg) as signer:
        # Generate the Keypair
        public_key = signer.generate_keypair()
        private_key = signer.export_secret_key()

        # Save the Private Key (The Root of Trust)
        with open("sentinel-root.key", "wb") as f:
            f.write(private_key)
        
        # Save the Public Key (The Gatekeeper's Key)
        with open("sentinel-root.pub", "wb") as f:
            f.write(public_key)

    print("✅ Success! Keys generated in your 'convergence' folder.")
    print(f"📄 Private: sentinel-root.key ({len(private_key)} bytes)")
    print(f"📄 Public:  sentinel-root.pub ({len(public_key)} bytes)")

if __name__ == "__main__":
    generate_sentinel_keys()