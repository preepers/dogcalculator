import streamlit as st

def calculate_adjusted_base_payouts(monthly_income, num_friends):
    # Max 60% of total income goes to friends combined
    max_friend_share = 0.6
    total_friend_payout = min(monthly_income * max_friend_share, monthly_income - 1)
    friend_payout = round(total_friend_payout / num_friends, 2)
    total_friend_payout = round(friend_payout * num_friends, 2)
    boss_payout = round(monthly_income - total_friend_payout, 2)
    return [friend_payout] * num_friends, boss_payout

def calculate_bonus(cycles_diff):
    if cycles_diff == 0:
        return 0
    bonus = 0
    for i in range(abs(cycles_diff)):
        if cycles_diff > 0:
            if i == 0:
                bonus += 3.00
            elif i == 1:
                bonus += 2.00
            else:
                bonus += 0.75
        else:
            if i == 0:
                bonus -= 2.50
            elif i == 1:
                bonus -= 3.00
            else:
                bonus -= 4.50
    return bonus

st.title("🐶 Dog Walking Business Monthly Payout Calculator")

monthly_income = st.number_input("Enter total monthly income (€):", min_value=0, value=300)
num_friends = st.number_input("How many friends work with you?", min_value=1, value=3)

weekly_data = {}
for i in range(num_friends):
    st.markdown(f"### Friend {i+1}")
    weekly_data[i] = []
    for week in range(1, 5):
        cycles = st.number_input(f"Week {week} cycle difference (e.g. 0, -1, +1):", key=f"friend_{i}_week_{week}", value=0)
        weekly_data[i].append(cycles)

# Get base pay
base_payouts, boss_base = calculate_adjusted_base_payouts(monthly_income, num_friends)

# Add bonuses/penalties
final_payouts = []
for i in range(num_friends):
    adjustment = sum(calculate_bonus(diff) for diff in weekly_data[i])
    final_payout = round(base_payouts[i] + adjustment, 2)
    final_payouts.append(final_payout)

# Recalculate boss cut after adjustments
total_friends = sum(final_payouts)
boss_payout = round(monthly_income - total_friends, 2)

# --- Output ---
st.markdown("## 💸 Monthly Payout")
total_paid = 0
for idx, payout in enumerate(final_payouts):
    st.write(f"Friend {idx+1}: €{payout}")
    total_paid += payout

st.write(f"Boss (You): €{boss_payout}")
st.write(f"Total payout: €{round(total_paid + boss_payout, 2)}")

