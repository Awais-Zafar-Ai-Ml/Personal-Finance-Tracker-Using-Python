from expense import Expense
import calendar
import datetime


def main():
    print("Running Expense Tracker")
    expense_file_path = "expense.csv"
    budget = 100000  # just a hardcoded monthly budget for now

    # Step 1: ask the user for their expense details
    expense = get_user_expense()

    # Step 2: save that expense into our csv file so it's not lost
    save_expense_to_file(expense, expense_file_path)

    # Step 3: go back through the whole file (including old expenses)
    # and print out a summary
    summarize_expense(expense_file_path, budget)


def get_user_expense(): 
    print("Getting user expense")
    expense_name = input("Enter expense name:")

    # Keep looping here until the user actually types a valid number.
    # If they type letters or leave it empty, float() will throw a
    # ValueError, and we just ask again instead of crashing.
    while True:
        try:
            expense_amount = float(input("Enter expense amount:"))
            break
        except ValueError:
            print("Please enter a valid number.")

    # Fixed categories for now, could probably load these from a file
    # later if we wanted it to be more flexible.
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc",
    ]

    # Same idea as above - keep showing the menu until they pick
    # something that's actually on the list.
    while True:
        print("Select a Category: ")
        for i, category_name in enumerate(expense_categories):
            # enumerate starts counting from 0, but showing "0. Food" to
            # a user looks weird, so we add 1 just for the display.
            print(f"{i + 1}. {category_name}")

        value_range = f"1-{len(expense_categories)}"

        try:
            # user typed a number starting from 1, but list indexes
            # start from 0, so we subtract 1 to line them back up
            selected_index = int(input(f"Enter a category number {value_range}:")) - 1
        except ValueError:
            print("Please enter a number.")
            continue

        # range(len(expense_categories)) is basically "is this a valid
        # index for our list", i.e. not negative and not too big
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]

            # got everything we need now, so bundle it into an Expense
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense

        else:
            print("Invalid Category. Please Try Again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    # Appends this expense as a new line in the csv. Using "a" (append)
    # instead of "w" (write) is important here - "w" would wipe out
    # every expense we've already saved and just leave this one.
    print(f"saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expense(expense_file_path, budget):
    print("Summarizing User Expense")
    expenses: list[Expense] = []

    # Open the csv and rebuild it back into a list of Expense objects.
    # Each line looks like "name,amount,category" so we split on commas
    # to pull the three values back out.
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")

            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),  # was stored as text, need it as a number again
                category=expense_category
            )

            expenses.append(line_expense)

    # Add up how much was spent per category. Using a dict here so each
    # category name is a key and its total is the value - if we've seen
    # the category before we just add to it, otherwise we start it off.
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expense By Category: ")
    for key, amount in amount_by_category.items():
        print(f"   {key}: {amount:.2f}")

    # Total across everything, not just one category
    total_spent = sum([x.amount for x in expenses])
    print(f"You've spent {total_spent:.2f} this month!")

    # Whatever's left in the budget after what's been spent
    remaining_budget = budget - total_spent
    print(f"Budget Remaining: {remaining_budget:.2f}")


    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]  # [1] because monthrange returns (weekday, num_days)
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(f"Budget per day: {daily_budget:.2f}")
    else:
        # last day of the month, dividing by 0 days would break things
        print("No days remaining in this month.")


if __name__ == "__main__":
    main()
