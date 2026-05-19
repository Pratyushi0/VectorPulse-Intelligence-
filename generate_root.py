import oqs
import os

# 1. Initialize the Signature mechanism for ML-DSA-65
sigalg = "ML-DSA-65" # This is the finalized NIST name for Dilithium3
with oqs.Signature(sigalg) as signer:
    print(f"📦 Generating Root Keys for Algorithm: {sigalg}")
    
    # 2. Generate the Keypair
    public_key = signer.generate_keypair()
    private_key = signer.export_secret_key()

    # 3. Save them to your 'convergence' folder
    with open("sentinel-root.key", "wb") as f:
        f.write(private_key)
    with open("sentinel-root.pub", "wb") as f:
        f.write(public_key)

    print("✅ Success! 'sentinel-root.key' and 'sentinel-root.pub' created.")
    print("🔒 Keep the .key file safe; it is the Root of Trust for your grid.")