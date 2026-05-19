# Create a multi-node cluster to simulate a distributed power grid
cat <<EOF > cluster-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker # Node 1: NYC Substation
- role: worker # Node 2: LA Substation
- role: worker # Node 3: Chicago Substation
EOF

kind create cluster --name sovereign-mesh --config cluster-config.yaml

# Install Cilium for eBPF observability
helm install cilium cilium/cilium --version 1.15.2 \
  --namespace kube-system \
  --set hubble.enabled=true \
  --set hubble.ui.enabled=true \
  --set bpf.masquerade=true