import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import datetime
import os
import tkinter.messagebox

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x200")
        self.title("Smooth Camera App")
        self.label = ctk.CTkLabel(self, text="Smooth Camera App\nDeveloped by Fozan Ahmed", font=("Arial", 20, "bold"))
        self.label.pack(expand=True)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.update_idletasks()
        # Center splash
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (200 // 2)
        self.geometry(f"400x200+{x}+{y}")
        self.after(2000, self.close_splash)
        self._parent = parent

    def close_splash(self):
        self.destroy()
        if self._parent:
            self._parent.deiconify()


class CameraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smooth Camera App")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.camera_on = False
        self.cap = None
        self.frame = None
        self.imgtk = None
        self.loader = None
        self.first_frame_ready = False

        self.create_widgets()

    def create_widgets(self):
        self.video_label = ctk.CTkLabel(self, text="", width=640, height=480)
        self.video_label.pack(pady=20)

        self.loader = ctk.CTkProgressBar(self, width=200, mode="indeterminate")
        self.loader.pack(pady=10)
        self.loader.stop()
        self.loader.pack_forget()

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start Camera", command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.capture_btn = ctk.CTkButton(self.btn_frame, text="Capture", command=self.capture_image, state="disabled")
        self.capture_btn.grid(row=0, column=1, padx=10)

        self.stop_btn = ctk.CTkButton(self.btn_frame, text="Stop Camera", command=self.stop_camera, state="disabled")
        self.stop_btn.grid(row=0, column=2, padx=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Idle", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Developer credit at the bottom
        self.credit_label = ctk.CTkLabel(self, text="Developed by Fozan Ahmed", font=("Arial", 12, "italic"))
        self.credit_label.pack(side="bottom", pady=5)

    def start_camera(self):
        if not self.camera_on:
            self.cap = cv2.VideoCapture(0)
            self.camera_on = True
            self.first_frame_ready = False
            self.capture_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.start_btn.configure(state="disabled")
            self.status_label.configure(text="Status: Buffering... Please wait.")
            self.loader.pack(pady=10)
            self.loader.start()
            self.after(100, self.update_frame)

    def update_frame(self):
        if self.camera_on and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(self.frame)
                img = img.resize((640, 480))
                self.imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=self.imgtk)
                if not self.first_frame_ready:
                    self.first_frame_ready = True
                    self.loader.stop()
                    self.loader.pack_forget()
                    self.capture_btn.configure(state="normal")
                    self.status_label.configure(text="Status: Camera Started")
            self.after(15, self.update_frame)

    def capture_image(self):
        if self.frame is not None:
            img = Image.fromarray(self.frame)
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # Get user's Pictures folder
            pictures_folder = os.path.join(os.path.expanduser("~"), "Pictures")
            if not os.path.exists(pictures_folder):
                os.makedirs(pictures_folder)
            filename = os.path.join(pictures_folder, f"capture_{now}.png")
            img.save(filename)
            self.status_label.configure(text=f"Status: Image Captured ({filename})")

    def stop_camera(self):
        if self.camera_on:
            self.camera_on = False
            if self.cap:
                self.cap.release()
            self.video_label.configure(image=None)
            self.capture_btn.configure(state="disabled")
            self.stop_btn.configure(state="disabled")
            self.start_btn.configure(state="normal")
            self.status_label.configure(text="Status: Camera Stopped")
            self.loader.stop()
            self.loader.pack_forget()
            tkinter.messagebox.showinfo("About", "Developed by Fozan Ahmed in Python")


# To build an executable, install pyinstaller:
#   pip install pyinstaller
# Then run:
#   pyinstaller --onefile --noconsole --add-data "capture.png;." camera_app.py
# The .exe will be in the 'dist' folder.

if __name__ == "__main__":
    root = CameraApp()
    root.withdraw()
    splash = SplashScreen(root)
    # If splash is closed early, show main window
    def on_splash_close():
        try:
            root.deiconify()
        except:
            pass
    splash.protocol("WM_DELETE_WINDOW", on_splash_close)
    root.mainloop()
