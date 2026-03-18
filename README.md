# Vending Machine (CLI)

## 1. Admin Features

- **Admin login**
  - Admin can log in with a username and password.
  - Only admin can manage items and prices.

- **Item management**
  - **Add item** with:
    - Item name
    - Item code (unique identifier, e.g. A1, B2, C3)
    - Price
    - Quantity in stock (number of items)
  - **View items**:
    - Show all items with:
      - Code
      - Name
      - Price
      - Available quantity
  - (Optional) **Update / remove item**:
    - Change price, name, or quantity.
    - Disable an item (out of stock / not for sale).

- **Total amount / revenue**
  - Track total money collected by the machine (lifetime or per session).
  - Admin can view the total amount collected.

---

## 2. User (Customer) Features

- **View items**
  - Show all available items with:
    - Code
    - Name
    - Price

- **Select items**
  - User can enter:
    - A **single item code**, or
    - **Multiple item codes** (e.g. `A1,B2,B2`), depending on your design.
  - If an invalid code is entered:
    - Show an error message.
    - Ask the user to re-enter the code(s).

- **Show order summary**
  - Display selected items and their individual prices.
  - Display the **total price** of all selected items.
  - Ask user to confirm (e.g. “OK” / “Cancel”).

---

## 3. Payment Flow

- **Payment input**
  - User enters the amount of money they insert into the machine.
  - (Optional) Support multiple inserts (e.g. insert more coins after first try).

- **Compare amount vs total price**
  - **If amount < total price**:
    - Show a message: not enough money.
    - Either:
      - Ask user to insert more money **OR**
      - Cancel the transaction and return the money.
  - **If amount == total price**:
    - Complete the purchase:
      - Dispense the selected items.
      - Decrease item quantities in stock.
      - Add the amount to the machine’s total amount.
      - Print “Thank you”.
  - **If amount > total price**:
    - Ask the user:
      - “Do you want to buy more items with the remaining balance?”
    - If **Yes**:
      - Keep the remaining balance.
      - Let the user enter more item codes.
      - Recalculate total price vs remaining balance.
      - Repeat the comparison logic.
    - If **No**:
      - Return the extra money (change).
      - Complete the purchase for the already selected items.
      - Decrease item quantities and add the spent amount to total.

- **Inventory update**
  - After a successful purchase:
    - Reduce the quantity of each purchased item.
    - If quantity reaches 0, mark item as out of stock (cannot be purchased).

---

## 4. Error Handling & UX

- **Invalid item code**
  - Show clear message and re-prompt for a valid code.

- **Out of stock**
  - If a selected item has zero quantity:
    - Inform the user.
    - Ask to choose another item or remove it from selection.

- **Cancel transaction**
  - User can cancel at any time before purchase is completed:
    - Return any inserted money.
    - Clear current selection.

- **Input validation**
  - Handle non-numeric input where numbers are expected (amount, quantity).
  - Handle empty input gracefully.