import wx


def show_message(message, caption, flag=wx.ICON_ERROR):
    """
    Show a message dialog
    """
    msg = wx.MessageDialog(None, message=message,
                           caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()


def row_builder(widgets):
    """
    Helper function for building a row of widgets
    """
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    lbl, txt = widgets
    sizer.Add(lbl, 0, wx.ALL, 5)
    sizer.Add(txt, 1, wx.ALL, 5)
    return sizer


class RecordDialog(wx.Dialog):
    """
    Add / Modify Record dialog
    """

    def __init__(self, row=None, title="Add", addRecord=True):
        """Constructor"""
        super().__init__(None, title="%s Ad" % title)
        self.addRecord = addRecord
        self.selected_row = row
        if row:
            email = self.selected_row.email
            kijiji_pass = self.selected_row.kijiji_pass
            email_pass = self.selected_row.email_pass
            imap_pass = self.selected_row.imap_pass
            forwarding = self.selected_row.forwarding
            useragent = self.selected_row.useragent
        else:
            email = kijiji_pass = email_pass = imap_pass = forwarding = useragent = ""

        # create the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        author_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create some widgets
        size = (90, -1)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        title_lbl = wx.StaticText(self, label="Title:", size=size)
        title_lbl.SetFont(font)
        self.title_txt = wx.TextCtrl(self, value=email)
        main_sizer.Add(row_builder([title_lbl, self.title_txt]),
                       0, wx.ALL)

        author_lbl = wx.StaticText(self, label="Description:", size=size)
        author_lbl.SetFont(font)
        author_sizer.Add(author_lbl, 0, wx.ALL, 5)
        self.author_first_txt = wx.TextCtrl(self, value=kijiji_pass, size=(300, -1), style=wx.TE_MULTILINE)
        author_sizer.Add(self.author_first_txt, 1, wx.ALL, 5)
        # self.author_last_txt = wx.TextCtrl(self, value=email_pass)
        # author_sizer.Add(self.author_last_txt, 1, wx.ALL, 5)
        main_sizer.Add(author_sizer, 0, wx.ALL)

        isbn_lbl = wx.StaticText(self, label="Price:", size=size)
        isbn_lbl.SetFont(font)
        self.isbn_txt = wx.TextCtrl(self, value=imap_pass)
        main_sizer.Add(row_builder([isbn_lbl, self.isbn_txt]),
                       0, wx.ALL)

        publisher_lbl = wx.StaticText(self, label="Postal code:", size=size)
        publisher_lbl.SetFont(font)
        self.publisher_txt = wx.TextCtrl(self, value=forwarding)
        main_sizer.Add(row_builder([publisher_lbl, self.publisher_txt]),
                       0, wx.ALL)

        address_lbl = wx.StaticText(self, label="Full Address:", size=size)
        address_lbl.SetFont(font)
        self.address_txt = wx.TextCtrl(self, value=imap_pass)
        main_sizer.Add(row_builder([address_lbl, self.address_txt]),
                       0, wx.ALL)

        ok_btn = wx.Button(self, label="%s Ad" % title)
        ok_btn.Bind(wx.EVT_BUTTON, self.on_record)
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        cancel_btn = wx.Button(self, label="Close")
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizerAndFit(main_sizer)

    def get_data(self):
        """
        Gets the data from the widgets in the dialog
        Also display an error message if required fields
        are empty
        """
        author_dict = {}
        book_dict = {}

        fName = self.author_first_txt.GetValue()
        lName = self.author_last_txt.GetValue()
        title = self.title_txt.GetValue()
        isbn = self.isbn_txt.GetValue()
        publisher = self.publisher_txt.GetValue()

        if fName == "" or title == "":
            show_message("Author and Title are Required!",
                         "Error")
            return None, None

        if "-" in isbn:
            isbn = isbn.replace("-", "")
        author_dict["first_name"] = fName
        author_dict["last_name"] = lName
        book_dict["title"] = title
        book_dict["isbn"] = isbn
        book_dict["publisher"] = publisher

        return author_dict, book_dict

    def on_edit(self):
        """
        Edit a record in the database
        """
        author_dict, book_dict = self.get_data()
        combo_dict = {**author_dict, **book_dict}
        # controller.edit_record(self.session, self.selected_row.id, combo_dict)
        show_message("Book Edited Successfully!", "Success",
                     wx.ICON_INFORMATION)
        self.Close()

    def on_add(self):
        """
        Add the record to the database
        """
        author_dict, book_dict = self.get_data()
        if author_dict is None or book_dict is None:
            return

        data = ({"author": author_dict, "book": book_dict})
        # controller.add_record(self.session, data)

        # show dialog upon completion
        show_message("Book Added",
                     "Success!", wx.ICON_INFORMATION)

        # clear dialog so we can add another book
        for child in self.GetChildren():
            if isinstance(child, wx.TextCtrl):
                child.SetValue("")

    def on_close(self, event):
        """
        Close the dialog
        """
        self.Close()

    def on_record(self, event):
        """
        Add or edit a record
        """
        if self.addRecord:
            self.on_add()
        else:
            self.on_edit()
        self.title_txt.SetFocus()
