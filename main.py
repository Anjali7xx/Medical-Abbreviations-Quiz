#import subprocess

#subprocess.run(["pip", "install", "streamlit"])
#subprocess.run(["pip", "install", "openai"])

import random
import streamlit as st

questions = [
    {"abbr": "PRN",  "answer": "As needed",            "options": ["As needed", "At bedtime", "By mouth", "Twice daily"],                           "cat": "Dosing"},
    {"abbr": "QID",  "answer": "Four times a day",      "options": ["Once a day", "Twice a day", "Three times a day", "Four times a day"],            "cat": "Dosing"},
    {"abbr": "NPO",  "answer": "Nothing by mouth",      "options": ["Nothing by mouth", "Normal saline", "Night procedure only", "No pain observed"], "cat": "General"},
    {"abbr": "SOB",  "answer": "Shortness of breath",   "options": ["Shortness of breath", "Signs of bleeding", "Status of bowels", "Swelling or bruising"], "cat": "Symptoms"},
    {"abbr": "BP",   "answer": "Blood pressure",        "options": ["Blood pressure", "Body posture", "Bacterial pneumonia", "Bleeding point"],       "cat": "Vitals"},
    {"abbr": "HR",   "answer": "Heart rate",            "options": ["Heart rate", "Hormone replacement", "High respirations", "Head rotation"],       "cat": "Vitals"},
    {"abbr": "BID",  "answer": "Twice daily",           "options": ["Twice daily", "Before insulin dose", "By intravenous drip", "Blood in discharge"],"cat": "Dosing"},
    {"abbr": "STAT", "answer": "Immediately",           "options": ["Immediately", "Standard treatment", "Short-term antibiotic therapy", "Status check"], "cat": "General"},
    {"abbr": "Hx",   "answer": "History",               "options": ["History", "Hypertension", "Hypoxia", "Hemorrhage"],                              "cat": "Documentation"},
    {"abbr": "Dx",   "answer": "Diagnosis",             "options": ["Diagnosis", "Drug exposure", "Dextrose", "Dysrhythmia"],                         "cat": "Documentation"},
    {"abbr": "Rx",   "answer": "Prescription",          "options": ["Prescription", "Reaction", "Recovery", "Resection"],                            "cat": "Documentation"},
    {"abbr": "MI",   "answer": "Myocardial infarction", "options": ["Myocardial infarction", "Multiple injuries", "Mild infection", "Mental illness"], "cat": "Cardiology"},
    {"abbr": "CHF",  "answer": "Congestive heart failure", "options": ["Congestive heart failure", "Chronic hepatic fibrosis", "Cardiac hormonal fluctuation", "Cerebral hemorrhagic fever"], "cat": "Cardiology"},
    {"abbr": "DVT",  "answer": "Deep vein thrombosis",  "options": ["Deep vein thrombosis", "Dual ventricular tachycardia", "Diffuse vascular tension", "Digital venous test"], "cat": "Hematology"},
    {"abbr": "UTI",  "answer": "Urinary tract infection", "options": ["Urinary tract infection", "Upper thoracic injury", "Ulcerative tissue inflammation", "Uterine tumor index"], "cat": "Urology"},
    {"abbr": "GI",   "answer": "Gastrointestinal",      "options": ["Gastrointestinal", "General illness", "Gynecological imaging", "Glomerular index"], "cat": "Systems"},
    {"abbr": "CNS",  "answer": "Central nervous system", "options": ["Central nervous system", "Chronic nerve syndrome", "Cranial nodule staging", "Cerebrospinal necrosis"], "cat": "Systems"},
    {"abbr": "ABG",  "answer": "Arterial blood gas",    "options": ["Arterial blood gas", "Antibody growth", "Abdominal biopsy guide", "Alveolar bronchial gradient"], "cat": "Labs"},
]

st.title("🏥 Medical Abbreviations Quiz")

# Initialize session state
if "pool" not in st.session_state:
    st.session_state.pool = random.sample(questions, len(questions))
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.best = 0
    st.session_state.answered = False
    st.session_state.chosen = None

pool = st.session_state.pool
idx = st.session_state.idx

# Score bar
col1, col2, col3 = st.columns(3)
col1.metric("Score", st.session_state.score)
col2.metric("Streak", st.session_state.streak)
col3.metric("Best Streak", st.session_state.best)

st.divider()

if idx >= len(pool):
    st.success(f"Quiz complete! Final score: {st.session_state.score}/{len(pool)}")
    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    q = pool[idx]
    st.caption(f"Question {idx+1} of {len(pool)}  •  {q['cat']}")
    st.subheader(f"What does **{q['abbr']}** mean?")

    if "shuffled_opts" not in st.session_state or not st.session_state.answered and st.session_state.chosen is None:
        if f"opts_{idx}" not in st.session_state:
            opts = q["options"][:]
            random.shuffle(opts)
            st.session_state[f"opts_{idx}"] = opts

    opts = st.session_state[f"opts_{idx}"]

    for opt in opts:
        if st.session_state.answered:
            if opt == q["answer"]:
                st.success(f"✓  {opt}")
            elif opt == st.session_state.chosen:
                st.error(f"✗  {opt}")
            else:
                st.button(opt, disabled=True, key=f"dis_{opt}")
        else:
            if st.button(opt, key=f"btn_{opt}"):
                st.session_state.answered = True
                st.session_state.chosen = opt
                if opt == q["answer"]:
                    st.session_state.score += 1
                    st.session_state.streak += 1
                    st.session_state.best = max(st.session_state.best, st.session_state.streak)
                else:
                    st.session_state.streak = 0
                st.rerun()

    if st.session_state.answered:
        if st.session_state.chosen == q["answer"]:
            st.success("Correct!")
        else:
            st.error(f"Wrong — the answer is: **{q['answer']}**")

        if st.button("Next →"):
            st.session_state.idx += 1
            st.session_state.answered = False
            st.session_state.chosen = None
            st.rerun()