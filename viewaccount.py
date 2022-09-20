import wx
from dialogs import row_builder


class ViewDialog(wx.Dialog):

    def __init__(self, title="View"):
        """Constructor"""
        super().__init__(None, title="%s Accounts" % title)

        # create the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        author_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create some widgets
        size = (400, 300)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        title_lbl = wx.StaticText(self, label="Number of profiles :", size=size)
        title_lbl.SetFont(font)
        self.title_txt = wx.TextCtrl(self, value="1")
        main_sizer.Add(row_builder([title_lbl, self.title_txt]),
                       0, wx.ALL)

        cancel_btn = wx.Button(self, label="Close")
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_register)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizerAndFit(main_sizer)

    def on_register(self):
        """
        Edit a record in the database
        """
        # author_dict, book_dict = self.get_data()
        # combo_dict = {**author_dict, **book_dict}
        # # controller.edit_record(self.session, self.selected_row.id, combo_dict)
        # show_message("Book Edited Successfully!", "Success",
        #              wx.ICON_INFORMATION)
        self.Close()