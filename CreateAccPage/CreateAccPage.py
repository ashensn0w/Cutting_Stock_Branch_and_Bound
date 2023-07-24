from tkinter import *
from tkinter import messagebox
from pathlib import Path
import mysql.connector


# Frame for start page
class CreateAccPage(Frame):
    # constants
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    # start page class init method
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # creating the whole canvas of the frame
        canvas = Canvas(self, bg = "#001524", height=523, width=395, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # creating the background design for start page
        self.image_bg = PhotoImage(file=self.relative_to_assets("bg.png"))
        canvas.create_image(197.0, 285.0, image=self.image_bg)
        
        # username entry
        self.username = StringVar()
        self.entry_imgUsername = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_imgUsername, bg="#E0FBFC")
        self.entry_img.place(x=37, y=195)
        self.entry_username = Entry(self, textvariable=self.username, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_username.place(x=49.0, y=197.0, width=298.0, height=50.0)
        
        # new password entry
        self.newPassword = StringVar()
        self.entry_imgNewPassword = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_imgNewPassword, bg="#E0FBFC")
        self.entry_img.place(x=37, y=278)
        self.entry_newPassword = Entry(self, textvariable=self.newPassword, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_newPassword.place(x=49.0, y=281.0, width=298.0, height=50.0)\
            
        # show new password bool
        self.isNewPassShown = BooleanVar(value=False)
        self.entry_newPassword.config(show="*")
        
        # show new password button
        self.button_imgShowNewPass = PhotoImage(file=self.relative_to_assets("showPass.png"))
        self.button_ShowNewPass = Button(self, image=self.button_imgShowNewPass, borderwidth=0, highlightthickness=0,
                                command=self.toggle_password_visibility_new_pass, relief="flat")
        self.button_ShowNewPass.place(x=329.0, y=298.0, width=18.0, height=18.0)
        
        # confirm password entry
        self.confirmPassword = StringVar()
        self.entry_imgConfirmPassword = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_imgConfirmPassword, bg="#E0FBFC")
        self.entry_img.place(x=37, y=361)
        self.entry_confirmPassword = Entry(self, textvariable=self.confirmPassword, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_confirmPassword.place(x=49.0, y=364.0, width=298.0, height=50.0)
        
        # show confirm password bool
        self.isConfirmPassShown = BooleanVar(value=False)
        self.entry_confirmPassword.config(show="*")
        
        # show confirm password button
        self.button_imgShowConfirmPass = PhotoImage(file=self.relative_to_assets("showPass.png"))
        self.button_ShowConfirmPass = Button(self, image=self.button_imgShowConfirmPass, borderwidth=0, highlightthickness=0,
                                command=self.toggle_password_visibility_confirm_pass, relief="flat")
        self.button_ShowConfirmPass.place(x=329.0, y=381.0, width=18.0, height=18.0)
        
        # create account button
        self.button_imgCreateAcc = PhotoImage(file=self.relative_to_assets("createAcc.png"))
        button_CreateAcc = Button(self, image=self.button_imgCreateAcc, borderwidth=0, highlightthickness=0,
                               command=lambda: self.create_account(controller), relief="flat")
        button_CreateAcc.place(x=117.0, y=441.0, width=162.0, height=36.0)
        
        # creating the back button
        self.button_imgBack = PhotoImage(file=self.relative_to_assets("back.png"))
        button_Exit = Button(self, image=self.button_imgBack, borderwidth=0, highlightthickness=0,
                               command=lambda: controller.show_frame("StartPage"), relief="flat")
        button_Exit.place(x=34.0, y=22.0, width=26.0, height=25.0)



    # function for the right path
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    # Function to establish the database connection
    def establish_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="daa"
            )
            return connection
        except mysql.connector.Error as error:
            print("Error while connecting to MySQL", error)
            return None

    def username_exists(self, username):
        connection = self.establish_db_connection()
        if connection is None:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return False

        try:
            cursor = connection.cursor()
            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            return len(result) > 0
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error checking username existence: {error}")
            return False

    def create_account(self, controller):
        username = self.username.get()
        password = self.newPassword.get()
        confirm_password = self.confirmPassword.get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Check if username already exists
        if self.username_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return

        # Establish database connection
        connection = self.establish_db_connection()
        if connection is None:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        try:
            # Insert account information into the database
            cursor = connection.cursor()
            insert_query = "INSERT INTO accounts (username, password) VALUES (%s, %s)"
            data = (username, password)
            cursor.execute(insert_query, data)
            connection.commit()
            cursor.close()

            messagebox.showinfo("Success", "Account created and saved successfully!")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error saving account: {error}")
        finally:
            connection.close()
            controller.show_frame("SignInPage")

    def toggle_password_visibility_new_pass(self):
        # Get the current show password state
        current_state = self.isNewPassShown.get()

        if current_state:
            # If the password is currently shown, hide it
            self.entry_newPassword.config(show="*")
            self.isNewPassShown.set(False)
            self.button_imgShowNewPass = PhotoImage(file=self.relative_to_assets("showPass.png"))
            self.button_ShowNewPass.config(image=self.button_imgShowNewPass)
            
        else:
            # If the password is currently hidden, show it
            self.entry_newPassword.config(show="")
            self.isNewPassShown.set(True)
            self.button_imgHideNewPass = PhotoImage(file=self.relative_to_assets("hidePass.png"))
            self.button_ShowNewPass.config(image=self.button_imgHideNewPass)

    def toggle_password_visibility_confirm_pass(self):
        # Get the current show password state
        current_state = self.isConfirmPassShown.get()

        if current_state:
            # If the password is currently shown, hide it
            self.entry_confirmPassword.config(show="*")
            self.isConfirmPassShown.set(False)
            self.button_imgShowConfirmPass = PhotoImage(file=self.relative_to_assets("showPass.png"))
            self.button_ShowConfirmPass.config(image=self.button_imgShowConfirmPass)
            
        else:
            # If the password is currently hidden, show it
            self.entry_confirmPassword.config(show="")
            self.isConfirmPassShown.set(True)
            self.button_imgHideConfirmPass = PhotoImage(file=self.relative_to_assets("hidePass.png"))
            self.button_ShowConfirmPass.config(image=self.button_imgHideConfirmPass)


