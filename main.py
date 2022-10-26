import ctypes
import wx
from mainpanel import MainPanel


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title="Kijiji Manager", size=(800, 600))
        panel = MainPanel(self)

        # Устанавливаем иконку
        self.SetIcon(wx.Icon("icon.ico"))
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class GenApp(wx.App):

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    app = GenApp()
    app.MainLoop()
