import time
import os
from collections import deque
from .org import tangle as tangle, detangle as detangle
from watchdog.events import FileSystemEventHandler

class TimedDeque:
    def __init__(self):
        self.deque = deque()
        self.oldest_event_time = None

    def add_event(self, event) -> bool:
        """Add an event to the timed deque. If the event is already in the deque, 
        return False, otherwise return True. When False is returned, it is considered
        that the event needs to be ignored."""
        current_time = time.time()

        # remove events that are older than 5 seconds
        while self.oldest_event_time is not None and current_time - self.oldest_event_time > 5:
            self.oldest_event_time = self.deque[0][0]
            self.deque.popleft()

            # if the deque is empty, we reset the oldest event time
            if len(self.deque) == 0:
                self.oldest_event_time = None

        # check if the event is already in the deque
        for event_time, event in self.deque:
            if event == event:
                return False

        # add the event to the deque
        self.deque.append((current_time, event))

        # update the oldest event time
        if self.oldest_event_time is None:
            self.oldest_event_time = current_time

        return True

class OrgFileChangeHandler(FileSystemEventHandler):
    def __init__(self, path):    
        self.path = path
        self.queue = TimedDeque()

    def on_modified(self, event):
        if not os.path.isdir(event.src_path):
            if self.queue.add_event(event):
                folder = os.path.dirname(event.src_path).replace(self.path, '').strip('/') + '/'
                if folder == '/': folder = '.'
                if event.src_path.endswith(".org"):
                    print('File changed, tangling:', event.src_path)
                    tangle(self.path, folder, [os.path.basename(event.src_path)])
                else:
                    print('File changed, detangling:', event.src_path)
                    detangle(self.path, folder, [os.path.basename(event.src_path)])
            else:
                print('File changed, but ignored:', event.src_path)
