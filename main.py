
from drone import DroneController, DroneView

def main():
    quadcopter = DroneController()
    quadcopter.start()
    quadcopter.start_video_stream()
    
    view = DroneView(quadcopter)
    view.detect_faces_on()

    while True:
        view.show_drone_view()
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exiting program...")
        print(e)