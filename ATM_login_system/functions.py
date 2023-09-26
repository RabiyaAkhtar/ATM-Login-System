import random
import os
import csv

csvfile = open('atm.csv', mode='a+', newline='')  # a+ mode to add new data to the end of file while
# also being able to read from it, thus ensuring data is correctly written in csv file
csv_reader = None  # a global variable to hold the CSV reader object, this will be reusable across functions


def initial_name():
    while True:  # a continuous loop
        name = input("Enter your name: ")
        if name == '':
            print("Type your name!\n")
        elif any(char.isdigit() for char in name):  # checking if name contains any digits
            print("Kindly enter your name using ALPHABETS, not numbers.\n")
        else:
            return name  # exiting the loop and returning the valid name


counter = 1  # a global variable that maintains a continuous count of generated usernames


def generate_unique_username(name):
    global counter  # retains its previous value across multiple function calls
    number = random.randint(1, 1000)
    user_name = str(counter) + str(number) + name  # concatenation
    counter = counter + 1  # counter variable updated by incrementation of 1
    return user_name  # user_name generated as an output of this function


def generate_unique_id():
    id_length = 10
    user_id = ''  # an empty string to store the generated unique_identifier
    for _ in range(id_length - 3):  # running loop 7 times to generate 7 random digits
        numbers = random.randint(0, 6)
        user_id += str(numbers)  # converting the generated random numbers to string and adding it to user_id
    new_num = random.randint(100, 999)  # generating 3 digit random number
    user_id += str(new_num)  # converting to string and adding to user_id
    return user_id  # user_id of 10 digits created


def user_deposit_amount():
    while True:  # a continuous loop
        deposit_amount1 = input("Please enter the amount you want to deposit: ")
        if deposit_amount1 == '':
            print("Can't be blank. Please enter a numerical deposit amount.\n")
        else:
            try:  # a try except block to handle potential exceptions
                deposit_amount1 = float(deposit_amount1)
                if deposit_amount1 < 50:
                    print(f"Please deposit more than PKR 50.\n")
                else:
                    return deposit_amount1  # returning valid deposit_amount1 as a result of function
            except ValueError:  # occurs when wrong value is assigned to an object
                print("Please enter a numerical deposit amount.\n")


def initial_pin_code():
    while True:
        pin_code1 = input("Enter 4-digit PIN code: ")
        if pin_code1 == "":
            print("Can\'t be blank. Please enter a four digit numerical pin code.\n")
        elif not pin_code1.isdigit() or len(pin_code1) != 4:
            print("Invalid input. Enter a four digit numerical pin code.\n")
        else:
            return pin_code1


def read_csv(filename):
    rows = []  # an empty list to store csv data
    with open(filename, mode='r') as my_csv_file:  # opening file in read mode
        csv_reader_inner = csv.DictReader(my_csv_file)  # creating DictReader object to read csv file.
        # naming this object csv_reader_inner
        for row_inner in csv_reader_inner:  # iterating over each row in csv file
            rows.append(row_inner)  # after reading a row, row is converted to a dict. that dict is appended to [rows]
    return rows  # after processing all rows, loop is exited, we get a rows list,
    # that contains dictionaries representing data of csv file


def write_csv(filename, data, fieldnames_inner):
    with open(filename, mode='w', newline='') as my_csv_file:  # opening file in write mode
        user_csv_writer = csv.DictWriter(my_csv_file, fieldnames=fieldnames_inner)  # creating DictWriter object.
        # naming this object user_csv_writer
        user_csv_writer.writeheader()  # writing header row to csv file
        user_csv_writer.writerows(data)  # writing data rows to csv file


def create_account():
    name = initial_name()
    deposit_amount = user_deposit_amount()
    pin_code = initial_pin_code()
    user_id = generate_unique_id()
    username = generate_unique_username(name)

    file_exists = os.path.isfile('atm.csv')  # checking if atm.csv exists

    if not file_exists or os.stat('atm.csv').st_size == 0:  # if file does not exist or exists but has no data
        with open('atm.csv', mode='w', newline='') as new_csvfile:  # open file in write mode
            header = ['Name', 'Username', 'User ID', 'Balance', 'Currency', 'PinCode', 'Status', 'Transaction_Type',
                      'Transaction_Amount']  # a list called headers containing labels for columns I want in my csv file
            writer_obj = csv.writer(new_csvfile)
            writer_obj.writerow(header)  # headers are written to the csvfile, first row of csv file created

    usernames = []
    user_ids = []
    with open('atm.csv', mode='a+', newline='') as csv_file_exists:  # opening in a+ mode so that we can check
        # if a username exists & to add new records if needed
        csv_file_exists.seek(0)  # moving cursor to beginning of file
        reader = csv.reader(csv_file_exists)  # reading contents of csv file
        for user_row in reader:  # iterating over each row of data in csv file
            usernames.append(user_row[1])  # extracting usernames from 2nd column & adding it to the username list
            user_ids.append(user_row[1])  # extracting user ids from 3rd column & adding it to the user ids list
        if username not in usernames and user_id not in user_ids:
            record_data = [name, username, user_id, deposit_amount, "PKR", pin_code, "Active"]  # new_user info
            writer = csv.writer(csv_file_exists)
            writer.writerow(record_data)  # the data entered by user is written to the csvfile as a new row
            print()
            print("Account created successfully.")
            print(f"Congratulations! You have successfully registered! "
                  f"For further reference, the user is advised to save the following information:"
                  f"\nYour username is: {username}\nYour user id / account number is: {user_id}"
                  f"\nYour pincode is: {pin_code}\nYour account is now ACTIVE.\n"
                  f"\nFor checking into your account, click on 'check-in option from the main menu.")
            print("----------------------------------------------------------------")
        else:
            print("Username or Userid is already taken! Try creating an account again.")


