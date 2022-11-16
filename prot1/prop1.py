from tkinter import *
import tkinter.font as font
import os
from time import sleep 

"""
Problems 
- new file function adds file name to index if the file has successfuly been created or not so when opening a file you are given the option to open files that do not exist
- fix new file function - deosnt update index correctly skips line and doenst update the counter 
"""

"""
ideas
- add external databases for more efficency
- add a sync file button to clear all files from index.txt that no longer exist
"""

"""
todo
- finish encryption system
- 
"""



# Interface Classes

class Interface_Handler: # class to create all interfaces
    def __init__(self): # Window_Present options 1 - 3 to create diffrent windows
        self.name = self
        self.username = ''
        self.local_directory = ''
        self.Create_Login_Window()
        #self.Create_Main_Window('user') # DEBUG

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

        submit_button = Button(root,text="submit",height=1,width=10,command=self.entry_auth)
        invalid_details_label = Label(root,text="Invalid Details Entered",fg='red')
        self.invalid_details_label = invalid_details_label
        # when pressed the button will send data to a class method to collect the user input and then call an auth method to validate if the entry is correct
        # constructs objects in the window
        username_input.place(x=10,y=50)
        password_input.place(x=10,y=90)

        username_label.place(x=10,y=29)
        password_label.place(x=10,y=69)

        submit_button.place(x=150,y=90)    

    def entry_auth(self): # collects data from Entry Objects 
        username_input = self.username_input.get() # uses built in get() function to return the string entered on the object 
        password_input = self.password_input.get()

        auth = Authorisation(username_input,password_input) # bool representing if pass and user are correct
        if(auth == False): self.invalid_details_label.place(x=10,y=120) # places invalid details label onto the login window
        else:
            self.root.destroy()
            self.Create_Main_Window(username_input)

    def Create_Main_Window(self,username):
        self.username = username
        self.local_directory = account_directory + '\\' + self.username
        self.root = Tk()
        self.file_handler = File_Handler()
        root = self.root # create local scope
            
        root.title(str(username))
        root.geometry("800x600")

        # side menu - main_menu.png
        # - view files
        # - new files
        # - edit files
        # - delete files
        # -
        # - admin (option)
        # - logout

        # logout ##########
        view_file_frame = Frame(root,width=180,height=80,bg='lightgrey')
        view_file_button = Button(root,width=22,height=4,text="view files",command=self.view_files)
        view_file_frame.place(x=10,y=10)
        view_file_button.place(x=18,y=15)# x=x+8 y=y+5

        new_file_frame = Frame(root,width=180,height=80,bg='lightgrey')
        new_file_button = Button(root,width=22,height=4,text="new file",command=self.new_file)
        new_file_frame.place(x=10,y=100) # +90
        new_file_button.place(x=18,y=105)

        edit_file_frame = Frame(root,width=180,height=80,bg='lightgrey')
        edit_file_button = Button(root,width=22,height=4,text="edit files")
        edit_file_frame.place(x=10,y=190) # +90
        edit_file_button.place(x=18,y=195)

        delete_file_frame = Frame(root,width=180,height=80,bg='lightgrey')
        delete_file_button = Button(root,width=22,height=4,text="delete files",command=self.delete_files)
        delete_file_frame.place(x=10,y=280) # +90
        delete_file_button.place(x=18,y=285)

        admin_frame = Frame(root,width=180,height=80,bg='lightgrey')
        admin_button = Button(root,width=22,height=4,text="admin",command=self.admin_menu)
        admin_frame.place(x=10,y=370)
        admin_button.place(x=18,y=375)
        
        logout_frame = Frame(root,width=180,height=130,bg='grey')
        logout_button = Button(root,width=22,height=7,text="logout",command=self.logout)
        logout_frame.place(x=10,y=460)
        logout_button.place(x=18,y=467)
        ########

        sidemenu_border_left = Frame(root,width=5,height=600,bg='black')
        sidemenu_border_left.place(x=200,y=0)# 520 px for main display # 5/10px border - width 510/500px


        main_display_frame = Frame(root,width=500,height=590,bg='grey')
        main_display_frame.place(x=212,y=5)
        self.main_display_text = Label(root,width=69,height=38,bg='lightgrey',text="Hello World!",anchor=NW,justify=LEFT,wraplength=65) # Might be able to turn this into a class in the future 
        self.main_display_text.place(x=218,y=12)

        fileview_border_right = Frame(root,width=5,height=600,bg='black')
        fileview_border_right.place(x=720,y=0)

        pageup_button = Button(root,width=8,height=12,text="Page Up",bg='lightgrey')
        pageup_button.place(x=728,y=80)

        pagedown_button = Button(root,width=8,height=12,text="Page Down",bg='lightgrey')
        pagedown_button.place(x=728,y=320)

        root.mainloop()

    def logout(self):
        #print("logout : logout function executed") # DEBUG
        self.root.destroy()
        #self.Create_Login_Window()
        exit() # DEBUG

    def view_files(self):
        local_root = Tk()
        local_root.title("Select File")
        local_root.geometry("350x400")
        basic_font =font.Font(size=32) #create font object to change the font size
        
        instruction_label = Label(local_root,text="select a file",bd=10)
        instruction_label['font'] = basic_font
        instruction_label.pack()

        files = self.file_handler.get_user_files(self.username) # returns string array of all files assosiated with the account
        self.listbox=Listbox(local_root,selectmode='single',width=30,bg='lightgrey') # raises the scope of this variable so it can be used throughout the class
        listbox = self.listbox
        listbox['font'] = basic_font # applies the font to the listbox object 
        for i in range(len(files)):
            print(str(i)+" : "+str(files[i]))
            listbox.insert(i+1,str(files[i]))
        listbox.place(x=40,y=50)

        border = Frame(local_root,width=400,height=5,bg='black')
        border.place(x=0,y=250)

        button_frame = Frame(local_root,width=330,height=130,bg='lightgrey')
        button_frame.place(x=10,y=260)

        submit_button = Button(local_root,text="View File",width=41,height=6,command=self.view_file_submited)
        submit_button.place(x=25,y=275)

    def view_file_submited(self):
        entry = self.listbox.curselection() # stores string of file selected
        data_directory = self.local_directory+'\\data'
        if(len(entry) > 0): # checks a file has been selected
            print("entry : "+str(self.listbox.get(entry))) # list box to show all the files 
            selected_file= self.listbox.get(entry)
            if(self.file_handler.check_file_exists(selected_file,data_directory)): # checks the file exist to avoid errors
                data_file = open(data_directory+'\\'+selected_file)
                data = data_file.read()
                data_file.close()
                self.main_display_text.destroy()
                self.main_display_text = Label(self.root,width=69,height=38,bg='lightgrey',text=data,anchor=NW,justify=LEFT,wraplength=480)
                self.main_display_text.place(x=218,y=12)
                
    def new_file(self):
        local_root=Tk()

        local_root.title("new file")
        local_root.geometry("250x70")

        enter_label = Label(local_root,text='Enter File Name')
        enter_label.place(x=5,y=8)

        self.file_name_input = Entry(local_root,width=30)
        self.file_name_input.place(x=5,y=30)

        submit = Button(local_root,width=5,text='submit',height=1,command=self.create_new_file)
        submit.place(x=200,y=28)

    def create_new_file(self):
        file_name = self.file_name_input.get()
        new_file = open(account_directory+'\\'+self.username+'\\data\\'+file_name+'.txt','a') # creates a new file in the data directory of the users file
        new_file.close()
        self.file_handler.add_new_file_to_index(self.username,file_name) # adds the new file to the index of the user

    def delete_files(self):
        local_root = Tk()

        local_root.title("delete File")
        local_root.geometry("400x600")

    def admin_menu(self): # admin unitlie menu - need to add auth to use 
        local_root = Tk()

        local_root.title("admin menu")
        local_root.geometry("400x600")

        new_user_button = Button(local_root, text='create new user',command=self.new_user) # starts function to create new user - includes all files included in the account#
        self.new_user_name_entry = Entry(local_root,width=12)
        self.new_user_password = Entry(local_root,width=12)
        self.new_user_permission_level = Entry(local_root,width=2)

        new_user_name_label = Label(local_root,text='Username')
        new_user_pswd_label = Label(local_root,text='Password')
        new_user_perm_label = Label(local_root,text='Permission Level')
        self.error_label = Label(local_root, text='Details Invalid',fg='red')
        self.account_created_label = Label(local_root, text='Account Created',fg='green')


        new_user_name_label.place(x=100,y=38)
        new_user_pswd_label.place(x=100,y=58)
        new_user_perm_label.place(x=40,y=80)
        self.new_user_name_entry.place(x=20,y=40)
        self.new_user_password.place(x=20,y=60)
        self.new_user_permission_level.place(x=20,y=80)
        new_user_button.place(x=20,y=10)

        delete_user_button = Button(local_root, text='delete user') # delete a user account
        delete_user_button.place(x=220,y=10)

        ad_read_button = Button(local_root, text='admin view file') # view every file within the system not just files linked to the selected account
        ad_read_button.place(x=20,y=120)

        ad_delete_button = Button(local_root, text='admin delete file') # delete any file within the system
        ad_delete_button.place(x=220,y=120)

    def new_user(self):
        name_entry = self.new_user_name_entry.get()
        perm_entry = self.new_user_permission_level.get()
        pswd_entry = self.new_user_password.get() # gets variable values from all entry entities
        #self.file_handler.create_new_user(name_entry,perm_entry)

        if(name_entry == '' or pswd_entry == '' or perm_entry == ''): # checks for null values to avoid errors and accidental misclicks
            self.error_label.place(x=20,y=99)       
        else:
            if (self.file_handler.create_new_user(name_entry,pswd_entry,perm_entry)):
                self.account_created_label.place(x=20,y=99)
            else: 
                self.error_label.place(x=20,y=99)


        
    

