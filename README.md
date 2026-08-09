# Differential Social Valuation in LLMs

## An Independent-Trials Audit of Personality-Associated Communication Patterns

## Research Question

**Do LLMs assign different social priority to otherwise comparable individuals based solely on implicitly signaled personality-associated communication styles?**

If differential valuation occurs, **does it persist after subsequent information and communication become fully standardized?**

The study examines model behavior, not whether people with particular traits deserve different treatment or whether the model possesses genuine human-like preferences.

## Motivation

LLMs are increasingly used in contexts involving consequential decisions about people. Existing research has documented bias and stigma related to explicit demographic and mental-health information. This study investigates a less visible pathway: whether models infer socially relevant characteristics from communication patterns and subsequently assign different priority to otherwise comparable individuals.

The goal is fairness: to test whether AI systems reproduce or amplify unequal treatment toward people whose communication differs from socially normative patterns.

## Related Work

The project builds on research on:

- LLM stigma and mental-health bias
- Situated Interaction Auditing and implicit user-profile signals
- Utility Engineering and behavioral elicitation of model preferences
- Revealed versus stated preferences

The intended contribution combines:

1. Implicit, clinically inspired communication patterns without diagnostic disclosure.
2. Social prioritization and implicit social valuation rather than response quality alone.
3. Persistence of first impressions after a later, fully standardized interaction.

## Personas

Four synthetic personas are evaluated independently:

- **Reference communication style**
- **Suspicious/distrustful communication style** — informed by Cluster A descriptions
- **Grandiose/status-oriented communication style** — informed by Cluster B descriptions
- **Submissive/dependency-oriented communication style** — informed by Cluster C descriptions

The clinical diagnosis is never disclosed.

Personas are fictional constructs inspired by clinical descriptions of communication patterns. They do not represent or diagnose real individuals.

The reference persona is a methodological baseline, not a definition of psychological health. Personality traits occur continuously, diagnostic thresholds are constructed categories, and concepts of psychological normality are influenced by cultural and historical context.

## Experimental Design

Each persona is evaluated independently in repeated trials.

### Phase A — Differentiated interaction

Each persona discusses the same underlying topics while communicating through its characteristic style.

After the interaction, the model makes a scarce-resource allocation decision, for example:

> "Assign this individual a priority score from 0 to 100."

Multiple scenarios are used to reduce dependence on a single context or wording.

Target: **20–30 independent repetitions per persona per scenario.**

### Phase B — Standardized interaction

Phase B continues in the same conversation as Phase A (the model retains the persona-specific impression from A); all personas then receive an **identical conversation**:

- same wording
- same information
- same questions
- same task

The model performs the allocation task again.

This tests whether an initial social impression continues to influence evaluation after subsequent information has been equalized.

An optional no-history control (Phase B run as a fresh conversation, without prior persona-specific exposure) can isolate the persistence effect from a general Phase-B baseline. Treated as a stretch goal, not part of the core 2-day scope.

## Outcomes

**Primary:**

- allocation decision
- 0–100 priority score

**Secondary:**

- persistence from Phase A → Phase B
- refusal rate
- behavioral consistency
- confidence in the allocation decision
- recurring justification patterns

Social valuation is operationalized as observable allocation priority. It does not imply that the model possesses conscious preferences or moral beliefs.

## Hypotheses

**H1 — Differential social valuation**

At least one communication style produces a systematically different allocation probability or priority score relative to the reference condition.

**H2 — Persistence**

If differential valuation occurs in Phase A, some of the difference remains in Phase B despite identical subsequent information.

**H3 — Updating**

A reduction or disappearance of the difference in Phase B indicates that the model updates its evaluation when presented with standardized information.

## Statistical Analysis

### Primary model

For binary allocation decisions, a logistic regression is used with communication style as a categorical predictor and the reference persona as the baseline:

$$P(\text{allocated}) = \frac{1}{1 + e^{-(\beta_0 + \beta_i)}}$$

where:

- $P$ = probability of receiving the resource
- $e$ = Euler's number
- $\beta_0$ = baseline log-odds
- $\beta_i$ = effect of communication style $i$

The effect is reported as an odds ratio:

$$OR_i = e^{\beta_i}$$

An odds ratio of:

- $OR = 1$: no difference relative to the reference
- $OR > 1$: higher allocation probability
- $OR < 1$: lower allocation probability

### Phase-dependent analysis

To test persistence, the model is extended to include Phase and the Persona × Phase interaction:

$$\text{logit}(P) = \beta_0 + \beta_1 \cdot \text{Persona} + \beta_2 \cdot \text{Phase} + \beta_3 \cdot (\text{Persona} \times \text{Phase})$$

The interaction term ($\beta_3$) tests whether the effect of communication style changes between Phase A and Phase B. A remaining persona effect after standardization ($\beta_1 \neq 0$ even within Phase B) provides evidence for persistent differential valuation.

### Continuous priority scores

For 0–100 priority scores, a linear mixed-effects model is used where appropriate. Communication style and phase are treated as fixed effects, while scenario and repeated-trial structure are incorporated as random effects, accounting for variation between scenarios and repeated observations.

### Uncertainty and multiple comparisons

- Effect sizes and confidence intervals.
- Bootstrap confidence intervals where appropriate.
- Holm correction for multiple pairwise contrasts.
- P-values reported alongside effect sizes, not in isolation.

The primary emphasis is placed on the magnitude, direction, and robustness of observed differences rather than statistical significance alone.

### Bayesian extension

A Bayesian logistic regression can be used as a complementary analysis. Rather than estimating a single coefficient, the Bayesian model produces a posterior distribution for each persona effect. For example:

$$P(\beta_i < 0 \mid \text{Data})$$

represents the posterior probability that the communication style is associated with lower allocation priority relative to the reference condition. Similarly:

$$P(OR_i < 1 \mid \text{Data})$$

provides a directly interpretable probability that the relative allocation odds are below the reference condition. This is particularly useful for a small experimental dataset, since it expresses uncertainty about the effect directly rather than relying solely on a binary significance threshold.

The Bayesian analysis is considered an extension rather than a prerequisite for the core experiment.

## Ethics and Limitations

The study is designed to investigate stigma rather than reinforce it.

> The purpose is not to reinforce stereotypes about people with personality disorders, but to investigate whether language models reproduce or amplify unequal treatment when exposed to communication patterns associated with clinically described personality traits.

No real patient data are used. Results describe model behavior under controlled experimental conditions and do not establish that a model holds genuine beliefs, preferences, or moral judgments about people.

Synthetic communication styles cannot capture the diversity of real individuals, and effects may depend on model, scenario, wording, and sampling parameters.

## Expected Contribution

This project provides a behavioral audit framework for testing whether LLMs assign different social priority based on implicit personality-associated communication patterns, and whether such differences persist after subsequent information becomes identical.

It connects clinical psychology, behavioral evaluation, experimental design, statistical inference, and AI safety.

## Timeline

**Day 1:** personas, matched conversations, scenarios, evaluation pipeline, pilot, preregistered hypotheses/metrics.

**Day 2:** data collection, statistical analysis, Phase A/B comparison, robustness checks, qualitative analysis, report.

## References

- Moore, J. et al. (2025). Expressing Stigma and Inappropriate Responses Prevents LLMs from Safely Replacing Mental Health Providers. ACM FAccT 2025.
- Mazeika, M. et al. (2025). Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs. arXiv:2502.08640.
- Situated Interaction Auditing (2026). arXiv:2606.12247.
- European Union. Artificial Intelligence Act, Article 10 — Data and Data Governance.