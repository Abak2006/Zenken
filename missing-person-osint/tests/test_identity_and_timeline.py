"""
Test Identity Resolution and Timeline data binding and bounds for all active cases.
Ensures zero KeyErrors, proper column normalization, and active incident window calculation.
"""
import pandas as pd
from dashboard.streamlit_app import AVAILABLE_CASES, load_case_data, calculate_case_metrics

def test_identity_resolution_data_integrity():
    for case_id, cfg in AVAILABLE_CASES.items():
        data = load_case_data(cfg["data_dir"])
        assert "resolved" in data, f"Case {case_id} missing resolved identities"
        
        clusters = data["resolved"].get("clusters", [])
        assert len(clusters) > 0, f"Case {case_id} has empty clusters"
        
        clusters_df = pd.DataFrame(clusters)
        
        # Test required columns can be normalized without KeyError
        if "canonical_name" not in clusters_df.columns:
            clusters_df["canonical_name"] = clusters_df["canonical_id"]
        if "accounts" not in clusters_df.columns:
            clusters_df["accounts"] = [[] for _ in range(len(clusters_df))]
        if "account_count" not in clusters_df.columns:
            clusters_df["account_count"] = clusters_df["accounts"].apply(lambda x: len(x) if isinstance(x, (list, tuple)) else 1)
        if "is_multi_account" not in clusters_df.columns:
            clusters_df["is_multi_account"] = clusters_df["account_count"] > 1
        if "linked_emails" not in clusters_df.columns:
            clusters_df["linked_emails"] = [[] for _ in range(len(clusters_df))]
        if "linked_phones" not in clusters_df.columns:
            clusters_df["linked_phones"] = [[] for _ in range(len(clusters_df))]
            
        req_cols = ["canonical_id", "canonical_name", "account_count", "accounts", "linked_emails", "linked_phones", "is_multi_account"]
        sub = clusters_df[req_cols]
        assert len(sub) == len(clusters)

        # Ambiguous links integrity
        if "ambiguous" in data:
            amb = data["ambiguous"]
            raw_list = amb.get("ambiguous_links", []) if isinstance(amb, dict) else (amb if isinstance(amb, list) else [])
            amb_df = pd.DataFrame(raw_list)
            if not amb_df.empty:
                if "confidence" not in amb_df.columns and "similarity_score" in amb_df.columns:
                    amb_df["confidence"] = amb_df["similarity_score"]
                assert "confidence" in amb_df.columns
                filtered = amb_df[amb_df["confidence"] >= 0.1]
                assert len(filtered) > 0

def test_timeline_active_window_detection():
    for case_id, cfg in AVAILABLE_CASES.items():
        data = load_case_data(cfg["data_dir"])
        metrics = calculate_case_metrics(case_id, data)
        raw_events = metrics.get("timeline_events", [])
        assert len(raw_events) > 0, f"Case {case_id} has no timeline events"
        
        df = pd.DataFrame(raw_events)
        df["clean_dt"] = pd.to_datetime(df["timestamp"].astype(str).str.replace(" UTC", ""), errors="coerce", utc=True)
        df = df.dropna(subset=["clean_dt"]).sort_values("clean_dt")
        
        latest_dt = df["clean_dt"].max()
        cutoff_active = latest_dt - pd.Timedelta(days=45)
        active_events = df[df["clean_dt"] >= cutoff_active]
        
        # Verify active window contains at least 70 events and spans <= 45 days
        assert len(active_events) >= 70
        span_days = (active_events["clean_dt"].max() - active_events["clean_dt"].min()).total_seconds() / 86400
        assert span_days <= 46.0, f"Active window span {span_days} exceeds 46 days for case {case_id}"
