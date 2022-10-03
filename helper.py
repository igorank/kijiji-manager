import wx


def show_message(message, caption, flag=wx.ICON_ERROR):
    """
    Show a message dialog
    """
    msg = wx.MessageDialog(None, message=message,
                           caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()


def row_builder(widgets, lbl_border=5):
    """
    Helper function for building a row of widgets
    """
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    lbl, txt = widgets
    sizer.Add(lbl, 0, wx.ALL, lbl_border)
    sizer.Add(txt, 1, wx.ALL, 5)
    return sizer

