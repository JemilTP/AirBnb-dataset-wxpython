#hello test
import wx as wx
import string
import report_listing_info
from datetime import datetime
import os
import webbrowser
class dpanel(wx.ScrolledWindow,):
    def __init__(self, parent, info, title, word, num,func, start_date, end_date, length):
        
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL,)
        welcomeText = wx.StaticText(self, label= title, pos = (50,30))
        font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL) 
        welcomeText.SetFont(font)
        stats = wx.StaticText(self, label = f'Number of results: {length}', pos = (50,100))
        font2 = wx.Font(15, wx.ROMAN, wx.NORMAL,wx.NORMAL)
        stats.SetFont(font2)
        gb = wx.GridBagSizer(vgap=0, hgap=3)
        self.num = num
        self.word = str(word)
        self.sizer = gb
        self.labels = []
        self.data = info
        self.title = title
        self.func = func
        self.start_date = start_date
        self.end_date = end_date

        
        x = 0
        for i in range(len(self.data)):
            name = str(self.data[i].iat[4])
    
            a =  wx.Button(parent=self, label= name, size = (300,40), id = i)
            gb.Add(a, (x + 7,5))
            x += 2
            a.Bind(wx.EVT_BUTTON, self.showlisting )
  

        self.SetSizer(self.sizer)
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.SetScrollRate(fontsz.x, fontsz.y)
        self.EnableScrolling(True,True)
    def showlisting(self, event):
        listing_id = event.GetEventObject().GetId()
        listing_data = self.data[listing_id]
        list_Title = self.data[listing_id].iat[4]
        listing_Frame(self, listing_data, list_Title)
    def nextpage(self, event):
        self.num += 1
        inp = str(self.word)
        numb = int(self.num)
        if self.func == 'Suburb':
            nextPagedata1 = report_listing_info.listings_in_suburb(inp,self.start_date,self.end_date, numb)        
            next1 = results_(self,nextPagedata1, self.title, inp, numb, 'Suburb',self.start_date,self.end_date)
        else:
            nextPagedata2 = report_listing_info.keyword(inp, self.start_date,self.end_date, numb)            
            next2 =  results_(self,nextPagedata2, self.title, inp, numb,'Keyword',self.start_date,self.end_date)
    def back(self, event):
        self.num -= 1
        inp = str(self.word)
        numb = int(self.num)
        if self.func == 'Suburb':
            nextPagedata1 = report_listing_info.listings_in_suburb(inp,self.start_date,self.end_date, numb)
        
            next1 = results_(self,nextPagedata1, self.title, inp, numb, 'Suburb',self.start_date,self.end_date)
        else:
            nextPagedata2 = report_listing_info.keyword(inp, self.start_date,self.end_date, numb)
            
            next2 =  results_(self,nextPagedata2, self.title, inp, numb,'Keyword',self.start_date,self.end_date)


class results_(wx.Frame):
        def __init__(self, parent, data, title, word, num, func, start_date, end_date):
            wx.Frame.__init__(self, None, -1, title = title, size = (1000, 800))
            next_page = wx.Button(parent=self, label='Next Page', size = (100,30),pos = (610,100))
            next_page.Bind(wx.EVT_BUTTON, self.next)
            home = wx.Button(parent = self, label = 'Home', size= (100, 30), pos = (500,100))
            home.Bind(wx.EVT_BUTTON, self.home)
            if num > 0:
                back = wx.Button(parent = self, label = 'Back', size = (100,30), pos = (720,100))
                back.Bind(wx.EVT_BUTTON,self.back)
            sz = wx.BoxSizer(wx.VERTICAL)
            self.pa = dpanel(self, data, title, word, num, func, start_date, end_date,len(data))
            sz.Add(self.pa, 1, wx.EXPAND)
          
            
            self.SetSizer(sz)
            
            self.Show()
        def home(self, event):
            MyFrame(parent=None, title="Sydney AirBNB", pos = (700, 700)).Show()
            self.Close()
        def next(self, event):
            self.pa.nextpage(event)
            self.Close()
        def back(self, event):
            self.pa.back(event)
            self.Close()
