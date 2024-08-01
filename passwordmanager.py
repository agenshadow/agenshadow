import passwordmanagerfunc as pmd
from hashlib import sha256
from os.path import isfile

#checking whetherornot you have booted this project or not
firstboot = False
boot_check = isfile("password.txt")

if boot_check == False:
    pmd.bootprocess()
    firstboot = True

#this makes sure it does not ask for the password on first boot
if firstboot != True:
    passwordguess = pmd.password()

#if password is correct grant access to password manager
while passwordguess == True:
    try:
        #the shell UI I guess
        user_input = input("Hello, Welcome to the virgin password manager, here is your menu:\nadding a password (add)        get a password (get)\ndelete a password (delete)         a list of all the accounts you have passwords for (getlist)\ngenerate a password(gen)        to quit (quit) (history will be deleted)\n").lower()
        
        if user_input == "add":
            username = input("give me your username\n").lower()
            password = input("give me your password\n")
            pmd.add(username, password)
            continue
        
        if user_input == "delete":
            pmd.remove()
            continue
        
        if user_input == "get":
            pmd.get()
            continue
        
        if user_input == "quit":
            print("\033[H\033[J", end="")
            break
        
        if user_input == "getlist":
            pmd.getallusr()
            continue
        
        if user_input == "gen":
            pmd.passwordgen()
            continue
        
        else:
            print("thats not on the menu!")

    #idk why this is here
    except ValueError as e:
        print(f"an unexpected error has occured: {e}")