def menu_options():
    print("MAIN MENU:\n1. Create Account\n2. Checkin\n3. Exit")


def submenu_options():
    print("SUB MENU:\n1. Account details\n2. Deposit\n3. Withdraw\n4. Update PIN\n5. Check statement\n6. Logout")


def account_details(user_checkin):
    filename = 'atm.csv'
    user_rows = read_csv(filename)
    for user_row in user_rows:
        if user_row['Username'] == user_checkin or user_row['User ID'] == user_checkin:
            print("Account Details:")
            print(f"Name: {user_row['Name']}")
            print(f"Username: {user_row['Username']}")
            print(f"User ID: {user_row['User ID']}")
            print(f"Balance: {user_row['Balance']}")
            print(f"Currency: {user_row['Currency']}")
            print(f"Status: {user_row['Status']}\n")
            return


def deposit(user_checkin):
    dep_amount = user_deposit_amount()
    filename = 'atm.csv'
    user_rows = read_csv(filename)
    for user_row in user_rows:
        if user_row['Username'] == user_checkin or user_row['User ID'] == user_checkin:
            current_balance = float(user_row['Balance'])
            new_balance = current_balance + dep_amount
            user_row['Balance'] = str(new_balance)
            user_row['Status'] = 'Active'
            user_row['Transaction_Type'] = 'Deposit'
            user_row['Transaction_Amount'] = dep_amount

    write_csv(filename, user_rows, fieldnames_inner=['Name', 'Username', 'User ID', 'Balance', 'Currency',
                                                     'PinCode', 'Status', 'Transaction_Type', 'Transaction_Amount'])

    print(f"You have successfully deposited: {dep_amount:.2f} PKR.\n")
    return


def withdraw(user_checkin):
    withdraw_amount = float(input(f"Please enter the amount you want to withdraw: "))
    filename = 'atm.csv'
    user_rows = read_csv(filename)
    for user_row in user_rows:
        if user_row['Username'] == user_checkin or user_row['User ID'] == user_checkin:
            current_balance = float(user_row['Balance'])
            if current_balance >= withdraw_amount:
                withdrawal_tax = 0.01 * withdraw_amount
                new_balance = current_balance - withdraw_amount - withdrawal_tax
                user_row['Balance'] = str(new_balance)
                user_row['Transaction_Type'] = 'Withdraw'
                user_row['Transaction_Amount'] = withdraw_amount

                print(f"You have successfully withdrawn: {withdraw_amount:.2f} PKR "
                      f"& tax applied is: {withdrawal_tax:.2f} PKR.\n")
            else:
                print("Insufficient balance to make a withdrawal from your account.\n")
                return
    # now write the updated data back to the CSV file
    write_csv(filename, user_rows, fieldnames_inner=['Name', 'Username', 'User ID', 'Balance', 'Currency',
                                                     'PinCode', 'Status', 'Transaction_Type', 'Transaction_Amount'])


def update_pin(user_checkin):
    filename = 'atm.csv'
    user_rows = read_csv(filename)
    while True:
        new_pin = input(f"Enter your new four-digit PIN code: ")
        if len(new_pin) == 4 and new_pin.isdigit():
            for user_row in user_rows:  # you have to find the row with the matching username and update the PIN code
                if user_row['Username'] == user_checkin or user_row['User ID'] == user_checkin:
                    previous_pin = user_row['PinCode']
                    if new_pin != previous_pin:
                        user_row['PinCode'] = new_pin
                        print("PIN code updated.\n")
                        write_csv(filename, user_rows, fieldnames_inner=['Name', 'Username', 'User ID',
                                                                         'Balance', 'Currency', 'PinCode', 'Status',
                                                                         'Transaction_Type', 'Transaction_Amount'])
                        return  # Exit the loop once the PIN code is updated
                    else:
                        print("The new PIN code is the same as the previous one. Please choose a different PIN code.\n")
                        break
        else:
            print("Invalid input. Please enter a four-digit numerical PIN code.\n")


def check_statement(user_checkin):
    i_user_found = False  # a variable to track if the user was found
    filename = 'atm.csv'
    user_rows = read_csv(filename)
    for user_row in user_rows:
        if user_row['Username'] == user_checkin or user_row['User ID'] == user_checkin:
            print(f"ACCOUNT STATEMENT:")
            print(f"User: {user_row['Name']}")
            print(f"Username: {user_row['Username']}")
            print(f"User ID: {user_row['User ID']}")
            print(f"Account Status: {user_row['Status']}")
            print("---------------------------")
            print("TRANSACTION HISTORY:")
            if user_row['Transaction_Type'] is None or user_row['Transaction_Amount'] is None:
                print("You have made no transaction yet.\n")
            else:
                print(f"Last Transaction type: {user_row['Transaction_Type']}")
                print(f"Last Transaction amount: {user_row['Transaction_Amount']} PKR\n")
            i_user_found = True  # variable declared True when the user is found
            break  # loop exited once the user is found
    if not i_user_found:
        print("User not found.")
