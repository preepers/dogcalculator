import streamlit as st
import datetime

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

    return max(total_points, 0)  # Avoid negative points

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
            raw_payout = (points / total_points) * len(walkers) * monthly_cap / 4  # Weekly pay
            payouts[name] = round(min(raw_payout, monthly_cap / 4), 2)

    return {
        'walker_points': walker_points,
        'walker_payouts': payouts
    }

# UI Setup
st.set_page_config(page_title="Dog Walking Pay Calculator", layout="centered")
st.title("🐶 Weekly Dog Walking Calculator")
st.markdown("""
Enter each walker's stats for the week. Max payout per person is **€80/month**, or **€20/week**.
Points system:
- Base walk: **10 pts**
- Weekend walk: **+2 pts**
- Rainy day: **+3 pts**
- Substitution: **+5 pts**
- Extra walk: **+6 pts**
- Missed walk: **–7 pts**
""")

current_week = st.date_input("Week Ending", value=datetime.date.today())
walker_names = ["Alice", "Ben", "Charlie"]
walker_inputs = {}

with st.form("weekly_form"):
    for name in walker_names:
        with st.expander(f"🚶 {name}"):
            walks = st.number_input(f"{name} - Total Walks", min_value=0, key=f"walks_{name}")
            weekend = st.number_input(f"{name} - Weekend Walks", min_value=0, key=f"weekend_{name}")
            rain = st.number_input(f"{name} - Rainy Walks", min_value=0, key=f"rain_{name}")
            sub = st.number_input(f"{name} - Substitutions", min_value=0, key=f"sub_{name}")
            extra = st.number_input(f"{name} - Extra Walks", min_value=0, key=f"extra_{name}")
            missed = st.number_input(f"{name} - Missed Walks", min_value=0, key=f"missed_{name}")
            walker_inputs[name] = {
                'walks': walks,
                'weekend': weekend,
                'rain': rain,
                'sub': sub,
                'extra': extra,
                'missed': missed
            }

    submitted = st.form_submit_button("📊 Calculate This Week's Pay")

if submitted:
    results = calculate_payouts(walker_inputs)
    st.success(f"Results for week ending {current_week.strftime('%B %d, %Y')}")
    
    st.subheader("🏆 Weekly Results")
    for name in walker_names:
        pts = results['walker_points'][name]
        pay = results['walker_payouts'][name]
        st.write(f"**{name}** — {pts} points → **€{pay}**")

    st.markdown("---")
    st.caption("Created with ❤️ to reward fair work")
