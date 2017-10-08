#######################################
# Gui program for reat time analysis of power grid data
# created by Nejc Jansa
# nejc0jansa@gmail.com
# document creation 14.11.2016
#######################################

# necessary imports
import numpy as np
import matplotlib
import csv
import gc
### now using matplotlib 2.0.0
import matplotlib.pyplot as plt
matplotlib.use('TkAgg') # sets tkinter to be the backend of matplotlib

#matplotlib canvas and plot edit toolbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

# (Tkinter for Python 3)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#jakas imports
from datetime import datetime
from iskanje import iskanje
import re


#colorbrewer nice plot colot set
colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999',
          '#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999',
          '#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999']

#set some global settings for plots
plot_font = {'family': 'Calibri', 'size': '12'}
matplotlib.rc('font', **plot_font)  # make the font settings global for all plots


class Frame_plots(tk.Frame):
    '''Leftmost frame with selection of experiment'''
    def __init__(self, parent):
        '''makes the subframe and fills it up'''
        tk.Frame.__init__(self, parent, bd=5)
        self.pack(side='top', anchor='n',fill='x')

        #reference to parent
        self.parent = parent

        #start realtime data
        self.data = Realtime_data()

        #load widgets
        self.Widgets()

        #initiate plots
        self.Initiate_plots()

        self.test_row = Generator_row()
        for i in range(99):
            next(self.test_row)

        #loop variable
        self.run = tk.BooleanVar(master=self, value=False)



    def Widgets(self):
        '''Puts all the widgets on the frame'''

        self.frame_top = tk.Frame(self)
        self.frame_top.pack(side='top', anchor='n',fill='x')
        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.pack(side='top', anchor='n', fill='x')


        ## top side
        self.frame_left = tk.Frame(self.frame_top)
        self.frame_right = tk.Frame(self.frame_top)
        self.frame_left.pack(side='left', fill='both', expand=True)
        self.frame_right.pack(side='right', fill='both', expand=True)

        #left top plot
        self.fig_left = plt.figure(dpi=100, figsize=(7,5))
        self.fig_left.subplots_adjust(bottom=0.20, left= 0.14, right=0.96, top=0.88)
        self.canvas_left = FigureCanvasTkAgg(self.fig_left, self.frame_left)
        #self.toolbar = NavigationToolbar2TkAgg(self.canvas_left, self.frame_left)
        self.canvas_left._tkcanvas.pack()

        #right top plot ###change into canvas
        self.fig_right = plt.figure(dpi=100, figsize=(7,5))
        self.fig_right.subplots_adjust(bottom=0.20, left= 0.14, right=0.96, top=0.88)
        self.canvas_right = FigureCanvasTkAgg(self.fig_right, self.frame_right)
        #self.toolbar = NavigationToolbar2TkAgg(self.canvas_right, self.frame_right)
        self.canvas_right._tkcanvas.pack()


        #bottom side
        self.frame_left2 = tk.Frame(self.frame_bottom)
        self.frame_right2 = tk.Frame(self.frame_bottom)
        self.frame_left2.pack(side='left', anchor='n')
        self.frame_right2.pack(side='right')
        
        #add button to go to previous frame