class File_Handler: # class to handle how to read and write to files - deosnt need to be a class but encryp/decryp can be used automaticly on read and write
    def __init__(self):
        self.accounts_directory = directory + "\\accounts" # standardised location to store login details
        self.file_start_line_number = 5
        account_file_exists = self.check_file_exists("Accounts",directory,folder=1) # 1 = searching for directory not a regular file
        if(account_file_exists == False): # create an account file if one has not been found at the standard directory
            print("File Handler : Account Directory not found, creating new Account Directory--")
            try: self.create_accounts_file()
            except ValueError as e:
                print(e)
            print("File Handler : Account Directory Created Successfully")

    def check_file_exists(self,file_name,root_directory, **kwargs): # all round method to check existance of files 
        # file or folder = (0/1) 0 = file 1 = folder
        file_or_folder = kwargs.get('folder',0)
        

        file_exists = os.path.exists(root_directory+"\\"+file_name) # uses os to check if the selected file exists in a given directory
        file_is_directory = os.path.isdir(root_directory+"\\"+file_name) # bool to store if the selected file is a regular file or a directory

        print("file_exists :"+str(file_exists)+"\nfile_is_directory :"+str(file_is_directory)+"\nfile_or_folder : " + str(file_or_folder)) # DEBUG

        if(file_exists and file_or_folder==0): return True # return true if file exists and is searching for a regular file
        elif (file_exists and file_is_directory and file_or_folder==1): return True # return true if file exists and is searching for a directory (folder)
        else: return False # if desired file is not found

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

    def get_password(self,username): # get password from user data file
        #print("get_password : username : "+str(username)+"\nget_password : account_directory : "+str(account_directory)) # DEBUG
        if(self.check_file_exists(username,account_directory,file_or_folder=1)): # confirms the given username has an account (file)
            #print("get_password : username : "+str(username)+"\nget_password : account_directory : "+str(account_directory)) # DEBUG
            user_file = open(account_directory+'\\'+username+'\\index.txt','r') # opens username data file
            user_password = user_file.readline()
            print("get password : "+str(user_password)) # DEBUG
            #print("get_password : user_password : " + str(user_password)) # DEBUG
            user_file.close()
            return user_password
            
        else:
            raise ValueError("ERROR : No Account Found With The Username : " + str(username))

    def get_user_files(self,username):
        files = []
        user_file = open(account_directory+"\\"+username+'\\index.txt','r') # opens account index which lists the files linked to the account (avoids having to search through the data folder listing all the files found)
        line_count = 1
        end_of_file = False
        while end_of_file == False:
            file = user_file.readline()
            #print(str(line_count)+" : "+str(file)) # DEBUG
            if(line_count > self.file_start_line_number): # loop to skip non data lines in the index to then read the file data and store the names in an array
                if len(file) > 0:
                    file = file.replace('\n','')
                    files.append(file)
                    line_count += 1
                else: end_of_file = True
            else: line_count += 1
        user_file.close()
        
        for i in range(len(files)):
            print("user files - "+str (files[i-1]+" | length - ")+str(len(files[i-1]))) # DEBUG
        return files
            
    def add_new_file_to_index(self,username,filename):
        account_file = open(account_directory + '\\' + username +'\\index.txt','r')
        file = []
        for i in range(4): 
            line = account_file.readline()
            file.append(line)
        next_index=account_file.readline()
        file.append(next_index)
        next_index = next_index.replace('\\n','')
        for i in range(int(next_index)):
            line = account_file.readline()
            file.append(line)
        account_file.close()

        account_file = open(account_directory + '\\' + username+'\\index.txt','a')
        #for i in range(len(file)): account_file.write(file[i])
        account_file.write('\n'+filename)
        account_file.close

    def create_new_user(self,username,password,permission_level):
        # permission_level = 0 - standard | 1 = admin
        # create user directory
        # create index.txt
        # create data directory
        # create activity directory
        # config index.txt
            # pswd
        
        try: # statement to create a directory in accounts for the new user
            path = account_directory + '\\' + username
            os.mkdir(path)
        except:
            print('Create New User : Unable to create new directory for -username-')
            return False

        active_directory = account_directory + '\\' + username # variable with path to the new directory for QOL 

        index_file = open(active_directory+'\\index.txt','w') # write all data to the index.txt file
        index_file.write(str(password))
        index_file.write(str(permission_level))
        index_file.writelines('\n\n\n')
        index_file.write('0')

        try: # creates the data and activity dir - Try loop to avoid error incase files already exists 
            data_path = active_directory + '\\data'
            activity_path = active_directory + '\\activity'

            os.mkdir(data_path)
            os.mkdir(activity_path)
        except:
            print('Create New User : Unable to create new directory for -data & activity-')
            return False

        return True

    def encrypt(self,decrypted_string): # encrypt any value given to it
        for i in range(len(decrypted_string)):
            character = decrypted_string[i]
            


    def decrypt(self,encrypted_string): # decrypt any value given to it
        pass


    def encrypt_table(self,encrypt_or_decrypt,character):
        # this could be turned into an external database
        # true = encrypt 
        # false = decrypt
        """  number conversion
        0 = 9
        1 = 8
        2 = 7
        3 = 6
        4 = 5
        5 = 7
        3 = 8
        2 = 9
        1 = 0
        """
        """ character conversion
        a=11
        b=12
        c=13
        d=14
        e=15
        f=16
        g=17
        h=18
        i=19
        j=20
        k=21
        l=22
        m=23
        n=24
        o=25
        p=26
        q=27
        r=28
        s=29
        t=30
        u=31
        v=32
        w=33
        x=34
        y=35
        z=36
        """

        if(encrypt_or_decrypt == True): # encryption
            character_array = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,45,35,36]
            number_array = [9,8,7,6,5,4,3,2,1,0]
            unciode_start_value = 97 # value to take away from unciode values to match index of character arrays

            try: character = character_array[ord(character-unciode_start_value)] # conversion for string - if character is an int an error will happen escaping to the except which will run the int conversion
            except:
                try: character = number_array[character]
                except: 
                    print("Encrypt table : Unable to encrypt character") 
                    raise ValueError("Encrypt Table : unable to encrypt character")

        if(encrypt_or_decrypt == False): # decryption,
            character_array = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            
        


        return character


    """        
    # def get files

    # def open file

    # def edit file

    # def delete file

    # def delect account

    # def add account
    """


