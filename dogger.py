import streamlit as st
import datetime
from streamlit_extras.metric_cards import style_metric_cards

# ---------- CALCULATION LOGIC ----------
def calculate_points(data):
    walks = data.get('walks', 0)
    weekend = data.get('weekend', 0)
    rain = data.get('rain', 0)
    sub = data.get('sub', 0)
    extra = data.get('extra', 0)
    missed = data.get('missed', 0)

    base_points = walks * 10
    bonus_points = weekend * 2 + rain * 3 + sub * 5 + extra * 6
    penalty_points = missed * 7
    total_points = base_points + bonus_points - penalty_points

    return max(total_points, 0)

def calculate_payouts(walkers):
    monthly_cap = 80
    walker_points = {}
    total_points = 0

    for name, data in walkers.items():
        points = calculate_points(data)
        walker_points[name] = points
        total_points += points

    payouts = {}
    for name, points in walker_points.items():
        if total_points == 0:
            payouts[name] = 0.0
        else:
            raw_payout = (points / total_points) * len(walkers) * monthly_cap / 4
            payouts[name] = round(min(raw_payout, monthly_cap / 4), 2)

    return {
        'walker_points': walker_points,
        'walker_payouts': payouts
    }

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Dog Walking Dashboard", layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .walker-box {
            background-color: #f8f9fa;
            padding: 1.2rem;
            border-radius: 1rem;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🐕 Weekly Dog Walking Manager")
st.caption("Motivate with points. Reward with fairness. Cap with logic.")

col1, col2 = st.columns([1, 2])
with col1:
    current_week = st.date_input("📅 Week Ending", value=datetime.date.today())
with col2:
    st.markdown("""
    **Points System:**
    - Regular walk: 10 pts  
    - Weekend: +2 pts  
    - Rain: +3 pts  
    - Sub: +5 pts  
    - Extra: +6 pts  
    - Missed: –7 pts
    """)

walker_names = ["Alice", "Ben", "Charlie"]
walker_inputs = {}

st.divider()
st.header("👣 Input Walk Data")

with st.form("weekly_form"):
    input_cols = st.columns(len(walker_names))

    for i, name in enumerate(walker_names):
        with input_cols[i]:
            st.markdown(f"### {name}", help="Input all weekly metrics")
            walks = st.number_input("Walks", min_value=0, key=f"walks_{name}")
            weekend = st.number_input("Weekend Walks", min_value=0, key=f"weekend_{name}")
            rain = st.number_input("Rainy Walks", min_value=0, key=f"rain_{name}")
            sub = st.number_input("Substitutions", min_value=0, key=f"sub_{name}")
            extra = st.number_input("Extra Walks", min_value=0, key=f"extra_{name}")
            missed = st.number_input("Missed Walks", min_value=0, key=f"missed_{name}")

            walker_inputs[name] = {
                'walks': walks,
                'weekend': weekend,
                'rain': rain,
                'sub': sub,
                'extra': extra,
                'missed': missed
            }

    submitted = st.form_submit_button("🚀 Calculate Weekly Pay")

# ---------- RESULTS ----------
if submitted:
    results = calculate_payouts(walker_inputs)
    st.success(f"Pay breakdown for the week ending {current_week.strftime('%B %d, %Y')}")

    st.header("📊 Results Overview")
    col1, col2, col3 = st.columns(3)
    for i, name in enumerate(walker_names):
        pts = results['walker_points'][name]
        pay = results['walker_payouts'][name]
        with [col1, col2, col3][i % 3]:
            st.metric(label=f"{name} Points", value=f"{pts} pts")
            st.metric(label=f"{name} Pay (€)", value=f"€{pay}")

    style_metric_cards()

    st.markdown("---")
    st.caption("Designed for efficiency, fairness, and a healthy business.")
