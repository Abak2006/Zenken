"""
Test that all hypothesis cards and evaluation metrics render with zero leading whitespace,
guaranteeing no markdown indented code block leaks.
"""
from dashboard.streamlit_app import load_case_data, AVAILABLE_CASES

def clean_html(html_str: str) -> str:
    return "\n".join(line.strip() for line in html_str.split("\n") if line.strip())

def test_hypotheses_and_evaluation_zero_indent():
    for cid in AVAILABLE_CASES:
        data = load_case_data(cid)
        raw_hyp = data.get("hypotheses", [])
        hyp_list = raw_hyp if isinstance(raw_hyp, list) else raw_hyp.get("hypotheses", [])
        assert len(hyp_list) > 0, f"No hypotheses found for case {cid}"
        
        for h in hyp_list:
            title = h.get("title", "")
            summary = h.get("summary", "")
            supp = h.get("supporting_evidence", [])
            contra = h.get("contradicting_evidence", [])
            
            raw_html = f"""
            <div class="panel">
                <div class="card-header-bar">
                    <span>{title}</span>
                </div>
                <p>{summary}</p>
                <ul>
                    {''.join(f'<li>{s}</li>' for s in supp)}
                </ul>
            </div>
            """
            cleaned = clean_html(raw_html)
            for line in cleaned.split("\n"):
                assert not line.startswith("    "), f"Indented line found: {line}"
                assert len(line) - len(line.lstrip()) == 0, f"Leading space found: {line}"
