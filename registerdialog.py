import wx
import resultevent
from helper import row_builder, show_message
from registerthread import RegisterThread
from wx.lib.pubsub import pub


# from ipchanger import IPChanger


class RegisterDialog(wx.Dialog):

    def __init__(self, config, proxy, main_sheet, title="Register"):
        """Constructor"""
        style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.RESIZE_BORDER) & (~wx.MINIMIZE_BOX)
        super().__init__(None, title="%s Accounts" % title, style=style)
        self.proxy = proxy
        self.Centre()

        self.config = config
        self.main_sheet = main_sheet

        self.ID_START = wx.NewId()
        self.ID_STOP = wx.NewId()

        self.num_profiles = None

        size = (-1, -1)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        # author_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.count = 0
        self.progress = wx.Gauge(self, range=100)
        # self.progress.Hide()
        # pub.subscribe(self.updateProgress, "update")
        self.main_sizer.Add(self.progress, 0, wx.CENTER | wx.ALL, 10)

        # font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.title_lbl = wx.StaticText(self, label="Number of Profiles :", size=size)
        # self.title_lbl.SetFont(font)
        self.title_txt = wx.TextCtrl(self, value="1", size=(65, -1))
        self.main_sizer.Add(row_builder([self.title_lbl, self.title_txt], 10),
                            0, wx.ALL)

        self.register_btn = wx.Button(self, self.ID_START, label="Register")
        self.register_btn.Bind(wx.EVT_BUTTON, self.on_register, id=self.ID_START)

        self.cancel_btn = wx.Button(self, self.ID_START, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel, id=self.ID_START)

        btn_sizer.Add(self.register_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.cancel_btn, 0, wx.ALL, 5)

        # self.status = wx.StaticText(self, -1, '', pos=(0, 100))
        self.status = wx.StaticText(self, -1, '')
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizerAndFit(self.main_sizer)

        resultevent.EVT_RESULT(self, self.on_result)

        self.worker = None

    def update_progress(self, msg):
        self.count += 10

        if self.count >= (int(self.num_profiles) * 100):
            self.Destroy()
            show_message(f"{self.num_profiles} profile(s) has/have been registered!", 'Success', wx.ICON_INFORMATION)

        self.progress.SetValue(self.count)

    def on_register(self, event):
        if not self.worker:
            # self.status.SetLabel('Starting computation')

            # Делаем кнопку Register неактивной
            self.register_btn.Disable()

            # Разрушаем текст и окно ввода количества акков
            self.num_profiles = self.title_txt.GetValue()
            self.title_txt.Destroy()
            self.title_lbl.Destroy()

            self.status.SetLabel('Registering...')
            self.status.SetPosition((int(self.GetSize()[0] / 2) - int(self.status.GetSize()[0] / 2), 40))
            self.main_sizer.Add(self.status, 0, wx.CENTER, 5)

            # Запускаем поток регистрации
            self.worker = RegisterThread(self, self.config, self.num_profiles, self.proxy, self.main_sheet)
            try:  # Перехват исключения не работает
                self.worker.start()
            except Exception as e:
                show_message(str(e), 'Error')
                self.Destroy()

            self.progress.Show()
            self.progress.SetRange((int(self.num_profiles)) * 100)
            pub.subscribe(self.update_progress, "update")
            # self.main_sizer.Add(self.progress, 0, wx.CENTER, 5)

    def on_cancel(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker:
            # self.status.SetPosition((70, 40))
            self.status.SetLabel('Canceling...')
            self.status.SetPosition((int(self.GetSize()[0] / 2) - int(self.status.GetSize()[0] / 2), 40))
            self.worker.abort()
            self.cancel_btn.Disable()
        else:
            self.Destroy()

    def on_result(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            # self.status.SetLabel('Computation aborted')
            self.Destroy()
        else:
            # Process results here
            self.status.SetLabel('Computation Result: %s' % event.data)
        # In either event, the worker is done
        self.worker = None
