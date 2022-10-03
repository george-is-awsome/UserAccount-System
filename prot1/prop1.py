from tkinter import *
import os
from time import sleep 

global directory
global account_directory
directory = os.getcwd() # gets directory of python file using the os library
account_directory = directory + "\\Accounts"
# Interface Classes

###################################################################################################################################################

class Interface_Handler: # class to create all interfaces
    def __init__(self): # Window_Present options 1 - 3 to create diffrent windows
        self.name = self

    ######################################################################################

    def Create_Login_Window(self):
        self.root = Tk()
        root = self.root # create local scope of self.root for convenience

        root.title("Login")      # defines type of window then begins construction of the interface window 
        root.geometry("300x200")
        # creates objects to display in window
        username_input = Entry(root)
        password_input = Entry(root,show="*")


        self.username_input = username_input
        self.password_input = password_input

        username_label = Label(root,text="Username",height=1)
        password_label = Label(root,text="Password",height=1)

        submit_button = Button(root,text="submit",height=1,width=10,command=self.Collect_Entry_Data)
        # when pressed the button will send data to a class method to collect the user input and then call an auth method to validate if the entry is correct
        # constructs objects in the window
        username_input.place(x=10,y=50)
        password_input.place(x=10,y=90)

        username_label.place(x=10,y=29)
        password_label.place(x=10,y=69)

        submit_button.place(x=150,y=90)

    ######################################################################################

    def Collect_Entry_Data(self): # collects data from Entry Objects 
        username_input = self.username_input.get() # uses built in get() function to return the string entered on the object 
        password_input = self.password_input.get()

        local_file_handler = File_Handler()
        try: local_file_handler.get_password(username_input)
        except ValueError as e:
            print(e)

    ######################################################################################

###################################################################################################################################################


class File_Handler: # class to handle how to read and write to files - deosnt need to be a class but encryp/decryp can be used automaticly on read and write
    def __init__(self):
        self.accounts_directory = directory + "\\accounts" # standardised location to store login details

        account_file_exists = self.check_file_exists("Accounts",directory,folder=1) # 1 = searching for directory not a regular file
        if(account_file_exists == False): # create an account file if one has not been found at the standard directory
            print("File Handler : Account Directory not found, creating new Account Directory--")
            try: self.create_accounts_file()
            except ValueError as e:
                print(e)
            print("File Handler : Account Directory Created Successfully")

        

    ######################################################################################

    def check_file_exists(self,file_name,root_directory, **kwargs): # all round method to check existance of files 
        # file or folder = (0/1) 0 = file 1 = folder
        file_or_folder = kwargs.get('folder',0)
        

        file_exists = os.path.exists(root_directory+"\\"+file_name) # uses os to check if the selected file exists in a given directory
        file_is_directory = os.path.isdir(root_directory+"\\"+file_name) # bool to store if the selected file is a regular file or a directory

        print("file_exists :"+str(file_exists)+"\nfile_is_directory :"+str(file_is_directory)+"\nfile_or_folder : " + str(file_or_folder)) # DEBUG

        if(file_exists and file_or_folder==0): return True # return true if file exists and is searching for a regular file
        elif (file_exists and file_is_directory and file_or_folder==1): return True # return true if file exists and is searching for a directory (folder)
        else: return False # if desired file is not found

        

    ######################################################################################

    def create_accounts_file(self): # used for new directory area to create a new account data directory if one deonst already exist
        if(self.check_file_exists("Accounts",directory)): # checks if there is already a file called "Accounts" to avoid errors
            raise ValueError("ERROR : A File Called Accounts Already Exists in\n " + directory)
            return False

        try: # avoid error in creating file incase anything unexpected happens with file creation 
            path = directory + "\\Accounts"
            os.mkdir(path)
        except:
            return False

        return True # represents the successfull creation of the account directory

    def get_password(self,username):
        username = username+'.txt'
        if(self.check_file_exists(username,account_directory)):
            user_file = open(directory+'\\'+username)
            
        else:
            raise ValueError("ERROR : No Account Found With The Username : " + str(username))
        

    ######################################################################################

    # def get files

    # def open file

    # def edit file

    # def delete file

    # def delect account

    # def add account
    
        
###################################################################################################################################################

def Authorisation(username, password):
    placeholder_username = "user" # placeholder to use while the file handler class is not functioning
    placeholder_password = "1234" # using username file handler will search for a file with the same name as the username then access and file in that which contains the password and then use that to check the entered password so both will have to be correct

    username_valid = False
    password_valid = False

    if(username == placeholder_username): username_valid = True # checks recived password with the password it had and username
    if(password == placeholder_password): password_valid = True

    if(username_valid and password_valid): return True
    else: return False
    

###################################################################################################################################################



def main():


    file_handler = File_Handler()
    
    interface = Interface_Handler()
    interface.Create_Login_Window()

###################################################################################################################################################


if __name__ == "__main__":
    main()
