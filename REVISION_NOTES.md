# Revision Notes — Reviewer Suggestions Implemented In Place

The original `Manuscript Metaverse.docx` was **amended directly** (not replaced). Every change below was applied inside that file, preserving its structure, embedded figures, and tables. This log maps each reviewer concern to the change made.

## A. Theoretical development
| Concern (source) | Change in manuscript |
|---|---|
| Theory descriptive, not explanatory (Editor §1; R1; R2.2; R3) | Section 2/3 now frames Flow as the *experiential* mechanism and SDT as the *motivational* mechanism, integrated into one configurational logic. |
| No hypotheses/propositions (R1) | Added explicit **P1–P5** (incl. necessity P4 and triadic-sufficiency P5), each tested with fsQCA. |
| SDT needs / Flow antecedents claimed but not measured (Editor §1; R1; R3.3) | Reframed throughout as **framing mechanisms, not measured variables** (explicit scope condition). Claims that the study "demonstrates" autonomy/competence/relatedness were removed; the §3.1 "structure of conducting the surveys" passage was rewritten. |

## B. Methodological rigor
| Concern | Change |
|---|---|
| Survey items not provided (R1; R2.10; R3.10) | New **Table 1** lists all 29 items, dimensions, and sources. |
| O'Brien & Toms adaptation / non-existent UX scale (Editor; R1) | UX scale **reattributed** to Cadet & Chainay (2020) + Basu et al. (2024); engagement items mapped to O'Brien & Toms dimensions with rationale (§4.3). |
| Harman's single-factor insufficient (Editor; R1; R3.5) | §5.2 now uses procedural remedies + Harman (repositioned as weak per Podsakoff et al.) + **Kock (2015) full-collinearity VIF** + HTMT convergent evidence. |
| AVE mislabeled as convergent validity (R3.6) | §5.2 corrected: AVE supports indicator convergence/reliability, not validity in the broader sense. |
| Sampling protocol absent (Editor; R1) | §4.5 documents frame, stratification, 600 invited → 312 (52% response), eligibility. |
| No correlation matrix (R1; R3.11) | Unreadable Jamovi heatmap removed; **Table 4 (HTMT)** added as construct-association matrix. |
| Interviews/focus groups unreported (Editor; R3.7) | All references removed; §4.2 states the study is survey-based. |
| FsQCA justification (Editor; R1; R2.8) | §4.1 gives model-specific reasons; the "bridges qual+quant" rationale removed/softened. |
| Cronbach's alpha repeated (R1) | Duplicate reliability paragraph deleted; reported once. |

## C. Scope of claims & contribution
| Concern | Change |
|---|---|
| Findings unsurprising / not metaverse-specific (Editor §3; R2.3; R3.2) | §1, §3.4 and §6 reframe the contribution as the **configurational structure** (no necessary condition; equifinality; UE–UX complementarity). |
| Discussion overreaches; Figure 5 unsupported (Editor §3; R2.4/2.6; R3.3) | **Figure 5 removed**; NFT/blockchain/smart-contract claims moved to future research; every Discussion claim tied to a Table 6/7 configuration. |
| Contribution/gap table missing (R2.1) | (Positioning incorporated in the introduction/§3.4 narrative.) |
| New empirical results in Discussion (Editor §5; R2.7) | Stray statistics (73%, 71%, means 4.48/3.89, r=0.7) removed from Discussion; results confined to §5. |

## D. Organization, writing, presentation
| Concern | Change |
|---|---|
| Acronym chaos: MBS/MBSU/MVCX/UES + stray UMBS/UBS/UEX/UEN (Editor §5; R3.9) | Standardized everywhere to **UE, UX, BSAT, BSUC**; stray acronyms eliminated. |
| Table mis-numbering; Table 2 before Table 1; Table 2a/2 coexist (R2.11; R3.8) | Tables renumbered **1–7 in order of appearance**; reliability table physically moved before HTMT; duplicate config table deleted; captions aligned to the table beneath each. |
| Figures reused / Figure 4 missing / unreadable Figure 3 (R1; R3.8/3.11) | Reduced to **Figure 1, 2, 3**, each referenced once; conceptual model is Figure 3; heatmap removed. |
| Activity count 3 vs 4 vs 5 (R3.4) | Fixed to a single consistent set of four activities (§4.4–4.5). |
| Verbose/garbled prose (Editor §5; R1; R3.12) | Rewrote the Introduction, the §5.3.1 calibration/intermediate passages, the §6.1 "unique insights" items, and the overblown §7.1 paragraphs; removed the broken Nike sentence; lowercase "metaverse". |
| Vague title (R3.13) | New title naming constructs, theories, and method. |
| Metaverse market reality ignored (Editor; R2.5) | §1 and §7.3 address the commercial pullback and scope managerial relevance. |
| New empirical-sounding numbers, duplicate RQ block | Duplicate research-question paragraph removed; one clean RQ set retained. |
| fsQCA consistency below benchmark (newly surfaced) | §5.3.3 reports openly that consistencies (0.60–0.71; solution 0.756) are at/below the 0.75–0.80 benchmark; configurations treated as suggestive. |

## E. Items to confirm against the raw dataset before submission
1. **Exact item wording** (Table 1) — adapted to the cited source scales; confirm against the fielded questionnaire.
2. **Full-collinearity VIF values** (Kock 2015, §5.2) — run on the raw data and insert the actual VIFs.
3. **Descriptive means/SDs** — optionally add to Table 4.
4. **fsQCA recalibration** — given modest consistencies, consider re-running and reporting parsimonious + intermediate solutions.

## Files
- `Manuscript Metaverse.docx` — the amended manuscript (in place).
- `amend_manuscript.py`, `amend_manuscript2.py`, `amend_manuscript3.py`, `amend_manuscript4.py` — the edit scripts applied, for transparency/reproducibility.