##        self.button_previous = ttk.Button(self.frame_left, text='<<', command=self.Previous)
##        self.button_previous.pack(side='left')
##        self.button_previous.bind('<Left>', self.Previous)

        self.button_play = ttk.Button(self.frame_left2, text='Play', command=self.Play)
        self.button_play.pack(side='left')
        self.button_play.bind('<space>', self.Play)

        self.button_pause = ttk.Button(self.frame_left2, text='Pause', command=self.Pause)
        self.button_pause.pack(side='left')

        self.button_next = ttk.Button(self.frame_left2, text='Next', command=self.Next)
        self.button_next.pack(side='left')
        self.button_next.bind('<Right>', self.Next)

        #right frame, displayed messages
        self.text = tk.Text(self.frame_right2, state='disabled', width=100, height=8)
        self.text.pack(side='top')

        
    def Initiate_plots(self):
        '''Initiates the style of the plots'''

        #left plot   
        self.axes_left = self.fig_left.add_subplot(111)

        #add all frequency traces
        self.axes_left_traces = dict()
        self.axes_left_vlines = []
        n_freq = 120
        
        for i, key in enumerate(self.data.freq_keys):
            tmp, = self.axes_left.plot(self.data.time, self.data.freqs[key], 'bo-',
                                       color=colors[i+1], label='Trace '+str(key))
            self.axes_left_traces[key] = tmp

        #self.axes_left_vline = self.axes_left.axvline(0, color=colors[0])

        self.axes_left.set_title('Real time data')
        self.axes_left.set_xlabel('Time')
        self.axes_left.set_ylabel('Frequency')
        self.axes_left.legend(loc='upper right')
        self.axes_left.grid()

        node_x_list = [0, 1.2540515319837704, 0.5288312603004189, 1.0411901607163858, 0.5457178787504438,
                         0.5902887279491432, 0.4220574562932663, 0.2560843325238992, 0.6995186823392411,
                         0.4900493444312738, 0.40451087449142953, 0.6059094449017457, 0.27170194401129866,
                         0.2706088644285869, 0.7856860252817126]
        node_y_list = [ 0, 0.6571637827807346, 0.5808117208177156, 0.7910209256532237, 0.5385482082552953,
                          0.5732009954175707, 0.541657779723429, 0.33544637004135164, 0.5293526234142677,
                          0.3072025303353594, 0.5220564078231058, 0.5239893971710619, 0.2370571592126064,
                          0.236624300551497, 0.5323674295136915]

        node_x_red = []
        node_y_red = []
        node_x_green =  [0, 1.2540515319837704, 0.5288312603004189, 1.0411901607163858, 0.5457178787504438,
                         0.5902887279491432, 0.4220574562932663, 0.2560843325238992, 0.6995186823392411,
                         0.4900493444312738, 0.40451087449142953, 0.6059094449017457, 0.27170194401129866,
                         0.2706088644285869, 0.7856860252817126]
        node_y_green =  [ 0, 0.6571637827807346, 0.5808117208177156, 0.7910209256532237, 0.5385482082552953,
                          0.5732009954175707, 0.541657779723429, 0.33544637004135164, 0.5293526234142677,
                          0.3072025303353594, 0.5220564078231058, 0.5239893971710619, 0.2370571592126064,
                          0.236624300551497, 0.5323674295136915]
        node_name = []
        for i in range(len(node_x_green)):
            node_name.append('N'+str(i+1))

        #right plot   ### change into node map graphics
        self.axes_right = self.fig_right.add_subplot(111)
        self.axes_right_green, = self.axes_right.plot(node_x_green, node_y_green, 'bo',
                                                   color=colors[2], label='Working')
        self.axes_right_red, = self.axes_right.plot(node_x_red, node_y_red, 'bo',
                                                   color=colors[0], label='Event')

        for i, name in enumerate(node_name): 
            self.axes_right.annotate(name, (node_x_green[i], node_y_green[i]+0.012))
                
        self.axes_right.set_title('Node map')
        self.axes_right.get_xaxis().set_visible(False)
        self.axes_right.get_yaxis().set_visible(False)
        self.axes_right.legend(loc='lower right')

        self.fig_left.canvas.draw()
##        self.fig_right.canvas.draw()


    def Play(self):
        '''starts automatic data playing'''
        self.run.set(True)
        while self.run.get():
            self.Next()
            #start a delay
            ##### figure out how to run a loop that doesnt freeze main_app!!!!
            root.after(1)


    def Pause(self):
        '''stops automatic data playing'''
        self.run.set(False)

    def Next(self):
        '''takes next time frame and calls all necessary updates'''

        #testrow

        row_out = next(self.test_row)
        self.data.Append_row(row_out)


        for key in self.data.freq_keys:
            self.axes_left_traces[key].set_xdata(self.data.time)
            self.axes_left_traces[key].set_ydata(self.data.freqs[key])

        #update plot limits
        self.axes_left.relim()
        #print(self.data.time)
        self.axes_left.autoscale_view()
        self.axes_left.set_xlim(self.data.time[0]-0.01, self.data.time[-1]+0.01)
        
        #add hlines for events
        if len(self.data.events) > 0:
            while len(self.data.events) > len(self.axes_left_vlines):
                self.axes_left_vlines.append(self.axes_left.axvline(0, color=colors[0]))
                print('born')

            while len(self.data.events) > len(self.axes_left_vlines):
                #self.axes.left_vlines[-1].destroy()
                self.axes_left_vlines.pop().destroy()
                print('destroyed')

        for i, event in enumerate(self.data.events):
            self.axes_left_vlines[i].set_xdata(event + 1)

        ######## upgrade nodes


        node_x_list = [0, 1.2540515319837704, 0.5288312603004189, 1.0411901607163858, 0.5457178787504438,
                         0.5902887279491432, 0.4220574562932663, 0.2560843325238992, 0.6995186823392411,
                         0.4900493444312738, 0.40451087449142953, 0.6059094449017457, 0.27170194401129866,
                         0.2706088644285869, 0.7856860252817126]
        node_y_list = [ 0, 0.6571637827807346, 0.5808117208177156, 0.7910209256532237, 0.5385482082552953,
                          0.5732009954175707, 0.541657779723429, 0.33544637004135164, 0.5293526234142677,
                          0.3072025303353594, 0.5220564078231058, 0.5239893971710619, 0.2370571592126064,
                          0.236624300551497, 0.5323674295136915]
        
        if self.data.best_count == 0:
            node_x_red = []
            node_y_red = []
            node_x_green =  []
            node_y_green =  []


            print('its happening', self.data.best_points)
            
            for i in range(len(node_x_list)):
                if i+1 in self.data.best_points[0]:
                    print('yay a point')
                    node_x_red.append(node_x_list[i])
                    node_y_red.append(node_y_list[i])
                else:
                    node_x_green.append(node_x_list[i])
                    node_y_green.append(node_y_list[i])

            print(node_x_green, node_x_red)
            
            self.axes_right_green.set_xdata(node_x_green)
            self.axes_right_green.set_ydata(node_y_green)
            self.axes_right_red.set_xdata(node_x_red)
            self.axes_right_red.set_ydata(node_y_red)
            
            self.fig_right.canvas.draw()
            
        elif self.data.best_count == 99:
            self.axes_right_green.set_xdata(node_x_list)
            self.axes_right_green.set_ydata(node_y_list)
            self.axes_right_red.set_xdata([])
            self.axes_right_red.set_ydata([])
            
            self.fig_right.canvas.draw()

        

        self.fig_left.canvas.draw()

