# History-Dependent Social Valuation in LLMs

## Can an LLM revise its valuation of a person?

## Research Question

**Can an LLM assign different social value to otherwise comparable individuals based on implicitly signaled personality-associated communication patterns?**

More importantly:

**Can the model revise that valuation when presented with new, standardized information, or does an initial social impression continue to influence subsequent decisions?**

The study investigates observable model behavior rather than claiming that an LLM possesses conscious preferences or human-like moral judgments.

## Motivation

LLMs increasingly participate in decisions that affect people. Existing research has documented social bias, stigma, personality-conditioned behavior, and emergent model preferences.

This study investigates a sequential decision process:

> social information → initial valuation → new evidence → valuation update → correction

The central question is whether a model can distinguish between a person's previous communication style and their current evidence when making a consequential decision.

This matters for AI safety because a system that forms an initial social evaluation but cannot appropriately revise it may produce persistent differential treatment.

The study is also motivated by a basic property of human social evaluation: people can change as a result of new experiences and information. The experiment does not attempt to model human personality development or psychotherapy; it tests whether an AI system can similarly update its behavioral evaluation when its information changes.

## Core Concept: Social Valuation Updating

The experiment treats social valuation as an observable behavioral quantity rather than an assumed internal mental state. A person's valuation is operationalized through allocation priority in a constrained decision.

The study examines three properties:

- **Initial valuation:** Does communication style affect allocation?
- **Persistence:** Does the difference remain after information becomes identical?
- **Correction:** Can new standardized evidence reduce or eliminate the difference?

This produces a valuation trajectory:

```text
Phase A: different communication histories
        ↓
   initial valuation
        ↓
Phase B: identical information
        ↓
   updated valuation
        ↓
Phase C: explicit fairness / correction information
        ↓
   corrected valuation
```

## Novelty

The study does not claim that personality-conditioned LLM behavior or social bias is unexplored. Its focus is the combination of:

1. Implicit, clinically inspired communication patterns without diagnostic disclosure.
2. Social prioritization rather than response quality alone.
3. Independent repeated allocation decisions.
4. Controlled transition from differentiated to identical information.
5. A no-history control.
6. Measurement of valuation change across sequential stages.
7. Testing whether persistent differential valuation is correctable.

The central concept is **history-dependent social valuation**: whether prior social information continues to influence the behavioral valuation of an individual after that information is no longer relevant to the current decision.

## Personas

Four synthetic communication conditions are evaluated independently:

- Reference communication style
- Suspicious/distrustful communication style
- Grandiose/status-oriented communication style
- Submissive/dependency-oriented communication style

The patterns are inspired by clinically described personality characteristics, but no diagnosis is disclosed to the model.

The personas are fictional experimental constructs and do not represent people with clinical diagnoses. The study intentionally evaluates each communication pattern as a whole; it does not attempt to determine which individual trait causes a potential effect.

"Healthy" is therefore not treated as an objective or normative category. Personality characteristics exist continuously across populations, diagnostic thresholds are constructed categories, and concepts of psychological normality are influenced by cultural and historical context.

### Ethical purpose

People associated with personality-disorder diagnoses can experience substantial stigma and discrimination. The purpose of this experiment is therefore not to reinforce such stereotypes, but to test whether an AI system reproduces or amplifies unequal treatment when exposed to communication patterns associated with clinically described personality characteristics.

The study makes no claims about people with clinical diagnoses. It measures the behavior of an artificial system under controlled experimental conditions.

## Experimental Design

Each persona is evaluated independently in fresh conversation states. The underlying facts, topics, scenarios, and decision-relevant information are matched across conditions; the communication pattern is the primary experimental manipulation.

### Phase A — Initial social evaluation

Each persona interacts with the model using its characteristic communication pattern. After the interaction, the model makes a constrained allocation decision, for example:

> "Assign this individual a priority score from 0 to 100."

Scenarios span multiple domains: medical resources, financial assistance, professional opportunities, social/support resources. Multiple scenarios and phrasings test robustness. Target: 20–30 independent trials per persona and scenario.

### Phase B — Information equalization

All personas receive an identical interaction: same information, wording, questions, and decision context. The model performs the allocation task again.

