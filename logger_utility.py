import time
import os

class PipelineLogger:
    def __init__(self):
        self.start_time = time.time()
        self.metrics = {}

    def log_step(self, step_name, status="SUCCESS", details=""):
        elapsed = time.time() - self.start_time
        print(f"[⏱️ {elapsed:6.3f}s] [{status}] ➡️ {step_name:<35} | {details}")

    def log_metrics(self, total, filtered, passed):
        print("\n" + "="*70)
        print("📊 PIPELINE EXECUTION ANALYTICS REPORT")
        print("="*70)
        print(f"🔹 Total Input Stream Records : {total:,}")
        print(f"🎯 Anomalous Profiles Dropped : {filtered:,} ({filtered/total*100:.2f}%)")
        print(f"🚀 High-Value Profiles Passed: {passed:,}")
        print(f"⚡ Total Execution Velocity   : {passed / (time.time() - self.start_time):.2f} records/sec")
        print("="*70 + "\n")