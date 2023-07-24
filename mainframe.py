import sys
from tkinter import *
from StartPage.StartPage import StartPage
from SignInPage.SignInPage import SignInPage
from CreateAccPage.CreateAccPage import CreateAccPage
from ComputeCutsPage.ComputeCutsPage import ComputeCutsPage


class MainFrame(Tk):
    """
    Main application window class derived from the Tk class.

    Attributes:
        container (Frame): A container to hold frames for different pages.

    Methods:
        __init__(*args, **kwargs): Initialize the main window.
        show_frame(page_name, username=None): Show the given frame with the specified page name.

    """
    
    def __init__(self, *args, **kwargs):
        # Initialize the main window
        Tk.__init__(self, *args, **kwargs)
        self.geometry("395x523")
        self.resizable(False, False)

         # Create a container to hold frames for different pages
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Show the start page initially
        self.show_frame("StartPage")
        
         
    def show_frame(self, page_name, username=None):
        """
        Show the given frame with the specified page name.

        Args:
            page_name (str): The name of the frame to be shown.
            username (str): The username to be passed to the frame.

        """
        
        self.username = username

        # Get the frame class dynamically using the page_name
        f = getattr(sys.modules[__name__], page_name)

        # Create an instance of the frame
        frame = f(self.container, self)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.tkraise()


# Initialize the main window app
window = MainFrame()
window.title("Cutting Stock Converter")
window.mainloop()