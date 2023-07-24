from tkinter import *
from pathlib import Path
import mysql.connector
from CuttingStockSolver import CuttingStockSolver
from tkinter import font, messagebox, filedialog
from datetime import datetime


# Frame for start page
class ComputeCutsPage(Frame):
    # constants
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    # start page class init method
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # creating the whole canvas of the frame
        canvas = Canvas(self, bg="#001524", height=523, width=395, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # creating the background design for start page
        self.image_bg = PhotoImage(file=self.relative_to_assets("bg.png"))
        canvas.create_image(197.0, 301.0, image=self.image_bg)

        # Get the font style and size from the input widget
        input_font = font.Font(family="Roboto", size=10)

        # Sign Out button
        self.button_imgSignOut = PhotoImage(file=self.relative_to_assets("signOut.png"))
        button_SignOut = Button(self, image=self.button_imgSignOut, borderwidth=0, highlightthickness=0,
                                command=lambda: controller.show_frame("StartPage"), relief="flat")
        button_SignOut.place(x=35.0, y=25.0, width=77.0, height=22.0)
        
        # Download history.txt button
        self.button_imgDownloadHistory = PhotoImage(file=self.relative_to_assets("history.png"))
        button_DownloadHistory = Button(self, image=self.button_imgDownloadHistory, borderwidth=0, highlightthickness=0, 
                                        command=lambda: self.download_history(controller.username), relief="flat")
        button_DownloadHistory.place(x=277.0, y=25.0, width=88.0, height=22.0)

        # stock length entry
        self.stock_length = StringVar()
        self.entry_imgStockLength = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_imgStockLength, bg="#E0FBFC")
        self.entry_img.place(x=36, y=183)
        self.entry_stock_length = Entry(self, textvariable=self.stock_length, bd=0, bg="#98C1D9", fg="#000716",
                                        highlightthickness=0)
        self.entry_stock_length.place(x=48.0, y=186.0, width=298.0, height=50.0)
        self.entry_stock_length.config(font=input_font)

        # length of items
        self.items_length = StringVar()
        self.placeholder_text = "e.g 2 5 4 6"
        self.items_length.set(self.placeholder_text)
        self.entry_imgItemLength = PhotoImage(file=self.relative_to_assets("entry.png"))
        self.entry_img = Label(self, image=self.entry_imgItemLength, bg="#E0FBFC")
        self.entry_img.place(x=36, y=267)
        self.entry_itemLength = Entry(self, textvariable=self.items_length, bd=0, bg="#98C1D9", fg="#000716",
                                      highlightthickness=0)
        self.entry_itemLength.place(x=48.0, y=270.0, width=298.0, height=50.0)
        self.entry_itemLength.config(font=input_font)

        # Bind the event handlers to the Entry widget
        self.entry_itemLength.bind("<FocusIn>", self.on_itemLength_entry_click)
        self.entry_itemLength.bind("<FocusOut>", self.on_itemLength_focus_out)
        self.set_entry_text_color()

        # generate cuts button
        self.button_imgGenerateCuts = PhotoImage(file=self.relative_to_assets("genCuts.png"))
        button_GenerateCuts = Button(self, image=self.button_imgGenerateCuts, borderwidth=0, highlightthickness=0,
                                     command=lambda: self.generate_cuts(controller.username), relief="flat")
        button_GenerateCuts.place(x=115.0, y=336.0, width=162.0, height=36.0)

        # Output
        self.output = StringVar()
        self.entry_imgOutput = PhotoImage(file=self.relative_to_assets("entry_Big.png"))
        self.entry_img = Label(self, image=self.entry_imgOutput, bg="#E0FBFC")
        self.entry_img.place(x=35, y=401)
        self.entry_output = Text(self, bd=0, bg="#98C1D9", fg="#000716", highlightthickness=0)
        self.entry_output.place(x=47.0, y=404.0, width=298.0, height=80.0)
        self.entry_output.config(font=input_font)

    # function for the right path
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    # Event handler to clear the placeholder text when the user starts typing
    def on_itemLength_entry_click(self, event):
        if self.items_length.get() == self.placeholder_text:
            self.items_length.set("")
            self.set_entry_text_color()

    def on_itemLength_focus_out(self, event):
        if self.items_length.get() == "":
            self.items_length.set(self.placeholder_text)
            self.set_entry_text_color()

    # Custom function to set the text color dynamically
    def set_entry_text_color(self):
        if self.items_length.get() == self.placeholder_text:
            self.entry_itemLength.config(fg="#5C6B6B")  # Placeholder color
        else:
            self.entry_itemLength.config(fg="#000716")  # User input color

    def generate_cuts(self, username):
        try:
            # Split the input string into a list of integers
            items_input = [int(x) for x in self.items_length.get().split(" ")]

            # Convert items_input list into a dictionary where the key is the index and the value is the item value
            items_dict = {index: value for index, value in enumerate(items_input)}

            problem = CuttingStockSolver(self.stock_length.get(), items_dict)
            problem.branch_and_bound_solve()

            # Get the solution as a string
            solution_str = problem.print_solution()

            # Disable the entry_output widget to prevent user input
            self.entry_output.config(state="normal")

            # Clear the previous content and set the solution to the output Text widget
            self.entry_output.delete(1.0, "end")
            self.entry_output.insert("insert", solution_str)

            # Insert the truncated_solution along with the current date and time into the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="daa"
            )

            cursor = connection.cursor()
            insert_query = "INSERT INTO history (entry, username, entry_date) VALUES (%s, %s, %s)"

            solution_str = f"Stock Length: {self.stock_length.get()}\n" + solution_str

            # Get the current date and time in the format "YYYY-MM-DD HH:MM:SS"
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(insert_query, (solution_str, username, current_datetime))
            connection.commit()

            connection.close()

        except ValueError:
            # Show a pop-up error message if a non-integer value is entered
            messagebox.showerror("Invalid Input", "Please enter integers separated by spaces.")
            # Clear the entry_itemLength widget
            self.items_length.set(self.placeholder_text)
            self.set_entry_text_color()
        
    def download_history(self, username):
        try:
            # Connect to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="daa"
            )

            cursor = connection.cursor()

            # Fetch all entries and entry dates from the database associated with the logged-in username
            select_query = "SELECT entry, entry_date FROM history WHERE username = %s"
            cursor.execute(select_query, (username,))
            entries = cursor.fetchall()

            connection.close()

            if not entries:
                # Display a message box if there are no entries for the given username
                messagebox.showinfo("No History Found", f"No history found for {username}.")
            else:
                # Display a file dialog to save the history.txt file
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="history.txt",
                                                        title="Save History", initialdir=".")
                if file_path:
                    with open(file_path, "w") as file:
                        for entry, entry_date in entries:
                            file.write(f"Date: {entry_date}\n")
                            file.write(entry)
                            file.write("\n\n")  # Separate each entry with two newlines

                    # Show a success message
                    messagebox.showinfo("History Downloaded", f"History for {username} has been downloaded to {file_path}")

        except mysql.connector.Error as err:
            # Show an error message if there's an issue with the database connection
            messagebox.showerror("Database Error", f"Error accessing the database: {err}")