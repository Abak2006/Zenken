# Digital Forensic & OSINT Investigative Report
## Case #MP-2026-0419: Disappearance of Maya Lin
**Investigation Status:** ACTIVE FORENSIC REFERRAL  
**Date of Report:** 2026-09-24 10:35:55 UTC  
**Investigating Unit:** Academic Cyber Forensics & Open Source Intelligence Laboratory  
**Benchmark Target:** Academic Simulation Dataset (100% Synthetic)

---

## 1. Executive Summary

On the morning of March 15, 2026, Maya Lin (age 21), a senior BFA photography student at Bayview Arts Institute, was reported missing by her roommate, Chloe Simmons. Digital evidence aggregation across social media microblogs, telecommunication call detail records (CDR), venue check-ins, and photographic EXIF telemetry was conducted using open-source intelligence (OSINT) and graph correlation methodologies.

Through multi-factor entity resolution, four disparate digital identities (`@mayalin_art`, `@m_lin99`, `@pixel_maya`, and `@m.shadow_7`) were conclusively linked with 92.3% pairwise F1 score. Movement anomaly analysis identified a significant departure from her routine geographic baseline, pinpointing a terminal cell tower ping and check-in at **Whispering Pines Ridge Sector** (Coordinates: `37.893, -122.573`) on **2026-03-14 at 21:45 UTC**. 

Corroborating telecommunications and web archive forensics indicate Maya was coerced or lured into an off-grid architectural photo shoot by an associate identified as **Kaelen Vance** (`@kaelen_v`, `+1-555-0188`).

---

## 2. Multi-Modal Evidence & Data Description

| Evidence Category | Source Modality | Count / Volume | Key Artifacts |
| :--- | :--- | :--- | :--- |
| **Social Microblogs** | HTML Scraping & JSON API | 31 Posts | 3 Deleted Posts recovered via Wayback Cache |
| **Identity Profiles** | Multi-Platform User Crawl | 25 Profiles | 4 Resolved Maya Lin accounts, 15 Associates |
| **Telephony / CDR** | Carrier Gateway Logs | 24 Call Records | 6 Cell Tower Sectors, 1 Burner SIM Activated |
| **Physical Check-ins** | Geolocation Check-in API | 27 Records | 4 Routine Venues, 2 Anomalous Outlier Venues |
| **Photographic Media** | Synthetic JPEG + EXIF | 10 Photos | Sony a7 IV, Pixel 7, iPhone 8 (Red Herring) |
| **Chain of Custody** | Cryptographic Ledger | 50+ Entries | SHA-256 Hashes, Source URIs, Custody Logs |

---

## 3. Investigation Methodology

The investigation followed a 6-stage forensically sound OSINT methodology:
```mermaid
flowchart LR
    A[Mock Platform & Data Collection] --> B[Normalization & Extraction]
    B --> C[Multi-Factor Entity Resolution]
    C --> D[Multi-Modal Investigation Graph]
    D --> E[Geospatial & Dwell Clustering]
    E --> F[Timeline & Hypotheses Generation]
```

1. **Custodial Evidence Acquisition:** Automated collection with strict chain-of-custody logging (SHA-256 verification and provenance timestamps).
2. **Forensic Extraction & Normalization:** Standardized mixed timestamps (PST, UTC, Unix Epoch) into ISO 8601 UTC. Converted EXIF rational DMS coordinates to decimal degrees and flagged metadata stripping.
3. **Identity Resolution:** Fuzzy string similarity (RapidFuzz), shared credentials (email, phone), bio token overlap, and perceptual image hashing (`imagehash.phash`).
4. **Graph Construction:** NetworkX and Neo4j relational graph modeling `Person`, `Account`, `Phone`, `Location`, `Post`, and `Photo` entities.
5. **Spatial Dwell-Time Clustering:** DBSCAN algorithmic clustering over Haversine distances to isolate routine hubs from final deviations.
6. **Timeline & Hypotheses Evaluation:** Chronological reconstruction across multi-source swimlanes with Bayesian-style hypothesis scoring.

---

## 4. Key Evidentiary Findings

