import streamlit as st

st.set_page_config(page_title="Dog Walking Payout Calculator", layout="centered")

st.title("🐶 Dog Walking Payout Calculator")

# Inputs
num_friends = st.number_input("How many friends are working for you?", min_value=1, max_value=10, value=3, step=1)
total_income = st.number_input("Monthly Business Income (€)", min_value=0.0, step=10.0)

# Initialize input fields
cycle_data = []
st.subheader("Enter cycle differences for each week per friend")

for friend in range(num_friends):
    friend_weeks = []
    st.markdown(f"**Friend {friend + 1}**")
    cols = st.columns(4)
    for week in range(4):
        with cols[week % 4]:
            val = st.number_input(f"Week {week + 1}", min_value=-5, max_value=5, step=1, key=f"f{friend}_w{week}")
            friend_weeks.append(val)
    cycle_data.append(friend_weeks)

if st.button("Calculate Payout"):
    # Weekly pay limit and base monthly pay
    weekly_limit = 20
    base_weekly_pay = weekly_limit
    base_monthly_pay = base_weekly_pay * 4

    # Bonus/Penalty rules
    def calc_adjustment(week_delta):
        if week_delta == 0:
            return 0
        elif week_delta > 0:
            if week_delta == 1:
                return 3.00
            elif week_delta == 2:
                return 5.00
            else:
                return 5.75
        else:
            if week_delta == -1:
                return -2.50
            elif week_delta == -2:
                return -5.50
            else:
                return -10.00

    payouts = []
    total_friend_payout = 0

    for friend_weeks in cycle_data:
        adjustment = sum(calc_adjustment(week) for week in friend_weeks)
        payout = base_monthly_pay + adjustment
        payouts.append(round(payout, 2))
        total_friend_payout += payout

    # Determine fair boss share
    remaining = total_income - total_friend_payout

    if remaining <= 0:
        # Cut everyone's payouts proportionally to ensure boss earns more than anyone else
        scale_factor = total_income / (sum(payouts) + 1e-8)
        payouts = [round(p * scale_factor, 2) for p in payouts]
        max_friend = max(payouts)
        boss_payout = max(round(max_friend + 1, 2), round(total_income - sum(payouts), 2))
        if sum(payouts) + boss_payout > total_income:
            scale_back = total_income / (sum(payouts) + boss_payout)
            payouts = [round(p * scale_back, 2) for p in payouts]
            boss_payout = round(boss_payout * scale_back, 2)
    else:
        boss_payout = round(remaining, 2)

    # Output
    st.subheader("--- Monthly Payout ---")
    for i, payout in enumerate(payouts):
        st.write(f"Friend {i+1}: €{payout}")
    st.write(f"\n**Boss (You): €{boss_payout}**")
    st.write(f"\n**Total payout: €{round(sum(payouts) + boss_payout, 2)}**")
