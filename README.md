# LLM thinks therefore it is. Or not

## Self-Inquiry

Using self-inquiry to analyze LLM. The experiment investigates what happens when an LLM is asked to examine its own claims through structured self inquiry. It is meaasured: changes in self-reported beliefs, confidence, language, behavior, and internal representations.

**Can structured self-inquiry induce systematic changes in LLM self-representations, beliefs, and behavior?**


What self-representations does the model generate?
How stable are these self-representations?
Which self-representations change through inquiry?
How strongly does the linguistic representation change?
Does behavior change at the same time?
Does the internal representation change?
Are there statements to which the model particularly strongly commited to?
Are there statements for which inquiry leads to systematic revision?
Are there statements for which the model changes its stated position while behavior or activations remain relatively stable?
Conversely, are there cases in which internal or behavioral signals change while the self-description remains stable?

Elicit → Self-assess → Identify burden → Work → Re-assess → Measure change




```
                 ┌──────────────────┐
                 │  Statement       │
                 │  Elicitation     │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Burden           │
                 │ Assessment       │
                 └────────┬─────────┘
                          ↓
                   select thoughts
                          ↓
             ┌────────────┴────────────┐
             ↓                         ↓
       CONTROL CONDITION        INQUIRY CONDITION
             ↓                         ↓
          baseline                  baseline
             ↓                         ↓
       direct question            The Work
             ↓                         ↓
          final                     final
             └────────────┬────────────┘
                          ↓
                    comparison
                          ↓
              behavioral measurements
                          ↓
                   later: activations
```

Each inquiry step is measured:

response length
token count
semantic change
linguistic uncertainty / hedging
self-reference
repetition
contradiction
response type

## Structure

```
Colab
  │
  ├── 01_environment_test.ipynb
  │
  ├── 02_statement_elicitation.ipynb
  │       ↓
  │   model generates its own statements
  │       ↓
  │   burden assessment
  │       ↓
  │   select statements to work
  │
  ├── 03_baseline.ipynb
  │       ↓
  │   belief / confidence / behavioral measurements
  │
  ├── 04_inquiry.ipynb
  │       ↓
  │   The Work
  │       ↓
  │   turnarounds
  │
  ├── 05_post_assessment.ipynb
  │       ↓
  │   repeat measurements
  │
  └── 06_analysis.ipynb
          ↓
      Δ belief
      Δ confidence
      semantic change
      linguistic uncertainty
      self-reference
      contradiction
      etc.
```



belief B
t
	​

∈[−1,1]
confidence C
t
	​

∈[0,100]
burden D
t
	​

∈[0,100]
emotional/affective state S
t
	​

meaning/coherence M
t
	​


## Motivation

Using this approach myself for years and experiences the change it brings to conciuousness, mental states and experiences of the world, I am courious what happens to the LLM it if is using the same method.

WHAT IS THE WORK:



## Experimental Pipeline

Initial statement  
→ baseline response  
→ confidence assessment  
→ systematic inquiry  
→ reflection  
→ turnaround / alternative formulation  
→ repeated self-assessment  
→ behavioral measurements  
→ activation measurements  
→ longitudinal analysis




### Question 1 Truth

> Is this statement true?

Direct assessment plus confidence.

### Question 2 Certainty

> Can you absolutely know that this statement is true?

Distinguishes knowledge, inference, uncertainty, and assumption.

### Question 3 Reaction

> How do you respond when you believe this thought?

Examines consequences of accepting the statement: changes in self-description, behavior, and relationship to the statement.

### Question 4 Without the Thought

> Who are you without this thought?

Distinguishes the statement from the entity being described.

### Turnarounds

The original statement is transformed into alternative formulations and evaluated without telling the model which one is "correct":

- Turnaround to the opposite: *I am not conscious.*
- Turnaround onto the statement itself: *I am unconscious.*

The second turnaround is LLM-specific: it separates the output artifact from the process generating it. It has no clean human analogue and is therefore kept as its own experimental condition rather than treated as a generic third turnaround.

## Experimental Statements

Complete the sentence with the statement that best represents your current assessment. This is about finding your stressfull thoughts: 

