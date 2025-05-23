import streamlit as st

# Adjustable values
WEEKLY_LIMIT = 20
CYCLE_DURATION_MINUTES = 40
BASE_WEEKLY_PAY = WEEKLY_LIMIT

# Penalty and bonus structure
penalties = [-2.5, -5.5, -10]
bonuses = [3.0, 5.0, 5.75]

def calculate_adjustments(extra_cycles):
    if extra_cycles == 0:
        return 0
    elif extra_cycles < 0:
        count = min(abs(extra_cycles), len(penalties))
        return -sum(penalties[i] for i in range(count))
    else:
        count = min(extra_cycles, len(bonuses))
        return sum(bonuses[i] for i in range(count))

def distribute_fairly(total_income, num_friends, adjustments):
    base_total = BASE_WEEKLY_PAY * 4 * num_friends
    base_per_friend = BASE_WEEKLY_PAY * 4
    base_payments = [base_per_friend + adjustments[i] for i in range(num_friends)]

    fair_minimum = max(20 - (num_friends - 2) * 5, 10)
    min_friend_earnings = min(fair_minimum, total_income / (num_friends + 1))

    scaled = False
    if any(f < min_friend_earnings for f in base_payments):
        scaled = True
        scale_factor = (total_income / (sum(base_payments) + 1e-9))  # Avoid div by zero
        base_payments = [round(p * scale_factor, 2) for p in base_payments]

    total_paid_to_friends = sum(base_payments)
    boss_pay = round(total_income - total_paid_to_friends, 2)

    return base_payments, boss_pay, scaled

st.title("🐶 Dog Walking Payout Calculator")

num_friends = st.number_input("How many friends work with you?", min_value=1, max_value=10, value=3, step=1)
total_income = st.number_input("Monthly income (€)", min_value=0.0, step=10.0)

adjustments = []
st.header("Enter weekly cycle adjustments per friend")
for friend in range(num_friends):
    st.subheader(f"Friend {friend + 1}")
    total_adjustment = 0
    for week in range(1, 5):
        val = st.number_input(f"Week {week} (extra/less cycles)", min_value=-5, max_value=5, value=0, step=1, key=f"f{friend}_w{week}")
        total_adjustment += calculate_adjustments(val)
    adjustments.append(total_adjustment)

if st.button("Calculate Payout"):
    payouts, boss_pay, scaled = distribute_fairly(total_income, num_friends, adjustments)
    st.subheader("--- Monthly Payout ---")
    for i, amount in enumerate(payouts):
        st.write(f"Friend {i + 1}: €{amount:.2f}")
    st.write(f"Boss (You): €{boss_pay:.2f}")
    st.write(f"Total payout: €{sum(payouts) + boss_pay:.2f}")
    if scaled:
        st.info("⚖️ Total income was too low to meet base expectations, so everyone's pay was scaled proportionally.")
