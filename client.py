import abc
from abc import ABC, abstractmethod

import pyhula
from modules.tflite_detector import tflite_detector
from modules.hula_video import hula_video

import threading, queue

class PostProcessor(ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __call__(self, frame):
        pass

class PostProcessors:
    def __init__(self):
        self.Google_IMDA = self.Google_IMDA()

    class Google_IMDA(PostProcessor):
        def __init__(self):
            self.detector = tflite_detector(
                r'.\assets\model1.tflite',
                r'.\assets\label.txt',
            )

        def __call__(self, frame):
            return self.detector.detect(frame)
PostProcessors = PostProcessors()

class Client(pyhula.UserApi):
    def __init__(self, activate_video:bool = True):
        super().__init__()
        assert self.connect(), 'Failed to connect'
        print(f'[Status] Battery: {self.get_battery()}%')

        #Initialise the video stream
        if activate_video:
            self.video = hula_video(
                hula_api = self,
                display = False
            )
            self.video.video_mode_on()
            self.video.startrecording()

        #Defining variables on the status of the runtime
        self.running = False
        self.height_data = None

    def get_frame(self, *postprocessors:PostProcessor):
        frame = self.video.get_video()
        results = {}
        for postprocessor in postprocessors:
            coords, frame = postprocessor(frame)
            results[postprocessor] = coords
        return frame, results

    def single_fly_takeoff(self, *args, **kwargs):
        self.running = True
        super().single_fly_takeoff(*args, **kwargs)

    def listen_height(self):
        self.height_data = []
        while self.running:
            self.height_data.append(self.get_plane_distance())

    def show_height_data(self):
        assert self.height_data is not None, 'No height data'

        import matplotlib.pyplot as plt
        plt.title('Height Data')
        counter = 0
        for i in self.height_data:
            plt.scatter(counter, i, s = 100)
            counter += 1
        plt.show()

class WorkerThread:
    def __init__(self, function:callable):
        self.function = function
        self.thread = threading.Thread(target = self.worker)
        self.running = threading.Event()
        self.output = queue.Queue()

    def worker(self):
        while not self.running.is_set():
            result = self.function()
            print(result)
            self.output.put(result)

        print("Ending Thread")

    def start(self):
        self.running.clear()
        self.thread.start()

    def stop(self):
        self.running.set()
        self.thread.join()
        results = []
        print("Started getting resutls")
        while not self.output.empty():
            results.append(self.output.get())
        return results