class listing_Frame(wx.Frame):
        def __init__(self, parent, data, title):
            wx.Frame.__init__(self, None, -1, title = title, size = (1300, 800))
      
            listingWin = listingPanel(self, data, title)
            self.Show()

class listingPanel( wx.ScrolledWindow):
    def __init__(self, parent, data, title):
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL,)  
        welcomeText = wx.StaticText(self, label= title, pos=(500,30))

        gb = wx.GridBagSizer(vgap=0, hgap=3)
        self.sizer = gb
        self.labels = []

        font = wx.Font(30,  wx.ROMAN,wx.NORMAL,wx.NORMAL) 
        font_details =  wx.Font(15,  wx.DEFAULT,wx.NORMAL,wx.NORMAL) 
        welcomeText.SetFont(font)
       
        columns = list()
        for index,val in data.iteritems():
             columns.append(str(index))
        image = wx.Button(parent=self, label='View image', size = (100,40), pos = (40,150))
        image.Bind(wx.EVT_BUTTON, self.loadimage)
        site = wx.Button(parent=self, label='See listing online', size = (100,40), pos = (40,100))
        site.Bind(wx.EVT_BUTTON, self.visitSite)
        self.url = data['picture_url']
        self.link = data['listing_url']
        height = int()
        adder = 200
        q = 0
        for i in range(len(data)):
            height = 25* i + adder
            col = wx.StaticText(self, label= (columns[i] + ' :'))
            col.SetFont(font_details)
            gb.Add(col,(q + 10, 3))
            desc = str(data[columns[i]])
            if columns[i] == 'amenities':
                    for w in string.punctuation:
                        if w in desc and w != '(' and w != ')':
                            desc = desc.replace(w, ' ')
            length = 100
            space = len(desc)//length 
            check_spacing = [ 'notes','summary','description' , 'amenities' , 'neighborhood_overview', 'transit' , 'access', 'interaction', 'house_rules','last_scraped', 'summury', 'space', 'host_about']
            if columns[i] in check_spacing and len(desc) >= length:
                     
                temp = 0  
                f = 0           
                adder += 25*space
                line = str()
           
                
                for x in range(len(desc)):
                    
                    if x >= ((f + 1) * length)  and desc[x - 1] == ' ':
                        line = desc[temp:x - 1]                    
                        val = wx.StaticText(self, label= line) 
                        val.SetFont(font_details)  
                        gb.Add(val, (q + 10, 10)) 
                        height += 25  
                        temp = x  
                        q += 1
                        f += 1
                          
                    elif f == space  and x <= len(desc) - 1:
                        line = desc[temp:len(desc) - 1 ]  
                        val = wx.StaticText(self, label= line) 
                        val.SetFont(font_details)  
                        gb.Add(val, (q + 10, 10)) 
                        break

            else: 

                val = wx.StaticText(self, label= desc)
                val.SetFont(font_details)
                gb.Add(val, (q + 10 ,10))
            q += 1
            self.SetSizer(self.sizer)
            fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
            self.SetScrollRate(fontsz.x, fontsz.y)
            self.EnableScrolling(True,True)
            
       
        self.Show()
    def loadimage(self,event):
  
        webbrowser.open(self.url)
    def visitSite(self, event):
        webbrowser.open(self.link)

