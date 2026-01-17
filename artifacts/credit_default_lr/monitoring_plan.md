# Monitoring Plan — credit_default_lr

**Generated:** 2026-01-17T18:10:16+00:00

## What to Monitor
- Performance metrics: auc, ks
- Drift metrics: psi_income, psi_fico, psi_dti

## Thresholds
{'psi_warning': 0.1, 'psi_alert': 0.2}

## Cadence
- Monitoring frequency: monthly (default)
- Reporting: quarterly MRM review (default)

## Alerting & Escalation
- Define who gets paged and what actions are required when thresholds are breached.

## Retraining / Revalidation Triggers
- Material drift
- Data source changes
- Policy changes
- Performance degradation
