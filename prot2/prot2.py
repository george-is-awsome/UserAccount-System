from tkinter import *
import tkinter.font as font
import os
import time
import string
import sqlite3
global defaulyKey
defaultKey = 8

global directory
global dataPath
global fileDataPath
global filesPath
global userDetailsPath
global fileIndexPath

directory = os.getcwd()
if(directory.endswith("prot2")): pass # python counts execution as the script but VS code counts execution location as the parent file
else: directory = directory + "\\prot2"
defaultkey = 8
activeUsers = []

dataPath = directory + "\\data"
fileDataPath = dataPath + "\\files"
filesPath = directory + "\\files"
userDetailsPath = dataPath + "\\userDetails"
fileIndexPath = dataPath + "\\fileIndex"

class User: # main class object for a user once they log in
    def __init__(self,userID,username,password):
        self.IDnO = userID
        self.ID = username
        self.password = password

        dbcon = sqlite3.connect(userDetailsPath)
        cursor = dbcon.cursor()
        cursor.execute(F"SELECT username FROM userDetails WHERE ID='{self.ID}'")
        username = cursor.fetchone()
        self.username = username[0]

        self.auth() #  checks password against saved password to gain access while keeping all the variables inside the users class
        
    def auth(self):
        encryptedPassword = encrypt(defaultKey,self.password)
        dbCon = sqlite3.connect(userDetailsPath)
        cursor = dbCon.cursor()

        getpassword = f"SELECT password FROM userDetails where ID = {self.ID}"
        try:
            cursor.execute(getpassword)
            if(int(encryptedPassword) == int(cursor.fetchone()[0])): authstat = True
            else: authstat = False
        except: authstat = False

        self.authstat = authstat        
    
    def verify(self):
        return self.authstat
    
    def mainWindow(self):
        time.sleep(1) # for dramatic effect

        root = Tk()
        root.title(str(self.username))
        root.geometry("800x600")


        # interface window colour variables
        button_frame_background_colour = "lightgrey"
        logout_frame_background_colour = "grey"
        button_colour = "white"
        border_colour = "black"
        main_display_frame_colour = "grey"
        main_display_colour = "lightgrey"


        # widget obj def
        view_file_frame = Frame(root,width=180,height=80,bg=button_frame_background_colour)
        view_file_button = Button(root,width=22,height=4,text="view files",command=lambda:self.view_files(root,main_display_text,main_display_colour))#,command=self.view_files,bg=button_colour)

        new_file_frame = Frame(root,width=180,height=80,bg=button_frame_background_colour)
        new_file_button = Button(root,width=22,height=4,text="new file",command=lambda:self.createFiles(root),bg=button_colour)

        edit_file_frame = Frame(root,width=180,height=80,bg=button_frame_background_colour)
        edit_file_button = Button(root,width=22,height=4,text="edit files",bg=button_colour)

        delete_file_frame = Frame(root,width=180,height=80,bg=button_frame_background_colour)
        delete_file_button = Button(root,width=22,height=4,text="delete files",command=self.deleteFile)#,command=self.delete_files,bg=button_colour)

        admin_frame = Frame(root,width=180,height=80,bg=button_frame_background_colour)
        admin_button = Button(root,width=22,height=4,text="admin",command=lambda:self.adminMenu(root,main_display_text,main_display_colour),bg=button_colour)
        
        logout_frame = Frame(root,width=180,height=130,bg=logout_frame_background_colour)
        logout_button = Button(root,width=22,height=7,text="logout",command=self.logout,bg=button_colour)
       
        sidemenu_border_left = Frame(root,width=5,height=600,bg=border_colour)
        
        main_display_frame = Frame(root,width=500,height=590,bg=main_display_frame_colour)
        main_display_text = Label(root,width=69,height=38,bg=main_display_colour,text="Hello World!",anchor=NW,justify=LEFT,wraplength=65)
        
        fileview_border_right = Frame(root,width=5,height=600,bg=border_colour)
        
        # widget obj placement
        view_file_frame.place(x=10,y=10)
        view_file_button.place(x=18,y=15)# x=x+8 y=y+5

        new_file_frame.place(x=10,y=100) # +90
        new_file_button.place(x=18,y=105)

        edit_file_frame.place(x=10,y=190) # +90
        edit_file_button.place(x=18,y=195)

        delete_file_frame.place(x=10,y=280) # +90
        delete_file_button.place(x=18,y=285)

        admin_frame.place(x=10,y=370)
        admin_button.place(x=18,y=375)
        
        logout_frame.place(x=10,y=460)
        logout_button.place(x=18,y=467)

        sidemenu_border_left.place(x=200,y=0)# 520 px for main display # 5/10px border - width 510/500px

        main_display_frame.place(x=212,y=5)
        main_display_text.place(x=218,y=12)

        fileview_border_right.place(x=720,y=0)

        root.mainloop()

    def createFiles(self, root):
        try:localRoot.destory() # stops mutiple of the same window being opened
        except: pass
        localRoot = Tk() #  creates a new window 
        localRoot.title("CREATE NEW FILE")
        localRoot.geometry("250x80")

        # colour variables
        labelColour = "lightgrey"
        entryColour = "white"
        buttonColour = "white"

        # widget obj def
        entryLabel = Label(localRoot, text='Enter File Name',background=labelColour)
        fileNameEntry = Entry(localRoot, width=30,background=entryColour)
        submitButton = Button(localRoot, text='Submit',width=5,height=1,background=buttonColour,command=lambda:self.newFileFunction(root, localRoot, fileNameEntry))

        # widget obj placements
        entryLabel.place(x=5,y=8)
        fileNameEntry.place(x=5,y=30)
        submitButton.place(x=200,y=28)

        localRoot.mainloop()        

    def newFileFunction(self, root, localRoot, entry):
        valid = True
        errorText = ''
        fileName = entry.get()
        fileDirectory = f"{fileDataPath}\\{fileName}.txt"

        if(fileName == ''): #  checks if the file is an empty string
            valid = False
            errorText = "file name cannot be empty string"
        elif(os.path.exists(fileDirectory)): # checks if a file with that name already exists
            valid = False
            errorText = "A file with that name already exists"
        elif(str(fileName[0]) not in string.ascii_letters): # the first letter of the filename must be a a letter not a number
            valid = False
            errorText = "The file name cannot being with a number"
        else: 
            for character in fileName: #  checks if the file contains any special characters which cannot be a file name
                if(character not in string.ascii_letters and character not in ['1','2','3','4','5','6','7','8','9']):
                    valid = False
                    errorText = "file name cannot contain special characters"
                    break
        if(valid == False):
           errorLabel = Label(localRoot,text=errorText, fg='red') 
           errorLabel.place(x=5,y=55)
           return
        
        
        newFile = open(fileDirectory,'w+')
        newFile.close()

        dbCon = sqlite3.connect(fileIndexPath)
        cursor = dbCon.cursor()
        cursor.execute("SELECT COUNT(*) FROM fileIndex")
        id = cursor.fetchone()
        id = id[0]
        print(id)
        cursor.execute(f"INSERT INTO fileIndex(ID, fileName, author, dateCreated) VALUES('{id}','{fileName}','{self.username}','1/1/1')")
        dbCon.commit()
        dbCon.close()
        #except:
        #    print("NEW FILE - Unexpected error occoured")
        #    return

        
        outputLabel = Label(localRoot, text='File Created Successfully!', fg='green')
        outputLabel.place(x=5,y=55)
        
    def view_files(self, root, maintext, mainDisplayColour):
        local_root = Tk()
        local_root.title("Select File")
        local_root.geometry("350x400")
        basic_font =font.Font(size=32) #create font object to change the font size

        lbColour = 'lightgrey'
        borderColour = 'black'
        bFrameColour = 'lightgrey'

        instruction_label = Label(local_root,text="select a file",bd=10)
        instruction_label['font'] = basic_font
        instruction_label.pack()
        
        #  get files - search through database collect filenames where author = userID
        dbCon = sqlite3.connect(fileIndexPath)
        cursor = dbCon.cursor()
        getUserFiles = f"SELECT filename FROM fileIndex WHERE author='{self.ID}'"
        cursor.execute(getUserFiles)
        files = cursor.fetchall()
        print(files)

        for i in range(len(files)): # format file names
            file = files[i]
            file = str(file)
            file=file.replace('(','')
            file=file.replace(')','')
            file=file.replace("'",'')
            file=file.replace(',','')
            files[i] = str(file)

        listbox=Listbox(local_root,selectmode='single',width=30,bg=lbColour)
        listbox['font'] = basic_font # applies the font to the listbox object 
        for i in range(len(files)): # add files to listbox
            listbox.insert(i+1,str(files[i]))
        listbox.place(x=40,y=50)

        border = Frame(local_root,width=400,height=5,bg=borderColour)
        border.place(x=0,y=250)

        button_frame = Frame(local_root,width=330,height=130,bg=bFrameColour)
        button_frame.place(x=10,y=260)

        submit_button = Button(local_root,text="View File",width=41,height=6,command=lambda:self.view_file_submited(root,maintext,listbox,mainDisplayColour))
        submit_button.place(x=25,y=275)

    def view_file_submited(self,root,maintext,listbox,mainDisplayColour):
        entry = listbox.curselection()
        entry = listbox.get(entry)
        if(len(entry) <= 0): # checks a file has been selected
            raise ValueError("file not selected")
            return
        if(os.path.exists(fileDataPath+f"\\{entry}.txt")):
            contentFile = open(fileDataPath+f"\\{entry}.txt")
            contents = contentFile.read()
            contentFile.close()
            maintext.destroy()
            maintext = Label(root,width=69,height=38,bg=mainDisplayColour,text=str(contents),anchor=NW,justify=LEFT,wraplength=65)
            maintext.place(x=218,y=12)
        else:
            raise ValueError("File Deosnt exist")
        
    def deleteFile(self):
        local_root = Tk()
        local_root.title("delete File")
        local_root.geometry("350x400")
        basic_font =font.Font(size=32) #create font object to change the font size

        lbColour = 'lightgrey'
        borderColour = 'black'
        bFrameColour = 'lightgrey'

        #  get files - search through database collect filenames where author = userID
        dbCon = sqlite3.connect(fileIndexPath)
        cursor = dbCon.cursor()
        getUserFiles = f"SELECT filename FROM fileIndex WHERE author='{self.ID}'"
        cursor.execute(getUserFiles)
        files = cursor.fetchall()
        
        for i in range(len(files)): # format file names
            file = files[i]
            file = str(file)
            file=file.replace('(','')
            file=file.replace(')','')
            file=file.replace("'",'')
            file=file.replace(',','')
            files[i] = str(file)

        listbox=Listbox(local_root,selectmode='single',width=30,bg=lbColour)
        listbox['font'] = basic_font # applies the font to the listbox object 
        for i in range(len(files)): # add files to listbox
            listbox.insert(i+1,str(files[i]))
        listbox.place(x=40,y=50)

        instruction_label = Label(local_root,text="select a file",bd=10)
        instruction_label['font'] = basic_font
        instruction_label.pack()
        
        border = Frame(local_root,width=400,height=5,bg=borderColour)
        border.place(x=0,y=250)

        button_frame = Frame(local_root,width=330,height=130,bg=bFrameColour)
        button_frame.place(x=10,y=260)

        submit_button = Button(local_root,text="Delete File",width=41,height=6,command=lambda:self.deleteFilesFunc(listbox))
        submit_button.place(x=25,y=275)

    def deleteFilesFunc(self,listbox):
        entry = listbox.curselection()
        entry = listbox.get(entry)
        if(len(entry) <= 0):
            raise ValueError("File not selected")
            return  
        if(os.path.exists(fileDataPath+f"\\{entry}.txt")):
            os.remove(fileDataPath+f"\\{entry}.txt")

            dbCon = sqlite3.connect(fileIndexPath)
            cursor = dbCon.cursor()

            getfileid = f"SELECT ID FROM fileIndex WHERE fileName='{entry}'"
            cursor.execute(getfileid)
            fileID=cursor.fetchall()

            deleteFile = f"DELETE FROM fileIndex WHERE fileName='{entry}'"
            cursor.execute(deleteFile)

            #updateID = F"UPDATE fileIndex SET ID = ID'-1' WHERE ID>'{fileID}'"
            """ this should update the id but i dont have time to sort it out
            """
            dbCon.commit()
            dbCon.close()
        else:
            raise ValueError("File Deosnt Exist")
            return

    def logout(self):
        exit()  

    def editFile(self):
        pass
        """this is also very complicated and i ran out of time to make it work
        """

    def adminMenu(self,mainroot,maindisplay,dColour):
        dbCon = sqlite3.connect(userDetailsPath)
        cursor = dbCon.cursor()
        cursor.execute(f"SELECT admin FROM userDetails WHERE ID='{self.ID}'")
        adminValue = cursor.fetchone()
        adminValue = adminValue[0]
        if(int(adminValue) == 0):
            local_root = Tk()
            local_root.title("denied")
            local_root.geometry("100x50")
            errorLabel = Label(local_root, text="No Permission",fg='red')
            errorLabel.place(x=20,y=10)
            local_root.mainloop()
            return

        local_root = Tk()
        local_root.title("admin menu")
        local_root.geometry("350x200")

        new_user_button = Button(local_root, text='create new user',command= lambda:self.createNewUser(new_user_ID_entry,new_user_username_entry,new_user_password,new_user_permission_level, error_label)) # starts function to create new user - includes all files included in the account
        new_user_ID_entry = Entry(local_root,width=12)
        new_user_username_entry = Entry(local_root, width=12)
        new_user_password = Entry(local_root,width=12)
        new_user_permission_level = Entry(local_root,width=2)

        new_user_ID_label = Label(local_root,text='userID')
        new_user_pswd_label = Label(local_root,text='Password')
        new_user_perm_label = Label(local_root,text='Permission Level')
        new_user_username_label = Label(local_root, text='Username')
        error_label = Label(local_root, text='Details Invalid',fg='red')
        account_created_label = Label(local_root, text='Account Created',fg='green')


        new_user_ID_label.place(x=100,y=38)
        new_user_pswd_label.place(x=100,y=58)
        new_user_perm_label.place(x=40,y=80)
        new_user_username_label.place(x=100,y=100)
        new_user_ID_entry.place(x=20,y=40)
        new_user_password.place(x=20,y=60)
        new_user_permission_level.place(x=20,y=80)
        new_user_username_entry.place(x=20,y=100)
        new_user_button.place(x=20,y=10)

        delete_user_button = Button(local_root, text='delete user',command=lambda:self.deleteUser()) # delete a user account
        delete_user_button.place(x=220,y=10)

        ad_read_button = Button(local_root, text='admin view file',command=lambda:self.adminViewFiles(mainroot,maindisplay,dColour)) # view every file within the system not just files linked to the selected account
        ad_read_button.place(x=20,y=120)

        ad_delete_button = Button(local_root, text='admin delete file',command=lambda:self.adminDeleteFiles()) # delete any file within the system
        ad_delete_button.place(x=220,y=120)

    def createNewUser(self,userID,username,password,admin,error):
        #  Get values from the Entry Obj in admin menu 
        userID = int(userID.get())
        username = username.get()
        password = int(encrypt(defaultKey,password.get()))
        admin = int(admin.get())
        

        dbCon = sqlite3.connect(userDetailsPath)
        cursor = dbCon.cursor()

        # check if userID is already taken (linear Search Through list of UserIDs)
        getIDs = "SELECT ID FROM userDetails"
        cursor.execute(getIDs)
        IDList = cursor.fetchall()

        # Check if ID given is unique
        for i in range(len(IDList)):
            x=int(IDList[i][0])
            if(IDList[i][0] == userID):
                error.place(x=120,y=10)
                return 
            
        newUser = f"INSERT INTO userDetails (ID, username, password, admin, dateCreated) VALUES('{userID}','{username}','{password}','{admin}',1/1/1)"
        cursor.execute(newUser)
        dbCon.commit()
        dbCon.close()

    def deleteUser(self):
        local_root = Tk()
        local_root.title("Delete User")
        local_root.geometry("350x400")
        basic_font =font.Font(size=32) #create font object to change the font size

        lbColour = 'lightgrey'
        borderColour = 'black'
        bFrameColour = 'lightgrey'

        instruction_label = Label(local_root,text="select a User",bd=10)
        instruction_label['font'] = basic_font
        instruction_label.pack()

        dbCon = sqlite3.connect(userDetailsPath)
        cursor = dbCon.cursor()
        
        getUsersID = "SELECT ID FROM userDetails"
        cursor.execute(getUsersID)
        usersID = cursor.fetchall()
        
        getUsername ="SELECT username FROM userDetails"
        cursor.execute(getUsername)
        usernames = cursor.fetchall()

        users = []
        for i in range(len(usersID)):
            users.append([usersID[i][0],usernames[i]])

        for i in range(len(users)): # format file names
            file = users[i][1]
            file = str(file)
            file=file.replace('(','')
            file=file.replace(')','')
            file=file.replace("'",'')
            file=file.replace(',','')
            users[i][1] = str(file)

        listbox=Listbox(local_root,selectmode='single',width=30,bg=lbColour)
        listbox['font'] = basic_font # applies the font to the listbox object 
        for i in range(len(users)):
            listbox.insert(i+1,str(users[i][1]))
        listbox.place(x=40,y=50)

        border = Frame(local_root,width=400,height=5,bg=borderColour)
        border.place(x=0,y=250)

        button_frame = Frame(local_root,width=330,height=130,bg=bFrameColour)
        button_frame.place(x=10,y=260)

        submit_button = Button(local_root,text="Delete File",width=41,height=6,command=lambda:self.deleteUserFunc(listbox,users,local_root))
        submit_button.place(x=25,y=275)

    def deleteUserFunc(self,entry,users,localRoot):
        entry = entry.curselection()
        entry = entry[0]
        userID = users[entry][0] # gets userID of selected username
        dbCon = sqlite3.connect(userDetailsPath)
        cursor = dbCon.cursor()

        deleteUser = f"DELETE FROM userDetails WHERE ID='{userID}'"
        cursor.execute(deleteUser)
        dbCon.commit()
        dbCon.close()

        localRoot.destroy()

    def adminViewFiles(self,root,display,dColour):
        local_root = Tk()
        local_root.title("Admin View File")
        local_root.geometry("350x400")
        basic_font =font.Font(size=32) #create font object to change the font size

        lbColour = 'lightgrey'
        borderColour = 'black'
        bFrameColour = 'lightgrey'

        instruction_label = Label(local_root,text="select a file",bd=10)
        instruction_label['font'] = basic_font
        instruction_label.pack()
        
        #  get files - search through database collect filenames where author = userID
        dbCon = sqlite3.connect(fileIndexPath)
        cursor = dbCon.cursor()
        getUserFiles = f"SELECT filename FROM fileIndex"
        cursor.execute(getUserFiles)
        files = cursor.fetchall()
        print(files)

        for i in range(len(files)): # format file names
            file = files[i]
            file = str(file)
            file=file.replace('(','')
            file=file.replace(')','')
            file=file.replace("'",'')
            file=file.replace(',','')
            files[i] = str(file)

        listbox=Listbox(local_root,selectmode='single',width=30,bg=lbColour)
        listbox['font'] = basic_font # applies the font to the listbox object 
        for i in range(len(files)): # add files to listbox
            listbox.insert(i+1,str(files[i]))
        listbox.place(x=40,y=50)

        border = Frame(local_root,width=400,height=5,bg=borderColour)
        border.place(x=0,y=250)

        button_frame = Frame(local_root,width=330,height=130,bg=bFrameColour)
        button_frame.place(x=10,y=260)

        submit_button = Button(local_root,text="View File",width=41,height=6,command=lambda:self.view_file_submited(root,display,listbox,dColour))
        submit_button.place(x=25,y=275)

    def adminDeleteFiles(self):
        local_root = Tk()
        local_root.title("Admin Delete File")
        local_root.geometry("350x400")
        basic_font =font.Font(size=32) #create font object to change the font size

        lbColour = 'lightgrey'
        borderColour = 'black'
        bFrameColour = 'lightgrey'

        #  get files - search through database collect filenames where author = userID
        dbCon = sqlite3.connect(fileIndexPath)
        cursor = dbCon.cursor()
        getUserFiles = f"SELECT filename FROM fileIndex"
        cursor.execute(getUserFiles)
        files = cursor.fetchall()
        
        for i in range(len(files)): # format file names
            file = files[i]
            file = str(file)
            file=file.replace('(','')
            file=file.replace(')','')
            file=file.replace("'",'')
            file=file.replace(',','')
            files[i] = str(file)

        listbox=Listbox(local_root,selectmode='single',width=30,bg=lbColour)
        listbox['font'] = basic_font # applies the font to the listbox object 
        for i in range(len(files)): # add files to listbox
            listbox.insert(i+1,str(files[i]))
        listbox.place(x=40,y=50)

        instruction_label = Label(local_root,text="select a file",bd=10)
        instruction_label['font'] = basic_font
        instruction_label.pack()
        
        border = Frame(local_root,width=400,height=5,bg=borderColour)
        border.place(x=0,y=250)

        button_frame = Frame(local_root,width=330,height=130,bg=bFrameColour)
        button_frame.place(x=10,y=260)

        submit_button = Button(local_root,text="Delete File",width=41,height=6,command=lambda:self.deleteFilesFunc(listbox))
        submit_button.place(x=25,y=275)


