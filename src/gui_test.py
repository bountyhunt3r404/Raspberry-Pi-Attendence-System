import customtkinter

#######################################---GUI---########################################
customtkinter.set_appearance_mode("Dark")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Attendance System")
        self.geometry(f"{1024}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        
        #Main Heading
        self.heading_pict = self.CTkLabel(self, text="PICT ATTENDANCE SYSTEM", text_color="white", height=50, corner_radius=20,
                      font=("Helvetica", 30, "bold"))
        self.heading_pict.grid_configure(sticky="ew", ipadx=0, ipady=0, columnspan=3)

if __name__ == "__main__":
    app = App()
    app.mainloop()