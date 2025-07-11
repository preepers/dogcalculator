import streamlit as st
from math import sqrt

def calculate_weekly_adjustment(balance):
    if balance < 0:
        if balance == -1:
            return -2.5
        elif balance == -2:
            return -5.5
        else:
            return -10
    elif balance > 0:
        if balance == 1:
            return 3.0
        elif balance == 2:
            return 5.0
        else:
            return 7.5  # Boosted to reflect extra work value
    else:
        return 0.0

def monthly_payout(total_monthly_income, weekly_balances, num_friends):
    base_weekly_pay = 20
    max_monthly_friend_pay = 80
    weeks = len(weekly_balances)
    expected_walks = weeks * 3  # 3 cycles per week

    friend_totals = [0.0] * num_friends
    friend_walks = [0] * num_friends

    for week in weekly_balances:
        for i, balance in enumerate(week):
            adjustment = calculate_weekly_adjustment(balance)
            pay = base_weekly_pay + adjustment
            friend_totals[i] += pay

            actual_walks = 3 + balance  # Balance modifies expected 3 walks
            friend_walks[i] += max(0, actual_walks)  # Cap minimum at 0

    if num_friends == 0:
        return [], total_monthly_income, total_monthly_income

    if sum(friend_totals) == 0:
        return [0.0] * num_friends, total_monthly_income, total_monthly_income

    # Calculate penalties and bonuses
    penalties = []
    bonuses = []
    total_penalties = 0
    total_bonuses = 0

    for i in range(num_friends):
        missed_walks = max(0, expected_walks - friend_walks[i])
        extra_walks = max(0, friend_walks[i] - expected_walks)
        penalty = (missed_walks ** 2) * 0.25
        bonus = (extra_walks ** 1.5) * 1.0  # Increased reward scaling

        penalties.append(penalty)
        bonuses.append(bonus)
        total_penalties += penalty
        total_bonuses += bonus

    # Adjust friends pay with penalties, bonuses and cap at max
    adjusted_friend_totals = []
    for i in range(num_friends):
        adjusted_pay = friend_totals[i] - penalties[i] + bonuses[i]
        capped_pay = min(adjusted_pay, max_monthly_friend_pay)
        adjusted_friend_totals.append(capped_pay)

    # Now calculate boss pay as 1.5x average of capped friend pay
    boss_base_pay = (sum(adjusted_friend_totals) / num_friends) * 1.5

    # Low income proportional scaling boost for light work
    if total_monthly_income <= 100:
        max_walks = max(friend_walks)
        if max_walks > 0:
            for i in range(num_friends):
                if friend_walks[i] > 0:
                    scale_up = (friend_walks[i] / max_walks) ** 0.8
                    boost_ratio = 0.15  # Control how much boost happens at low income
                    new_value = adjusted_friend_totals[i] + boost_ratio * (scale_up * total_monthly_income / num_friends)
                    boss_base_pay -= max(0, new_value - adjusted_friend_totals[i])
                    adjusted_friend_totals[i] = min(new_value, max_monthly_friend_pay)

    total_raw_payout = sum(adjusted_friend_totals) + boss_base_pay + total_penalties - total_bonuses

    if total_raw_payout <= total_monthly_income:
        scaled_friends = [round(pay, 2) for pay in adjusted_friend_totals]
        leftover = total_monthly_income - total_raw_payout
        boss_pay = round(boss_base_pay + total_penalties - total_bonuses + leftover, 2)
        total_payout = total_monthly_income
    else:
        scale_factor = total_monthly_income / total_raw_payout
        scaled_friends = [round(pay * scale_factor, 2) for pay in adjusted_friend_totals]
        boss_pay = round((boss_base_pay + total_penalties - total_bonuses) * scale_factor, 2)
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
