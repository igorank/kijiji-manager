import time
from threading import *
import wx
import resultevent


class ResultEvent(wx.PyEvent):

    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(resultevent.EVT_RESULT_ID)
        self.data = data


class WorkerThread(Thread):
    # def __init__(self, notify_window, num):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # self.num = num
        self.start()

    def run(self):
        """Run Worker Thread."""
        for i in range(10):
            time.sleep(1)
            print(i)
            if self._want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            wx.PostEvent(self._notify_window, ResultEvent(10))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
