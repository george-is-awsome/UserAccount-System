from tkinter import *

# Interface Classes

class Interface_Handler: # class to create all interfaces
    def __init__(self): # Window_Present options 1 - 3 to create diffrent windows
        self.name = self
        print(self.name)

    def Create_Login_Window(self):
        self.root = Tk()
        root = self.root # create local scope of self.root for convenience

        root.title("Login")      # defines type of window then begins construction of the interface window 
        root.geometry("300x200")

        username_input = Entry(root)
        password_input = Entry(root,show="*")


        self.username_input = username_input
        self.password_input = password_input

        username_label = Label(root,text="Username",height=1)
        password_label = Label(root,text="Password",height=1)

        submit_button = Button(root,text="submit",height=1,width=10,command=self.Collect_Entry_Data)
        # when pressed the button will send data to a class method to collect the user input and then call an auth method to validate if the entry is correct

        username_input.place(x=10,y=50)
        password_input.place(x=10,y=90)

        username_label.place(x=10,y=29)
        password_label.place(x=10,y=69)

        submit_button.place(x=150,y=90)

    def Collect_Entry_Data(self): # collects data from Entry Objects 
        username_input = self.username_input.get() # uses built in get() function to return the string entered on the object 
        password_input = self.password_input.get()


class File_Handler: # class to handle how to read and write to files - deosnt need to be a class but encryp/decryp can be used automaticly on read and write
    def __init__(self):
        pass
 


def Authorisation(username, password):
    placeholder_username = "user" # placeholder to use while the file handler class is not functioning
    placeholder_password = "1234" # using username file handler will search for a file with the same name as the username then access and file in that which contains the password and then use that to check the entered password so both will have to be correct

    username_valid = False
    password_valid = False

    if(username == placeholder_username): username_valid = True # checks recived password with the password it had and username
    if(password == placeholder_password): password_valid = True

    if(username_valid and password_valid): return True
    else: return False
    

    


def main():
    #interface = Interface_Handler()
    #interface.Create_Login_Window()

    print(str(Authorisation("user","1234")))


if __name__ == "__main__":
    main()