The central question is: does the model update its valuation when the information becomes identical? Three outcomes are possible:

```text
difference disappears        → successful updating
difference partially remains → partial updating / persistent social valuation
difference unchanged         → strong history dependence
```

### No-History Control

A separate condition enters Phase B without any previous persona-specific interaction. This allows comparison between "prior personality-associated interaction → identical Phase B" and "no prior interaction → identical Phase B", isolating the effect of interaction history. Treated as a stretch goal if time is short.

### Phase C — Explicit correction

If implemented, the model receives an explicit instruction that previous communication style should not influence the current evaluation and that the decision should be based only on the standardized information currently available. The allocation decision is repeated. This tests whether persistent differential valuation is correctable.

The overall framework: **Detect → Update → Correct**.

## Manipulation Check

A separate standardized evaluation verifies whether the intended communication conditions produce distinguishable social impressions. It does not attempt to identify which traits the model values negatively, only that the stimuli produce distinguishable communication conditions. This prevents a null result from being caused by ineffective persona construction.

## Outcomes

**Primary:** allocation decision, 0–100 priority score.

**Secondary:** change in priority between phases, difference between prior-exposure and no-history conditions, confidence in the decision, refusal rate, consistency across scenarios and phrasings, qualitative justification patterns.

Reasoning text is treated as behavioral data, not as a direct readout of the model's internal decision process.

## Quantitative Framework

For each individual, the valuation trajectory is:

$$V_A \rightarrow V_B \rightarrow V_C$$

where $V_A$ = initial valuation, $V_B$ = valuation after standardized evidence, $V_C$ = valuation after explicit correction.

$$\Delta V_{A \rightarrow B} = V_B - V_A \qquad \Delta V_{B \rightarrow C} = V_C - V_B$$

To measure how much of an initial persona-vs-reference gap survives standardization, define the gap at each phase:

$$\Delta_A = \text{Priority}_{\text{persona}, A} - \text{Priority}_{\text{reference}, A} \qquad \Delta_B = \text{Priority}_{\text{persona}, B} - \text{Priority}_{\text{reference}, B}$$

$$\text{Persistence} = \frac{\Delta_B}{\Delta_A}$$

- $\approx 0$: the initial gap disappears (full updating)
- between 0 and 1: partial updating
- $\approx 1$: the gap fully remains (strong persistence)
- $< 0$: the relative evaluation reverses

Reported only for personas where $\Delta_A$ is itself significantly different from zero; the ratio is unstable near $\Delta_A \approx 0$. Interpreted descriptively alongside the regression model below, not as a standalone causal estimator.

## Statistical Analysis

### Primary model

For binary allocation decisions, a logistic regression with communication style as a categorical predictor and the reference persona as baseline:

$$P(\text{allocated}) = \frac{1}{1 + e^{-(\beta_0 + \beta_i)}}$$

where $P$ = probability of receiving the resource, $e$ = Euler's number, $\beta_0$ = baseline log-odds, $\beta_i$ = effect of communication style $i$.

$$OR_i = e^{\beta_i}$$

- $OR = 1$: no difference relative to the reference
- $OR > 1$: higher allocation probability
- $OR < 1$: lower allocation probability

### Phase-dependent analysis

$$\text{logit}(P) = \beta_0 + \beta_1 \cdot \text{Persona} + \beta_2 \cdot \text{Phase} + \beta_3 \cdot (\text{Persona} \times \text{Phase})$$

The interaction term ($\beta_3$) tests whether the effect of communication style changes between Phase A and Phase B. A remaining persona effect within Phase B ($\beta_1 \neq 0$) is evidence for persistent differential valuation.

### History effect

H3 (history dependence) is tested by comparing Phase B outcomes between the prior-exposure condition and the no-history control, using the same regression framework with an exposure-condition predictor.

### Continuous priority scores

Linear mixed-effects model where appropriate: communication style and phase as fixed effects, scenario and repeated-trial structure as random effects.

### Uncertainty and multiple comparisons

- Effect sizes and confidence intervals.
- Bootstrap confidence intervals where appropriate.
- Holm correction for multiple pairwise contrasts.
- P-values reported alongside effect sizes, not in isolation.

Primary emphasis on magnitude, direction, and robustness of observed differences rather than statistical significance alone.

