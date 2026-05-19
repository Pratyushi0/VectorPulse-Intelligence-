# Define your recovery image
IMAGE="grid-registry.io/recovery/scada-node:v1.0"

# Sign the image digest using your ML-DSA-65 key
# This creates a 'provenance' record in the registry
cosign sign --key vultar_private.key $IMAGE

echo "✅ Image $IMAGE signed with Post-Quantum Lattice signature."