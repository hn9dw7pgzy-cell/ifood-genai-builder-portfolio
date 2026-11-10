import json
from pathlib import Path

base = Path(__file__).parent
request = json.loads((base / "sample-request.json").read_text())
classification = json.loads((base / "sample-llm-response.json").read_text())

confidence = float(classification.get("confidence", 0))
route = "human_review" if classification.get("needs_human_review") or confidence < 0.75 else classification["category"]

result = {
    "request_id": "demo-request-0001",
    "input": request,
    "classification": classification,
    "decision": {
        "route": route,
        "automatic": route != "human_review",
        "reason": "confiança acima do limiar de 0.75" if route != "human_review" else "confiança baixa ou revisão solicitada"
    },
    "audit": {
        "mode": "synthetic-demo",
        "llm_called": True,
        "contains_real_customer_data": False
    }
}

print(json.dumps(result, ensure_ascii=False, indent=2))
