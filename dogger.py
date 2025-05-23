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

    for week in weekly_balances:
        for i, balance in enumerate(week):
            adjustment = calculate_weekly_adjustment(balance)
            pay = base_weekly_pay + adjustment
            friend_totals[i] += pay

    total_friend_raw_pay = sum(friend_totals)
    if num_friends == 0:
        return [], total_monthly_income, total_monthly_income
    if total_friend_raw_pay == 0:
        return [0.0] * num_friends, total_monthly_income, total_monthly_income

    average_friend_pay_raw = total_friend_raw_pay / num_friends
    boss_base_pay = average_friend_pay_raw * 1.5

    total_raw_payout = total_friend_raw_pay + boss_base_pay

    if total_raw_payout <= total_monthly_income:
        # Enough money: pay friends full, boss gets leftover
        scaled_friends = [round(pay, 2) for pay in friend_totals]
        leftover = total_monthly_income - total_raw_payout
        boss_pay = round(boss_base_pay + leftover, 2)
        total_payout = total_monthly_income
    else:
        # Not enough money: scale everything proportionally (friends and boss)
        scale_factor = total_monthly_income / total_raw_payout
        scaled_friends = [round(pay * scale_factor, 2) for pay in friend_totals]
        boss_pay = round(boss_base_pay * scale_factor, 2)
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
