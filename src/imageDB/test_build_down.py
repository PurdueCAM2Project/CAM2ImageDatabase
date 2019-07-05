from routine_no_down import Routine
import time

def build_up_test():
    # Keep retrieving images from camera
    print("\nInitializing Connection...")
    example = Routine()
    print("Finished connection intialization... ELAPSED: ", time.perf_counter())

    print("\n Start retrieveImage...")
    example.retrieveImage(threshold=0.9, max_fps=10, store_interval=0.1, num_of_cams=5)

build_up_test()
