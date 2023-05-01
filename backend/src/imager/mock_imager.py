from time import sleep


class MockImager():
    def __init__(self):
        pass


    def run_image_acquisition(self, path):
        print(f"saving to {path}")
        for i in range(10):
            sleep(0.2)
            print(f"saving image {i}")

