import tkinter as tk 
from tkinter        import ttk, DoubleVar, Canvas, BooleanVar, Scale
from tkinter        import Button, Entry, Frame, Label,StringVar, Checkbutton
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk    import Combobox, Progressbar
from PIL            import Image,ImageTk
import os 
if "win" in os.name:
    from ctypes     import windll
import random
from matplotlib     import pyplot       as plt 
import random 
#from trainer import Trainer
from trainer        import Trainer      as trainer 
from trainerIMG     import TrainerIMG   as trainerIMG
from PIL import Image
from telemetry      import ARCHITECTURES, LOSSES ,OPTIMIZERS, DEFAULTS, ACTIVATIONS
import copy 
from threading      import Thread
import numpy 
import time 
import utilities



class TrainerApp:

    def __init__(self,width,height):
        self.best_game = [] 
        self.best_score = 0
        #Build window 
        self.window         = tk.Tk()
        self.window         .geometry(str(width)+ "x" +str(height))
        self.window.resizable()
        self.window.columnconfigure(0,weight=1)
        self.window.columnconfigure(1,weight=7)

        self.window.rowconfigure(0,weight=1)
        self.window.rowconfigure(1,weight=16)
        self.window.grid()

        #Build general frames
        self.top_frame      = tk.Frame(self.window)
        self.control_frame  = tk.Frame(self.window)
        self.view_frame     = tk.Frame(self.window)
        
        #Assemble General Frames
        self.control_frame.columnconfigure(0,weight=1)
        self.top_frame.grid(row=0,column=0,columnspan=2,sticky=tk.NSEW)
        self.control_frame.grid(row=1,column=0,sticky=tk.NSEW)

        self.view_frame.grid(row=1,column=1,sticky=tk.NSEW)
        self.view_frame.rowconfigure(0,weight=1)
        self.view_frame.rowconfigure(1,weight=2)
        self.view_frame.columnconfigure(0,weight=2)
        self.view_frame.columnconfigure(1,weight=1)
        self.view_frame.columnconfigure(2,weight=2)

        self.top_frame.configure(background="#545C6A")
        self.control_frame.configure(background="#545C6A")
        self.view_frame.configure(background="#545C6A")
       
        #Keep track of settings
        self.settings = {   "gameX"         : None,
                            "gameY"         : None,
                            "iters"         : None,
                            "arch"          : None,
                            "te"            : None,
                            "ps"            : None,
                            "ss"            : None,
                            "bs"            : None,
                            "lr"            : None,
                            "kw"            : None,
                            "ll"            : None,
                            "ep"            : None,
                            "mx"            : None,
                            "lo"            : None,
                            "op"            : None,
                            "ac"            : None,
                            "tr"            : None,
                            "drop"          : None,
                            "gam"           : None,
                            "rew"           : None,
                            "rpick"         : None,
        }

        self.setting_frames = {

                        "gameX" : Frame(self.control_frame,padx=1,pady=1),
                        "gameY" : Frame(self.control_frame,padx=1,pady=1),
                        "iters" : Frame(self.control_frame,padx=1,pady=1),
                        "te"    : Frame(self.control_frame,padx=1,pady=1),
                        "ps"    : Frame(self.control_frame,padx=1,pady=1),
                        "ss"    : Frame(self.control_frame,padx=1,pady=1),
                        "bs"    : Frame(self.control_frame,padx=1,pady=1),
                        "lr"    : Frame(self.control_frame,padx=1,pady=1),
                        "kw"    : Frame(self.control_frame,padx=1,pady=1),
                        "ll"    : Frame(self.control_frame,padx=1,pady=1),
                        "ep"    : Frame(self.control_frame,padx=1,pady=1),
                        "mx"    : Frame(self.control_frame,padx=1,pady=1),
                        "arch"  : Frame(self.control_frame,padx=1,pady=1),
                        "lo"    : Frame(self.control_frame,padx=1,pady=1),
                        "op"    : Frame(self.control_frame,padx=1,pady=1),
                        "ac"    : Frame(self.control_frame,padx=1,pady=1),
                        "tr"    : Frame(self.control_frame,padx=1,pady=1),
                        "drop"  : Frame(self.control_frame,padx=1,pady=1),
                        "gam"   : Frame(self.control_frame,padx=1,pady=1),
                        "rew"   : Frame(self.control_frame,padx=1,pady=1),
                        "rpick" : Frame(self.control_frame,padx=1,pady=1)
        }
        
        for sf in self.setting_frames:
            self.setting_frames[sf].columnconfigure(0,weight=1)
            self.setting_frames[sf].columnconfigure(1,weight=1)
        
        #Build control Frame 
        label_w         =   15
        label_h         =   1
        self.labels    = {      "gameX"     :   Label( self.setting_frames["gameX"],
                                                    text="Game X"),
                                "gameY"     :   Label( self.setting_frames["gameY"],
                                                    text="Game Y"),
                                "iters"     :   Label( self.setting_frames["iters"],
                                                    text="Iters"),
                                "te"        :   Label( self.setting_frames["te"],
                                                    text="Train Rate"),
                                "ps"        :   Label( self.setting_frames["ps"],
                                                    text="Pool Size"),
                                "ss"        :   Label( self.setting_frames["ss"],
                                                    text="Sample Size"),
                                "bs"        :   Label( self.setting_frames["bs"],
                                                    text="Batch Size"),
                                "lr"        :   Label( self.setting_frames['lr'],
                                                    text="Learning Rate"),
                                "kw"        :   Label( self.setting_frames['kw'],
                                                    text="optimizer kwargs"),
                                "ll"        :   Label( self.setting_frames['ll'],
                                                    text="lr progression"),
                                "ep"        :   Label( self.setting_frames["ep"],
                                                    text="Epochs"),
                                "mx"        :   Label( self.setting_frames["mx"],
                                                    text="Max Steps"),
                                "arch"      :   Label( self.setting_frames["arch"],
                                                    text="Arch"),
                                "lo"        :   Label( self.setting_frames["lo"],
                                                    text="Loss Function"),
                                "op"        :   Label( self.setting_frames["op"],
                                                    text="Optimizer"),
                                "ac"        :   Label( self.setting_frames["ac"],
                                                    text="Activation"),
                                "tr"        :   Label( self.setting_frames["tr"],
                                                    text="Transfer Rate"),
                                "drop"      :   Label( self.setting_frames["drop"],
                                                    text="Droput Rate"),
                                "gam"        :   Label( self.setting_frames["gam"],
                                                    text="Gamma γ"),
                                "rew"       :   Label( self.setting_frames['rew'],
                                                    text="Reward"),
                                "rpick"     :   Label( self.setting_frames['rpick'],
                                                    text="Rand Pick Drop")
                                        
        }
        self.game_tracker = []
        self.training_epoch_finished        = False 

        #Prepr Vars
        arch_options    = list(ARCHITECTURES.keys())
        losses_options  = list(LOSSES.keys())
        optim_options   = list(OPTIMIZERS.keys())
        acti_options    = list(ACTIVATIONS.keys())
        entry_w = 10
        self.fields     = {     "gameX"     :   Entry(self.setting_frames["gameX"],width=entry_w),
                                "gameY"     :   Entry(self.setting_frames["gameY"],width=entry_w),
                                "iters"     :   Entry(self.setting_frames["iters"],width=entry_w),
                                "te"        :   Entry(self.setting_frames["te"],width=entry_w),
                                "gameY"     :   Entry(self.setting_frames["gameY"],width=entry_w),
                                "iters"     :   Entry(self.setting_frames["iters"],width=entry_w),
                                "te"        :   Entry(self.setting_frames["te"],width=entry_w),
                                "ps"        :   Entry(self.setting_frames["ps"],width=entry_w),
                                "ss"        :   Entry(self.setting_frames["ss"],width=entry_w),
                                "bs"        :   Entry(self.setting_frames["bs"],width=entry_w),
                                "lr"        :   Entry(self.setting_frames["lr"],width=entry_w),
                                "kw"        :   Entry(self.setting_frames["kw"],width=entry_w+30),
                                "ll"        :   Entry(self.setting_frames["ll"],width=entry_w+30),
                                "ep"        :   Entry(self.setting_frames["ep"],width=entry_w),
                                "mx"        :   Entry(self.setting_frames["mx"],width=entry_w),
                                "arch"      :   Combobox(self.setting_frames["arch"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "lo"        :   Combobox(self.setting_frames["lo"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "op"        :   Combobox(self.setting_frames["op"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "ac"        :   Combobox(self.setting_frames["ac"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "tr"        :   Entry(self.setting_frames["tr"],width=entry_w),
                                "drop"      :   Entry(self.setting_frames["drop"],width=entry_w),
                                "gam"       :   Entry(self.setting_frames['gam'],width=entry_w),
                                "rew"       :   Entry(self.setting_frames['rew'],width=entry_w*3),
                                "rpick"     :   Entry(self.setting_frames['rpick'],width=entry_w*3)
        }

        #Place all Items
        self.fields['arch']['values'] = arch_options
        self.fields['lo']['values'] = losses_options
        self.fields['op']['values'] = optim_options
        self.fields['ac']['values'] = acti_options
        self.fields['arch'].current(1)
        self.fields['lo'].current(0)
        self.fields['op'].current(0)
        self.fields['ac'].current(0)

        for i,(frame,b,f) in enumerate(zip(self.setting_frames,self.labels,self.fields)):
            self.labels[f].grid(row=0,column=0,sticky=tk.W)#(side=tk.LEFT,anchor=tk.E,padx=0,pady=0)
            self.fields[b].grid(row=0,column=1,sticky=tk.E)#pack(side=tk.RIGHT,anchor=tk.W,padx=0,pady=0)
            try:
                self.fields[b].insert(0,str(DEFAULTS[b]))
            except AttributeError:
                pass

            self.setting_frames[frame].grid(row=i+1,column=0,pady=1,padx=0,sticky=tk.NSEW)
        
        

        #Runing Items
        self.run_frame      = Frame(self.control_frame)
        self.run_frame.columnconfigure(0,weight=2)
        self.run_frame.columnconfigure(1,weight=1)
        #self.train_label    = Label(self.run_frame)
        self.train_button   = Button(self.run_frame,text="Train",command=self.run_training)
        self.cancel_button  = Button(self.run_frame,text="Stop",command=self.cancel_training)

        self.cancel_button.grid(row=0,column=0)
        self.train_button.grid(row=0,column=1,sticky=tk.NSEW)
        self.run_frame.grid(row=i+2,column=0,sticky=tk.NSEW)
        
        #Telemetry items
        self.telemetry_frame        = Frame(self.control_frame)
        self.telemetry_frame.columnconfigure(0,weight=1)
        self.telemetry_frame.rowconfigure(0,weight=8)
        self.telemetry_frame.rowconfigure(1,weight=1)
        self.telemetry_frame_title  = Label(self.control_frame,text="TELEMETRY",height=self.train_button.winfo_height()+1)
        self.telemetry_frame_title.grid(row=i+3,column=0,sticky=tk.NSEW,pady=0)

        self.telemetry_box      = ScrolledText(self.telemetry_frame,width=self.run_frame.winfo_width())
        self.telemetry_box.grid(row=0,column=0,sticky=tk.NSEW)
        self.telemetry_frame.grid(row=i+4,column=0,sticky=tk.NSEW)
        
        self.progress_var       = DoubleVar()
        self.progress_var.set(0)
        self.progress_label     = Label(self.telemetry_frame,text="Train Progress")
        self.progress_bar       = Progressbar(self.telemetry_frame,variable=self.progress_var,maximum=1.0)
        self.progress_label.grid(row=2,column=0,columnspan=2,sticky=tk.NSEW)
        self.progress_bar.grid(row=3,column=0,columnspan=2,sticky=tk.NSEW)

        self.stats_frame        = Frame(self.control_frame)
        self.stats_frame.rowconfigure(0,weight=1)
        self.stats_frame.columnconfigure(0,weight=1)
        self.stats_frame.columnconfigure(1,weight=1)
        self.stats_frame.columnconfigure(2,weight=1)
        self.stats_frame.columnconfigure(3,weight=1)


        self.gui_var_step       = None 
        self.gui_var_score      = None 
        self.var_step           = StringVar()
        self.var_score          = StringVar()
        self.var_step.set("0")
        self.var_score.set("0") 
        self.steps_avg_label    = Label(self.stats_frame,text="Steps:",width=5)
        self.steps_output       = Entry(self.stats_frame,state="readonly",width=5,textvariable=self.var_step)
        self.scored_avg_label   = Label(self.stats_frame,text="Score:",width=5)
        self.scored_output      = Entry(self.stats_frame,state="readonly",width=5,textvariable=self.var_score)

        self.steps_avg_label.grid(row=0,column=0)
        self.steps_output.grid(row=0,column=1)
        self.scored_avg_label.grid(row=0,column=2)
        self.scored_output.grid(row=0,column=3)
        self.steps_output.insert(0,"0")
        self.scored_output.insert(0,"0")

        self.stats_frame.grid(row=i+5,column=0,sticky=tk.NSEW)

        self.slider_control = Frame(self.control_frame)
        self.viewer_control = Frame(self.control_frame)

        self.slider_control.grid(row=i+6,column=0,sticky=tk.NSEW)
        self.viewer_control.grid(row=i+7,column=0,sticky=tk.NSEW)

        self.slider_control.rowconfigure(0,weight=1)
        self.slider_control.columnconfigure(0,weight=1)
        self.viewer_control.rowconfigure(0,weight=1)
        self.viewer_control.rowconfigure(1,weight=1)
        self.slider         = Scale(self.slider_control,from_=0,to=100,orient="horizontal")
        self.slider.set(100)
        self.play_button    = Button(self.viewer_control,text="Play",command=self.play_game)
        self.best_button    = Button(self.viewer_control,text="Play Best",command = self.play_best)
        self.slider.grid(row=0,column=0,sticky=tk.NSEW)
        self.play_button.grid(row=0,column=1,sticky=tk.NSEW)
        self.best_button.grid(row=0,column=2,sticky=tk.NSEW)

        self.fps_slide      = Scale(self.control_frame,from_=1,to=60,orient="horizontal")
        self.fps_slide.set(32)
        self.fps_slide.grid(row=i+8,column=0,sticky=tk.NSEW)
        
        #Graph Items 
        self.step_telemetry                         = Frame(self.view_frame,background='gray')
        self.score_telemetry                        = Frame(self.view_frame,background='gray')
        for tel in [self.step_telemetry,self.score_telemetry]:
            tel.rowconfigure(0,weight=2)
            tel.rowconfigure(1,weight=10)
            tel.rowconfigure(2,weight=1)
            tel.columnconfigure(0,weight=1)
        
        self.step_telemetry.grid(row=0,column=0,padx=0,pady=0,sticky=tk.NSEW)
        self.score_telemetry.grid(row=0,column=2,padx=0,pady=0,sticky=tk.NSEW)
        #Graph Titles
        self.step_title                             = Label(self.step_telemetry,background='white',text="Step Telemetry",font=("Arial",10))
        self.score_title                            = Label(self.score_telemetry,background='white',text="Score Telemetry",font=("Ariel",10))
        self.step_canvas                            = Canvas(self.step_telemetry,background='black')
        self.score_canvas                           = Canvas(self.score_telemetry,background='black')
        
        self.step_title.grid(row=0,column=0,sticky=tk.NSEW)
        self.score_title.grid(row=0,column=0,sticky=tk.NSEW)
        self.step_canvas.grid(row=1,column=0,sticky=tk.NSEW)
        self.score_canvas.grid(row=1,column=0,sticky=tk.NSEW)   


        print(f"score {self.score_canvas.winfo_width()},{self.score_canvas.winfo_height()}")

        #Game View Items 
        self.IMG_W                      = 800
        self.IMG_H                      = 800
        self.game_canvas                = Canvas(self.view_frame,background="gray",width=self.IMG_W,height=self.IMG_H)
        self.game_canvas                .grid(row=1,column=0,sticky=tk.NSEW,columnspan=3)
        self.game_image                 = None
    
    def run_loop(self):
        self.window.after(100,self.update)
        self.window.mainloop()
        print("exit window mainloop")

    def set_vars(self):

        for s_key in self.settings:
            if s_key == 'arch':
                self.settings[s_key] = copy.deepcopy(ARCHITECTURES[self.fields[s_key].get()])
            elif s_key == 'lo':
                self.settings[s_key] = LOSSES[self.fields[s_key].get()]

            elif s_key == 'op':
                self.settings[s_key] = OPTIMIZERS[self.fields[s_key].get()]
            
            elif s_key == 'ac':
                self.settings[s_key] = ACTIVATIONS[self.fields[s_key].get()]
            
                self.settings[s_key]    = bool(self.fields[s_key].get())
            elif s_key in ['kw','rew','ll']:
                self.settings[s_key] = eval(self.fields[s_key].get())
            else:
                self.settings[s_key] = float(eval(self.fields[s_key].get()))

    def run_training(self):
        self.set_vars()

        #Reset the vars
        self.best_score             = 0 
        self.best_game              = [] 

        #Start
        self.longest_run        = []
        self.cur_game_steps     = [] 
        self.cur_game_scores    = []
        self.cancel_var         = False 
        self.trainer = trainerIMG( int(self.settings["gameX"]),
                                int(self.settings["gameY"]),
                                visible         = False,
                                loading         = False,
                                loss_fn         = self.settings['lo'],
                                optimizer_fn    = self.settings['op'],
                                kwargs          = dict(self.settings['kw'],**{'lr':self.settings['lr']}),
                                architecture    = self.settings['arch']['arch'],
                                gpu_acceleration= False,
                                m_type          = self.settings['arch']['type'],
                                progress_var    = self.progress_var,
                                output          = self.telemetry_box,
                                steps           = self.gui_var_step,
                                scored          = self.gui_var_score,
                                score_tracker   = self.cur_game_scores,
                                step_tracker    = self.cur_game_steps,
                                best_score      = self.best_score,
                                best_game       = self.best_game,
                                game_tracker    = self.game_tracker,
                                gamma           = self.settings['gam'],
                                instance        = self,
                                dropout_p       = self.settings['drop'],
                                lr_threshs      = self.settings['ll'],
                                activation      = self.settings['ac'],
                                gui=True
                                ) 
        
        
        self.telemetry_box.insert(tk.END,"\n\nTrainer Created Successfully\n")
        self.train_thread = Thread( target=self.trainer.train_concurrent,
                                     kwargs={       "iters":int(self.settings['iters']),
                                                    "train_every":int(self.settings['te']),
                                                    "pool_size":int(self.settings['ps']),
                                                    "sample_size":int(self.settings['ss']),
                                                    "batch_size":int(self.settings['bs']),
                                                    "epochs":int(self.settings['ep']),
                                                    "transfer_models_every":int(self.settings['tr']),
                                                    "rewards":self.settings['rew'],
                                                    "verbose":True,
                                                    "random_pick":True,
                                                    "drop_rate":self.settings['rpick'],
                                                    "max_steps":self.settings['mx']
                                            },
                                     )
        
        self.telemetry_box.insert(tk.END,"Starting train thread\n")
        self.train_thread.start()

    def cancel_training(self):
        self.var_step.set("0")
        self.var_score.set("0") 
        self.cancel_var = True 
        self.progress_var.set(0)
        self.broke_training         = False 
        self.trainer.best_score     = 0 
        self.best_score             = 0 
        self.best_game              = [] 
        try:
            self.telemetry_box.insert(tk.END,"Cancelling Training\n")
            self.trainer            = None 
        except AssertionError as AE:
            print(f"error joining thread")
            print(AE)
            
    def place_steps(self):
        self.step_canvas.update()
        self.step_telemetry.update()
        self.score_telemetry.update()

        steps       = copy.deepcopy(self.cur_game_steps)
        steps       = utilities.reduce_arr(steps,200)


        plt.rcParams["figure.figsize"] = (self.step_canvas.winfo_width()/self.window.winfo_fpixels('1i'),self.step_canvas.winfo_height()/self.window.winfo_fpixels('1i'))
        plt.plot(steps,color='goldenrod')

        plt.savefig("steps.png")
        plt.clf()
        self.step_img = ImageTk.PhotoImage(Image.open("steps.png"))
        self.step_canvas.create_image(self.step_canvas.winfo_width()/2,self.step_canvas.winfo_height()/2,image=self.step_img)

        self.telemetry_box.yview(tk.END)
    
    def place_scores(self): 
        self.score_canvas.update()
        self.step_telemetry.update()
        self.score_telemetry.update()

        scores      = copy.deepcopy(self.cur_game_scores)
        scores      = utilities.reduce_arr(scores,200)

        
 
        plt.rcParams["figure.figsize"] = (self.score_canvas.winfo_width()/self.window.winfo_fpixels('1i'),self.score_canvas.winfo_height()/self.window.winfo_fpixels('1i'))
        plt.plot(scores,color='cyan')

        plt.savefig("scores.png")
        plt.clf()
        self.score_img = ImageTk.PhotoImage(Image.open("scores.png"))
        self.score_canvas.create_image(self.score_canvas.winfo_width()/2,self.score_canvas.winfo_height()/2,image=self.score_img)

    def play_game(self):
        self.FPS = self.fps_slide.get()
        self.set_vars()
        game_to_play = self.slider.get()

        index = int((game_to_play / 100) * len(self.game_tracker))-1

        game = self.game_tracker[index]
        for frame in game:
            t0 = time.time()
            self.place_game_img2(frame)
            while time.time() - t0 < (1/self.FPS):
                time.time()

    def play_best(self):

        self.FPS = self.fps_slide.get()
        self.set_vars()

        game = self.best_game
        for frame in game:
            t0 = time.time()
            self.place_game_img2(frame)
            while time.time() - t0 < (1/self.FPS):
                time.time()

    def place_game_img(self,game):
        green   = (25,245,167)
        red     = (234,45,63)

        t0 = time.time()
        game_x,game_y   = int(self.settings['gameX']),int(self.settings['gameY'])
        
        square_w        = int(self.IMG_W / game_x)
        square_h        = int(self.IMG_H / game_y)
        
        temp_im = Image.new("RGB",(self.IMG_W,self.IMG_H))
        pixs                            = temp_im.load()

        #Create blank img 
        for pack in [(x,y) for x in range(self.IMG_W) for y in range(self.IMG_H)]:
            i,j = pack
            pixs[i,j] = (0,0,0)
        
        #Fill in segments 
        for segment in game['snake']:
            min_x = int(segment[0]*square_w)
            min_y = int(segment[1]*square_h)

            max_x = min_x + square_w
            max_y = min_y + square_h

            for x_i in range(min_x,max_x):
                for y_i in range(min_y,max_y):
                    pixs[x_i,y_i] = green 
            
        min_x   = int(game['food'][0]*square_w)
        min_y   = int(game['food'][1]*square_h)

        max_x   = min_x + square_w
        max_y   = min_y + square_h 

        for x_i in range(min_x,max_x):
                for y_i in range(min_y,max_y):
                    pixs[x_i,y_i] = red 


        self.game_image = temp_im
        self.show_image = ImageTk.PhotoImage(self.game_image)
        self.view_frame.update()
        self.top_x = self.game_canvas.winfo_width()/2 
        self.top_y = self.game_canvas.winfo_height()/2

        self.game_canvas.create_image(self.top_x,self.top_y,image=self.show_image)
        self.game_canvas.update()
        print(f"frametime is {(time.time()-t0):.2f}s")

    def place_game_img2(self,game):
        
        #Define Colors 
        green   = (25,245,167)
        red     = (234,45,63)
        
        #Track frametime
        t0 = time.time()

        # Create base image that ix gamex,gamey
        # It will be scaled 
        grid_w, grid_h  = int(self.settings['gameX']),int(self.settings['gameY'])
        prescaled_image = Image.new("RGB",(grid_w,grid_h))
        pixs                            = prescaled_image.load()
        
        x_scale         = int(self.IMG_W / grid_w)
        y_scale         = int(self.IMG_H / grid_h)
        

        #Create blank img 
        for pack in [(x,y) for x in range(grid_w) for y in range(grid_h)]:
            i,j = pack
            pixs[i,j] = (0,0,0)
        
        #Fill in segments 
        for segment in game['snake']:
            x           = segment[0]
            y           = segment[1]
            pixs[x,y]   = green 
        
        #Fill in food
        x   = game['food'][0]
        y   = game['food'][1]
        pixs[x,y] = red 

        #Scale img up to size 
        self.game_image = prescaled_image.resize((self.IMG_W,self.IMG_H),resample=Image.Resampling.NEAREST)
        self.show_image = ImageTk.PhotoImage(self.game_image)
        self.view_frame.update()
        self.top_x = self.game_canvas.winfo_width()/2 
        self.top_y = self.game_canvas.winfo_height()/2

        self.game_canvas.create_image(self.top_x,self.top_y,image=self.show_image)
        self.game_canvas.update()

    def update(self):
        self.lock                   = True 
        if self.training_epoch_finished:
            self.place_steps()
            self.place_scores()
            self.training_epoch_finished = False

        self.lock                   = False 
        self.window.after(100,self.update)

class TrainerAppNoImg:

    def __init__(self,width,height):
        self.best_game = [] 
        self.best_score = 0
        #Build window 
        self.window         = tk.Tk()
        self.window.title("Yung Charles")
        self.window         .geometry(str(width)+ "x" +str(height))
        self.window.resizable()
        self.window.columnconfigure(0,weight=1)
        self.window.columnconfigure(1,weight=7)

        self.window.rowconfigure(0,weight=1)
        self.window.rowconfigure(1,weight=16)
        self.window.grid()

        #Build general frames
        self.top_frame      = tk.Frame(self.window)
        self.control_frame  = tk.Frame(self.window)
        self.view_frame     = tk.Frame(self.window)
        
        #Assemble General Frames
        self.control_frame.columnconfigure(0,weight=1)

        self.top_frame.grid(row=0,column=0,columnspan=2,sticky=tk.NSEW)
        self.control_frame.grid(row=1,column=0,sticky=tk.NSEW)

        self.view_frame.grid(row=1,column=1,sticky=tk.NSEW)
        self.view_frame.rowconfigure(0,weight=4)
        self.view_frame.rowconfigure(1,weight=5)
        self.view_frame.columnconfigure(0,weight=2)
        self.view_frame.columnconfigure(1,weight=1)
        self.view_frame.columnconfigure(2,weight=2)

        self.top_frame.configure(background="#545C6A")
        self.control_frame.configure(background="#545C6A")
        self.view_frame.configure(background="#545C6A")

        
        #Keep track of settings
        self.settings = {   "gameX"         : None,
                            "gameY"         : None,
                            "ps"            : None,
                            "ss"            : None,
                            "iters"         : None,
                            "arch"          : None,
                            "te"            : None,
                            "bs"            : None,
                            "lr"            : None,
                            "hs"            : None,
                            "kw"            : None,
                            "ll"            : None,
                            "ep"            : None,
                            "mx"            : None,
                            "lo"            : None,
                            "op"            : None,
                            "ac"            : None,
                            "tr"            : None,
                            "drop"          : None,
                            "gam"           : None,
                            "rew"           : None,
                            "rpick"         : None,
        }

        self.setting_frames = {

                        "game_dim" : Frame(self.control_frame,padx=1,pady=1),
                        "samp"    : Frame(self.control_frame,padx=1,pady=1),
                        #"gameY" : Frame(self.control_frame,padx=1,pady=1),
                        "iters" : Frame(self.control_frame,padx=1,pady=1),
                        "te"    : Frame(self.control_frame,padx=1,pady=1),
                        #"ss"    : Frame(self.control_frame,padx=1,pady=1),
                        "bs"    : Frame(self.control_frame,padx=1,pady=1),
                        "lr"    : Frame(self.control_frame,padx=1,pady=1),
                        "hs"    : Frame(self.control_frame,padx=1,pady=1),
                        "kw"    : Frame(self.control_frame,padx=1,pady=1),
                        "ll"    : Frame(self.control_frame,padx=1,pady=1),
                        "ep"    : Frame(self.control_frame,padx=1,pady=1),
                        "mx"    : Frame(self.control_frame,padx=1,pady=1),
                        "arch"  : Frame(self.control_frame,padx=1,pady=1),
                        "lo"    : Frame(self.control_frame,padx=1,pady=1),
                        "op"    : Frame(self.control_frame,padx=1,pady=1),
                        "ac"    : Frame(self.control_frame,padx=1,pady=1),
                        "tr"    : Frame(self.control_frame,padx=1,pady=1),
                        "drop"  : Frame(self.control_frame,padx=1,pady=1),
                        "gam"   : Frame(self.control_frame,padx=1,pady=1),
                        "rew"   : Frame(self.control_frame,padx=1,pady=1),
                        "rpick" : Frame(self.control_frame,padx=1,pady=1)
        }
        
        for sf in self.setting_frames:
            self.setting_frames[sf].rowconfigure(0,weight=1)
            self.setting_frames[sf].columnconfigure(0,weight=1)
            self.setting_frames[sf].columnconfigure(1,weight=1)

            if sf == "game_dim" or sf == "samp":
                self.setting_frames[sf].columnconfigure(2,weight=1)
                self.setting_frames[sf].columnconfigure(3,weight=1)

        
        
        #Build control Frame 
        self.labels    = {      "gameX"     :   Label( self.setting_frames["game_dim"],
                                                    text="Game X"),
                                "gameY"     :   Label( self.setting_frames["game_dim"],
                                                    text="Game Y"),
                                "ps"        :   Label( self.setting_frames["samp"],
                                                    text="Pool Size"),
                                "ss"        :   Label( self.setting_frames["samp"],
                                                    text="Sample Size"),
                                "iters"     :   Label( self.setting_frames["iters"],
                                                    text="Iters"),
                                "te"        :   Label( self.setting_frames["te"],
                                                    text="Train Rate"),
                                "bs"        :   Label( self.setting_frames["bs"],
                                                    text="Batch Size"),
                                "lr"        :   Label( self.setting_frames['lr'],
                                                    text="Learning Rate"),
                                "hs"        :   Label( self.setting_frames['hs'],
                                                    text="History Len"),
                                "kw"        :   Label( self.setting_frames['kw'],
                                                    text="optimizer kwargs"),
                                "ll"        :   Label( self.setting_frames['ll'],
                                                    text="lr progression"),
                                "ep"        :   Label( self.setting_frames["ep"],
                                                    text="Epochs"),
                                "mx"        :   Label( self.setting_frames["mx"],
                                                    text="Max Steps"),
                                "arch"      :   Label( self.setting_frames["arch"],
                                                    text="Arch"),
                                "lo"        :   Label( self.setting_frames["lo"],
                                                    text="Loss Function"),
                                "op"        :   Label( self.setting_frames["op"],
                                                    text="Optimizer"),
                                "ac"        :   Label( self.setting_frames["ac"],
                                                    text="Activation"),
                                "tr"        :   Label( self.setting_frames["tr"],
                                                    text="Transfer Rate"),
                                "drop"      :   Label( self.setting_frames["drop"],
                                                    text="Droput Rate"),
                                "gam"        :   Label( self.setting_frames["gam"],
                                                    text="Gamma γ"),
                                "rew"       :   Label( self.setting_frames['rew'],
                                                    text="Reward"),
                                "rpick"     :   Label( self.setting_frames['rpick'],
                                                    text="Rand Pick Drop")
                                        
        }

        
        self.game_tracker = []
        self.training_epoch_finished        = False 

        #Prepr Vars
        arch_options    = list(ARCHITECTURES.keys())
        losses_options  = list(LOSSES.keys())
        optim_options   = list(OPTIMIZERS.keys())
        acti_options    = list(ACTIVATIONS.keys())
        entry_w = 10
        self.fields     = {     "gameX"     :   Entry(self.setting_frames["game_dim"],width=entry_w),
                                "gameY"     :   Entry(self.setting_frames["game_dim"],width=entry_w),
                                "ps"        :   Entry(self.setting_frames["samp"],width=entry_w),
                                "ss"        :   Entry(self.setting_frames["samp"],width=entry_w),
                                "iters"     :   Entry(self.setting_frames["iters"],width=entry_w),
                                "te"        :   Entry(self.setting_frames["te"],width=entry_w),
                                "bs"        :   Entry(self.setting_frames["bs"],width=entry_w),
                                "lr"        :   Entry(self.setting_frames["lr"],width=entry_w),
                                "hs"        :   Entry(self.setting_frames["hs"],width=entry_w),
                                "kw"        :   Entry(self.setting_frames["kw"],width=entry_w+30),
                                "ll"        :   Entry(self.setting_frames["ll"],width=entry_w+30),
                                "ep"        :   Entry(self.setting_frames["ep"],width=entry_w),
                                "mx"        :   Entry(self.setting_frames["mx"],width=entry_w),
                                "arch"      :   Combobox(self.setting_frames["arch"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "lo"        :   Combobox(self.setting_frames["lo"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "op"        :   Combobox(self.setting_frames["op"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "ac"        :   Combobox(self.setting_frames["ac"],width=entry_w+2,textvariable=self.settings['arch'],state="readonly"),
                                "tr"        :   Entry(self.setting_frames["tr"],width=entry_w),
                                "drop"      :   Entry(self.setting_frames["drop"],width=entry_w),
                                "gam"       :   Entry(self.setting_frames['gam'],width=entry_w),
                                "rew"       :   Entry(self.setting_frames['rew'],width=entry_w*3),
                                "rpick"     :   Entry(self.setting_frames['rpick'],width=entry_w*3)
        }

        #Place all Items
        self.fields['arch']['values'] = arch_options
        self.fields['lo']['values'] = losses_options
        self.fields['op']['values'] = optim_options
        self.fields['ac']['values'] = acti_options
        self.fields['arch'].current(1)
        self.fields['lo'].current(0)
        self.fields['op'].current(0)
        self.fields['ac'].current(0)

        
        for i,(b,f) in enumerate(zip(self.labels,self.fields)):
            frame = b
            if f == "gameX" or f == "ps":
                frame   = "game_dim" if f == "gameX" else "samp"
                self.labels[f].grid(row=0,column=0,sticky=tk.W)
                self.fields[b].grid(row=0,column=1,sticky=tk.W)

            if f == "gameY" or f == "ss":
                frame   = "game_dim" if f == "gameY" else "samp"
                self.labels[f].grid(row=0,column=2,sticky=tk.E)
                self.fields[b].grid(row=0,column=3,sticky=tk.E)
            else:
                self.labels[f].grid(row=0,column=0,sticky=tk.W)#(side=tk.LEFT,anchor=tk.E,padx=0,pady=0)
                self.fields[b].grid(row=0,column=1,sticky=tk.E)#pack(side=tk.RIGHT,anchor=tk.W,padx=0,pady=0)
            try:
                self.fields[b].insert(0,str(DEFAULTS[b]))
            except AttributeError:
                pass
            print(f"packing {(b,f)}]")
            self.setting_frames[frame].grid(row=i+1,column=0,pady=1,padx=0,sticky=tk.NSEW)
        
        #self.setting_frames["samp"].grid(row=i+1,column=0,sticky=tk.NSEW)
        
        i += 1
        #Runing Items
        self.run_frame      = Frame(self.control_frame)
        self.run_frame.columnconfigure(0,weight=2)
        self.run_frame.columnconfigure(1,weight=1)
        #self.train_label    = Label(self.run_frame)
        self.train_button   = Button(self.run_frame,text="Train",command=self.run_training)
        self.cancel_button  = Button(self.run_frame,text="Stop",command=self.cancel_training)

        self.cancel_button.grid(row=0,column=0)
        self.train_button.grid(row=0,column=1,sticky=tk.NSEW)
        self.run_frame.grid(row=i+1,column=0,sticky=tk.NSEW)
        
        #Telemetry items
        self.telemetry_frame        = Frame(self.control_frame)
        self.telemetry_frame.columnconfigure(0,weight=1)
        self.telemetry_frame.rowconfigure(0,weight=1)
        self.telemetry_frame.rowconfigure(1,weight=1)
        self.telemetry_frame_title  = Label(self.control_frame,text="TELEMETRY",height=self.train_button.winfo_height()+1)
        self.telemetry_frame_title.grid(row=i+3,column=0,sticky=tk.EW,pady=0)

        self.telemetry_box      = ScrolledText(self.telemetry_frame,width=self.run_frame.winfo_width(),height=8)
        self.telemetry_box.grid(row=0,column=0,sticky=tk.EW)
        self.telemetry_frame.grid(row=i+4,column=0,sticky=tk.EW)
        
        self.progress_var       = DoubleVar()
        self.progress_var.set(0)
        self.progress_label     = Label(self.telemetry_frame,text="Train Progress")
        self.progress_bar       = Progressbar(self.telemetry_frame,variable=self.progress_var,maximum=1.0)
        self.progress_label.grid(row=2,column=0,columnspan=2,sticky=tk.NSEW)
        self.progress_bar.grid(row=3,column=0,columnspan=2,sticky=tk.NSEW)

        self.stats_frame        = Frame(self.control_frame)
        self.stats_frame.rowconfigure(0,weight=1)
        self.stats_frame.columnconfigure(0,weight=1)
        self.stats_frame.columnconfigure(1,weight=1)
        self.stats_frame.columnconfigure(2,weight=1)
        self.stats_frame.columnconfigure(3,weight=1)
        self.stats_frame.columnconfigure(4,weight=1)
        self.stats_frame.columnconfigure(5,weight=1)


        self.gui_var_step       = None 
        self.gui_var_score      = None 
        self.gui_var_error      = None 
        self.var_step           = StringVar()
        self.var_score          = StringVar()
        self.var_error          = StringVar()
        self.var_step.set("0")
        self.var_score.set("0") 
        self.var_error.set("0") 
        self.steps_avg_label    = Label(self.stats_frame,text="Steps:",width=5)
        self.steps_output       = Entry(self.stats_frame,state="readonly",width=5,textvariable=self.var_step)
        self.scored_avg_label   = Label(self.stats_frame,text="Score:",width=5)
        self.scored_output      = Entry(self.stats_frame,state="readonly",width=5,textvariable=self.var_score)
        self.error_avg_label    = Label(self.stats_frame,text="Error:",width=5)
        self.error_output       = Entry(self.stats_frame,state="readonly",width=8,textvariable=self.var_error)

        self.steps_avg_label.grid(row=0,column=0)
        self.steps_output.grid(row=0,column=1)
        self.scored_avg_label.grid(row=0,column=2)
        self.scored_output.grid(row=0,column=3)
        self.error_avg_label.grid(row=0,column=4)
        self.error_output.grid(row=0,column=5)

        self.steps_output.insert(0,"0")
        self.scored_output.insert(0,"0")
        self.error_output.insert(0,"0")

        self.stats_frame.grid(row=i+5,column=0,sticky=tk.NSEW)

        self.slider_control = Frame(self.control_frame)
        self.viewer_control = Frame(self.control_frame)

        self.slider_control.grid(row=i+6,column=0,sticky=tk.NSEW)
        self.viewer_control.grid(row=i+7,column=0,sticky=tk.NSEW)

        self.slider_control.rowconfigure(0,weight=1)
        self.slider_control.columnconfigure(0,weight=1)
        self.viewer_control.rowconfigure(0,weight=1)
        self.viewer_control.rowconfigure(1,weight=1)
        self.slider         = Scale(self.slider_control,from_=0,to=100,orient="horizontal")
        self.slider.set(100)
        self.play_button    = Button(self.viewer_control,text="Play",command=self.play_game)
        self.best_button    = Button(self.viewer_control,text="Play Best",command = self.play_best)
        self.slider.grid(row=0,column=0,sticky=tk.NSEW)
        self.play_button.grid(row=0,column=1,sticky=tk.NSEW)
        self.best_button.grid(row=0,column=2,sticky=tk.NSEW)

        self.fps_slide      = Scale(self.control_frame,from_=1,to=60,orient="horizontal")
        self.fps_slide.set(32)
        self.fps_slide.grid(row=i+8,column=0,sticky=tk.NSEW)
        
        #Graph Items 
        self.step_telemetry                         = Frame(self.view_frame,background='gray')
        self.score_telemetry                        = Frame(self.view_frame,background='gray')
        for tel in [self.step_telemetry,self.score_telemetry]:
            tel.rowconfigure(0,weight=2)
            tel.rowconfigure(1,weight=10)
            tel.rowconfigure(2,weight=1)
            tel.columnconfigure(0,weight=1)
        
        self.step_telemetry.grid(row=0,column=0,padx=0,pady=0,sticky=tk.NSEW)
        self.score_telemetry.grid(row=0,column=2,padx=0,pady=0,sticky=tk.NSEW)
        #Graph Titles
        self.step_title                             = Label(self.step_telemetry,background='white',text="Step Telemetry",font=("Arial",10))
        self.score_title                            = Label(self.score_telemetry,background='white',text="Score Telemetry",font=("Ariel",10))
        self.step_canvas                            = Canvas(self.step_telemetry,background='black')
        self.score_canvas                           = Canvas(self.score_telemetry,background='black')
        
        self.step_title.grid(row=0,column=0,sticky=tk.NSEW)
        self.score_title.grid(row=0,column=0,sticky=tk.NSEW)
        self.step_canvas.grid(row=1,column=0,sticky=tk.NSEW)
        self.score_canvas.grid(row=1,column=0,sticky=tk.NSEW)   


        print(f"score {self.score_canvas.winfo_width()},{self.score_canvas.winfo_height()}")

        #Game View Items 
        self.IMG_W                      = 550
        self.IMG_H                      = 550
        self.game_canvas                = Canvas(self.view_frame,background="gray",width=self.IMG_W,height=self.IMG_H)
        self.game_canvas                .grid(row=1,column=0,sticky=tk.NSEW,columnspan=3)
        self.game_image                 = None
    
    def run_loop(self):
        self.window.after(100,self.update)
        self.window.mainloop()
        print("exit window mainloop")

    def set_vars(self):

        for s_key in self.settings:
            if s_key == 'arch':
                self.settings[s_key] = copy.deepcopy(ARCHITECTURES[self.fields[s_key].get()])
            elif s_key == 'lo':
                self.settings[s_key] = LOSSES[self.fields[s_key].get()]

            elif s_key == 'op':
                self.settings[s_key] = OPTIMIZERS[self.fields[s_key].get()]
            
            elif s_key == 'ac':
                self.settings[s_key] = ACTIVATIONS[self.fields[s_key].get()]
            
            elif s_key in ['kw','rew','ll']:
                self.settings[s_key] = eval(self.fields[s_key].get())
            elif s_key  in ['hs']:
                self.settings[s_key]    = int(eval(self.fields[s_key].get()))
            else:
                self.settings[s_key] = float(eval(self.fields[s_key].get()))

    def run_training(self):
        self.set_vars()

        #Reset the vars
        self.best_score             = 0 
        self.best_game              = [] 

        #Start
        self.longest_run        = []
        self.cur_game_steps     = [] 
        self.cur_game_scores    = []
        self.cancel_var         = False 
        self.trainer = trainer( int(self.settings["gameX"]),
                                int(self.settings["gameY"]),
                                visible         = False,
                                loading         = False,
                                loss_fn         = self.settings['lo'],
                                optimizer_fn    = self.settings['op'],
                                history         = self.settings['hs'],
                                kwargs          = dict(self.settings['kw'],**{'lr':self.settings['lr']}),
                                progress_var    = self.progress_var,
                                output          = self.telemetry_box,
                                steps           = self.gui_var_step,
                                scored          = self.gui_var_score,
                                score_tracker   = self.cur_game_scores,
                                step_tracker    = self.cur_game_steps,
                                best_score      = self.best_score,
                                best_game       = self.best_game,
                                game_tracker    = self.game_tracker,
                                gamma           = self.settings['gam'],
                                instance        = self,
                                dropout_p       = self.settings['drop'],
                                lr_threshs      = self.settings['ll'],
                                activation      = self.settings['ac'],
                                gui=True
                                ) 
        
        
        self.telemetry_box.insert(tk.END,"\n\nTrainer Created Successfully\n")
        self.train_thread = Thread( target=self.trainer.train_concurrent,
                                     kwargs={       "iters":int(self.settings['iters']),
                                                    "train_every":int(self.settings['te']),
                                                    "pool_size":int(self.settings['ps']),
                                                    "sample_size":int(self.settings['ss']),
                                                    "batch_size":int(self.settings['bs']),
                                                    "epochs":int(self.settings['ep']),
                                                    "transfer_models_every":int(self.settings['tr']),
                                                    "rewards":self.settings['rew'],
                                                    "verbose":False,
                                                    "random_pick":True,
                                                    "drop_rate":self.settings['rpick'],
                                                    "max_steps":self.settings['mx']
                                            },
                                     )
        
        self.telemetry_box.insert(tk.END,"Starting train thread\n")
        self.train_thread.start()

    def cancel_training(self):
        self.var_step.set("0")
        self.var_score.set("0") 
        self.cancel_var = True 
        self.progress_var.set(0)
        self.broke_training         = False 
        self.trainer.best_score     = 0 
        self.best_score             = 0 
        self.best_game              = [] 
        try:
            self.telemetry_box.insert(tk.END,"Cancelling Training\n")
            self.trainer            = None 
        except AssertionError as AE:
            print(f"error joining thread")
            print(AE)
            
    def place_steps(self):
        self.step_canvas.update()
        self.step_telemetry.update()
        self.score_telemetry.update()

        steps       = copy.deepcopy(self.cur_game_steps)
        steps       = utilities.reduce_arr(steps,100)


        plt.rcParams["figure.figsize"] = (self.step_canvas.winfo_width()/self.window.winfo_fpixels('1i'),self.step_canvas.winfo_height()/self.window.winfo_fpixels('1i'))
        plt.plot(steps,color='goldenrod')

        plt.savefig("steps.png")
        plt.clf()
        self.step_img = ImageTk.PhotoImage(Image.open("steps.png"))
        self.step_canvas.create_image(self.step_canvas.winfo_width()/2,self.step_canvas.winfo_height()/2,image=self.step_img)

        self.telemetry_box.yview(tk.END)
    
    def place_scores(self): 
        self.score_canvas.update()
        self.step_telemetry.update()
        self.score_telemetry.update()

        scores      = copy.deepcopy(self.cur_game_scores)
        scores      = utilities.reduce_arr(scores,100)

        plt.rcParams["figure.figsize"] = (self.score_canvas.winfo_width()/self.window.winfo_fpixels('1i'),self.score_canvas.winfo_height()/self.window.winfo_fpixels('1i'))
        plt.plot(scores,color='cyan')
        
        plt.savefig("scores.png")
        plt.clf()
        self.score_img = ImageTk.PhotoImage(Image.open("scores.png"))
        self.score_canvas.create_image(self.score_canvas.winfo_width()/2,self.score_canvas.winfo_height()/2,image=self.score_img)

    def play_game(self):
        self.FPS = self.fps_slide.get()
        self.set_vars()
        game_to_play = self.slider.get()

        index = int((game_to_play / 100) * len(self.game_tracker))-1

        game = self.game_tracker[index]
        for frame in game:
            t0 = time.time()
            self.place_game_img2(frame)
            while time.time() - t0 < (1/self.FPS):
                time.time()

    def play_best(self):

        self.FPS = self.fps_slide.get()
        self.set_vars()

        game = self.best_game
        for frame in game:
            t0 = time.time()
            self.place_game_img2(frame)
            while time.time() - t0 < (1/self.FPS):
                time.time()

    def place_game_img(self,game):
        green   = (25,245,167)
        red     = (234,45,63)

        t0 = time.time()
        game_x,game_y   = int(self.settings['gameX']),int(self.settings['gameY'])
        
        square_w        = int(self.IMG_W / game_x)
        square_h        = int(self.IMG_H / game_y)
        
        temp_im = Image.new("RGB",(self.IMG_W,self.IMG_H))
        pixs                            = temp_im.load()

        #Create blank img 
        for pack in [(x,y) for x in range(self.IMG_W) for y in range(self.IMG_H)]:
            i,j = pack
            pixs[i,j] = (0,0,0)
        
        #Fill in segments 
        for segment in game['snake']:
            min_x = int(segment[0]*square_w)
            min_y = int(segment[1]*square_h)

            max_x = min_x + square_w
            max_y = min_y + square_h

            for x_i in range(min_x,max_x):
                for y_i in range(min_y,max_y):
                    pixs[x_i,y_i] = green 
            
        min_x   = int(game['food'][0]*square_w)
        min_y   = int(game['food'][1]*square_h)

        max_x   = min_x + square_w
        max_y   = min_y + square_h 

        for x_i in range(min_x,max_x):
                for y_i in range(min_y,max_y):
                    pixs[x_i,y_i] = red 


        self.game_image = temp_im
        self.show_image = ImageTk.PhotoImage(self.game_image)
        self.view_frame.update()
        self.top_x = self.game_canvas.winfo_width()/2 
        self.top_y = self.game_canvas.winfo_height()/2

        self.game_canvas.create_image(self.top_x,self.top_y,image=self.show_image)
        self.game_canvas.update()
        print(f"frametime is {(time.time()-t0):.2f}s")

    def place_game_img2(self,game):
        
        #Define Colors 
        green   = (25,245,167)
        red     = (234,45,63)
        
        #Track frametime
        t0 = time.time()

        # Create base image that ix gamex,gamey
        # It will be scaled 
        grid_w, grid_h  = int(self.settings['gameX']),int(self.settings['gameY'])
        prescaled_image = Image.new("RGB",(grid_w,grid_h))
        pixs                            = prescaled_image.load()
        
        x_scale         = int(self.IMG_W / grid_w)
        y_scale         = int(self.IMG_H / grid_h)
        

        #Create blank img 
        for pack in [(x,y) for x in range(grid_w) for y in range(grid_h)]:
            i,j = pack
            pixs[i,j] = (0,0,0)
        
        #Fill in segments 
        for segment in game['snake']:
            x           = segment[0]
            y           = segment[1]
            pixs[x,y]   = green 
        
        #Fill in food
        x   = game['food'][0]
        y   = game['food'][1]
        pixs[x,y] = red 

        #Scale img up to size 
        self.game_image = prescaled_image.resize((self.IMG_W,self.IMG_H),resample=Image.Resampling.NEAREST)
        self.show_image = ImageTk.PhotoImage(self.game_image)
        self.view_frame.update()
        self.top_x = self.game_canvas.winfo_width()/2 
        self.top_y = self.game_canvas.winfo_height()/2

        self.game_canvas.create_image(self.top_x,self.top_y,image=self.show_image)
        self.game_canvas.update()

    def update(self):
        self.lock                   = True 
        if self.training_epoch_finished:
            self.place_steps()
            self.place_scores()
            self.training_epoch_finished = False

        self.lock                   = False 
        self.window.after(100,self.update)

if __name__ == "__main__":
    #    OPTIONS                                        GAME 

    #Create the root frame 
    try:
        ta = TrainerAppNoImg(1200,800)

        ta.run_loop()
    
    except Exception as e:
        print(e)





