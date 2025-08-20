# Database connection details
import mysql.connector

conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="67808033",
    database="Python_Project")
cur_obj = conn_obj.cursor()

# create this function when you design password in registration part
import re

#1
def strong_password(password):
    if (len(password) >= 6 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[\W_]', password)):
        return True
    return False

#2
def strong_userid(user_id):
    if (len(user_id) >= 3 and
            re.search(r'[A-Z]', user_id) and
            re.search(r'[0-9]', user_id)):
        return True
    return False

#3
# Define function data_entry_sql
def data_entry_sql(full_name, address, phone_number, user_id, password):
    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO cust_details (full_name,address,phone_number,user_id,password) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name, address, phone_number, user_id, password)

    try:
        cur_obj.execute(sql, data)
        print(full_name, ", Now You are Successfully Registered")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

#4
# Define function data_retrieve
def data_retrieve(user_id):
    # Build the query with user-provided name using LIKE operator
    # select * from students_details WHERE Roll_no=1;
    query = f"select * from cust_details where user_id=\'{user_id}\'"

    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result



#5
def login():
    user_id = input("Enter your user id - ")   #if you want you can keep user_id validation by strong_userid()
    password = input("Enter your password - ")
    user_details = data_retrieve(user_id)
    if user_details:
        actuall_password = user_details[-1]
        if actuall_password == password:
            print("log in successfull")
        else:
            print("Wrong entry , log in failed")

    else:
        print("you are not registered, Please Register Yourself Below")
        cust_registration()
        print("Now Log In")
        login()



#6
def cust_registration():
    full_name = input("Enter your full name - ").upper()
    address = input("Enter your address - ")

    while True:
        phonr_number = input("Enter your phone number - ")
        if phonr_number.isdigit() and len(phonr_number) == 10:
            break
        else:
            print("wrong entry")

    cur_obj.execute("SELECT * FROM cust_details WHERE phone_number = %s", (phonr_number,))
    if cur_obj.fetchone():
        print("already registered .. Please Log in")
        return  # single return uporer function ke aar egote na dewar jonno use hoy

    while True:  # eta different
        user_id = input("Make your user id - ")
        if not strong_userid(user_id):
            print("Username must include uppercase and digit.")
            continue

        cur_obj.execute("SELECT * FROM cust_details WHERE user_id = %s", (user_id,))
        if cur_obj.fetchone():
            print("This user ID is already used. Please try something unique.")
        else:
            break

    while True:
        password = input("Make the password -")
        if strong_password(password):
            break
        else:
            print("Password must include uppercase, lowercase, digit, and special character.")

    data_entry_sql(full_name, address, phonr_number, user_id, password)
    print("Now Log In")
    login()



#7
def Data_Retrieve(phone_number, cust_id):
    # Build the query with user-provided name using LIKE operator
    # select * from students_details WHERE Roll_no=1;

    # Query = f"select * from cust_details where user_id=\'{user_id}\'"
    # Query = f"select * from cust_details where phone_number=\'{phone_number}\' and cust_id=\'{cust_id}\'"
    Query = f"select * from cust_details where phone_number={phone_number} and cust_id={cust_id}"

    try:
        cur_obj.execute(Query)
        Result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    if Result:
        cust_id, full_name, address, phone_number, user_id, password = Result
        print("Customer ID - ", cust_id)
        print("Customer Name - ", full_name)
        print("Customer Address - ", address)
        print("Customer Contact Number - ", phone_number)
    else:
        print("No data found")

#8
def profile_view() :
    while True:
        # user_id = input("Enter Your user ID - ")
        phone_number = input("enter your phone number - ")

        # if strong_userid(user_id) :
        if phone_number.isdigit() and len(phone_number) == 10:
            break
        else:
            print("WRONG ENTRY")

    while True:

        cust_id = input("Enter your customer id - ")
        if cust_id.isdigit():
            break
        else:
            print("wrong format, customer id should be in digit")

    Data_Retrieve(phone_number, cust_id)

