import json
import sys
import wx
import wx.richtext as rt
import socketio
import datetime

import random
import logging
import os
import DSS




if not os.path.isdir('log'):
    os.mkdir('log')
filename = datetime.datetime.now()
filename = filename.strftime("%Y%m%d%H%M%S")
filename = 'log\\Client_' + filename + '.log'

logger = logging.getLogger('client_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

sio = socketio.Client(logger=False)
class Messenger(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Digital Signature authentication Application')
        self.InitUI()
        self.Centre()

        self.makeMenuBar()

        self.CreateStatusBar()
        self.log("Write your user name and Server Address, then Click to connect...")

        self.Show()

        self.connected = False
        self.sessionOpen = False

        self.pub_key = None
        self.sender_pub_key = None
        self.priv_key = None

        self.dh = None
        self.users = {}

    
    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbUser = wx.BoxSizer(wx.HORIZONTAL)
        self.lblUser = wx.StaticText(panel, label='User Name')
        self.txtUser = wx.TextCtrl(panel)
        hbUser.Add(self.lblUser, flag=wx.RIGHT, border=8)
        hbUser.Add(self.txtUser, proportion=1)
        vbox.Add(hbUser, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 5))

        hbServer = wx.BoxSizer(wx.HORIZONTAL)
        self.lblSever = wx.StaticText(panel, label='Server Address')
        self.txtServer = wx.TextCtrl(panel,value='http://localhost:5000')
        self.btnConnect = wx.Button(panel, label='Connect')
        hbServer.Add(self.lblSever, flag=wx.RIGHT, border=8)
        hbServer.Add(self.txtServer, proportion=1)
        hbServer.Add(self.btnConnect, proportion=0.5)
        vbox.Add(hbServer, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 10))

        hbUsers = wx.BoxSizer(wx.HORIZONTAL)
        self.lblUsers = wx.StaticText(panel, label='Connected users')
        self.cmbUsers = wx.ComboBox(panel)
        self.btnChatWith = wx.Button(panel, label='Chat...')
        hbUsers.Add(self.lblUsers, flag=wx.RIGHT, border=8)
        hbUsers.Add(self.cmbUsers, proportion=1)
        hbUsers.Add(self.btnChatWith, proportion=0.5)
        vbox.Add(hbUsers, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 10))

        hbChat = wx.BoxSizer(wx.HORIZONTAL)
        lblChat = wx.StaticText(panel, label='Chat Box')
        hbChat.Add(lblChat)
        vbox.Add(hbChat, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add((-1, 10))

        hbChatBx = wx.BoxSizer(wx.HORIZONTAL)
        self.txtChat = rt.RichTextCtrl(panel, style=wx.VSCROLL|wx.HSCROLL|wx.TE_READONLY)
        hbChatBx.Add(self.txtChat, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbChatBx, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.EXPAND,border=10)

        hbMsg = wx.BoxSizer(wx.HORIZONTAL)
        self.txtMsg = wx.TextCtrl(panel)
        self.btnSendMsg = wx.Button(panel,label='Send')
        self.btnSendFile = wx.Button(panel,label='Send File...')
        hbMsg.Add(self.txtMsg, proportion=1)
        hbMsg.Add(self.btnSendMsg, proportion=0.3)
        hbMsg.Add(self.btnSendFile, proportion=0.3)
        vbox.Add(hbMsg, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,border=10)
        vbox.Add((-1, 10))

        

        vbData = wx.BoxSizer(wx.VERTICAL)
        self.lblPriv_key = wx.StaticText(panel, label='Private key:')
        self.lblPub_key = wx.StaticText(panel, label='Public key:')
        self.lblSender_pub_key = wx.StaticText(panel, label='Sender public key:')
        vbData.Add(self.lblPriv_key)
        vbData.Add(self.lblPub_key)
        vbData.Add(self.lblSender_pub_key)
        vbox.Add(vbData, proportion=1,flag=wx.TOP, border=10)
        vbox.Add((-1, 10))

        
        panel.SetSizer(vbox)

        self.cmbUsers.Enabled = False
        self.btnChatWith.Enabled = False

        self.btnConnect.Bind(wx.EVT_BUTTON, self.OnConnect)
        self.btnChatWith.Bind(wx.EVT_BUTTON, self.OnChatWith)
        self.btnSendMsg.Bind(wx.EVT_BUTTON,self.OnSendMsg)
        self.btnSendFile.Bind(wx.EVT_BUTTON,self.OnSendFile)

        self.initControls()
        

    def log(self,msg):
        self.SetStatusText(msg)
        logger.info(msg)

    def initControls(self):
        self.cmbUsers.Enabled = False
        self.btnChatWith.Enabled = False
        self.txtChat.Enabled = False
        self.txtMsg.Enabled = False
        self.btnSendMsg.Enabled = False
        self.btnSendFile.Enabled = False

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)



    def create_keys(self):
        self.log(f'Creating public and private keys keys...')
        pub_key, priv_key = DSS.newkeys(1024)
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.log(f'Public Keys created {pub_key} - {priv_key}')

        self.lblPriv_key.Label =  'Private key: ' + str(priv_key)
        self.lblPub_key.Label = 'Public key: ' + str(pub_key)
        

    
    def OnExit(self, event):
            """Close the frame, terminating the application."""
            self.Close(True)

    def OnAbout(self, event):
        """Display an About Dialog"""
        message = '''
            Author: Asahi Cantu Moreno
            Application Description: This project emulates the Digital Signature Schema implementig RSA Algotithm 
            from one user to another.
            Created for the assignment of  Network Security and Cryptography for the University of Stavanger
        '''
        wx.MessageBox(message,"About Client Application",wx.OK|wx.ICON_INFORMATION)

    
    def OnConnect(self, event):
        if not self.connected: #Connect to web server
            self.log("Connecting to server...")
            #try:
            self.btnConnect.LabelText = 'Disconnect'
            self.create_keys()
            user = self.txtUser.Value
            server = self.txtServer.Value
            sio.connect(server)
            sio.emit('login', {'session':sio.sid,'user':user})
            self.cmbUsers.Clear()
            self.connected = True
            # except:
            # err = sys.exc_info()[0]
            # log(f"System error! {err}")
        else: #Disconnect
            self.log("Disconecting from server...")
            self.btnConnect.LabelText = 'Connect'
            sio.emit('logout', {'session':sio.sid,'user':self.txtUser.Value})
            self.connected = False
            self.log("Disconnected")
            sio.disconnect()
        self.txtUser.Enabled = not self.connected
        self.txtServer.Enabled = not self.connected
        self.initControls()

    def OnChatWith(self,event):
        user = self.cmbUsers.GetStringSelection()
        data = {
            'requester':self.txtUser.Value, 
            'requester_sid': sio.sid,
            'user': user,
            'user_sid':self.users[user],
            'pub_key_dict':DSS.extract_pub_key(self.pub_key)
            }

        self.log(f'Sending chat request to user {user} with public_key {self.pub_key}')
        sio.emit('chatwith', data)

    def OnSendMsg(self,event):
        message = self.txtMsg.Value
        now = datetime.datetime.now()
        nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
        if len(message):
            msg = f'{nowStr} \t {self.txtUser.Value}: {self.txtMsg.Value}'
            self.txtChat.BeginTextColour((0, 0, 255))
            self.txtChat.WriteText(msg)
            self.txtChat.EndTextColour()
            self.txtChat.Newline()
            self.log('Signing message...')
            msg = msg.encode('UTF-8')
            crypt = DSS.encrypt(msg,self.pub_key)
            self.log('Signing message...')
            signature = DSS.sign(msg,self.priv_key) 
            user = self.cmbUsers.GetStringSelection()
            s_id = self.users[user]
            data = {
                'requester':self.txtUser.Value, 
                'requester_sid': sio.sid,
                'user': user,
                'message':msg,
                'user_sid':s_id,
                'crypt':crypt,
                'signature':signature,
            }

            self.log(f'Sending Message for authentication...')
            sio.emit('sendmessage',data)
            self.txtMsg.Clear()
    
    def OnSendFile(self,evnt):
        with wx.FileDialog(self, "Select a file to be sent...", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user   
            pathname = fileDialog.GetPath()
            filename =  os.path.basename(pathname)
            try:
                bit_file = b''
                with open(pathname, 'rb') as file:
                    while (byte := file.read(1)):
                        bit_file+=byte
                signature = DSS.sign(bit_file,self.priv_key)     
                self.log(f'File has been signed with private key {str(self.priv_key)}')
                user = self.cmbUsers.GetStringSelection()
                s_id = self.users[user]
                data = {
                    'requester':self.txtUser.Value, 
                    'requester_sid': sio.sid,
                    'user': user,
                    'file_data':bit_file,
                    'user_sid':s_id,
                    'signature':signature,
                    'filename':filename,
                }            
                sio.emit('sendfile',data)
            except IOError:
                wx.LogError(f"Cannot open file {filename}" )

          
    def verifytMessage(self,message,signature):
        frame.log(f'Message received {message} authenticating...')
        verified = DSS.verify(message,signature,self.sender_pub_key)
        if verified:
            frame.log('Message has been verified!')    
            self.txtChat.BeginTextColour((0, 150, 100))
        else:
            self.txtChat.BeginTextColour((255, 0, 0))
            frame.log('Message verification failed!')
        msg = message.decode('UTF-8')
        self.txtChat.WriteText(msg)
        self.txtChat.EndTextColour()
        self.txtChat.Newline()

    def verifyfile(self,filename,data,signature):
        self.log(f'File received {filename} authenticating...')
        self.log(data)
        
        verified = DSS.verify(data,signature,self.sender_pub_key)
        if verified:
            frame.log('File has been verified! Saving...')    
            at = datetime.datetime.now()
            filename = at.strftime("%Y%m%d%H%M%S") + filename
            filename = 'log\\Client_' + filename
            with open(filename,'bw') as f:
                f.write(data)
            self.log(f'File saved in {filename}')    
        else:
            self.log('File verification failed!')

  

@sio.on("logged_users")
def users(data):
    print(f'receiving new users {data}')
    if data:
        for key in data:
            user = data[key]
            if user != frame.txtUser.Value:
                if user not in frame.cmbUsers.Strings:
                    frame.users[user] = key
                    frame.cmbUsers.Append(user)
                    print(f'User {user} connected!')
    if not frame.cmbUsers.IsListEmpty():
        frame.cmbUsers.SetSelection(0)
        frame.cmbUsers.Enabled = True
        frame.btnChatWith.Enabled = True
        frame.SetStatusText('New Users Received')
    else:
        frame.cmbUsers.Enabled = False
        frame.btnChatWith.Enabled = False
        frame.SetStatusText('Waiting for users...')


@sio.on("chatwith")
def beginchat(data):
    #: sio.sid,
    requester = data['requester']
    requester_sid = data['requester_sid']
    user = data['user']
    user_sid = data['user_sid']
    msg  =f'{requester} wants to start chat session with {user}... '  
    frame.log(msg)
    if frame.connected and not frame.sessionOpen:
        result = wx.MessageDialog(frame, msg, caption='Click Yes to Accept',
              style=wx.YES_NO|wx.CENTRE, pos=wx.DefaultPosition).ShowModal()
        if result == wx.ID_YES:
            frame.log('Storing public key...')
            pub_key_dict = data['pub_key_dict']
            frame.sender_pub_key = DSS.create_pub_key(pub_key_dict)
            frame.log('Linking messaging...')
            location = frame.cmbUsers.FindString(requester)
            frame.cmbUsers.SetSelection(location)
            frame.cmbUsers.Enabled = False
            frame.btnChatWith.Enabled = False
            data['requester'] = user
            data['requester_sid'] = sio.sid
            data['user'] = requester
            data['user_sid'] = requester_sid
            data['pub_key_dict'] = DSS.extract_pub_key(frame.pub_key)

            sio.emit('onhandshake',data)

@sio.on('handshake')
def handshake(data):
    requester = data['requester']
    requester_sid = data['requester_sid']
    user = data['user']
    user_sid = data['user_sid']
    if sio.sid != requester_sid:
        pub_key_dict = data['pub_key_dict']
        frame.sender_pub_key =  DSS.create_pub_key(pub_key_dict)
    
    frame.lblSender_pub_key.Label = 'Sender public key: ' + str(frame.sender_pub_key)
    
    frame.btnChatWith.Enabled = False
    frame.cmbUsers.Enabled = False
    frame.txtMsg.Enabled = True
    frame.btnSendMsg.Enabled = True
    frame.btnSendFile.Enabled = True
    frame.txtChat.Enabled = True
    frame.log(f'Connection established')
        
@sio.on("sendmessage")
def sendmessage(data):
    requester =  data['requester']
    requester_sid =  data['requester_sid']
    user =  data['user']
    user_sid =  data['user_sid']
    message = data['message']
    crypt =  data['crypt']
    signature = data['signature']
    frame.verifytMessage(message,signature)

@sio.on("sendfile")
def sendmessage(data):
    requester =  data['requester']
    requester_sid =  data['requester_sid']
    user =  data['user']
    user_sid =  data['user_sid']
    file_data = data['file_data']
    signature = data['signature']
    filename = data['filename']
    frame.verifyfile(filename,file_data,signature)

if __name__ == '__main__':
    app = wx.App()
    frame = Messenger()
    frame.SetSize(wx.Size(600,500))
    frame.log('Client Application has started')
    app.MainLoop()
    
    
