# Mechanism Review Checklist

Use this template when reviewing newly created or updated mechanisms for quality, accuracy, and alignment with project principles.

## Reviewer Information
- **Reviewer:** [Name]
- **Date:** [YYYY-MM-DD]
- **Mechanism ID:** [mechanism_id]
- **Version:** [version number]

---

## 1. Schema Validation ✓/✗

**Run validation:**
```bash
python mechanism-bank/scripts/validate_mechanisms.py mechanism-bank/mechanisms/[filename].yaml
```

- [ ] Schema validation passes
- [ ] All required fields present
- [ ] Value types correct (numeric, string, enum)
- [ ] YAML syntax valid (proper indentation)

**Notes:**

---

## 2. Effect Size Plausibility ✓/✗

**Assess:**
- [ ] Effect size in plausible range (-5 to 5 for log ratios)
- [ ] Confidence interval makes sense (lower < upper, contains estimate)
- [ ] Uncertainty appropriately quantified
- [ ] Functional form appropriate for relationship

**Effect size details:**
- Point estimate: [value]
- 95% CI: [lower, upper]
- Interpretation: [plain language]

**Plausibility assessment:**
- Compared to similar mechanisms: [similar/larger/smaller]
- Compared to literature: [consistent/optimistic/conservative]

**Red flags:**
- [ ] Effect size implausibly large (>2.0 log ratio = 7x change)
- [ ] Confidence interval extremely wide (uncertainty > ±2)
- [ ] Zero not in CI but p-value suggests non-significance

**Notes:**

---

## 3. Evidence Quality ✓/✗

**Citations:**
- [ ] All citations properly formatted (Chicago style)
- [ ] DOIs included where available
- [ ] Study types classified correctly
- [ ] Citations support claimed effect size

**Quality tier assessment:**
- Assigned tier: [A/B/C]
- Number of studies: [N]
- Study types: [meta-analysis/systematic review/RCT/cohort/etc.]
- Sample sizes: [total N across studies]

**A-tier criteria (all must be met):**
- [ ] Meta-analysis or systematic review with ≥5 studies
- [ ] Clear effect size with narrow CI (< ±0.5)
- [ ] Low heterogeneity
- [ ] High-quality primary studies

**B-tier criteria:**
- [ ] Systematic review with <5 studies OR
- [ ] Single large, well-designed study (RCT, large cohort)
- [ ] Moderate uncertainty

**C-tier:**
- [ ] Single small study
- [ ] Wide uncertainty
- [ ] Preliminary evidence

**Tier justification:**

---

## 4. Effect Size Derivation ✓/✗

**Check `effect_size_derivation` field:**
- [ ] Derivation clearly explained
- [ ] Conversions documented (if OR → log OR, etc.)
- [ ] Pooling method specified (if meta-analysis)
- [ ] Assumptions stated
- [ ] Limitations acknowledged

**Questions:**
- Can derivation be reproduced from citations?
- Are conversions mathematically correct?
- Is uncertainty propagated properly?

**Notes:**

---

## 5. Moderator Justification ✓/✗

**For each moderator, check:**

### Policy Environment Moderators
- [ ] Each moderator has clear rationale
- [ ] Effect direction makes sense (positive/negative)
- [ ] Rationale cites evidence or logical mechanism
- [ ] Framed structurally (not individually)

**Policy moderators:**
[List each with brief assessment]

### Demographic Moderators
- [ ] Framed in structural terms (not biological/behavioral)
- [ ] Avoid victim-blaming language
- [ ] Explain structural roots of differential effects
- [ ] Consider intersectionality where relevant

**Demographic moderators:**
[List each with brief assessment]

### Geographic Moderators
- [ ] Geographic variation explained
- [ ] Policy/environmental context specified
- [ ] Not just urban/rural without explanation

**Geographic moderators:**
[List each with brief assessment]

### Implementation Moderators
- [ ] Implementation factors realistic
- [ ] Consider equity in implementation (who gets quality implementation?)

**Implementation moderators:**
[List each with brief assessment]

**Red flags:**
- [ ] Moderators with no rationale
- [ ] Biological explanations for racial disparities
- [ ] "Cultural factors" without structural context
- [ ] "Compliance" or "motivation" as moderators

**Notes:**

---

## 6. Structural Competency Alignment ✓/✗

