import streamlit as st

# Mapping balances to walk count
BALANCE_TO_WALKS = {
    -3: 0,
    -2: 1,
    -1: 2,
     0: 3,
     1: 4,
     2: 5,
     3: 6
}

MINIMUM_WALK_PAYOUT = 6.50
EXPECTED_WALKS = 12


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
            return 5.75
    else:
        return 0.0


def monthly_payout(total_monthly_income, weekly_balances, num_friends):
    base_weekly_pay = 20
    weeks = len(weekly_balances)

    friend_totals = [0.0] * num_friends
    friend_walks = [0] * num_friends

    for week in weekly_balances:
        for i, balance in enumerate(week):
            adjustment = calculate_weekly_adjustment(balance)
            pay = base_weekly_pay + adjustment
            friend_totals[i] += pay
            friend_walks[i] += BALANCE_TO_WALKS.get(balance, 0)

    total_friend_raw_pay = sum(friend_totals)
    if num_friends == 0:
        return [], total_monthly_income, total_monthly_income
    if total_friend_raw_pay == 0:
        return [0.0] * num_friends, total_monthly_income, total_monthly_income

    average_friend_pay_raw = total_friend_raw_pay / num_friends
    boss_base_pay = average_friend_pay_raw * 1.5

    if boss_base_pay > total_monthly_income:
        return [0.0] * num_friends, total_monthly_income, total_monthly_income

    if total_friend_raw_pay + boss_base_pay > total_monthly_income:
        available_for_friends = total_monthly_income - boss_base_pay
        scale_factor = available_for_friends / total_friend_raw_pay
        scaled_friends = [pay * scale_factor for pay in friend_totals]
    else:
        scaled_friends = friend_totals[:]

    # Apply hybrid fairness penalty
    adjusted_friends = []
    for pay, walks in zip(scaled_friends, friend_walks):
        if walks >= 6:
            adjusted = pay
        elif walks >= 3:
            adjusted = pay * ((walks / EXPECTED_WALKS) * 1.5)
        elif walks > 0:
            adjusted = max(pay * (walks / EXPECTED_WALKS), MINIMUM_WALK_PAYOUT)
        else:
            adjusted = 0.0
        adjusted_friends.append(round(adjusted, 2))

    total_adjusted_friends = sum(adjusted_friends)
    boss_pay = round(total_monthly_income - total_adjusted_friends, 2)
    total_payout = round(total_adjusted_friends + boss_pay, 2)

    return adjusted_friends, boss_pay, total_payout


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
        st.write(f"**Boss (You): €{boss_pay}**")
        st.write(f"**Total payout: €{total_payout}**")


if __name__ == "__main__":
    main()
