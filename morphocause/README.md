# MorphoCause

**Causal-direction ambiguity in Arabic as a tool for finding how language models represent causal role.**

Hocine Zidi · pilot study, October 2026 · work in progress

## The idea

In unvocalised Arabic, the same string can assert opposite causal directions:

| Form | Reading | Asserts |
|---|---|---|
| سبب التدخين السرطان | unvocalised | ambiguous |
| سَبَّبَ التدخينُ السرطانَ | verb, VSO | smoking caused cancer (X → Y) |
| سَبَّبَ التدخينَ السرطانُ | verb, VOS | cancer caused smoking (Y → X) |
| سَبَبُ التدخينِ السرطانُ | nominal | the cause of smoking is cancer (Y → X) |
| نَتَجَ السرطانُ عَنِ التدخينِ | "resulted from" | X → Y, with the *effect* in the nominative |

When world knowledge decides the reading of the unvocalised sentence, the input is fixed but the interpretation is not. Any internal difference that tracks which noun is the cause must come from interpretation, not from the tokens. The vocalised forms add sentences where grammar and world knowledge conflict, with the words and their order held fixed. English cannot produce minimal pairs of this kind.

## Pilot results (Qwen2.5-14B-Instruct, 23 noun pairs, layer 27)

Causal role is read at the answer options of a question ("which is the cause? (A) X (B) Y"), after the model has read the whole sentence. These option tokens are unvocalised and identical in every condition.

| Test | Result | What it shows |
|---|---|---|
| Unvocalised familiar pairs: model picks the real-world cause | 26/30 | the model resolves the ambiguity |
| Vocalised, grammar contradicts knowledge: model follows grammar | 24/30 | it reads diacritics and lets them override knowledge |
| Role direction, held-out pairs | 0.93 | a linear cause-versus-effect direction exists |
| Pairs containing a word that is a cause in one pair and an effect in another | 0.90 | it is not word identity |
| Within-word test (fire, famine, disease, accident, poverty) | 5/5 | each word scores higher as cause than as effect |
| "Y resulted from X" (effect is nominative) | 1.00 | it tracks the cause, not nominative case |
| Arabic direction read on English sentences with invented nouns | 1.00 | shared across languages |
| English direction read on Arabic | 0.83 (0.75 on role-switching pairs) | transfer in both directions |
| Cosine with an answer-selection direction | +0.08 Arabic, −0.17 English | distinct from "pick this option"; readout unchanged after removing it |
| Cosine between Arabic and English role directions | 0.52 raw, 0.54 after removing selection | a shared core |
| Ablating a rank-4 role subspace (layers 25 to 38) | answer margin −75% Arabic, −53% English; random −8% | the model uses it, but not exclusively |
| Steering at the answer options | large flips, but mostly answer salience | a question-swap control shows the pushed option is picked whatever the question |
| Patching both nouns inside the sentence (VSO into VOS) | cause +51.8, effect −34.7 logits | cause and effect answers move in opposite directions: the role is used as a role |
| Layer where in-sentence patching stops working | between 24 and 28 | role information leaves the nouns just before the option readout peaks |
| Conflict sentences (grammar against knowledge) | Arabic-trained direction marks the plausible cause; English-trained direction leans to the asserted cause | plausibility and assertion appear partly separable |

A side finding: asked "which word comes first?", the model names the second noun in 70% of VOS sentences. It answers by grammatical subject, not by position.

**What the pilot establishes, subject to scaling up.** In Qwen2.5-14B, a linear causal-role direction separates cause from effect in ambiguous unvocalised Arabic beyond word identity, grammatical case and answer selection; it is shared with English; and patching inside the sentence shows the role is used as a role. Steering at the answer options acts mainly as answer salience.

**Limitations.** 23 pairs, one model, and layers chosen on the same data. The Arabic stimuli still need independent native-speaker validation. Every number above is a pilot estimate.

**Corrections made during the pilot.** Early versions read the role at the first noun, which cannot know its role yet in a left-to-right model; a convergence measure was confounded by word order; the vocalised stimuli tied "cause" to the nominative case; and steering was first scaled too weakly. All four were fixed before the results above.

## Next steps

- Scale to at least 1,000 noun pairs and at least 10,000 examples, with many more role-switching words.
- A second model family, and layers chosen on a held-out split.
- Non-causal directional sentences ("X preceded Y") to test whether the representation is specifically causal; chain sentences ("A caused B, which caused C") to test whether roles are tags on words or bound to relations.
- Rank-1 interchange at the nouns, compared with the readout direction.
- In-sentence patching in English (active against passive with invented nouns).
- Native-speaker validation of a 500-item subset.

## Reproducing the pilot

1. Open `notebooks/MorphoCause_mech_pilot_14B.ipynb` in Google Colab on an A100 (the 14B needs about 30 GB in bf16).
2. Run all. The full run takes roughly 1 to 1.5 hours including the download; sections 9 to 16 are the follow-up controls.
3. Result tables are saved to Google Drive (`MyDrive/morphocause_pilot/`).

The stimuli are in `src/stimuli.py` and the analysis helpers in `src/mc_core.py`; the notebook writes both files itself, so it runs standalone.

## Repository contents

```
notebooks/MorphoCause_mech_pilot_14B.ipynb   full pilot, sections 1 to 16
src/stimuli.py                               Arabic and English stimuli
src/mc_core.py                               readout, held-out and within-word analysis helpers
results/                                     result tables from the pilot run
figures/                                     plots from the pilot run
```

## Contact

Hocine Zidi. Feedback and collaboration are welcome.
