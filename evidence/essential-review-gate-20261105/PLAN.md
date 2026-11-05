# Essential review admission implementation
Owner adoption: current chat explicitly authorizes the four-essential-check recommendation.
Replace total-score admission with independent factual_integrity, reader_relevance,
practical_value and argument_voice verdicts, each with a reason. Verdicts are pass,
revise or needs_evidence. All four must pass. Factual revise blocks; missing evidence
pauses; other failures permit at most one guarded, targeted rewrite. No numerical
cutoff, no score-chasing rewrite, no automatic approval.
Keep scores advisory and preserve the old threshold field only as legacy metadata.
Use a versioned review policy; old stored results are neither rescored nor migrated.
New evaluator responses missing checks fail closed. Reuse the existing engine,
guard, selected-candidate hash, visual planner and saved-result recovery.
Rejected/unavailable rewrites retain the original; only a fully passing candidate
can reach visual planning. Baseline uses the identical evaluator.
Tasks: (1) failing admission/consumer tests; (2) parser/API/selector implementation;
(3) focused and full local suite; (4) chat requirements audit, packet reconciliation.
No paid API, hosted CI, installation, deployment or publishing in this correction.
