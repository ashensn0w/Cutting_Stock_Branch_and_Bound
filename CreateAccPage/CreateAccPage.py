from tkinter import *
from tkinter import messagebox
from pathlib import Path
import mysql.connector
import bcrypt



class CreateAccPage(Frame):
    """
    Frame for the create account page.

    Attributes:
        OUTPUT_PATH (Path): Path to the output directory.
        ASSETS_PATH (Path): Path to the assets directory.
        username (StringVar): Variable to store the username entered by the user.
        new_password (StringVar): Variable to store the new password entered by the user.
        confirm_password (StringVar): Variable to store the confirm password entered by the user.
        is_new_pass_shown (BooleanVar): Boolean variable to store the state of new password visibility.
        is_confirm_pass_shown (BooleanVar): Boolean variable to store the state of confirm password visibility.

    Methods:
        __init__(parent, controller): Initialize the CreateAccPage frame.
        relative_to_assets(path): Return the path relative to the assets directory.
        toggle_password_visibility_new_pass(): Toggle new password visibility on button click.
        toggle_password_visibility_confirm_pass(): Toggle confirm password visibility on button click.
        create_account(controller): Handle account creation when the create account button is clicked.

    """
    
    # constants
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        canvas = Canvas(self, bg = "#001524", height=523, width=395, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Fame background
        self.image_bg = PhotoImage(file=self.relative_to_assets("bg.png"))
        canvas.create_image(197.0, 285.0, image=self.image_bg)
        
        # Back button
        self.button_img_back = PhotoImage(file=self.relative_to_assets("back.png"))
        button_Exit = Button(self, image=self.button_img_back, borderwidth=0, highlightthickness=0,
                               command=lambda: controller.show_frame("StartPage"), relief="flat")
        button_Exit.place(x=34.0, y=22.0, width=26.0, height=25.0)
        
        # Username entry
        self.username = StringVar()
        self.entry_img_username = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_img_username, bg="#E0FBFC")
        self.entry_img.place(x=37, y=195)
        self.entry_username = Entry(self, textvariable=self.username, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_username.place(x=49.0, y=197.0, width=298.0, height=50.0)
        
        # New password entry
        self.new_password = StringVar()
        self.entry_img_new_password = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_img_new_password, bg="#E0FBFC")
        self.entry_img.place(x=37, y=278)
        self.entry_new_password = Entry(self, textvariable=self.new_password, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_new_password.place(x=49.0, y=281.0, width=298.0, height=50.0)\
            
        # Show new password button
        self.is_new_pass_shown = BooleanVar(value=False)
        self.entry_new_password.config(show="*")
        self.button_img_show_new_pass = PhotoImage(file=self.relative_to_assets("showPass.png"))
        self.button_show_new_pass = Button(self, image=self.button_img_show_new_pass, borderwidth=0, highlightthickness=0,
                                command=self.toggle_password_visibility_new_pass, relief="flat")
        self.button_show_new_pass.place(x=329.0, y=298.0, width=18.0, height=18.0)
        
        # Confirm password entry
        self.confirm_password = StringVar()
        self.entry_img_confirm_password = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_img_confirm_password, bg="#E0FBFC")
        self.entry_img.place(x=37, y=361)
        self.entry_confirm_password = Entry(self, textvariable=self.confirm_password, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_confirm_password.place(x=49.0, y=364.0, width=298.0, height=50.0)
        
        # Show confirm password button
        self.is_confirm_pass_shown = BooleanVar(value=False)
        self.entry_confirm_password.config(show="*")
        self.button_img_show_confirm_pass = PhotoImage(file=self.relative_to_assets("showPass.png"))
        self.button_show_confirm_pass = Button(self, image=self.button_img_show_confirm_pass, borderwidth=0, highlightthickness=0,
                                command=self.toggle_password_visibility_confirm_pass, relief="flat")
        self.button_show_confirm_pass.place(x=329.0, y=381.0, width=18.0, height=18.0)
        
        # Create account button
        self.button_img_create_acc = PhotoImage(file=self.relative_to_assets("createAcc.png"))
        button_create_acc = Button(self, image=self.button_img_create_acc, borderwidth=0, highlightthickness=0,
                               command=lambda: self.create_account(controller), relief="flat")
        button_create_acc.place(x=117.0, y=441.0, width=162.0, height=36.0)
        
        
        
        
        
        
        
    def relative_to_assets(self, path: str) -> Path:
        """
        Convert a relative path to an absolute path in the 'assets' directory.

        Args:
            path (str): The relative path of the file.

        Returns:
            Path: The absolute path of the file in the 'assets' directory.

        """
        return self.ASSETS_PATH / Path(path)



    def establish_db_connection(self):
        """
        Establish a connection to the MySQL database.

        Returns:
            mysql.connector.connection.MySQLConnection or None: The database connection or None if connection fails.

        """
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
        """
        Check if the given username already exists in the database.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.

        """
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
        """
        Create a new user account and save it in the database.

        Args:
            controller: The controller to manage frame switching.

        """
        username = self.username.get()
        password = self.new_password.get()
        confirm_password = self.confirm_password.get()

        # Check if any of the required fields are empty
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled.")
            return
    
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
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Insert account information into the database
            cursor = connection.cursor()
            insert_query = "INSERT INTO accounts (username, password) VALUES (%s, %s)"
            data = (username, hashed_password.decode("utf-8"))  # Convert bytes to string for database insertion
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
        """
        Toggle the visibility of the new password entry.

        """
        
        # Get the current show password state
        current_state = self.is_new_pass_shown.get()

        if current_state:
            # If the password is currently shown, hide it
            self.entry_new_password.config(show="*")
            self.is_new_pass_shown.set(False)
            self.button_img_show_new_pass = PhotoImage(file=self.relative_to_assets("showPass.png"))
            self.button_show_new_pass.config(image=self.button_img_show_new_pass)
            
        else:
            # If the password is currently hidden, show it
            self.entry_new_password.config(show="")
            self.is_new_pass_shown.set(True)
            self.button_imgHideNewPass = PhotoImage(file=self.relative_to_assets("hidePass.png"))
            self.button_show_new_pass.config(image=self.button_imgHideNewPass)



    def toggle_password_visibility_confirm_pass(self):
        """
        Toggle the visibility of the confirm password entry.

        """
        # Get the current show password state
        current_state = self.is_confirm_pass_shown.get()

        if current_state:
            # If the password is currently shown, hide it
            self.entry_confirm_password.config(show="*")
            self.is_confirm_pass_shown.set(False)
            self.button_img_show_confirm_pass = PhotoImage(file=self.relative_to_assets("showPass.png"))
            self.button_show_confirm_pass.config(image=self.button_img_show_confirm_pass)
            
        else:
            # If the password is currently hidden, show it
            self.entry_confirm_password.config(show="")
            self.is_confirm_pass_shown.set(True)
            self.button_imgHideConfirmPass = PhotoImage(file=self.relative_to_assets("hidePass.png"))
            self.button_show_confirm_pass.config(image=self.button_imgHideConfirmPass)


