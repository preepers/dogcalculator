import streamlit as st

def calculate_weekly_adjustment(balance):
    if balance < 0:
        if balance == -1:
            return -2.5
        elif balance == -2:
            return -5.5
        else:
            return -10
    elif balance > 0:
        # Reward curve for extra cycles (non-linear, moderate growth)
        if balance == 1:
            return 4.0
        elif balance == 2:
            return 7.0
        else:
            return 9.0
    else:
        return 0.0

def monthly_payout(total_monthly_income, weekly_balances, num_friends):
    base_weekly_pay = 20
    weeks = len(weekly_balances)
    expected_walks = weeks * 3  # 3 cycles per week

    friend_totals = [0.0] * num_friends
    friend_walks = [0] * num_friends

    for week in weekly_balances:
        for i, balance in enumerate(week):
            adjustment = calculate_weekly_adjustment(balance)
            pay = base_weekly_pay + adjustment
            friend_totals[i] += pay

            actual_walks = 3 + balance
            friend_walks[i] += max(0, actual_walks)

    penalties = []
    rewards = []
    for i in range(num_friends):
        missed = max(0, expected_walks - friend_walks[i])
        extra = max(0, friend_walks[i] - expected_walks)

        penalty = (missed ** 2) * 0.35
        reward = (extra ** 2) * 0.15

        penalties.append(penalty)
        rewards.append(reward)

    adjusted_friend_totals = []
    excess_pay = 0.0

    for i in range(num_friends):
        adjusted = friend_totals[i] - penalties[i] + rewards[i]
        if adjusted > 80:
            excess = adjusted - 80
            adjusted = 80
            excess_pay += excess
        adjusted_friend_totals.append(max(0, adjusted))

    average_capped_pay = sum(adjusted_friend_totals) / num_friends if num_friends > 0 else 0
    boss_base_pay = average_capped_pay * 1.5
    boss_pay = boss_base_pay + excess_pay

    total_raw_payout = sum(adjusted_friend_totals) + boss_pay

    if total_raw_payout <= total_monthly_income:
        leftover = total_monthly_income - total_raw_payout
        boss_pay += leftover
        boss_pay = round(boss_pay, 2)
        scaled_friends = [round(pay, 2) for pay in adjusted_friend_totals]
        total_payout = total_monthly_income
    else:
        scale_factor = total_monthly_income / total_raw_payout
        scaled_friends = [round(pay * scale_factor, 2) for pay in adjusted_friend_totals]
        boss_pay = round(boss_pay * scale_factor, 2)
        total_payout = round(sum(scaled_friends) + boss_pay, 2)

    return scaled_friends, boss_pay, total_payout

def main():
    st.title("Dog Walking Monthly Payout Calculator")

    num_friends = st.number_input("How many friends are working?", min_value=1, max_value=10, value=3)
    total_monthly_income = st.number_input("Enter total monthly income (€):", min_value=0.0, format="%.2f")

    weeks = 4
    weekly_balances = []

    st.write("### Enter cycle balances per friend for each week")
    st.write("Use values between -3 (3 cycles less) and +3 (3 cycles extra). 0 means completed all cycles.")

    for w in range(weeks):
        st.write(f"**Week {w+1}**")
        week_data = []
        cols = st.columns(num_friends)
        for i in range(num_friends):
            val = cols[i].number_input(f"Friend {i+1}", min_value=-3, max_value=3, value=0, key=f"w{w}f{i}")
            week_data.append(val)
        weekly_balances.append(week_data)

    if st.button("Calculate Payout"):
        friends_pay, boss_pay, total_payout = monthly_payout(total_monthly_income, weekly_balances, num_friends)

        st.write("### Monthly Payout")
        for i, pay in enumerate(friends_pay, 1):
            st.write(f"Friend {i}: €{pay}")
        st.write(f"Boss (You): €{boss_pay}")
        st.write(f"Total payout: €{total_payout}")

if __name__ == "__main__":
    main()
