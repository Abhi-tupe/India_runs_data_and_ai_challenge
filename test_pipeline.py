import unittest
import json
from rank import is_honeypot, clean_text, extract_searchable_text

class TestATSEngine(unittest.TestCase):

    def setUp(self):
        """Set up standard base candidate mock data for unit assertions."""
        self.valid_candidate = {
            "candidate_id": "CAND_TEST_001",
            "profile": {
                "anonymized_name": "Test Engineer",
                "current_title": "Senior ML Engineer",
                "current_company": "Tech Platform",
                "years_of_experience": 6.5
            },
            "redrob_signals": {
                "verified_email": True,
                "verified_phone": True,
                "profile_views_received_30d": 12,
                "recruiter_response_rate": 0.85
            },
            "career_history": [{"company": "Razorpay", "title": "AI Engineer"}],
            "skills": [{"name": "pgvector", "duration_months": 24, "proficiency": "advanced"}]
        }

    def test_valid_candidate_passes_sieve(self):
        """Ensure an ideal candidate sweeps through the sieve cleanly."""
        self.assertFalse(is_honeypot(self.valid_candidate), "Valid profile flagged as honeypot anomaly.")

    def test_honeypot_unverified_contact(self):
        """Stage 1 Trap: Catch profiles with unverified contact vectors."""
        bad_cand = self.valid_candidate.copy()
        bad_cand["redrob_signals"] = {"verified_email": False, "verified_phone": True}
        self.assertTrue(is_honeypot(bad_cand), "Failed to sieve unverified email footprint.")

    def test_honeypot_ghost_candidate(self):
        """Stage 1 Trap: Catch low-engagement profiles with anomalously high view rates."""
        ghost_cand = self.valid_candidate.copy()
        ghost_cand["redrob_signals"] = {
            "verified_email": True,
            "verified_phone": True,
            "profile_views_received_30d": 55,
            "recruiter_response_rate": 0.05  # High views, near-zero engagement
        }
        self.assertTrue(is_honeypot(ghost_cand), "Failed to detect inactive ghost candidate trap.")

    def test_service_firm_exclusion(self):
        """Stage 1 Trap: Blacklist corporate service firms."""
        service_cand = self.valid_candidate.copy()
        service_cand["career_history"] = [{"company": "Tata Consultancy Services", "title": "System Analyst"}]
        self.assertTrue(is_honeypot(service_cand), "Failed to filter out corporate service firm.")

    def test_impossible_skill_durations(self):
        """Stage 1 Trap: Flag impossible profile skill metrics (expert with 0 duration)."""
        fake_skill_cand = self.valid_candidate.copy()
        fake_skill_cand["skills"] = [{"name": "FAISS", "duration_months": 0, "proficiency": "expert"}]
        self.assertTrue(is_honeypot(fake_skill_cand), "Failed to catch impossible skill duration anomaly.")

    def test_text_normalization(self):
        """Utility Check: Ensure structural string cleaners normalize text accurately."""
        self.assertEqual(clean_text("  PyTorch  "), "pytorch")
        self.assertEqual(clean_text(None), "")

if __name__ == "__main__":
    print("\n🚀 Launching Redrob ATS Infrastructure Unit Testing Suite...")
    unittest.main()