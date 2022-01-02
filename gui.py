import tkinter as tk
import threading

from PIL import Image, ImageTk

class ControlWindow:

    def __init__(self, window, drone, view):
        self.window = window
        self.window.title("Drone Control")
        self.panel = None

        #self.canvas = tk.Canvas(self.window, height=720, width=960)
        #self.canvas.pack()
        self.drone = drone
        self.droneview = view

        self.is_grabbing = False
        self.current_photo = None
        self.frame_grabber_thread = threading.Thread(target=self._update_frame, daemon=True)
        self.frame_grabber_thread.start()

        self.btn_connect = tk.Button(self.window, text="Connect", width=20, command=self._on_btn_connect)
        self.btn_disconnect = tk.Button(self.window, text="Disconnect", width=20, command=self._on_btn_disconnect)
        self.btn_connect.pack(anchor=tk.CENTER)
        self.btn_disconnect.pack(anchor=tk.CENTER)

        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.window.mainloop()


    def _on_btn_connect(self):
        """Starts the DroneController, its videostream,
        and turns on face detection.
        """
        self.drone.start()

        self.drone.start_video_stream()
        self.droneview.detect_faces_on()

        self.is_grabbing = True
    
    def _on_btn_disconnect(self):
        """Stops the DroneController.
        """
        self.drone.stop()
        self.droneview.detect_faces_off()

    def _update_frame(self):
        """Worker thread for grabbing images from the DroneView.
        """
        while True:
            if not self.is_grabbing:
                continue
            self.frame = self.droneview.show_drone_view()
            self.current_photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))

            if self.panel is None:
                self.panel = tk.Label(image=self.current_photo)
                self.panel.image = self.current_photo
                self.panel.pack(anchor=tk.NW)
            else:
                self.panel.configure(image=self.current_photo)
                self.panel.image = self.current_photo

            # crashes here
            # # if self.ret:
            # if self.current_photo is not None:
            #     self.canvas.create_image(0, 0, image=self.current_photo, anchor=tk.NW)

            
            # time.sleep(0.015)
    
    def _on_closing(self):
        """Called on tkinter window closing.
        """
        self._on_btn_disconnect()
        self.window.destroy()