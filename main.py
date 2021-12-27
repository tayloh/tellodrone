
from drone import DroneController, DroneView

def main():
    drone = DroneController()
    drone.start()
    drone.start_video_stream()
    
    view = DroneView(drone)
    view.detect_faces_on()

    while True:
        _ = view.show_drone_view()

        if drone.get_drone_telemetry().battery < 10:
            drone.stop()
            view.exit_view()
            break
            
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exiting with error.")
        print(e)