# can be used to both encrypt and decrypt 
def encrypt(key,message): # method to encrypt a message using caeser cipher
    # list of characters that can be encrypted
    message = str(message)

    lowerAlphabet = string.ascii_lowercase
    upperAlphabet = string.ascii_uppercase
    numeric = ['1','2','3','4','5','6','7','8','9','0']
    message_lenth = len(message)

    encrypted_message = ""
    
    #iteration through diffrent characters till the correct one is found to be encrypted
    for i in range(message_lenth):
        value = 0
        newindex = 0
        if message[i] in lowerAlphabet:
            value = lowerAlphabet.index(message[i])
            newindex = (value + key) % len(lowerAlphabet)
            encrypted_message = encrypted_message + lowerAlphabet[newindex]
        elif message[i] in upperAlphabet:
            value = upperAlphabet.index(message[i])
            newindex = (value + key) % len(upperAlphabet)
            encrypted_message = encrypted_message + upperAlphabet[newindex]
        elif message[i] in numeric:
            value = numeric.index(message[i])
            newindex = (value + key) % len(numeric)
            encrypted_message = encrypted_message + numeric[newindex]
        elif message[i] == ' ':
            encrypted_message = encrypted_message + ' '
        else: # if a value that cannot be encrypyed is entered raise an error
            raise TypeError(f"couldnt find character : {message[i]} in avaliable characters")
    return encrypted_message


