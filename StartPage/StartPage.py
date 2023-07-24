from tkinter import *
from pathlib import Path

# Frame for start page
class StartPage(Frame):
    """
    Frame for the start page.

    Attributes:
        OUTPUT_PATH (Path): Path to the output directory.
        ASSETS_PATH (Path): Path to the assets directory.

    Methods:
        __init__(parent, controller): Initialize the StartPage frame.
        relative_to_assets(path): Convert a relative path to an absolute path in the 'assets' directory.

    """
    
    # Constants
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    # Start page class init method
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Creating the whole canvas of the frame
        canvas = Canvas(self, bg = "#001524", height=523, width=395, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Creating the background design for start page
        self.image_bg = PhotoImage(file=self.relative_to_assets("bg.png"))
        canvas.create_image(198.0, 194.0, image=self.image_bg)

        # Creating the sign in button
        self.button_img_sign_in = PhotoImage(file=self.relative_to_assets("signin.png"))
        button_sign_in = Button(self, image=self.button_img_sign_in, borderwidth=0, highlightthickness=0,
                                command=lambda: controller.show_frame("SignInPage"), relief="flat")
        button_sign_in.place(x=117.0, y=262.0, width=162.0, height=36.0)
        
        # Creating the exit button
        self.button_img_exit = PhotoImage(file=self.relative_to_assets("exit.png"))
        button_exit = Button(self, image=self.button_img_exit, borderwidth=0, highlightthickness=0,
                               command=self.exit_program, relief="flat")
        button_exit.place(x=318.0, y=24.0, width=54.0, height=36.0)
        
        # Creating the create account button
        self.button_img_create_acc = PhotoImage(file=self.relative_to_assets("createAcc.png"))
        button_create_acc = Button(self, image=self.button_img_create_acc, borderwidth=0, highlightthickness=0,
                               command=lambda: controller.show_frame("CreateAccPage"), relief="flat")
        button_create_acc.place(x=118.0, y=298.0, width=162.0, height=36.0)



    def relative_to_assets(self, path: str) -> Path:
        """
        Convert a relative path to an absolute path in the 'assets' directory.

        Args:
            path (str): The relative path of the file.

        Returns:
            Path: The absolute path of the file in the 'assets' directory.

        """
        return self.ASSETS_PATH / Path(path)
    
    
    
    def exit_program(self):
        """
        Exit the program.

        Returns:
            None

        """
        self.quit()



