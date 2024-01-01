# requirment 
# menu options 
# view budget 
# add expense
# add income 
# transfer 
# need to modulaer  so make differnt classes that will be called by the main menu function

from datetime import datetime, timedelta
import mysql.connector
import sys
from Data_base.Create_database import Create_data_base
from Data_base.Create_new_table import Create_table
from Input_data.Add_starting_balance import StartBalance
from Input_data.Add_fixed_expense import Add_fixed_expense
from Input_data.Add_expense import Add_Expense
from Input_data.Add_income import Add_Income
import subprocess

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'


# Create an instance of the class
database_creator = Create_data_base()
table_creator = Create_table()
Starter_balance = StartBalance()
add_fixed_expense = Add_fixed_expense()
add_expense = Add_Expense()
add_income = Add_Income()



def Print_menu ():
    subprocess.run("clear", shell=True)

    header_size = 50
    i = 0
    
    while i < header_size:
        print ("-", end="")
        i = 1 + i
        
        
    print ("")
    print ("\t\t    Main Menu")
    print ("Options Below")
    print ("[1] Add Fixed Expense") # works 
    print ("[2] Add Expense")# works 
    print ("[3] Add income")# works 
    print ("[4] Create a new data base") # works 
    print ("[5] Add a new year budget") # works 
    print ("[6] Add_starting_balance") #works 
    
    Display_menu()

def Display_menu():
    db_name = 'test'
    choice  = int(input("Choice :"))
    
    if choice  == 1:
        print ("your choice is ", choice)
        start_date = input ("Enter start date (YYYY-MM-DD) :")
        amount = float(input("Enter Amount :"))
        note = input ("Enter Note :")
        add_fixed_expense.Add_Fixed_expense(db_host, db_user, db_password, db_name, start_date, note, amount) 
    elif choice == 2:
        print("Choice is ",choice)
        print ("your choice is ", choice)
        Expense_date = "2023-04-19"
        amount = 10.00
        note = "note expense test"
        Category = "test"
        add_expense.Add_expense(db_host, db_user, db_password, db_name, Expense_date, note, amount, Category) 
    elif choice == 3:
        print("Choice is ",choice)
        print ("your choice is ", choice)
        Income_date = "2023-03-23"
        amount = 100
        note = "note income test"
        Category = "test"
        add_income.Add_income(db_host, db_user, db_password, db_name, Income_date, note, amount, Category) 
    
    elif choice == 4:
        name = input("What would the the database name to be: ")
        db_name = name
        # Call the method with the necessary parameters
        database_creator.create_database_main(db_host, db_user, db_password, db_name)
        Print_menu ()
    
    elif choice == 5:
        print ("connect to recent database [y/n]")
        choice_2 = (input("Choice :"))
        if choice_2 == "y" or "Y":
            year = input("what year :")
            table_name = f"Budget{year}"
            table_creator.populate_single_table( db_host, db_user, db_password, db_name, table_name,year)
        elif choice_2 == "n" or "N":
            db_name = input("Database name :")
            year = input("what year :")
            table_name = f"Budget{year}"
            table_creator.populate_single_table( db_host, db_user, db_password, db_name, table_name,year)
        else:
            print("Invalid choice")
            print (f"connect to {db_name}? [y/n]")
            choice_2 = (input("Choice :"))
        Print_menu ()
    
    elif choice == 6:
        print ("connect to recent database [y/n]")
        choice_2 = (input("Choice :"))
        if choice_2 == "y" or "Y":
            year = input("what year :")
            table_name = f"Budget{year}"
            checking_account = float(input("Checking account balance :"))
            bail_out = float(input("bail_outg account balance :"))
            saveings = float(input("saveings account balance :"))
            Starter_balance.add_starting_balance(db_host, db_user,db_password,db_name,table_name,year,checking_account,bail_out, saveings)
        elif choice_2 == "n" or "N":
            db_name = input("Database name :")
            year = input("what year :")
            table_name = f"Budget{year}"
            checking_account = float(input("Checking account balance :"))
            bail_out = float(input("bail_out account balance :"))
            saveings = float(input("saveings account balance :"))
            Starter_balance.add_starting_balance(db_host, db_user,db_password,db_name,tablbbe_name,year,checking_account,bail_out, saveings)
        else:
            print("Invalid choice")
            print (f"connect to {db_name}? [y/n]")
            choice_2 = (input("Choice :"))
            
        
        
    
Print_menu ()


#source venv/bin/activate

#TODO Create transfer money module and connect it to post transaction 
#TODO create add expense module and connect it to post transaction
#TODO create add income module and connect it to post transaction 
#TODO create view budget module