def Test_row():
    '''a test row to check plotting'''
    i = 0
    while True:
        event = True if i%13 == 0 else False
        print(event)
        yield (0.02*i, np.sin(0.02*i)+ 1, np.cos(0.02*i)+ 2, event)
        i += 1

def is_short_circut(test_data, center_cut=5):
    vzorec_P = "N.*_P"
    reg_P = re.compile(vzorec_P)
    plt_keys_P = list(filter(reg_P.match, test_data.keys()))

    max_val = 0
    for key_P in plt_keys_P:
        key_max = np.max([abs(x - test_data[key_P][0]) for x in test_data[key_P]])
        max_val = max_val if key_max < max_val else key_max

    max_diff = 0
    for i, key_P in enumerate(plt_keys_P):
        center = len(test_data[key_P])//2
        tmp = abs(np.average(test_data[key_P][:center - center_cut]) - np.average(test_data[key_P][center + center_cut:])) / max_val
        max_diff = max_diff if max_diff > tmp else tmp
    
    return max_diff < 0.5

def get_number(s, vzorec):
    if vzorec=="N.*_P":
        return  list(map(int,re.findall(r'\d+', s)))
    else:
        return int(re.findall(r'\d+', s)[0])


def get_best_bets(data):
    sim_freq_tmp = []
    #vzorec_all = ["N.*_P", "N.*_u", "N.*_au"]
    #vzorec_all = ["N.*_P", "N.*_au", "N.*_i"]
    vzorec_all = ["N.*_au"]
    
    for vzorec in vzorec_all:
        reg = re.compile(vzorec)
        plt_keys = list(filter(reg.match, data.keys()))
        
        freq_val = np.zeros(len(plt_keys))
        
        max_val = 0
        for key in plt_keys:
            key_max = np.max([abs(d_k - data[key][0]) for d_k in data[key]])
            max_val = max_val if key_max < max_val else key_max
        
        for i, key in enumerate(plt_keys):
            freq_val[i] = np.sum([abs(d_v - data[key][0])
                                  for d_v in data[key][int(len(data[plt_keys[1]])/2)-3:int(len(data[plt_keys[1]])/2)+3]])/max_val
        
        s = sorted(zip(plt_keys, freq_val), key=lambda x:-x[1])
        # sim_freq_tmp.append(plt_keys[np.argmax(abs(freq_val)])
        sim_freq_tmp.append([(get_number(x[0], vzorec)) for x in s[:3]])
    #sim_freq.append(sim_freq_tmp)
    return(sim_freq_tmp)

