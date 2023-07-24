from tkinter import *
from tkinter import messagebox
from pathlib import Path
import mysql.connector
import bcrypt


# Frame for start page
class SignInPage(Frame):
    """
    Frame for the sign-in page.

    Attributes:
        OUTPUT_PATH (Path): Path to the output directory.
        ASSETS_PATH (Path): Path to the assets directory.
        username (StringVar): Variable to store the username entered by the user.
        password (StringVar): Variable to store the password entered by the user.
        show_password (BooleanVar): Boolean variable to store the state of password visibility.

    Methods:
        __init__(parent, controller): Initialize the SignInPage frame.
        relative_to_assets(path): Convert a relative path to an absolute path in the 'assets' directory.
        toggle_password_visibility(): Toggle password visibility on button click.
        login(controller): Handle login process when the sign-in button is clicked.

    """
    
    # constants
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Whole canvas of the frame
        canvas = Canvas(self, bg = "#001524", height=523, width=395, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Background design for the page
        self.image_bg = PhotoImage(file=self.relative_to_assets("bg.png"))
        canvas.create_image(197.0, 285.0, image=self.image_bg)
        
        # Username entry
        self.username = StringVar()
        self.entry_img_username = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_img_username, bg="#E0FBFC")
        self.entry_img.place(x=37, y=223)
        self.entry_Name = Entry(self, textvariable=self.username, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_Name.place(x=49.0, y=226.0, width=298.0, height=50.0)
        
        # Password entry
        self.password = StringVar()
        self.entry_img_pssword = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_img_pssword, bg="#E0FBFC")
        self.entry_img.place(x=37, y=315)
        self.entry_password = Entry(self, textvariable=self.password, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_password.place(x=49.0, y=317.0, width=298.0, height=50.0)
        
        # Show password state variable
        self.show_password = BooleanVar(value=False)
        self.entry_password.config(show="*")

        # Show password button
        self.button_img_show_pass = PhotoImage(file=self.relative_to_assets("showPass.png"))
        self.show_pass_button = Button(self, image=self.button_img_show_pass, borderwidth=0, highlightthickness=0,
                                       command=self.toggle_password_visibility, relief="flat")
        self.show_pass_button.place(x=327.0, y=334.0, width=18.0, height=18.0)
        
        # Sign in account button
        self.button_imgSignIn = PhotoImage(file=self.relative_to_assets("signIn.png"))
        button_SignIn = Button(self, image=self.button_imgSignIn, borderwidth=0, highlightthickness=0,
                               command=lambda: self.login(controller), relief="flat")
        button_SignIn.place(x=117.0, y=408.0, width=162.0, height=36.0)
        
        # Back button
        self.button_imgBack = PhotoImage(file=self.relative_to_assets("back.png"))
        button_back = Button(self, image=self.button_imgBack, borderwidth=0, highlightthickness=0,
                               command=lambda: controller.show_frame("StartPage"), relief="flat")
        button_back.place(x=34.0, y=22.0, width=26.0, height=25.0)




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
        Establishes a connection to the MySQL database.

        Returns:
            mysql.connector.connection.MySQLConnection or None: A connection object if successful, None if there was an error.

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



    def toggle_password_visibility(self):
        """
        Toggles the visibility of the password in the password entry field.

        """
        
        # Get the current show password state
        current_state = self.show_password.get()

        if current_state:
            # If the password is currently shown, hide it
            self.entry_password.config(show="*")
            self.show_password.set(False)
            self.button_img_show_pass = PhotoImage(file=self.relative_to_assets("showPass.png"))
            self.show_pass_button.config(image=self.button_img_show_pass)
            
        else:
            # If the password is currently hidden, show it
            self.entry_password.config(show="")
            self.show_password.set(True)
            self.button_imgHidePass = PhotoImage(file=self.relative_to_assets("hidePass.png"))
            self.show_pass_button.config(image=self.button_imgHidePass)



    def login(self, controller):
        """
        Handle the login process when the sign-in button is clicked.

        Args:
            controller: The controller to manage frame switching.

        """
        
        username = self.username.get()
        password = self.password.get()

        # Establish database connection
        connection = self.establish_db_connection()
        if connection is None:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        try:
            # Check if the username exists in the database
            cursor = connection.cursor()
            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchall()

            if not result:
                messagebox.showerror("Error", "Username does not exist.")
                cursor.close()
                return

            # Get the hashed password from the result
            stored_password = result[0][1].encode("utf-8")

            # Verify the password using bcrypt
            if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                # Passwords match, login successful
                messagebox.showinfo("Success", "Login successful!")
                cursor.close()
                controller.show_frame("ComputeCutsPage", username)
            else:
                # Incorrect password
                messagebox.showerror("Error", "Incorrect password.")
                cursor.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error during login: {error}")
        finally:
            connection.close()