#9
def update_profile() :
    user_id = input("Enter your user ID - ")    # here we can nott use login(), cause login() function:Only prints "Log in successful" if credentials match.Does not return any user details.
    password = input("Enter your password - ")

    user_details = data_retrieve(user_id)
    if not user_details:
        print("User ID not found. Please register.")
        return

    stored_password = user_details[-1]
    if password != stored_password:
        print("Incorrect password. Access denied.")
        return
    # here we taking agin userid & password to verify the credentials correct or not .. If correct, we are able to get and use user_details for updating. If incorrect, to exit

    print("Login successful. You can now update your details.")
    print("Leave a field blank if you don't want to change it.")
    print()
    full_name =input("Enter your new full name - ") .upper()
    address = input("Enter your new address - ")

    while True:
        phone_number = input("Enter new phone number   Otherwise      leave blank to keep unchanged - ")
        #                                 2                                          1
        if not phone_number    or         phone_number.isdigit() and len(phone_number) ==10 :
        #         1                                             2
        # phone_number==" "(blank)    Otherwise  Phone_number == not blank, filled new phone number by user
            break
        else:
            print("Invalid phone number.")

    while True :
        new_password = input("Enter Your new password    Otherwise    leave blank to keep unchanged - ")
        #                              2                                           1
        if new_password == "" :               #1
            new_password = stored_password
            break
        elif strong_password(new_password) :  #2
            break
        else:
            print("Password must include uppercase, lowercase, digit, and special character.")

    # knowing the position of old values
    cust_id=user_details[0]
    old_name = user_details[1]
    old_address = user_details[2]
    old_phone_number = user_details[3]

    #prepare new/updated values
    updated_name = full_name or old_name
    # If the user typed a new name (full_name is not empty), then updated_name becomes that new name(full_name). else the user left it blank, then updated_name keeps the old name
    updated_address = address or old_address
    updated_phone_number = phone_number or old_phone_number
    qry = "UPDATE cust_details SET full_name = %s, address = %s, phone_number = %s, password = %s WHERE cust_id = %s"
    vlu = (updated_name,updated_address,updated_phone_number,new_password,cust_id)
    try:
        cur_obj.execute(qry, vlu)
        conn_obj.commit()
        print("Details updated successfully.")
    except mysql.connector.Error as e:
        print("Error updating data:", e)
        conn_obj.rollback()


#10
def delete_account() :
    user_id=input("Enter The User ID - ")
    password = input("Enter Your Password - ")
    user_dtls=data_retrieve(user_id)
    if not user_dtls :
        print("You are not registered user")
        return

    strd_pswrd=user_dtls[-1]
    if password != strd_pswrd :
        print("You have entered worng password")
        return
    #verify entered credentials correct or not

    print("ACCOUNT DELETE !")
    print()
    user_choice_to_delete=input("Are you sure want to Delete your account ? Type YES to confirm - ") .upper()
    if user_choice_to_delete == "YES" :
        try:
            cur_obj.execute("DELETE FROM cust_details WHERE user_id = %s", (user_id,))
            conn_obj.commit()
            print("Your account has been successfully deleted.")
        except mysql.connector.Error as e:
            print("Error deleting account:", e)
            conn_obj.rollback()

    else:
            print("Account deletion cancelled.")



# Main Code



cust_choice = input("1 - Log In \n2 - Register Yourself \n3 - Profile View \n4 - Update Your Profile \n5 - Delete Account \n    Enter Your Choice - ")


if cust_choice == "1":
    login()


elif cust_choice == "2":
    # register yourself
    cust_registration()


elif cust_choice == "3":
    profile_view()


elif cust_choice == "4" :
    update_profile()
    print("View Your Profile")
    profile_view()


elif cust_choice == "5" :
    delete_account()




else:
    print("invalid entry")

conn_obj.close()

