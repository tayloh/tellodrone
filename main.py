
from drone import DroneController, DroneView

drone = DroneController()
view = DroneView(drone)

def main():
    global drone, view
    drone.start()
    drone.start_video_stream()
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
        drone.stop()
        view.exit_view()
        print("Exiting with error.")
        print(e)