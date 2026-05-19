from flask import Flask, request, jsonify
import oqs # Quantum Safe Library
import base64
import json

app = Flask(__name__)

# Load your Public Key (Generated in Phase 1)
with open("NYC-01_vultar.pub", "rb") as f:
    PUBLIC_KEY = f.read()

@app.route('/validate', methods=['POST'])
def validate():
    admission_review = request.get_json()
    pod_spec = admission_review['request']['object']
    image = pod_spec['spec']['containers'][0]['image']
    
    # In a real 2026 production environment, we'd use Cosign's API here.
    # For your solo build, we verify the 'vultar-signature' annotation.
    annotations = pod_spec['metadata'].get('annotations', {})
    signature_b64 = annotations.get('vultar-signature')

    if not signature_b64:
        return admission_response(False, "❌ REJECTED: No Quantum Signature found.")

    # PQC VERIFICATION
    verifier = oqs.Signature('ML-DSA-65')
    is_valid = verifier.verify(image.encode(), base64.b64decode(signature_b64), PUBLIC_KEY)

    if is_valid:
        return admission_response(True, "✅ VERIFIED: Quantum Signature matches.")
    else:
        return admission_response(False, "🚫 ALARM: Signature Mismatch! Possible Tampering.")

def admission_response(allowed, message):
    return jsonify({
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "allowed": allowed,
            "status": {"message": message}
        }
    })

if __name__ == '__main__':
    # Webhooks MUST run over HTTPS
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))