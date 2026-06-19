from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import json

app = FastAPI(
    title="Redrob Candidate Discovery Engine API",
    description="Enterprise REST endpoints for querying high-performance filtered technical shortlists.",
    version="1.0.0"
)

# Load the generated artifact globally for lightning-fast reads
try:
    RANKED_DF = pd.read_csv("team_abhi.csv")
except Exception:
    RANKED_DF = None

@app.get("/api/v1/health")
def health_check():
    """System heartbeat endpoint to verify infrastructure availability."""
    if RANKED_DF is None:
        raise HTTPException(status_code=503, detail="Shortlist artifact team_abhi.csv not found locally.")
    return {"status": "ONLINE", "records_loaded": len(RANKED_DF)}

@app.get("/api/v1/candidates/top")
def get_top_candidates(limit: int = Query(default=10, ge=1, le=100)):
    """
    Exposes the top ranked candidate pool payload.
    Allows downstream services to consume sorted profiles dynamically.
    """
    if RANKED_DF is None:
        raise HTTPException(status_code=500, detail="Data layer unavailable.")
    
    # Slice the exact slice requested by the user
    subset = RANKED_DF.head(limit)
    return subset.to_dict(orient="records")