# USER ACCOUNT SYSTEM

def main():
    verifyFiles()
    createLoginWindow()

 
def verifyFiles():
    # set up all files that need to exist if they dont - data file and database files

    # Checks the datafile exists and if it deosnt creates a datafile in the datapath directory 
    if(os.path.exists(dataPath) and os.path.isdir(dataPath)): pass
    else:
        os.makedirs(dataPath)
        print("MAIN : dataPath not found - creating dataPath directory")

    # Checks the fileData file exists and if it deosnt creates a filedata file in the filedatapath directory 
    if(os.path.exists(fileDataPath) and os.path.isdir(fileDataPath)): pass
    else: 
        os.makedirs(fileDataPath)
        print("MAIN : fileDataPath not found - creating new fileDataPath directory")

    # Checks the file directory exists and if it deosnt creates a new file directory in the filespath directory 
    if(os.path.exists(filesPath) and os.path.isdir(filesPath)): pass
    else: 
        os.makedirs(filesPath)
        print("MAIN : filesPath not found - creating new filesPath directory")

    if(os.path.exists(userDetailsPath)): pass #  check if userDetails database exists 
    else: # create new user details database
        dbCon = sqlite3.connect(userDetailsPath)
        cursor = dbCon.cursor()

        createTable = "CREATE TABLE userDetails (ID INTEGER PRIMARY KEY, username TEXT, password INTEGER, admin INTEGER, dateCreated TEXT)"
        cursor.execute(createTable)
        defaultUser = "INSERT INTO userDetails (ID, username, password, admin, dateCreated) VALUES ('0','user','90123','1','1/1/1')"
        cursor.execute(defaultUser)
        defaultUser = "INSERT INTO userDetails (ID, username, password, admin, dateCreated) VALUES ('1','user2','90123','0','1/1/1')"
        cursor.execute(defaultUser)
        dbCon.commit()
        dbCon.close()
        print("MAIN : userDetails database not found - creating new userDetails database")

    if(os.path.exists(fileIndexPath)): pass
    else: #  create new fileindex database
        dbCon = sqlite3.connect(fileIndexPath)
        cursor = dbCon.cursor()

        createTable = "CREATE TABLE fileIndex (ID INTEGER PRIMARY KEY, filename TEXT, author TEXT, dateCreated TEXT)"
        cursor.execute(createTable)
        dbCon.close()
        print("MAIN : fileIndex database not found - creating new fileIndex database")

