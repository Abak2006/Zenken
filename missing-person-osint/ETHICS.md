# Ethical Framework, Legal Boundaries, and Academic Scope

## 1. Project Purpose and Educational Scope

This academic project, titled **"Missing Person Investigation Through Simulated Social Media Evidence"**, is designed strictly for educational instruction, scientific research, and professional training in digital forensics, open-source intelligence (OSINT), and multi-modal link analysis. 

The primary objectives are:
- To teach computational methodologies for identity resolution, spatiotemporal clustering, and forensic graph correlation.
- To demonstrate how public digital footprints and metadata hygiene impact personal privacy and safety.
- To provide an ethically sound, fully reproducible sandbox that eliminates the legal and privacy hazards inherent in investigating real persons.

---

## 2. Hard Constraints & Safety Safeguards

### 2.1 Exclusively Synthetic Data (No Real Individuals)
- **Zero Real PII:** All personas, names, screen names, biographies, emails, and locations within this repository are 100% fictional.
- **Reserved Fictional Telephony:** All telephone numbers use the North American Numbering Plan (NANP) fictional reservation range (`+1-555-0100` through `+1-555-0199`). Under no circumstances should real telephone numbers be inserted into the scenario.
- **No Real Faces or Biometrics:** All media artifacts are programmatically generated using Pillow as geometric, landscape, or abstract gradient canvases. No photographs of real human beings, synthetic deepfakes, or facial biometric models are used or permitted.

### 2.2 Strict Prohibition on Live Social Media Scraping
- **No Live Target Surveillance:** Investigators and students must **never** direct automated scrapers, crawlers, or enumeration tools against real production social media platforms (e.g., Instagram, X/Twitter, LinkedIn, Meta, TikTok) for real individuals as part of this coursework.
- **Opt-In Tooling with Prominent Warnings:** Tool wrappers (such as `sherlock_wrapper.py` and `spiderfoot_wrapper.py`) operate in **Mock Mode by default**. Querying live platforms for fictional usernames is disabled because any resulting hits would belong to real, unrelated third parties, producing dangerous false positives and violating their privacy rights.

### 2.3 Chain of Custody & Cryptographic Provenance
- All collected digital artifacts are hashed immediately upon acquisition using SHA-256 and recorded in an immutable JSONL audit ledger (`data/chain_of_custody.jsonl`).
- Forensic evidence integrity must be preserved to model standard legal evidentiary admissibility (Federal Rules of Evidence 901/902 and ISO/IEC 27037 standards).

---

## 3. Privacy Settings & Metadata Hygiene Implications

This project highlights how unintended digital exhaust can compromise personal security:
1. **EXIF Geolocation Leakage:** Default smartphone camera settings frequently record high-precision GPS coordinates, altitude, and timestamps within image EXIF headers. Uploading uncompressed imagery exposes residences, daily commutes, and routine vulnerabilities.
2. **Handle Enumeration and Cross-Platform Tracking:** Individuals frequently reuse identical or near-identical handles across public forums, professional registries, and personal microblogs. This enables adversaries to correlate disparate identities and map complete personal networks.
3. **Telecommunication Sector Triangulation:** Even when GPS is turned off on a mobile device, cellular tower routing pings reveal approximate geographic sectors and dwell times.

---

## 4. Legal Compliance & Code of Conduct

Users of this codebase agree to adhere to the following standards:
- **Computer Fraud and Abuse Act (CFAA) & Regional Computer Misuse Acts:** Users must never deploy these tools to access unauthorized systems, bypass access controls, or harass individuals.
- **Terms of Service (ToS) Compliance:** Academic labs must respect platform terms of service and robots.txt directives.
- **Dual-Use Awareness:** While the analytical methods (graph centrality, DBSCAN clustering, entity resolution) have legitimate search-and-rescue (SAR) and missing-persons applications, they can also be weaponized for stalking or doxxing. Users are obligated to apply these techniques exclusively under lawful, defensive, and academic mandates.

---

## 5. Ground Truth Partitioning

To maintain academic rigor and prevent data leakage:
- `case/ground_truth.json` is strictly partitioned from extraction, correlation, and graph construction modules.
- Only the `evaluation/evaluate.py` script is permitted to access ground truth data to objectively benchmark pipeline performance.
