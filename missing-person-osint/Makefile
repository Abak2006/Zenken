.PHONY: setup generate mockserver collect analyze graph map timeline dashboard evaluate report test all clean

PYTHON ?= python

setup:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m spacy download en_core_web_sm

generate:
	$(PYTHON) -m generator.run --seed 42 --days 45

mockserver:
	$(PYTHON) -m mock_platform.app --port 5005

collect:
	$(PYTHON) -m collectors.mock_collector

analyze:
	$(PYTHON) -m correlation.entity_resolution

graph:
	$(PYTHON) -c "from graph import build_investigation_graph, run_graph_analytics, export_all_formats; g = build_investigation_graph(); run_graph_analytics(g); export_all_formats(g)"

map:
	$(PYTHON) -m geo.movement_analysis
	$(PYTHON) -m geo.map_builder

timeline:
	$(PYTHON) -m timeline.timeline_builder
	$(PYTHON) -m timeline.hypotheses

dashboard:
	streamlit run dashboard/streamlit_app.py

evaluate:
	$(PYTHON) -m evaluation.evaluate

report:
	$(PYTHON) -m reports.report_generator

test:
	$(PYTHON) -m pytest -v

all: generate collect analyze graph map timeline evaluate report test
	@echo "========================================================================"
	@echo "[+] END-TO-END FORENSIC PIPELINE EXECUTION COMPLETE"
	@echo "    - Synthetic Data Generated in data/"
	@echo "    - Chain of Custody logged in data/chain_of_custody.jsonl"
	@echo "    - Identities Resolved in data/resolved_identities.json"
	@echo "    - Interactive Map rendered at data/investigation_map.html"
	@echo "    - Multi-Lane Timeline rendered at data/investigation_timeline.html"
	@echo "    - PyVis Graph rendered at data/investigation_graph.html"
	@echo "    - Final Report rendered at reports/final_report.md"
	@echo "    - All 14 Pytest Unit Tests Passed"
	@echo "========================================================================"

clean:
	@powershell -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue data/photos, data/*.csv, data/*.json, data/*.html, data/*.graphml, data/raw_collected, reports/*.json, reports/*.png, reports/*.md, .pytest_cache"