def createLoginWindow():
    # LOGIN WINDOW  
    # colour variables 
    frameColour = "lightgrey"
    entryColour = "white"
    labelColour = 'lightgrey'
    buttonColour = 'white'

    # tk variables
    root = Tk()
    root.title("LOGIN")
    root.geometry("300x200")
    root.maxsize(height=200,width=300)

    # tk object variables 
    backFrame = Frame(root,height=200,width=300,background=frameColour)

    usernameEntry = Entry(root,background=entryColour)
    passwordEntry = Entry(root,background=entryColour)

    usernameLabel = Label(root,text="UserID",height=1,background=labelColour)
    passwordLabel = Label(root,text="Password",height=1,background=labelColour)        
    invalid_details_label = Label(root,text="Invalid Details Entered",fg='red')
    valueErrorLabel = Label(root,text="Integer Only Values Accepted",fg='red')
    loggedInLabel = Label(root,text="Loggin Successfull", fg='green')

    submitButton = Button(root,text="Submit",height=1,width=10,background=buttonColour,command= lambda : logginTrigger(usernameEntry, passwordEntry, activeUsers, root, invalid_details_label, valueErrorLabel, loggedInLabel)) # lambda allows arguments to be passed

    # tk packaging objects
    backFrame.pack()

    usernameEntry.place(x=10,y=50)
    passwordEntry.place(x=10,y=90)

    usernameLabel.place(x=10,y=29)
    passwordLabel.place(x=10,y=69)

    submitButton.place(x=150,y=90)   

    root.mainloop()

def logginTrigger(usernameObj, passwordObj, activeUsers, root, errorLabel,valueErrorLabel,logLabel):
    errorLabel.place_forget()
    valueErrorLabel.place_forget()


    enteredUsername = usernameObj.get()
    enteredPassword = passwordObj.get()

    # check values
    try:
        enteredUsername = int(enteredUsername)
        enteredPassword = int(enteredPassword)
    except:
        print("LOGIN - non int value found in entry")
        valueErrorLabel.place(x=10,y=120)

    users = len(activeUsers) # list of all users currently logged in, tuple of name and user class instance
    user = [enteredUsername, User(users,enteredUsername,enteredPassword)] # if auth is  incorrect the user instance deletes itself
    activeUsers.append(user)

    if(user[1].verify()):
        print(f"LOGIN - {str(user[0])} logged in:")
        logLabel.place(x=10,y=160)
        user[1].mainWindow()
    else:
        errorLabel.place(x=10,y=140)


    
if __name__ == "__main__":
    main()


