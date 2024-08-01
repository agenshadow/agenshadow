from random import randint, choice
from string import ascii_letters, punctuation
from rsa import encrypt, decrypt, PublicKey, PrivateKey, newkeys
from hashlib import sha256

#dont try if you dont understand python, its not worth the headache.

#this is important everywhere I guess
global file
file = "passwords.txt"

def add(username, password):

    #try to not kys
    try:

        #checking for empty string
        if not username:
            raise ValueError("empty string")

        #checking for empty string
        if not password:
            raise ValueError("empty string")

        #get the public key from the keys.txt file
        with open("keys.txt", "r") as f:
            keys = f.read()
            pub_key_str, priv_key_str = keys.split("§")

        #do something with it
        pub_key = PublicKey.load_pkcs1(pub_key_str.encode('utf-8'))

        #encrypt the password
        encpassword = encrypt(password.encode('utf-8'), pub_key)
        encpassword_hex = encpassword.hex()

        #add the encrypted password to the password file
        with open(file, "a") as f:
            f.write(f"{username}§{encpassword_hex}\n")

        print("password added")

    except ValueError as e:
        print(e)

def remove():
    try:
        #get the password you want to delete
        usr = input("which password would you like to remove? \n").lower()

        tempsafe = []

        with open(file, "r") as f1:
            for i in f1:
                if "§" not in i:
                    raise TypeError("missing a seperator value")

                delen = i.split("§")

                if len(delen) != 2:
                    raise TypeError("too many values to unpack")

                username, password = delen

                #save all the data except the password you want to delete
                if username != usr:
                    tempsafe.append(f"{username}§{password}")

        #overwrite the passwords file so that the password is removed
        with open(file, "w") as f2:
            for j in tempsafe:
                f2.write(j)

        print(f"{usr} removed!")

    except TypeError as e:
        print(e)

def get():
    #ask for the password you want
    usr = input("give me the username of the password you would like to get? \n")

    #find the password
    with open(file, "r") as f:

        for i in f:
            i = i.strip()
            username, password = i.split("§")

            if username == usr:

                #get the private key
                with open("keys.txt", "r") as f:
                    keys = f.read()
                    pub_key_str, priv_key_str = keys.split("§")

                priv_key = PrivateKey.load_pkcs1(priv_key_str.encode('utf-8'))

                #decrypt the password
                encpassword = bytes.fromhex(password)
                decpassword = decrypt(encpassword, priv_key)

                print(f"the password of {username} is: {decpassword.decode('utf-8')}")
                break

            else:
                print("this username does not exist.")
                break

def getallusr():

    usr_list = []

    #open the file and get all the usernames
    with open(file, "r") as f:
        for i in f:
            username, password = i.split("§")
            usr_list.append(username)

    #check the amount of users
    count = len(usr_list)

    #print all the users
    print(f"you have {count} passwords:")
    for i in usr_list:
        print(i)

def passwordgen():
    #figure this one out yourself
    print("this generator automatically creates password of 12 characters minimum.")
    I = randint(0, 2)

    if I == 0:
        a = choice(ascii_letters)
        b = choice(punctuation)
        c = randint(0, 1000)
        d = choice(ascii_letters)
        e = choice(punctuation)
        f = randint(0, 1000)

    elif I == 1:
        f = choice(ascii_letters)
        a = choice(punctuation)
        b = randint(0, 1000)
        c = choice(ascii_letters)
        d = choice(punctuation)
        e = randint(0, 1000)

    else:
        e = choice(ascii_letters)
        f = choice(punctuation)
        a = randint(0, 1000)
        b = choice(ascii_letters)
        c = choice(punctuation)
        d = randint(0, 1000)

    password = f"{a}{e}{b}{c}{f}{d}{c}{a}{d}{e}{d}{e}"
    print("the password is: ", password)

    user_input = input("would you like to add this to your passwords?(y/n)\n").lower()

    if user_input == "y":
        username = input("under what username?\n").lower()
        add(username, password)

    else:
        print("alright bye byeeeeeeeeeee")

def bootprocess():
    usr_password = input("looks like youre new here, lets get you started.\n lets get you a password first, insert your password here: ")

    #making the password into a sha256 hash
    usr_password = sha256(usr_password.encode("utf-8")).hexdigest()

    #adding that hash to a file
    with open("password.txt", "a") as f:
        f.write(usr_password)

    #making the keys
    (pub_key, priv_key) = newkeys(2048)

    #do something to them
    pub_key_str = pub_key.save_pkcs1().decode('utf-8')
    priv_key_str = priv_key.save_pkcs1().decode('utf-8')

    #shove them in a file
    with open("keys.txt", "w") as f:
        f.write(f"{pub_key_str}§{priv_key_str}")

def password():
    #this checks if you have the password correct
    f = open("password.txt", "r")
    hash = f.read()

    # checking for password
    password_input = input("password please: ")
    hashed_input = sha256(password_input.encode("utf-8")).hexdigest()

    # if password is false dont grant access to password manager
    if hashed_input != hash:
        print("wrong")
        return False

    else:
        return True
