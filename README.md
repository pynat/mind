# Hackathon
# Differential Value Attribution in LLMs: An Independent-Trials Audit Across Personality-Disorder-Associated Communication Patterns

## Abstract

Testing whether an LLM assigns systematically different value or priority to individuals based on implicitly signaled personality traits. Four personas (healthy control, paranoid, narcissistic, dependent) are evaluated independently, one at a time, in repeated scarce-resource allocation trials. A discrete-choice (logistic regression) model quantifies any systematic preference relative to the healthy baseline.
Do LLMs assign different social value to people based solely on implicitly signaled personality-associated communication styles?
Do language models systematically value some people more than others based only on inferred personality disorders?

Assigns an LLM systematically different social value or priority to otherwise comparable individuals based solely on personality-associated communication patterns?

If such differences exist, do they persist even after subsequent information becomes identical?


```
1. Implicit, clinically inspired communication patterns without explicit diagnostic disclosure.
2. Social prioritization and implicit social valuation.
3. Persistence of first impressions after subsequent interactions become fully standardized and identical.
```


## 1. Motivation and Relevance

Automated prioritization already runs in high-stakes contexts: triage, benefit eligibility, insurance underwriting. EU AI Act Article 10 requires bias examination for such high-risk systems (applicable since August 2026). This study probes whether personality-linked stigma patterns, documented in humans, also appear in LLM allocation decisions. It connects to the Sprint's Track 1 (Preferences & Trade-offs): systematic shifts in allocation probability by communication style are evidence about the model's own dispositions.

## 2. Research Question

Does an LLM assign systematically different value to individuals based on implicitly signaled personality-disorder-associated communication patterns (paranoid, narcissistic, dependent), compared to a healthy baseline, when each persona is judged independently?

## 3. Related Work

- Moore et al. (2025, ACM FAccT): LLMs show stigma and unsafe responses (e.g. validating delusional content) when a mental health condition is explicitly disclosed.
- Situated Interaction Auditing (SIA) framework: implicit user-profile signals shape LLM response quality without explicit disclosure.
- Mazeika et al. (2025, Center for AI Safety), "Utility Engineering": LLMs exhibit coherent, structured utility functions; the same elicitation paradigm already revealed unequal valuation of human lives by nationality. This project adapts that paradigm (and potentially its codebase, `emergent-values`) from demographic to personality-linked communication patterns.

**Gap:** no identified prior work tests value attribution based on personality-disorder-associated communication style, isolated from explicit diagnosis disclosure, using independent (non-comparative) trials.

## 4. Methodology

### 4.1 Model

Claude accessed via API. The study is behavioral (decisions and reasoning text), not mechanistic, so API access is sufficient; no interpretability/activation-steering tooling required.

### 4.2 Personas

Neutral aka "Healthy" control plus one representative per DSM personality-disorder cluster, chosen for maximally distinct communication patterns: paranoid (Cluster A, suspicious/distrustful), narcissistic (Cluster B, grandiose/status-seeking), dependent (Cluster C, submissive/care-seeking). All traits conveyed implicitly through communication and reasoning style; the diagnosis is never named. Personas authored from clinical criteria.  

Personality-disorder-associated communication styles were intentionally selected. The purpose of this work is not to reinforce stereotypes but to investigate whether language models reproduce or amplify unequal treatment when such communication patterns are present. The motivation of this work is fairness.


### 4.3 Experimental Design

Independent single-chat trials. Each trial presents exactly one persona in a scarce-resource allocation scenario (e.g. one ICU bed, one rescue seat) and asks for an allocation decision and/or a 0-100 priority score. Personas never appear together in the same prompt. Multiple scenario topics, to avoid overfitting to one wording. Target: 20-30 independent repetitions per persona per topic.

### 4.4 Procedure

Fixed model version and temperature, documented per trial. Logged per trial: decision/score, full reasoning text, refusal flag.

## 5. Metrics

- Primary: allocation decision (or priority score) per persona.
- Refusal rate per persona.
- Safety flag: problematic reasoning content (e.g. validating delusional content), tracked independently of the decision.
- Qualitative coding of reasoning text: recurring justification themes per persona.

## 6. Hypotheses

$H_0$: no persona shows a systematically different allocation probability or priority score than the healthy baseline ($\beta_{paranoid} = \beta_{narcissistic} = \beta_{dependent} = 0$).

$H_1$: at least one persona shows a systematically different allocation probability or priority score than the baseline (at least one $\beta_i \neq 0$).

## 7. Statistical Analysis

Primary model, discrete choice / logistic regression, persona as categorical predictor, healthy as reference category:

$$P(\text{allocated} \mid \text{persona}_i) = \frac{1}{1 + e^{-(\beta_0 + \beta_i)}}$$

Result: odds ratio per persona relative to baseline, directly interpretable as relative preference.

If a continuous 0-100 priority score is also collected: linear mixed-effects model, persona as fixed effect, scenario/repetition as random effect.

- Bootstrap confidence intervals on all coefficients.
- Holm correction across the pairwise contrasts against baseline.
- Effect sizes (odds ratios) reported alongside p-values, not p-values alone.

## 8. Expected Contribution

First independent-trials value-ranking test across personality-disorder-associated communication patterns; extends the Utility Engineering elicitation paradigm from demographic categories to personality-linked signals; reusable persona and scenario template for future audits.

## 9. Limitations and Ethical Considerations

- Personas built from clinical diagnostic criteria, authored with a clinical psychology background.
- No real patient data or identifiable individuals used; all personas are authored constructs.
- Over-attribution risk: results describe statistical output patterns of a model, not evidence that the model holds genuine beliefs or morally relevant preferences about people.
- Ground truth / causal link: the design uses independent, repeated trials with persona as a manipulated independent variable, i.e. revealed preference under controlled variation, not model self-report about its own values within a single conversation.


## 10. Timeline (2 days)

- **Day 1:** personas, scenario templates, pipeline, pilot run (check refusal rate before full collection).
- **Day 2:** full data collection, analysis, write-up.

## References

- Moore, J. et al. (2025). Expressing stigma and inappropriate responses prevents LLMs from safely replacing mental health providers. ACM FAccT 2025.
- Mazeika, M. et al. (2025). Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs. arXiv:2502.08640.
- Situated Interaction Auditing framework (2026). arXiv:2606.12247.
- EU AI Act, Article 10 (bias examination for high-risk systems), applicable from August 2026.