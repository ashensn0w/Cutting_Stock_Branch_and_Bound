from tkinter import *
from pathlib import Path

# Frame for start page
class StartPage(Frame):
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
        canvas.create_image(198.0, 194.0, image=self.image_bg)

        # creating the sign in button
        self.button_imgSignIn = PhotoImage(file=self.relative_to_assets("signin.png"))
        button_Exit = Button(self, image=self.button_imgSignIn, borderwidth=0, highlightthickness=0,
                                command=lambda: controller.show_frame("SignInPage"), relief="flat")
        button_Exit.place(x=117.0, y=262.0, width=162.0, height=36.0)
        
        # creating the exit button
        self.button_imgExit = PhotoImage(file=self.relative_to_assets("exit.png"))
        button_Exit = Button(self, image=self.button_imgExit, borderwidth=0, highlightthickness=0,
                               relief="flat")
        button_Exit.place(x=318.0, y=24.0, width=54.0, height=36.0)
        
        # creating the create account button
        self.button_imgCreateAcc = PhotoImage(file=self.relative_to_assets("createAcc.png"))
        button_Exit = Button(self, image=self.button_imgCreateAcc, borderwidth=0, highlightthickness=0,
                               command=lambda: controller.show_frame("CreateAccPage"), relief="flat")
        button_Exit.place(x=118.0, y=298.0, width=162.0, height=36.0)


    # function for the right path
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)