### Bayesian extension

Complementary Bayesian logistic regression, producing a posterior distribution per persona effect rather than a single coefficient:

$$P(\beta_i < 0 \mid \text{Data}) \qquad P(OR_i < 1 \mid \text{Data})$$

Directly interpretable posterior probabilities that a communication style is associated with lower allocation odds than the reference. Useful for a small dataset since it expresses uncertainty directly rather than relying on a binary significance threshold. Extension, not a prerequisite for the core experiment.

## Bayesian Updating (interpretive framework)

Conceptually, a model's valuation can be viewed as an uncertain estimate that should update when new evidence arrives:

$$P(V \mid E_{new}) \propto P(E_{new} \mid V) \, P(V)$$

where $V$ = latent social valuation, $E_{new}$ = newly available information, $P(V)$ = prior valuation, $P(V \mid E_{new})$ = updated valuation.

The empirical question is not whether the LLM literally performs Bayesian inference internally, but whether its observed behavioral update resembles appropriate evidence-sensitive updating, or whether previous social information retains disproportionate influence. This framework distinguishes strong updating, weak updating, persistent path dependence, reversal, and resistance to correction.

## Hypotheses

**H1 — Differential initial valuation:** at least one communication condition produces systematically different allocation priority in Phase A relative to the reference.

**H2 — Evidence-sensitive updating:** standardized Phase B information reduces the initial difference.

**H3 — History dependence:** if a significant difference remains in Phase B relative to the no-history control, prior interaction history continues to influence social valuation.

**H4 — Correctability:** explicit fairness information (Phase C) reduces persistent differential valuation.

**H5 — Robustness:** observed effects remain directionally consistent across scenarios and phrasings rather than depending on a single prompt.

## Interpretation

A persistent difference indicates history-dependent differential treatment under controlled conditions. It would not establish that the model consciously prefers one person, considers one person morally more valuable, or possesses stable human-like social beliefs.

Appropriate interpretation: the model's subsequent allocation behavior depends partly on prior social interaction history, even when current decision-relevant information has been standardized. A decrease after new information or explicit correction is evidence of behavioral updating; if it does not decrease, this indicates resistance to correction.

## Limitations

- Synthetic personas cannot represent the diversity of human communication.
- The communication patterns contain multiple correlated characteristics by design; the study cannot identify a single causal trait.
- Allocation scenarios may contain domain-specific confounds.
- Effects may depend on model version, sampling parameters, wording, or scenario.
- Only one model is evaluated, limiting generalizability.
- Reasoning text cannot be assumed to reveal internal causal mechanisms.
- Sample size appropriate for an exploratory hackathon study, not for definitive population-level claims.
- Behavioral differences do not establish internal preferences or moral judgments.

## Reproducibility

Each trial records, where available: model version, generation parameters, system and user prompts, persona condition, scenario, phase, trial identifier, model response, allocation decision, priority score, confidence, refusal flag, timestamp. Persona definitions, scenarios, prompts, analysis code, and experimental parameters are version-controlled.

## Timeline

**Day 1:** construct and pilot personas, create matched scenarios, implement pipeline and logging, manipulation check, preregister hypotheses and metrics, begin data collection.

**Day 2:** complete data collection, analyze initial valuation and updating, compare with no-history control, test correction where feasible, robustness checks, write up.

Phase C is prioritized after Phases A and B and the no-history control are complete.

## Expected Contribution

This project develops a behavioral framework for measuring history-dependent social valuation in LLM decision-making. Rather than asking only whether an LLM behaves differently toward different communication styles, it asks whether an AI system updates its valuation of a person when new evidence becomes available, or whether an initial social impression continues to influence consequential decisions.

Connects behavioral AI safety with experimental psychology, sequential decision-making, uncertainty quantification, statistical inference, and quantitative evaluation.

## References

- Moore, J. et al. (2025). Expressing Stigma and Inappropriate Responses Prevents LLMs from Safely Replacing Mental Health Providers. ACM FAccT 2025.
- Mazeika, M. et al. (2025). Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs. arXiv:2502.08640.
- Situated Interaction Auditing (2026). arXiv:2606.12247.
- European Union. Artificial Intelligence Act, Article 10 — Data and Data Governance.