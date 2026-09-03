class Expense:
    # This class is basically just a container for one expense.
    # Every time the user logs something, we make one of these objects
    # so we have the name, category and amount all bundled together
    # instead of passing 3 separate variables around everywhere.
    def __init__(self, name, category, amount):
        self.name = name        # what the expense was for, e.g "Pizza"
        self.category = category  # which bucket it belongs to, e.g "Food"
        self.amount = amount    # how much it cost

    # Without this, printing an Expense would just show something ugly
    # like <__main__.Expense object at 0x7f...>. This makes it print
    # in a readable way instead, e.g:
    # <Expense : Pizza, Food, 500.00>
    def __repr__(self):
        return f"<Expense : {self.name}, {self.category}, {self.amount:.2f}>"
