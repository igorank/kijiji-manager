import wx
from ObjectListView import ObjectListView, ColumnDefn
from gsheet import GSheet


class Account(object):

    def __init__(self, email, kijiji_pass, email_pass, imap_pass, forwarding, useragent):
        self.email = email
        self.kijiji_pass = kijiji_pass
        self.email_pass = email_pass
        self.imap_pass = imap_pass
        self.forwarding = forwarding
        self.useragent = useragent


def show_message(message, caption, flag=wx.ICON_ERROR):
    """
    Show a message dialog
    """
    msg = wx.MessageDialog(None, message=message,
                           caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()


class PostAdsPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        gsheets = GSheet("1gO3m2DJmO6Lwf27Wjustop9eyik9TGO5_9MeJZbetP0", "kijiji-362509-c751d3f68ea1.json")
        self.main_sheet = gsheets.get_main_worksheet(0)
        list_of_hashes = self.main_sheet.get_all_records()
        self.data = []
        for i in list_of_hashes:
            self.data.append(Account(i['Email'], i['Kijiji password'], i['Email Password'], i['IMAP password'],
                                     i['Forwarding'], i['Useragent']))

        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        # self.dataOlv.SetEmptyListMsg("No Records Found")
        self.setData()
        # Allow the cell values to be edited when double-clicked
        # self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK

        # create an update button
        updateBtn = wx.Button(self, wx.ID_ANY, "Update")
        updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)

        # create an edit button
        edit_record_btn = wx.Button(self, label="Edit")
        edit_record_btn.Bind(wx.EVT_BUTTON, self.edit_record)
        btn_sizer.Add(edit_record_btn, 0, wx.ALL, 5)

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(updateBtn, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)

    def edit_record(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        if selected_row is None:
            show_message('No row selected!', 'Error')
            return

        # with dialogs.RecordDialog(self.session,
        #                           selected_row,
        #                           title='Modify',
        #                           addRecord=False) as dlg:
        #     dlg.ShowModal()

        # self.show_all_records()

    def updateControl(self, event):
        # product_dict = [{"email": "Core Python Programming", "author": "Wesley Chun",
        #                  "isbn": "0132269937", "mfg": "Prentice Hall"},
        #                 {"email": "Python Programming for the Absolute Beginner",
        #                  "author": "Michael Dawson", "isbn": "1598631128",
        #                  "mfg": "Course Technology"},
        #                 {"email": "Learning Python", "author": "Mark Lutz",
        #                  "isbn": "0596513984", "mfg": "O'Reilly"}]
        list_of_hashes = self.main_sheet.get_all_records()


        # data = self.data + product_dict
        self.data = []
        for i in list_of_hashes:
            self.data.append(Account(i['Email'], i['Kijiji password'], i['Email Password'], i['IMAP password'],
                                     i['Forwarding'], i['Useragent']))

        self.dataOlv.SetObjects(self.data)

    def setData(self, data=None):
        self.dataOlv.SetColumns([
            ColumnDefn("Email", "left", -1, "email"),
            ColumnDefn("Kijiji password", "left", -1, "kijiji_pass"),
            ColumnDefn("Email Password", "left", -1, "email_pass"),
            ColumnDefn("IMAP password", "left", -1, "imap_pass"),
            ColumnDefn("Forwarding", "left", -1, "forwarding"),
            ColumnDefn("Useragent", "left", -1, "useragent")
        ])

        self.dataOlv.SetObjects(self.data)