**Scale classification:**
- Assigned scale: [structural/institutional/individual]
- [ ] Scale appropriate for intervention type
- [ ] Prioritizes structural/institutional over individual

**Intervention framing:**
- [ ] Focuses on policy/institutional change
- [ ] Not individual behavior change as primary mechanism
- [ ] Avoids victim-blaming language

**Outcome framing:**
- [ ] Outcomes described as shaped by structural factors
- [ ] Suffering/illness framed as consequence of structural violence, not individual failure

**Language check:**
- [ ] No "patient compliance"
- [ ] No "lifestyle choices" (without structural context)
- [ ] No "health literacy" (without system complexity context)
- [ ] No "personal responsibility"

**Notes section:**
- [ ] Explicitly states structural framing
- [ ] Identifies policy levers
- [ ] Discusses power/resources needed for implementation

**Structural competency verdict:** [Aligned / Minor issues / Major revision needed]

**Notes:**

---

## 7. Equity Considerations ✓/✗

**Baseline disparities:**
- [ ] Baseline disparities in outcome documented
- [ ] Structural roots of disparities explained (racism, economic inequality, etc.)
- [ ] Specifies who is most affected and why

**Differential effects:**
- [ ] Moderators include equity dimensions (race, income, geography)
- [ ] Differential effects explained structurally
- [ ] Considers intersectionality

**Equity impact:**
- [ ] Assesses whether intervention reduces or exacerbates disparities
- [ ] Quantifies disparity reduction if possible
- [ ] Identifies implementation equity considerations

**Implementation equity:**
- [ ] Considers who will receive intervention
- [ ] Addresses barriers to equitable access
- [ ] Includes safeguards against harm (displacement, stigma, etc.)

**Equity verdict:** [Disparity-reducing / Neutral / Exacerbating / Unclear]

**Notes:**

---

## 8. Citation Completeness ✓/✗

**For each citation, verify:**
- [ ] Author(s) listed
- [ ] Article title
- [ ] Journal name
- [ ] Volume and issue
- [ ] Year
- [ ] Page numbers
- [ ] DOI (if available)
- [ ] Study type classified

**Citation formatting:**
- [ ] Chicago style format correct
- [ ] Consistent formatting across all citations

**Citation-evidence alignment:**
- [ ] Citations actually support claimed effect size
- [ ] No cherry-picking (if conflicting evidence, address it)
- [ ] Most recent/comprehensive evidence used

**Notes:**

---

## 9. Intervention & Outcome Specification ✓/✗

**Intervention:**
- [ ] Type follows taxonomy (housing, labor, food, etc.)
- [ ] Description clear and specific
- [ ] Target population specified
- [ ] Typical implementation described realistically

**Outcome:**
- [ ] Type follows taxonomy
- [ ] Measurement specific (not vague)
- [ ] Timeframe realistic and specified

**Clarity:**
- [ ] Another researcher could implement intervention from description
- [ ] Outcome measurement could be operationalized

**Notes:**

---

## 10. Overall Quality Assessment

**Strengths:**
1.
2.
3.

**Weaknesses:**
1.
2.
3.

**Required changes before approval:**
- [ ] [Change 1]
- [ ] [Change 2]
- [ ] [Change 3]

**Suggested improvements (optional):**
-
-

---

## Final Verdict

**Status:** [APPROVED / APPROVED WITH REVISIONS / REJECTED - MAJOR REVISION NEEDED]

**Summary:**

**Next steps:**

**Reviewer signature:** [Name, Date]

---

## Appendix: Quick Reference

### Plausible Effect Size Ranges

**Log rate/odds ratios:**
- Small: 0.1-0.3 (10-35% change)
- Medium: 0.3-0.7 (35-100% change)
- Large: 0.7-1.5 (100-350% change)
- Very large: >1.5 (>350% change) - rare, scrutinize carefully

**Correlations:**
- Small: 0.1-0.3
- Medium: 0.3-0.5
- Large: 0.5-0.7
- Very large: >0.7 - rare for complex health outcomes

### Common Issues Checklist

- [ ] Biological race explanations
- [ ] Individual blame language
- [ ] Missing equity analysis
- [ ] Implausible effect sizes
- [ ] Missing citations
- [ ] Vague intervention description
- [ ] No structural framing
- [ ] Missing moderator rationales
- [ ] Incomplete uncertainty quantification
- [ ] Schema validation errors