### 4.1 Digital Identity Resolution
- Primary showcase handle `@mayalin_art` and casual handle `@m_lin99` share identical email domains and phone reference `+1-555-0144`.
- Archived portfolio `@pixel_maya` shares camera hardware fingerprint (`Sony ILCE-7M4`) and bio keywords.
- Pseudonymous account `@m.shadow_7` (activated March 3, 2026) was correlated via attached photo pHash and shared check-in at Whispering Pines Overlook.

### 4.2 Critical 72-Hour Behavioral Shift
- **Day 31 (Mar 01):** Unsolicited message from `@kaelen_v` offering high-paying off-grid architectural commissions.
- **Day 33 (Mar 03):** Post sentiment drops abruptly; subject publishes notes regarding feeling watched.
- **Day 40 (Mar 10):** Primary phone (`+1-555-0144`) ceases outbound traffic; anonymous burner handset (`+1-555-0199`) activated.
- **Day 42 (Mar 12):** Subject scrubs 3 public posts from `@mayalin_art` mentioning a dinner appointment at Pacific Horizon Diner.
- **Day 44 (Mar 14, 17:15 UTC):** Both Maya (`@m.shadow_7`) and Kaelen Vance are co-located at Pacific Horizon Diner.
- **Day 44 (Mar 14, 21:45 UTC):** Burner handset connects to Tower Sector `TOWER-PAC-09` (Whispering Pines Ridge) and transmits final SMS routing packet before battery removal or shutdown.

---

## 5. Resolution of Red Herrings

1. **Red Herring 1 (Ex-Partner Lucas Reed Suspicion):**
   - *Suspicion:* Angry comments posted on Day 20 regarding unreturned studio gear.
   - *Forensic Verdict:* **EXONERATED.** SFO Marriott check-in at 18:50 UTC and airline booking confirm Lucas boarded flight SEA-441 to Seattle at 20:15 UTC.
2. **Red Herring 2 (Parody Cabo Travel Account `@mayalin_travels`):**
   - *Suspicion:* Post claiming Maya fled to Mexico.
   - *Forensic Verdict:* **FABRICATED DISINFORMATION.** EXIF metadata on photo `PH-010` revealed a 2024 capture date on an iPhone 8; pHash matched stock photography.
3. **Red Herring 3 (Abandoned Vehicle at Silver Sands):**
   - *Suspicion:* Vehicle found abandoned near coastal motel.
   - *Forensic Verdict:* **FALSE ALARM.** Vehicle registration linked to student Marcus Cole, who experienced mechanical failure out of gas.

---

## 6. Academic Evaluation Benchmark

The algorithmic pipeline was benchmarked against the isolated ground-truth scenario:
- **Entity Resolution Precision:** 85.7%
- **Entity Resolution Recall:** 100.0%
- **Entity Resolution F1 Score:** 92.3%
- **Target Persona Cluster Accuracy:** 100% (All 4 handles correctly merged)
- **Last Known Location Distance Error:** **117.3 meters** (Exact sector match)
- **Red Herring Traps Avoided:** **2 / 2** (Zero false suspect referrals)

---

## 7. Operational Limitations

1. **End-to-End Encryption & Private Profiles:** Private accounts restrict automated scraping. Investigators must rely on external mutual links and metadata residue.
2. **EXIF Stripping by Major Social Platforms:** Mainstream networks (Instagram, X) automatically strip EXIF upon upload. Forensic extraction relies on uncompressed attachments, cloud backup links, or camera cache leaks.
3. **Fuzzy Matching False Positives:** Aggressive handle matching without corroborating secondary signals (phones, emails, pHash) risks merging innocent bystanders.

---

## 8. Digital Privacy & Metadata Hygiene Recommendations

How privacy settings affect personal investigability and safety:
1. **Camera Geotagging Hygiene:** Disable GPS tagging in camera firmware when photographing sensitive or routine locations to prevent stalkers or adversaries from profiling routines.
2. **Handle Reuse Risks:** Reusing handles or near-identical alphanumeric variants enables cross-platform aggregation in seconds.
3. **Profile Metadata Hygiene:** Avoid embedding recovery emails or cellular digits in public bio descriptions.

---

## 9. Ethics and Legal Boundaries

All activities in this investigation were performed within an isolated academic environment using 100% synthetic data. No real human subjects were tracked, surveilled, or contacted. OSINT techniques demonstrated herein are intended exclusively for authorized law enforcement, search-and-rescue (SAR), and academic cyber-forensics instruction.
