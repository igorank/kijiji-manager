import wx
import dialogs
from viewprofile import ViewDialog
from registerdialog import RegisterDialog
from ObjectListView import ObjectListView, ColumnDefn
from gsheet import GSheet


class Account(object):

    def __init__(self, user_id, email, kijiji_pass, email_pass, imap_pass, forwarding, token):
        self.user_id = user_id
        self.email = email
        self.kijiji_pass = kijiji_pass
        self.email_pass = email_pass
        self.imap_pass = imap_pass
        self.forwarding = forwarding
        self.token = token


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        gsheets = GSheet("1gO3m2DJmO6Lwf27Wjustop9eyik9TGO5_9MeJZbetP0", "kijiji-362509-c751d3f68ea1.json")
        self.main_sheet = gsheets.get_main_worksheet(0)
        list_of_hashes = self.main_sheet.get_all_records()
        self.data = []
        for i in list_of_hashes:
            self.data.append(Account(i['User ID'], i['Email'], i['Kijiji password'], i['Email Password'], i['IMAP password'],
                                     i['Forwarding to'], i['Token']))

        self.dataOlv = ObjectListView(self, wx.ID_ANY, sortable=False, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        # self.dataOlv.SetEmptyListMsg("No Records Found")
        self.setData()
        for i in range(7):
            print(self.dataOlv.GetColumnWidth(i))
        # Allow the cell values to be edited when double/single-clicked
        # self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        # self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK

        # create an register button
        registerBtn = wx.Button(self, wx.ID_ANY, "Register")
        registerBtn.Bind(wx.EVT_BUTTON, self.registerControl)
        btn_sizer.Add(registerBtn, 0, wx.ALL, 5)

        # create delete button
        deleteBtn = wx.Button(self, wx.ID_ANY, "Delete")
        deleteBtn.Bind(wx.EVT_BUTTON, self.deleteControl)
        btn_sizer.Add(deleteBtn, 0, wx.ALL, 5)

        # create an update button
        updateBtn = wx.Button(self, wx.ID_ANY, "Update")
        updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)
        btn_sizer.Add(updateBtn, 0, wx.ALL, 5)

        # create an update button
        ViewBtn = wx.Button(self, wx.ID_ANY, "View Profile")
        ViewBtn.Bind(wx.EVT_BUTTON, self.view_record)
        btn_sizer.Add(ViewBtn, 0, wx.ALL, 5)

        # create an edit button
        # edit_record_btn = wx.Button(self, label="Post Ad")
        # edit_record_btn.Bind(wx.EVT_BUTTON, self.edit_record)
        # btn_sizer.Add(edit_record_btn, 0, wx.ALL, 5)

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
        # mainSizer.Add(updateBtn, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)

    def registerControl(self, event):
        with RegisterDialog() as dlg:
            dlg.ShowModal()
            self.updateSpreadsheet()

    def deleteControl(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        if not selected_row:
            dialogs.show_message('Please select one profile from the list!', 'Error')
            return

        cell = self.main_sheet.find(selected_row.email)
        self.main_sheet.delete_row(cell.row)

        # Update
        self.updateSpreadsheet()

        dialogs.show_message("Profile has been deleted!", 'Deleted', wx.ICON_INFORMATION)

    # def edit_record(self, event):
    #     selected_row = self.dataOlv.GetSelectedObject()
    #     # selected_rows = self.dataOlv.GetSelectedObjects()
    #     if not selected_row:
    #         dialogs.show_message('No row selected!', 'Error')
    #         return
    #
    #     with dialogs.RecordDialog(selected_row,
    #                               title='Post',
    #                               addRecord=False) as dlg:
    #         dlg.ShowModal()
    #
    #     # self.show_all_records()

    def view_record(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        # selected_rows = self.dataOlv.GetSelectedObjects()
        if not selected_row:
            dialogs.show_message('Please select one profile from the list!', 'Error')
            return

        with ViewDialog(selected_row) as dlg:
            dlg.ShowModal()

        # self.show_all_records()

    def updateControl(self, event):
        self.updateSpreadsheet()
        dialogs.show_message("The spreadsheet has been updated!", 'Updated', wx.ICON_INFORMATION)

    def updateSpreadsheet(self):
        list_of_hashes = self.main_sheet.get_all_records()

        self.data = []
        for i in list_of_hashes:
            self.data.append(
                Account(i['User ID'], i['Email'], i['Kijiji password'], i['Email Password'], i['IMAP password'],
                        i['Forwarding to'], i['Token']))

        self.dataOlv.SetObjects(self.data)

    def setData(self):
        self.dataOlv.SetColumns([
            ColumnDefn("User ID", "left", 70, "user_id", minimumWidth=70),
            ColumnDefn("Email", "left", 213, "email", minimumWidth=213),
            ColumnDefn("Kijiji password", "left", 89, "kijiji_pass", minimumWidth=89),
            ColumnDefn("Email Password", "left", 116, "email_pass", minimumWidth=116),
            ColumnDefn("IMAP password", "left", 88, "imap_pass", minimumWidth=88),
            ColumnDefn("Forwarding to", "left", 211, "forwarding", minimumWidth=211),
            ColumnDefn("Token", "left", 1783, "token", minimumWidth=1783)
        ])

        self.dataOlv.SetObjects(self.data)
