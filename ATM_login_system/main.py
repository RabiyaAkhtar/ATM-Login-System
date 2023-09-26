import csv

from functions import create_account, menu_options, submenu_options, account_details,\
    deposit, withdraw, update_pin, check_statement

print()
print("                                     WELCOME TO THE ONLINE BANKING SYSTEM!                                     ")
print()
print("USER GUIDE:\n1. User must deposit more than PKR 50 to create an account "
      "and to make a deposition anytime later."
      " After successful account creation, your username, user id and pincode will be printed. "
      "Please save them for further reference.\n2. Your user id is your account number."
      "\n3. In case of three wrong pincode attempts, your account will be blocked and hence, become inaccessible. "
      "You will have to create a new account then.\n4. 1% tax will be applied on the withdrawal amount."
      "\n5. You can change your four digit pin code if required. "
      "In this case, please note your new pin code for further reference.")
print("--------------------------------------------------------------------------------")


def user_decides_to_continue():
    continues = True
    while continues:
        user_continues = input("Do you want to select any other option from submenu? Type 'yes' or 'no': ").lower()
        if user_continues == 'yes':
            print()
            submenu_options()
            print()
            user_continues_choice = input(f"Please enter your choice: ")
            print()
            if user_continues_choice == '1':
                account_details(user_checkin)
            elif user_continues_choice == '2':
                deposit(user_checkin)
            elif user_continues_choice == '3':
                withdraw(user_checkin)
            elif user_continues_choice == '4':
                update_pin(user_checkin)
            elif user_continues_choice == '5':
                check_statement(user_checkin)
            elif user_continues_choice == '6':
                print("You have logged out of your account.")
                print("You\'ll be redirected to the main menu now.")
                print("----------------------------------------------------------------")
                break
            else:
                print("invalid submenu choice.")
                print("----------------------------------------------------------------")
        else:
            print()
            print("See you later alligator! You are redirected to main menu now.")
            print("----------------------------------------------------------------\n")
            continues = False


ATM_working = True
while ATM_working:
    menu_options()
    print()
    choice = input(f"Enter your choice: ")
    print()

    if choice == '1':
        create_account()
    elif choice == '2':
        user_checkin = input(f"Enter your user id or username: ")
        if user_checkin.isdigit():
            user_identifier = 'User ID'
        else:
            user_identifier = 'Username'

        with open('atm.csv', 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            user_found = False  # a variable used later to exit for loop

            for row in csv_reader:
                if (user_identifier == 'User ID' and row['User ID'] == user_checkin) \
                        or (user_identifier == 'Username' and row['Username'] == user_checkin):
                    pin_attempts = 3
                    if row['Status'] == 'Blocked':
                        print('Access denied. Your account is blocked.')
                        print("----------------------------------------------------------------\n")
                        break
                    else:
                        account_blocked = False
                        while pin_attempts > 0:
                            pin = input(f"Enter your four-digit PIN code: ")
                            if pin == row['PinCode']:
                                print("You have successfully checked in.")
                                print("----------------------------------------------------------------")
                                submenu_options()
                                print()
                                new_choice = input(f"Please enter your choice: ")
                                print()
                                if new_choice == '1':
                                    account_details(user_checkin)
                                    user_decides_to_continue()
                                elif new_choice == '2':
                                    deposit(user_checkin)
                                    user_decides_to_continue()
                                elif new_choice == '3':
                                    withdraw(user_checkin)
                                    user_decides_to_continue()
                                elif new_choice == '4':
                                    update_pin(user_checkin)
                                    user_decides_to_continue()
                                elif new_choice == '5':
                                    check_statement(user_checkin)
                                    user_decides_to_continue()
                                elif new_choice == '6':
                                    print("You have logged out of your account.")
                                    print("You will be redirected to the main menu now.")
                                    print("----------------------------------------------------------------")
                                else:
                                    print("Invalid submenu choice.")
                                    print("----------------------------------------------------------------")
                                user_found = True
                                break  # loop exited when the user is found and successfully checked in
                            else:
                                pin_attempts -= 1
                                if pin_attempts > 0:
                                    print(f"Incorrect PIN. {pin_attempts} attempts left.")
                                else:
                                    print("Incorrect PIN. Account blocked. You need to create a new account now.")
                                    print("----------------------------------------------------------------\n")

                                    account_blocked = True
                                    row['Status'] = 'Blocked'
                                    # Reopen the CSV file in write mode to update the blocked status
                                    with open('atm.csv', 'w', newline='') as csv_file:
                                        # Create a DictWriter object and write the header
                                        csv_writer = csv.DictWriter(csv_file, fieldnames=[
                                            'Name', 'Username', 'User ID', 'Balance', 'Currency', 'PinCode',
                                            'Status', 'Transaction_Type', 'Transaction_Amount'])
                                        csv_writer.writeheader()
                                        csv_writer.writerow(row)  # now write the updated row to the CSV file
                                    break  # Exit the while loop when the user is blocked
            if not user_found and row['Status'] != 'Blocked':
                print(f"The {user_identifier} '{user_checkin}' does not exist or is blocked. "
                      f"Kindly login using the correct {user_identifier}."
                      f"\nYou will be redirected to main menu now.")
                print("----------------------------------------------------------------")
                print()
    elif choice == '3':
        print("You have exited the program. Thank you for choosing online banking system. ^.^ ")
        print("----------------------------------------------------------------")
        ATM_working = False
    else:
        print("You have entered an invalid choice. Please select a valid option.\n")

# No need to close the file here as it was already closed within the 'with' statement
