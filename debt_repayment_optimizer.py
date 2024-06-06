class Account:
    def __init__(self, name, balance, months_left):
        self.name = name
        self.initial_balance = balance
        self.balance = balance
        self.months_left = months_left
        self.monthly_payment = balance / months_left
        self.closed = False


def apply_extra_payment(accounts, extra_payment_funds):
    applied_extra_payment = False
    while extra_payment_funds > 0:
        # Find the account with the next lowest balance
        next_lowest_account = None
        for account in accounts:
            if account.balance > 0 and (next_lowest_account is None or account.balance < next_lowest_account.balance):
                next_lowest_account = account

        if next_lowest_account:
            if next_lowest_account.balance <= extra_payment_funds:
                extra_payment = next_lowest_account.balance
                extra_payment_funds -= extra_payment
                print(f"  Applying extra payment of ${
                      extra_payment:.2f} to {next_lowest_account.name}")
                next_lowest_account.balance = 0
                next_lowest_account.closed = True
                print(f"  {next_lowest_account.name} is paid in full")
                applied_extra_payment = True
            else:
                next_lowest_account.balance -= extra_payment_funds
                print(f"  Applying extra payment of ${
                      extra_payment_funds:.2f} to {next_lowest_account.name}")
                extra_payment_funds = 0
                applied_extra_payment = True
        else:
            break

    return extra_payment_funds, applied_extra_payment


def calculate_payments(accounts, added_amount, added_amount_distribution=None):
    total_months = max(account.months_left for account in accounts)
    first_month_payment = sum(account.monthly_payment for account in accounts)
    extra_payment_funds = 0

    # Apply added_amount to specified accounts if distribution is provided
    if added_amount_distribution:
        for account_name, amount in added_amount_distribution.items():
            for account in accounts:
                if account.name == account_name and amount > 0:
                    if account.balance <= amount:
                        print(f"  Applying added amount of ${
                              account.balance:.2f} to {account.name}")
                        amount -= account.balance
                        account.balance = 0
                        account.closed = True
                    else:
                        account.balance -= amount
                        print(f"  Applying added amount of ${
                              amount:.2f} to {account.name}")
                        amount = 0

    # Apply remaining added_amount to lowest balance accounts
    added_amount_remaining = added_amount - \
        sum(added_amount_distribution.values()
            ) if added_amount_distribution else added_amount
    for account in sorted(accounts, key=lambda x: x.balance):
        if added_amount_remaining > 0:
            if account.balance <= added_amount_remaining:
                print(f"  Applying added amount of ${
                      account.balance:.2f} to {account.name}")
                added_amount_remaining -= account.balance
                account.balance = 0
                account.closed = True
            else:
                account.balance -= added_amount_remaining
                print(f"  Applying added amount of ${
                      added_amount_remaining:.2f} to {account.name}")
                added_amount_remaining = 0

    for month in range(1, total_months + 1):
        total_payment = first_month_payment
        actual_payment = 0

        print(f"Month {month}:")

        closed_accounts = []

        for i, account in enumerate(accounts):
            if account.balance == 0 and not account.closed:
                print(f"  {account.name} is closed with an original payment of ${
                      int(account.monthly_payment):.2f}")
                account.closed = True
                closed_accounts.append(i)

            if account.balance > 0:
                payment = min(account.monthly_payment, account.balance)
                account.balance -= payment
                actual_payment += payment
                print(f"  {account.name} payment: ${payment:.2f}")

                if account.balance <= 0:
                    print(f"  {account.name} is paid in full")
                    account.closed = True

        for i in closed_accounts:
            paid_off_account = accounts[i]
            payment = paid_off_account.monthly_payment
            extra_payment_funds += payment
            print(f"  Allocating ${payment:.2f} from {
                  paid_off_account.name} to extra payment funds")

        extra_payment_funds += total_payment - actual_payment

        if extra_payment_funds > 0:
            print(f"Applying extra payment of ${
                  extra_payment_funds:.2f} to next lowest balance account(s):")
            extra_payment_funds, applied_extra_payment = apply_extra_payment(
                accounts, extra_payment_funds)
            if not applied_extra_payment:
                print("  No accounts to apply extra payment to")

        for account in accounts:
            if account.balance > 0:
                print(f"  {account.name} remaining balance: ${
                      account.balance:.2f}")

        print(f"Total payment for Month {month}: ${total_payment:.2f}")
        print(f"Extra funds left after Month {
              month} payment cycle: ${extra_payment_funds:.2f}")
        print()

        if all(account.balance == 0 or account.closed for account in accounts):
            print("\nEnd of All Payments")
            break


accounts = [
    Account("Account H", 2300, 23),
    Account("Account F", 820, 16),
    Account("Account S", 9000, 15),
    Account("Account W", 6300, 23)]

added_amount = 5250
added_amount_distribution = {
    "Account F": 500,
    "Account H": 1000
}

calculate_payments(accounts, added_amount, added_amount_distribution)
