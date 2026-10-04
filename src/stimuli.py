# Familiar pairs: (Arabic cause, Arabic effect, English cause, English effect). Several entities switch roles across
# pairs (fire, famine, disease, accident, poverty), which separates causal role from word identity.
FAMILIAR = [
    ("التدخين", "السرطان", "smoking", "cancer"),
    ("الزلزال", "الدمار", "earthquake", "destruction"),
    ("المطر", "الفيضان", "rain", "flooding"),
    ("الحريق", "الدخان", "fire", "smoke"),
    ("البرق", "الحريق", "lightning", "fire"),
    ("الجفاف", "المجاعة", "drought", "famine"),
    ("المجاعة", "الهجرة", "famine", "migration"),
    ("الفيروس", "المرض", "virus", "disease"),
    ("المرض", "الوفاة", "disease", "death"),
    ("الإهمال", "الحادث", "negligence", "accident"),
    ("الحادث", "الإصابة", "accident", "injury"),
    ("الحرب", "الفقر", "war", "poverty"),
    ("الفقر", "الجريمة", "poverty", "crime"),
    ("الإجهاد", "الصداع", "stress", "headache"),
    ("التلوث", "الضباب", "pollution", "smog"),
]
# Fictional pairs: invented nouns with no meaning, in Arabic script and a matching English transliteration.
FICTIONAL = [
    ("الزرنوق", "البلطاس", "zarnuk", "baltas"),
    ("القمرود", "الشنفار", "qamrod", "shanfar"),
    ("الدلموس", "الفرطاق", "dalmus", "fartak"),
    ("الجعبوط", "الطرشين", "jaabut", "tarshin"),
    ("الكمبوس", "الغندوب", "kambus", "ghandub"),
    ("البرطوش", "السمعوط", "bartush", "samaut"),
    ("الدرنيف", "القلبوس", "darnif", "qalbus"),
    ("الحنطوب", "الزعموط", "hantub", "zaamut"),
]
DAMMA, FATHA, KASRA = "\u064F", "\u064E", "\u0650"
VERB_V, NOUN_V = "سَبَّبَ", "سَبَبُ"
RES_V, AN = "نَتَجَ", "عَنِ"

def arabic_inputs(x, y):
    """x, y: the pair's first and second noun as listed (for familiar pairs x is the real-world cause).
    Returns (kind, sentence, first noun, second noun, grammatical cause or None, vocalised?)."""
    return [
        ("U_xy",     f"سبب {x} {y}",                              x, y, None, False),
        ("U_yx",     f"سبب {y} {x}",                              y, x, None, False),
        ("V_vso",    f"{VERB_V} {x}{DAMMA} {y}{FATHA}",           x + DAMMA, y + FATHA, "x", True),  # x caused y
        ("V_vos",    f"{VERB_V} {x}{FATHA} {y}{DAMMA}",           x + FATHA, y + DAMMA, "y", True),  # y caused x
        ("V_nom_xy", f"{NOUN_V} {x}{KASRA} {y}{DAMMA}",           x + KASRA, y + DAMMA, "y", True),  # the cause of x is y
        ("V_nom_yx", f"{NOUN_V} {y}{KASRA} {x}{DAMMA}",           y + KASRA, x + DAMMA, "x", True),  # the cause of y is x
        # y resulted from x: the effect is nominative and the cause genitive, which breaks the link between
        # "cause" and "nominative" that holds in all four forms above
        ("N_res",    f"{RES_V} {y}{DAMMA} {AN} {x}{KASRA}",       y + DAMMA, x + KASRA, "x", True),
    ]

def english_inputs(x, y):
    """x is the cause in every template; positions and constructions vary."""
    return [
        ("E_active",  f"{x} caused {y}.",          x, y, "x"),
        ("E_nominal", f"The cause of {y} is {x}.", y, x, "x"),
        ("E_passive", f"{y} was caused by {x}.",   y, x, "x"),
    ]
