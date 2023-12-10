import wx
from clnt import client


class GUI(wx.Frame):
    def __init__(self):
        super(GUI, self).__init__(None, title='שרת טכנאי', size=(300, 250))
        # A list of text boxes which corresponds to wx.TextCtrl
        self.params = []
        # The combo box (dropdown menu)
        self.combo_box = None
        # The client object
        self.client = None

        self.InitUI()

    def InitUI(self):
        # This is our client, yours can look differently
        # This code goes after the all the UI elements have been added
        # Inside the InitUI function
        self.client = client.Client()
        # In order to add menus, first we create a MenuBar
        menu_bar = wx.MenuBar()
        # We then add a menu
        file_menu = wx.Menu()
        # wx.ID_EXIT = once the menu item is clicked the window closes
        menu_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        # We append an item to the menu, (append = The end of the menu)
        # 'Menu' = The name of the item
        menu_bar.Append(file_menu, 'Menu&')
        # Sets the MenuBar of this frame to be this MenuBar
        # This inherits from wx.Frame so it is also a Frame object
        self.SetMenuBar(menu_bar)
        # Similar to the button bind, in the previous exercise
        # We bind a certain function (OnQuit) to this menu item
        self.Bind(wx.EVT_MENU, self.OnQuit, menu_item)
        # Creation of the Panel
        pnl = wx.Panel(self)
        # A static box is a vertical / horizontal sequence of items
        sb = wx.StaticBox(pnl, label='Parameters')
        # A static box sizer provides a border around a static box
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        # The param 1 text
        text_one = wx.StaticText(pnl, label='Param 1')
        # The param 2 text
        text_two = wx.StaticText(pnl, label='Param 2')
        # The first parameter box
        param_one = wx.TextCtrl(pnl)
        # The second parameter box
        param_two = wx.TextCtrl(pnl)
        # We append the first parameter box
        self.params.append(param_one)
        # We append the second parameter box
        self.params.append(param_two)
        # Add the first text to the vertical box
        sbs.Add(text_one)
        # Add the first text box (TextCtrl)
        # flag = The orientation
        # border = distance from orientation point
        sbs.Add(self.params[0], flag=wx.LEFT, border=5)
        # Add the second text
        sbs.Add(text_two)
        # Add the second text box
        sbs.Add(self.params[1], flag=wx.LEFT, border=5)
        # Set this static box sizer to be the one we just created
        pnl.SetSizer(sbs)
        # List of known commands
        commands = ['DIR', 'TAKE_SCREENSHOT', 'SEND_FILE', 'DELETE', 'COPY',
                    'EXECUTE', 'HISTORY']
        # Static text above the dropdown menu
        wx.StaticText(pnl, pos=(130, 50), label="Command")
        # A combo box is a dropdown menu
        self.combo_box = wx.ComboBox(pnl, pos=(130, 70), choices=commands,
                                     style=wx.CB_READONLY)
        # Creation of a button
        cbtn = wx.Button(pnl, label='Send', pos=(140, 150))
        # Binds a certain method to the button, will be called when pressed
        cbtn.Bind(wx.EVT_BUTTON, self.on_send)
        self.Centre()
        self.Show(True)

    def OnQuit(self, e):
        """
        when the user presses the quit button,
        the function is called, ending the GUI loop
        """
        self.Close()

    def on_send(self, e):
        """
        when the user presses the send button,
        this function is called, which in turn
        generates the query by combining all parameters
        given by the user, and transfers them to the client.
        after client returns the response, the function creates
        a message box containing it.
        """
        command = self.combo_box.GetStringSelection()
        params = ""
        for x in range(0, 2):
            params += self.params[x].GetLineText(0)
        params += ' '
        # This is how we send commands, you can send commands however you wish
        response = self.client.send_command(command + ' ' + params)
        if response == "EXIT":
            self.Close()
        wx.MessageBox(response, 'Response', wx.OK | wx.ICON_INFORMATION)


def main():
    """
     begins an app loop,
     creates a GUI.
     when user quits, ends loop.
     """
    ex = wx.App()
    GUI()
    ex.MainLoop()


if __name__ == '__main__':
    main()
