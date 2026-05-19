import hashlib
import json
import time
from typing import List

class ConsensusNode:
    def __init__(self, node_id: str, total_nodes: int):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.threshold = (2 * (total_nodes // 3)) + 1 # 2f + 1
        self.vote_ledger = {} # Stores: {threat_id: [list_of_voters]}

    def propose_healing(self, threat_evidence: dict):
        """
        Step 1: Pre-Prepare.
        A node detects a threat and broadcasts the evidence.
        """
        threat_id = hashlib.sha256(json.dumps(threat_evidence).encode()).hexdigest()
        print(f"[CONSENSUS] Node {self.node_id} proposing HEAL for Threat: {threat_id[:8]}")
        return threat_id

    def cast_vote(self, threat_id: str, voter_id: str):
        """
        Step 2: Prepare/Commit.
        Nodes verify the XAI evidence and cast a 'Commit' vote.
        """
        if threat_id not in self.vote_ledger:
            self.vote_ledger[threat_id] = set()
        
        self.vote_ledger[threat_id].add(voter_id)
        vote_count = len(self.vote_ledger[threat_id])
        
        print(f"[VOTE] Threat {threat_id[:8]} has {vote_count}/{self.threshold} votes.")
        
        if vote_count >= self.threshold:
            return True # CONSENSUS REACHED
        return False

# --- LIVE DEMO LOGIC ---
def simulate_grid_consensus():
    nodes = [ConsensusNode(f"Grid-Node-{i}", 4) for i in range(4)]
    evidence = {"target_pod": "smart-meter-alpha", "entropy": 0.98, "type": "Quantum_Injection"}
    
    # Node 0 detects the threat
    threat_id = nodes[0].propose_healing(evidence)
    
    # Other nodes verify and vote
    consensus_reached = False
    for i in range(4): # Simulating all nodes voting
        for node in nodes:
            if node.cast_vote(threat_id, f"Grid-Node-{i}"):
                consensus_reached = True
                break
        if consensus_reached:
            print(f"✅ [SUCCESS] Consensus Reached for {threat_id[:8]}. Executing Self-Healing...")
            break

if __name__ == "__main__":
    simulate_grid_consensus()