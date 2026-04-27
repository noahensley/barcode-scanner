from cv_utils import device_init,show_live_frame,capture_images,get_px_rows

N_PIXEL_ROWS = 3
N_IMAGES = 3

def run():
    print("Initializing video device...",end="")
    dev = device_init()
    print("DONE")

    print("Initializing live feed...",end="")
    (x1,y1),(x2,y2) = show_live_frame(device=dev)
    print("DONE")

    print("Capturing images...",end="")
    images = capture_images(dev,rpos=((x1,y1),(x2,y2)),n=N_IMAGES)
    print("DONE")

    print(f"Selecting {N_PIXEL_ROWS} pixel rows...")
    rows = get_px_rows(images[0], n=N_PIXEL_ROWS)
    print("DONE")
    print(rows)

if __name__ == "__main__":
    run()