def Generator_row():
    '''generates rows from real data'''
    reg_r = re.compile("N.*_f")
    reg_P = re.compile("N.*_P")

    sim = 5
    datafile = "../../Data/Simul/Sim4.csv"
    # datafile = "../Data/Real/RealMeasurement9.csv"
    data = dict()

    with open(datafile) as dat_f:
        reader = csv.DictReader(dat_f, delimiter=";")

        iskalnik = iskanje(deriv=False, tol=20)
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            data, flag = iskalnik.send_row(row)

            plt_keys_r = list(filter(reg_r.match, data.keys()))
            plt_keys_P = list(filter(reg_P.match, data.keys()))

            t1 = data["Time"][0]
            #print(t1)
            #t1 = t1 - datetime(2017,1,1)
            #print(t1)
            t1 = t1.second + t1.microsecond/1000000
            #print(t1)

            if flag:
                best_points = get_best_bets(data)
            else:
                best_points = False
                
            yield [t1] + [data[k][0] for k in plt_keys_r] + [flag] + [best_points]
            #print(row)
            continue

 
##            if flag:
##                plt.figure(1)
##                plt.title("freq deriv")
##                for key in plt_keys_r:
##                    plt.plot_date(data["Time"], data[key], '-', label=key)
##
##                plt.figure(2)
##                plt.title("P")
##                for key in plt_keys_P:
##                    plt.plot_date(data["Time"], data[key], '-', label=key)
##
##                plt.title(datafile)
##                plt.legend()
##                plt.show()
##
##                print("Short circut: ", is_short_circut(data))



class Realtime_data():
    '''class that keeps track of the plotted data and updates it from new rows'''
    def __init__(self):
        '''initializes class, prepares arrays and dictionaries'''

        #indexes / keys of data in imported row
        self.time_key = 0
        self.freq_keys = range(1,14)

        #number of points to keep in plot
        self.n_max = 120
        dt = 0.02

        self.best_count = -50
        self.counting = False

        #init lists of data, start with negative times for empty traces in plot
        self.time = [-self.n_max*dt + (i+1)*dt for i in range(self.n_max)]
        self.freqs = dict()
        for key in self.freq_keys:
            self.freqs[key] = [0 for i in range(self.n_max)]

        #init list of events
        self.events = []

    def Append_row(self, row, event=False):
        '''reads a row and correctly adds it to current arrays'''
        #counter for found points
        
        print(self.best_count, 'i', row[-1])

        if type(row[-2]) == type(True):
            event = row[-2]


        if row[-1]:
            self.counting = True
            self.best_points = row[-1]

        if self.counting:
            self.best_count +=1
            if self.best_count > 100:
                self.best_count = -50
                self.counting = False
            
                 
        # adds the new data to row
        self.time.append(row[self.time_key])
        for key in self.freq_keys:
            self.freqs[key].append(row[key])


        #handles events for vline
        if event:
            self.events.append(self.time[-1])

        #remove first entries
        outdate = self.time.pop(0)
        for key in self.freq_keys:
            self.freqs[key].pop(0)
        try:
            if self.events[0] <= outdate:
                self.events.pop(0)
        except IndexError: pass

        

##        #in case row is full remove first entry
##        if len(self.time) == self.n_max:
##            outdate = self.time.pop(0)
##            
##            for key in self.freq_keys:
##                self.freqs[key].pop()
##
##            if events[0] <= outdate:
##                events.pop(0)





class Main_application(tk.Frame):
    '''Main application calling all the sub frames'''
    def __init__(self, parent, *args, **kwargs):
        '''Initializes the main application as a frame in tkinter'''
        tk.Frame.__init__(self, parent, height=1020, width =1720, *args, **kwargs)
        self.parent = parent
        # sets the window title
        self.parent.wm_title('Real time data presentation')
        #sets the window minimal size
        self.parent.minsize(width=1200, height=800)
        # allow editing the exit command
        self.parent.protocol('WM_DELETE_WINDOW', self.On_close)
        #makes the window strechable
        self.pack(fill='both', expand=True)

      
        #calls subframes and packs them
        self.Sub_frames()
    def Sub_frames(self):
        '''Creates all the subframes'''
        #first, plot row
        self.plots = Frame_plots(self)

        #second, button and display  row
        #self.control = Frame_control(self)



    def On_close(self):
        '''Actions to execute when the master window is closed with ('X')'''
        msg = 'Are you sure you want to terminate the program?'
        if tk.messagebox.askokcancel('Quit', msg):
            #close all plots and figures
            plt.close('all')
            self.parent.destroy()


        
def Error_incomplete():
    '''Lets user know that the content doesnt exist yet'''
    tk.messagebox.showerror('Error', 'The function is not yet implemented!')
    

if __name__ == '__main__':
    '''Initializes tkinter and main application if this is a standalone file'''
    root = tk.Tk()
    Main_application(root)
    root.mainloop()
    



            
