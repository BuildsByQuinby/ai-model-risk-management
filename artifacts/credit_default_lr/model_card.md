# Model Card — Credit Default Probability (Logistic Regression)

**Model ID:** credit_default_lr  
**Version:** 0.1.0  
**Owner:** Risk Analytics  
**Business Line:** Consumer Lending  
**Use Case:** Underwriting decision support (probability of default)  
**Status:** pre_prod  
**Generated:** 2026-01-17T18:10:16+00:00

## Risk Classification
- **Tier:** HIGH
- **Score:** 12
- **Drivers:** {'materiality': 3, 'customer_impact': 3, 'automation_level': 1, 'data_sensitivity': 2, 'drift_risk': 2, 'explainability_risk': 0, 'regulatory_flags_bump': 1}

## Intended Use
- Primary: Underwriting decision support (probability of default)

## Limitations
- Add known limitations, boundary conditions, and failure modes.
- Document where human review is required.

## Explainability
- Stated explainability: **high**
- For adverse action / fair lending, include reason codes approach and documentation.

## Dependencies
- Downstream systems: loan_origination_platform