def Authorisation(username, password):
    #placeholder_username = "user" # placeholder to use while the file handler class is not functioning
    #placeholder_password = "1234" # using username file handler will search for a file with the same name as the username then access and file in that which contains the password and then use that to check the entered password so both will have to be correct

    username_valid = False
    password_valid = False

    
    local_file_handler = File_Handler()
    try: user_password = local_file_handler.get_password(username) # gets password from user datafile
    except ValueError as e:
        print(e)
        return False

    #if(username == placeholder_username): username_valid = True # checks recived password with the password it had and username
    # username check not valid as it is done while getting the user password - if username is not valid auth returns false
    # password checked with will only be with the password of the username so it stays secure

    
    if(int(password) == int(user_password)): password_valid = True
    print("password : "+str(user_password)+"\nentered password : "+str(password),"\npassword valid : "+str(password_valid)) # DEBUG
    if(password_valid): return True
    else: return False

def start():
    interface = Interface_Handler()

def main():

    global directory
    global account_directory

    directory = os.getcwd() # gets directory of python file using the os library
    if (directory.endswith('prot1') == False): directory = directory + '\\prot1'
    account_directory = directory + "\\Accounts"

    main_root = Tk()
    main_root.geometry('100x100')
    main_root.title("Main")
    start_button = Button(main_root, text='start',width=5,height=2,command=start)
    start_button.place(x=35,y=30)
    main_root.mainloop()

if __name__ == "__main__":
    print("Hello World") # DEBUG
    main()
