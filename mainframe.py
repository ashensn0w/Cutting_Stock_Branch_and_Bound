import sys
from tkinter import *
from StartPage.StartPage import StartPage
from SignInPage.SignInPage import SignInPage
from CreateAccPage.CreateAccPage import CreateAccPage
from ComputeCutsPage.ComputeCutsPage import ComputeCutsPage

# class for the main frame
class MainFrame(Tk):
    # init method of the class Mainframe
    def __init__(self, *args, **kwargs):
        # init method of the tk class
        Tk.__init__(self, *args, **kwargs)

        # setting the default screen size
        self.geometry("395x523")
        self.resizable(False, False)

        # creating a container for all
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # calling the first screen
        self.show_frame("StartPage")
        
        
     # showing the current frame above everything
    def show_frame(self, page_name, username=None):
        self.username = username

        # converting the page_name str into class
        f = getattr(sys.modules[__name__], page_name)

        # raising a specific frame
        frame = f(self.container, self)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.tkraise()


# initialize main window app
window = MainFrame()
window.title("Cutting Stock Converter")
window.mainloop()