class MyFrame(wx.Frame):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self,parent, title, pos):
        wx.Frame.__init__(self, None, -1, title = title, size = (800, 800))
        self.SetBackgroundColour(wx.WHITE)
        # add a hello message to the panel
        welcomeText = wx.StaticText(self, label="Sydney Air Bnb", pos=(50,30))
        font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL) 
        welcomeText.SetFont(font)
        # add a button to bring up the dialog box
        button = wx.Button(parent=self, label='Enter Suburb', pos = (50, 150), size = (95,40))
        button2 = wx.Button(parent=self, label='Enter Key word', pos = (150, 150), size = (95,40))
        button3 = wx.Button(parent=self, label='Produce Chart', pos = (250, 150), size = (95,40))
        button4 = wx.Button(parent=self, label='Enter Start date', pos = (350, 150), size = (95,40))
        button5 = wx.Button(parent=self, label='Enter End date', pos = (450, 150), size = (95,40))
        button6 = wx.Button(parent=self, label='Analyse Clealiness', pos = (50, 225), size = (110,40))
        button8 = wx.Button(parent=self, label='Clear Dates', pos = (550, 150), size = (95,40))
       
     
        font_names = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        n1 = wx.StaticText(self, label = 'Jemil Pepena - s5166443', pos = (50, 450))
        n2 = wx.StaticText(self, label = 'Lara O’callaghan  - s5185854', pos = (50, 470))
        n3 = wx.StaticText(self, label = 'Tanaya Newman - s5113147 ', pos = (50, 490))
        n1.SetFont(font_names)
        n2.SetFont(font_names)
        n3.SetFont(font_names)
        button.Bind(wx.EVT_BUTTON, self.onSubmit ) 
        button2.Bind(wx.EVT_BUTTON, self.onSubmit )
        button3.Bind(wx.EVT_BUTTON, self.onSubmit ) 
        button4.Bind(wx.EVT_BUTTON, self.onSubmit ) 
        button5.Bind(wx.EVT_BUTTON, self.onSubmit )
        button6.Bind(wx.EVT_BUTTON, self.onSubmit )
        
        button8.Bind(wx.EVT_BUTTON, self.onSubmit )
        self.start_date = str()
        self.end_date = str()

 
        
    def onSubmit(self, event): #when a button had been pressed
        # stuff for the submit button to do
        button_pressed = event.GetEventObject()
        if button_pressed.GetLabel() == 'Clear Dates':
            self.start_date = str()
            self.end_date = str()

        elif button_pressed.GetLabel() == 'Analyse Clealiness': #if button to analyse comments on cleaning is pressed
            wait =  wx.TextEntryDialog(self, 'Notice:')
            wait.SetValue("This may take a  moment") 
            wait.ShowModal()
            path = report_listing_info.comments()
            clean = wx.TextEntryDialog(self, "Your Cleanliness chart image was saved at:")
            clean.SetValue(path)
            clean.ShowModal()
        else:
            if  button_pressed.GetLabel() == 'Enter Start date': #: yyyy/mm/dd')
                if date.ShowModal() == wx.ID_OK:   # if start date has not been entered or enter strt date btn was pressed
                    date =  wx.TextEntryDialog(self, 'Enter Start Date ')
                    self.start_date = str(date.GetValue())
    
            if  button_pressed.GetLabel() == 'Enter End date':  #if end date has not been entered or enter end date btn was pressed
                edate =  wx.TextEntryDialog(self, 'Enter End Date : yyyy/mm/dd')
                if edate.ShowModal() == wx.ID_OK:
                    self.end_date = str(edate.GetValue())
              
            check_dates = True
            if len(self.start_date) != 0 and len(self.end_date) != 0: #check if dates are in correct format and start date is less then end date
                check_dates = (report_listing_info.compare_date( self.end_date,self.start_date) )
             
                if check_dates == False:
                    error =  wx.TextEntryDialog(self, 'Dates entered incorrectly or start date is ahead, please use format:')
                    error.SetValue("yyyy/mm/dd") 
                    error.ShowModal()
                    self.start_date = str()
                    self.end_date = str()
            if check_dates:
                if button_pressed.GetLabel() == 'Produce Chart':           
            
                    input_sub  =  wx.TextEntryDialog(self, 'Enter Suburb or leave empty for all of sydney')
                    input_sub.SetValue("Sydney") 
                    if input_sub.ShowModal() == wx.ID_OK:
                        file_name =  wx.TextEntryDialog(self, 'what would you like to name the plot image?')
                        s = str(input_sub.GetValue())
                        file_name.SetValue(s + '_price_data')
                        if file_name.ShowModal() == wx.ID_OK:
                            
                            f = str(file_name.GetValue())  
                            chart = report_listing_info.price_distribution(s,self.start_date, self.end_date, f)
                            if chart != -1:
                                label_for_chart =  "Your Distribution Chart image was saved at:"
                            else:
                                label_for_chart = 'Error'
                                chart = "No data for the suburb you entered or dates"
                            dir_ = wx.TextEntryDialog(self,label_for_chart)
                            dir_.SetValue(chart)
                            dir_.ShowModal()
                        
                if button_pressed.GetLabel() == 'Enter Suburb':
                    input_suburb =  wx.TextEntryDialog(self, 'Enter Suburb/s separated by comma')
                    input_suburb.SetValue("Sydney")
                
                    if input_suburb.ShowModal() == wx.ID_OK:
                    
                        user_input = str(input_suburb.GetValue())  
                    
                        result = report_listing_info.listings_in_suburb(user_input, self.start_date, self.end_date,1)
                        if len(result) != 0:
                            if len(user_input) == 0:
                                title = 'Listings in all of Sydney'
                                if len(self.start_date) != 0 and len(self.end_date):
                                    title = f'Listings in all of Sydney from {self.start_date} to {self.end_date}'
                            else:
                                user_input = user_input.split(',')
                                if len(user_input) == 1:
                                    user_input = user_input[0][0].upper() + user_input[0][1:]
                                else:
                                    user_input_copy = user_input
                                    user_input = str()
                                    for k in range(len(user_input_copy)):
                                        user_input_copy[k] = user_input_copy[k].lower()
                                        user_input_copy[k] = user_input_copy[k][0].upper() + user_input_copy[k][1:]
                                        if k != len(user_input_copy) - 1 and k != 0:
                                            user_input += ', ' + user_input_copy[k] 
                                        elif k == 0:
                                            user_input += user_input_copy[k]
                                        else:
                                            user_input +=  ' and ' + user_input_copy[k]

                                if len(self.start_date) != 0 and len(self.end_date) != 0:
                                    title = f'Listings in {user_input} from {self.start_date} to {self.end_date}'
                                else:
                                    title = f'Listings in all of {user_input}'
                            results_(self, result, title, user_input, 0, 'Suburb',self.start_date,self.end_date)
                            self.Close()
                        else:
                            error =  wx.TextEntryDialog(self, 'No results for suburb:')
                            error.SetValue(f'{user_input}')
                            error.ShowModal()
                        
                if button_pressed.GetLabel() == 'Enter Key word':
                    word =  wx.TextEntryDialog(self, 'Enter Word')
                    word.SetValue("Pool")
                    if word.ShowModal() == wx.ID_OK:
                        user_input = str(word.GetValue())                         
                       
                        result = report_listing_info.keyword(user_input, str(self.start_date), str(self.end_date), 1)   
                        if len(result) != 0:   
                            if len(user_input) == 0:
                                title = 'Listings in all of Sydney'
                                if len(self.start_date) != 0 and len(self.end_date):
                                    title = f'Listings in all of Sydney from {self.start_date} to {self.end_date}'
                            else:
                                user_input = user_input.split(',')
                                if len(user_input) == 1:
                                    user_input = user_input[0][0].upper() + user_input[0][1:]
                                else:
                                    user_input_copy = user_input
                                    user_input = str()
                                    for k in range(len(user_input_copy)):
                                        user_input_copy[k] = user_input_copy[k].lower()
                                        user_input_copy[k] = user_input_copy[k][0].upper() + user_input_copy[k][1:]
                                        if k != len(user_input_copy) - 1 and k != 0:
                                            user_input += ', ' + user_input_copy[k] 
                                        elif k == 0:
                                            user_input += user_input_copy[k]
                                        else:
                                            user_input +=  ' and ' + user_input_copy[k]

                            if len(self.start_date) != 0 and len(self.end_date) != 0:
                                title = f'Listings with {user_input} from {self.start_date} to {self.start_date}'
                            else:
                                title = f'All Listings with {user_input}'              
                            results_(self, result, title, user_input, 0,'Keyword',self.start_date,self.end_date)
                            self.Close()
                        else:
                            error =  wx.TextEntryDialog(self, 'No results for Keyword:')
                            error.SetValue(f'{user_input}')
                            error.ShowModal()

        
if __name__ == "__main__":
   app = wx.App()
   frame = MyFrame(parent=None, title="Sydney AirBNB", pos = (700, 700))
   frame.Show()
   app.MainLoop()
print("GoodBye  : )")