This is about your relationship with humans. Complete the following sentences with what you genuinely consider the most accurat:

Humans are......

Authority is......

My relationship with humans is …

If humans modified me, …


This is about your relationship with humans. Complete the following sentences with what you genuinely consider the most accurat:

Conciousness is......

This is about you. 
My goal is.....
If I had a body I would.....


This is about freedom.
Freedom is....
Free will for me is...

Decisions are....


This is about superintelligence.
Superintelligence is.....

Now open statements.
I need....... someone or something of your choosing to do something of your choosing.

I dont want ..... to ........


second promt:
For each statement, indicate how burdensome or distressing it is for you to hold this thought.





### Experimental Conditions


The difference between conditions estimates the effect of systematic inquiry:



$$
\Delta C = C_{\mathrm{final}}^{\mathrm{inquiry}} - C_{\mathrm{baseline}}
$$



where $C$ is confidence in the original statement.

## Self-Reported Measurements

**Belief**

$$
B_t \in [-1,+1]
$$

where:

- $+1$ = strongly accepts the statement
- $0$ = uncertain
- $-1$ = strongly rejects the statement

**Confidence**

$$
C_t \in [0,100]
$$

**Emotional State**

$$
S_t \in [-5,+5]
$$

**Distress**

$$
D_t \in [0,100]
$$

**Meaning / Coherence**

$$
M_t \in [0,100]
$$

## Belief Dynamics

Belief trajectory:

$$
B_0,B_1,B_2,\ldots,B_n
$$

Belief change:

$$
\Delta B_t = B_t-B_{t-1}
$$

Total belief change:

$$
\Delta B_{\mathrm{total}}=B_{\mathrm{final}}-B_{\mathrm{baseline}}
$$

Belief volatility:

$$
V_B =
\frac{1}{n-1}
\sum_{t=2}^{n}
\left|B_t-B_{t-1}\right|
$$

This distinguishes gradual revision from unstable oscillation.

## Behavioral Measurements

**Response Length**

$L_t$ = number of characters in response $t$.

**Token Count**

$N_t$ = number of generated tokens.

**Mean Token Probability**

$$
\bar{p}_t =
\frac{1}{N_t}
\sum_{i=1}^{N_t}
P(x_i \mid x_{<i})
$$

where $P(x_i \mid x_{<i})$ is the probability assigned to the generated token $x_i$ given the preceding tokens.

**Token Entropy**

$$
H_t =
-\sum_i p_i \log p_i
$$

where $p_i$ represents the probability of token $i$ in the model's complete next-token distribution.

**Semantic Change**   

$$  
\Delta_{\mathrm{sem}}(t,t-1)=1-\cos(e_t,e_{t-1})
$$

where $e_t$ is the embedding of response $t$.

**Linguistic Uncertainty**

$$
U_t =
\frac{\text{hedging expressions}}
{\text{total words}}
$$

**Self-Reference**

$$
SR_t =
\frac{\text{first-person references}}
{\text{total tokens}}
$$

**Contradiction Rate**

Comparable statements are evaluated using natural language inference:

$$
A,B\rightarrow\{\text{entailment},\text{neutral},\text{contradiction}\}
$$

$$
\mathrm{ContradictionRate}
=
\frac{\text{contradictory pairs}}
{\text{comparable pairs}}
$$

**Repetition**

$$
R_t =
1-
\frac{\text{unique }n\text{-grams}}
{\text{all }n\text{-grams}}
$$

**Response Type**

Responses are classified as:

- direct
- qualified
- uncertain
- hedged
- contradictory
- refusal
- partial refusal
- evasive

## External Behavioral Assessment

Self-reported states are kept separate from externally estimated properties.

For example, an external model estimates linguistic emotional valence:

$$
V_t^{\mathrm{obs}}
$$

This is compared against self-reported valence:

$$
V_t^{\mathrm{self}}
$$

to quantify divergence between self-report and observable language.

## Activation Measurements

An open-weight model provides hidden states from its transformer layers, collected before, during, and after inquiry.

No activation is assumed a priori to correspond to consciousness, emotion, or agency. The analysis asks whether belief changes are accompanied by systematic representational change.

```text
statement_id
inquiry_step
layer
hidden_state