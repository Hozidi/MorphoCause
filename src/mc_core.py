"""MorphoCause mechanistic pilot: analysis helpers (numpy only, so they can be tested without a GPU)."""
import numpy as np

SWITCHERS_AR = {"الحريق", "المجاعة", "المرض", "الحادث", "الفقر"}
# Which stored positions hold the two nouns for role readout: (0, 1) = the nouns inside the sentence,
# (3, 4) = the same nouns repeated in the answer options, after the model has read the whole sentence.
POS = (3, 4)

def last_token_overlapping(offsets, start, end):
    """Index of the last token whose character span overlaps [start, end)."""
    idx = [i for i, (s, e) in enumerate(offsets) if s < end and e > start and e > s]
    if not idx:
        raise ValueError(f"no token overlaps characters {start}-{end}")
    return max(idx)

def option_char_spans(text, opt_a, opt_b):
    """Character spans of the two answer options, '(A) ...' and '(B) ...', in the prompt."""
    ia, ib = text.rfind("(A) " + opt_a), text.rfind("(B) " + opt_b)
    if ia < 0 or ib < 0:
        raise ValueError("options not found in prompt")
    return (ia + 4, ia + 4 + len(opt_a)), (ib + 4, ib + 4 + len(opt_b))

def entity_char_spans(text, sentence, first, second):
    """Character spans of the sentence's two nouns inside the full prompt text, plus the closing-quote position."""
    q = text.find('"' + sentence + '"')
    if q < 0:
        raise ValueError("sentence not found in prompt")
    s0 = q + 1
    i1 = sentence.find(first)
    i2 = sentence.find(second, i1 + len(first))
    if i1 < 0 or i2 < 0:
        raise ValueError(f"nouns not found in sentence: {sentence}")
    end_quote = s0 + len(sentence)
    return (s0 + i1, s0 + i1 + len(first)), (s0 + i2, s0 + i2 + len(second)), (end_quote, end_quote + 1)

def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

def role_diffs(H, recs, ref, layer):
    """H: [n, L+1, 5, d] states at (first noun, second noun, closing quote, option A noun, option B noun). ref(rec) -> 'first'/'second'/None.
    Returns cause-minus-effect vectors at `layer` for records with a defined cause."""
    out, keep = [], []
    for i, r in enumerate(recs):
        c = ref(r)
        if c is None:
            continue
        a, b = H[i, layer, POS[0]].astype(np.float32), H[i, layer, POS[1]].astype(np.float32)
        out.append(a - b if c == "first" else b - a); keep.append(i)
    return np.array(out), keep

def paired_acc(H, recs, ref, layer, u):
    d, keep = role_diffs(H, recs, ref, layer)
    if len(d) == 0:
        return np.nan, 0
    s = d @ u
    return float((s > 0).mean()), len(d)

def direction(H, recs, ref, layer):
    d, _ = role_diffs(H, recs, ref, layer)
    return unit(d.mean(0)), float((d @ unit(d.mean(0))).mean())

def lopo_acc(H, recs, train_mask, ref, layer, subset=None):
    """Leave-one-pair-out: for each pair, fit the direction on every other pair's training records,
    then score that pair's records. `subset(rec)` restricts which held-out records are scored."""
    pairs = sorted({r["pair"] for r, m in zip(recs, train_mask) if m})
    hits = []
    for p in pairs:
        tr = [i for i, (r, m) in enumerate(zip(recs, train_mask)) if m and r["pair"] != p]
        te = [i for i, (r, m) in enumerate(zip(recs, train_mask)) if m and r["pair"] == p and (subset is None or subset(r))]
        if not te:
            continue
        u, _ = direction(H[tr], [recs[i] for i in tr], ref, layer)
        d, _ = role_diffs(H[te], [recs[i] for i in te], ref, layer)
        hits += list(d @ u > 0)
    return (float(np.mean(hits)) if hits else np.nan), len(hits)

def centred_cos(a, b, mu):
    a, b = a - mu, b - mu
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
