import tkinter as tk
import time
import random
import utilitaires
from utilitairesPays import continent_codes
import utilitairesPays
import mapManager as mapM
from tkinter import messagebox
from tkinter import ttk
backG = "#F9F7F7"

primaryColor = "#3F72AF"
secondColor = "#112D4E"
thirdColor = "#DBE2EF"
fourthColor = "#3c5370"
fontName = "verdana"

#style  =utilitaires.getStyle()
favoriteCities = utilitaires.getListFavoriteCities()

def changeColorStar(C,starId):
    if C.itemcget(starId, "fill") == backG:
        C.itemconfig(starId,fill = primaryColor)
    else:
        C.itemconfig(starId,fill = backG)


class EnterCity(tk.Frame):
    def __init__(self, parent, controller):
        
        super().__init__(parent)
        self.controller = controller

        self.title  = tk.Label(self, text = "Enter City name",font =(fontName,30), fg = secondColor,bg= backG)

        self.entry = tk.Entry(self,font =(fontName,20), fg = primaryColor , relief=tk.FLAT, bd = 8, insertbackground = primaryColor)
        self.entry.bind('<Return>', lambda event: self.SetGuess())
        
        style = utilitaires.getStyle()
        self.search = ttk.Button(self, text="search city", style='SearchCity.TButton',command = self.SetGuess)
        #self.search = tk.Button(self,text = "search city", font =(fontName,25),fg = secondColor,activeforeground = primaryColor,
                   #relief = tk.FLAT,command = self.SetGuess,bg = backG,activebackground=backG)
        
        self.menuButton = tk.Menubutton(self, text="Favourite cities",font =(fontName,20) ,fg=secondColor, bg=backG,
                                        activeforeground = primaryColor )
       
        self.menu = tk.Menu(self.menuButton,fg = primaryColor ,bg = backG,font =(fontName,20),tearoff=20)
        self.menuButton["menu"] = self.menu
        self.update_menu_items()
        
        self.entry.focus()
            
        self.title.pack()
        self.entry.pack()
        self.search.pack(pady = 10)
        self.menuButton.pack()
    
    def onDisplay(self): # when you switch window its called
        self.entry.focus()
        self.title.config(text = "Enter City name" )
        self.entry.delete(0, tk.END)
        self.update_menu_items()
        # add updating the favourite cities
    
    def SetGuess(self,name = "none"):
        name = name if name != "none" else self.entry.get()
    
        if not name:
            self.title.config(text="Please enter a city name")
            return

        currentTemperature = utilitaires.getTemperature(name)

        if currentTemperature:
            app.changeFrame("GuessWindow")
            app.frames["GuessWindow"].configure(name, currentTemperature)
        else:
            self.title.config(text="City Not Found")
            self.entry.delete(0, tk.END)

    def update_menu_items(self):
    # Clear existing menu items
        self.menu.delete(0, tk.END)
        # Add new menu items from favoriteCities
        for city in favoriteCities:
            self.menu.add_command(label=city, command=lambda c=city: self.SetGuess(name=c))
 

class GuessWindow(tk.Frame):
    def __init__(self, parent, controller):
        
        super().__init__(parent)
        self.controller = controller  # Store reference to the main application


        UnitWidht = 120 # creating the widget for unit choosing
        UnitLenght = UnitWidht/3
        self.change = tk.Canvas(self,width =UnitWidht,height=UnitLenght,bg = backG,highlightthickness=1, highlightbackground=secondColor )
        
        self.change.pack(anchor = "ne",padx = 20,pady = 10)
        self.rec  = self.change.create_rectangle(0,0,UnitLenght+1,UnitLenght+1,outline=backG,fill=primaryColor)
        self.change.create_text((UnitWidht/8)+2,UnitLenght/2,fill= secondColor,text = "°C",font=(fontName,20))
        self.change.create_text(UnitWidht- UnitWidht/8,UnitLenght/2,fill= secondColor,text = "°F",font=(fontName,20))

        self.change.bind("<Button-1>",self.changeValue)
        
        self.title  = tk.Label(self, text = "Guess the temperature",font =(fontName,30), fg = secondColor,bg =backG)
        self.title.pack()


        self.spinbox = tk.Spinbox(self, from_=-100, to=100, width=10,font=(fontName, 34), bg="white", fg=primaryColor,insertbackground = primaryColor)
        self.spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=False)
        self.spinbox.insert(0, 0)
        self.spinbox.bind('<Return>',lambda event:  self.checkAnswer())
        
        self.spinbox.bind('<Escape>', lambda event: self.returnBack())

        style = utilitaires.getStyle()
        checkTemperature = tk.Button(self, text = "Check Guess", font=(fontName, 12),activeforeground =primaryColor, fg=secondColor,command=self.checkAnswer)
        #checkTemperature = ttk.Button(self, text="Check Guess", style='CheckGuess.TButton',command=self.checkAnswer)

        hbox = tk.Frame(self, padx=5, pady=5,bg = backG)
        hbox.pack(side='top', anchor='n')  # Anchor to the top right corner
        
        self.cityLabel = tk.Label(hbox,font =(fontName,20),fg = secondColor,bg=backG)
        self.cityLabel.pack(padx=20,side = "left") # making the widget for making a city in favourites
        w = 40
        h = 40
        self.canva = tk.Canvas(hbox,width=w,height=h,bg = backG, highlightthickness=0)
        self.canva.pack(side = "right")
        self.starId = utilitaires.create_star(self.canva,w/2,h/2,18,5,backG,secondColor)
        
       
        self.Temperature_Unit = True
        self.numberSteps = 0
            
           
        def starClicked(event):
            changeColorStar(self.canva,self.starId)

            if self.city not in favoriteCities:
                favoriteCities.add(self.city)
                print("we are addingv",self.city )
            else:
                favoriteCities.remove(self.city)
        self.canva.tag_bind("star", "<Button>", starClicked)
        
        self.spinbox.pack(padx=20, pady=20)
        
        checkTemperature.pack()
    
    
    def returnBack(self):
        app.changeFrame("EnterCity")
    
    def changeValue(self,event):
            if self.Temperature_Unit:
                self.change.move(self.rec, 10, 0)
            else:
                self.change.move(self.rec, -10, 0)
            self.numberSteps+=1
            if self.numberSteps==8:
                self.numberSteps = 0
                self.Temperature_Unit = not self.Temperature_Unit
                self.temperature = self.TemperatureC if self.Temperature_Unit else self.TemperatureF
                
            else:
                self.after(10,self.changeValue,event)
           
    
    def onDisplay(self): # when you switch window its called
        self.title.config(text = "Guess the temperature")
        self.spinbox.focus()
        self.spinbox.delete(0,tk.END)
        self.canva.itemconfig(self.starId,fill = backG)

        
    
    def reset(self):
        app.changeFrame("EnterCity")
       
    
    def configure(self,city,temperature):
        self.city  = city
        self.TemperatureC = int(utilitaires.kelvin_to_celcius(temperature))
        self.TemperatureF = int(utilitaires.kelvin_to_farenheit(temperature))

        self.temperature = self.TemperatureC if self.Temperature_Unit else self.TemperatureF
        
        self.cityLabel.config(text = city)

        if self.city in favoriteCities:
            self.canva.itemconfig(self.starId,fill = primaryColor)
        
    def checkAnswer(self):

        digits = set("0123456789")
        value = self.spinbox.get()
        check = True
        if not value or value.isspace(): 
            check = False
        
        for i in value:
            if not digits.__contains__(i):
                message = tk.Label(self,text ="incorrect entry",fg =primaryColor, font=(fontName,10),bg = backG)
                message.pack(pady = 5)
                self.spinbox.delete(0,tk.END)
                self.after(1500,message.pack_forget)
                check = False
                break

        if check:            
            value = int(value)
            print(value)    
            
            if value > self.temperature:
                self.title.configure(text = "The Temperature is lower")
            elif value < self.temperature:
                self.title.configure(text = "The Temperature is higher")
            else:
                self.title.configure(text = "Congrats")
                app.after(800, self.reset)

class chooseGamemode(tk.Frame):
    def __init__(self, parent, controller):

        self.numberOfSteps = 0
        self.gameModes = ["peaceful","against the clock","best score","best score V2","big brainer"]
        
        self.current = 2

        super().__init__(parent)
        self.controller = controller

        self.title = tk.Label(self,text = "choose game settings",font=(fontName,35,"bold"),fg = secondColor,bg =backG)
        self.title.pack()

        He = 56
        Wi = 420
        self.typeGuess = tk.Canvas(self,bg = backG,highlightthickness=2,width=Wi,height=He,highlightbackground=fourthColor)

        self.capital = self.typeGuess.create_rectangle(Wi/3,0,Wi*2/3,He+3,fill=backG, outline="")
        self.country = self.typeGuess.create_rectangle(Wi*2/3,0,Wi+3,He+3,fill=backG, outline="")
        self.city = self.typeGuess.create_rectangle(0,0,Wi/3,He+3,fill=backG,outline = "")
        self.RecChoice = self.typeGuess.create_rectangle(0,0,Wi/3,He+3,fill=fourthColor,outline = "")

        self.typeGuess.tag_bind(self.capital,"<Button-1>", lambda event: self.changeType("capital"))
        self.typeGuess.tag_bind(self.country,"<Button-1>", lambda event: self.changeType("country"))
        self.typeGuess.tag_bind(self.city,"<Button-1>", lambda event: self.changeType("city"))

        self.city = self.typeGuess.create_text(Wi * 0.1, He / 2, anchor='w', fill=backG, text="city", font=(fontName, 18,"bold"),activefill=primaryColor)
        self.capital = self.typeGuess.create_text(Wi / 2, He / 2, anchor='center', fill=fourthColor, text="capital", font=(fontName, 18,"bold"),activefill=primaryColor)
        self.country = self.typeGuess.create_text(Wi * 0.95, He / 2, anchor='e', fill=fourthColor, text="country", font=(fontName, 18,"bold"),activefill=primaryColor)
        self.typeGuess.pack(pady =20)
        
        self.currentType = "city"
        self.currentTypePos = {"city": Wi/3,"capital":Wi,"country":Wi*1.68}
        self.currentTypeTexts = {"city": self.city,"capital":self.capital,"country":self.country}

        self.typeGuess.tag_bind(self.capital,"<Button-1>", lambda event: self.changeType("capital"))
        self.typeGuess.tag_bind(self.country,"<Button-1>", lambda event: self.changeType("country"))
        self.typeGuess.tag_bind(self.city,"<Button-1>", lambda event: self.changeType("city"))

        self.changeType("country")

        hbox = tk.Frame(self, padx=10, pady=10,bg = backG)
        hbox.pack(side='top', anchor="center") 

        self.arrowH = 50
        self.arrowL = 50
        
        self.leftArrow = tk.Canvas(hbox,height=self.arrowH,width=self.arrowL,bg = backG,highlightthickness =0)
        self.rightArrow = tk.Canvas(hbox,height=self.arrowH,width=self.arrowL,bg = backG, highlightthickness = 0)
        self.leftArrow.create_polygon(utilitaires.getTriangleCoordinates(self.arrowH,self.arrowL,1),fill = secondColor,activefill=primaryColor)
        self.rightArrow.create_polygon(utilitaires.getTriangleCoordinates(self.arrowH,self.arrowL,0),fill = secondColor,activefill=primaryColor)
        
        border = tk.Frame(hbox,bg = secondColor,height=80)
        self.labelGamemode = tk.Label(border,text ="best score",font = (fontName,24,"bold"),fg= backG,bg = secondColor,width = 14, anchor='center',)
        
        self.labelGamemode.pack(pady =3,padx = 17)
        self.leftArrow.pack(side = "left")
        border.pack(side="left",padx =5,pady =20)
        self.rightArrow.pack(side = "right")

        self.leftArrow.bind("<Button-1>", lambda event: self.changeGamemode(-1))
        self.rightArrow.bind("<Button-1>", lambda event: self.changeGamemode(1))
        

        self.description = ["no stress, just vibes. play as long as you want","150 seconds to answer 5 rounds","best score out of 10 rounds. 40 seconds per guess",
                       "highest score in 4 minutes, infinte number of rounds","no time, get the best score out of 5 rounds"]
        self.descriptionLabel = tk.Label(self,text = self.description[self.current],fg = fourthColor,bg = backG,font=(fontName,13,"bold"))
        self.descriptionLabel.pack(pady=20)
        
        
        container = tk.Frame(self,bg = backG)
        
        self.choiceContinent = tk.Menubutton(container, text="Continent",font =(fontName,20) ,fg=secondColor, bg=backG,
                                        activeforeground = primaryColor)
       
        self.menuChoice = tk.Menu(self.choiceContinent,fg = primaryColor ,bg = backG,font =(fontName,14),tearoff=0)
        self.choiceContinent["menu"] = self.menuChoice
        self.menuChoice.add_command(label="any", command=lambda c="any": self.changeContinentChoosed(name=c))
        for item in continent_codes.keys():
            if item !="antarctica":
                print(item)    
                self.menuChoice.add_command(label=item.title(), command=lambda c=item.title(): self.changeContinentChoosed(name=c))
        
        self.choiceContinent.pack()
  
        self.choiceLanguage = tk.Menubutton(container, text="language spoken",font =(fontName,20) ,fg=secondColor, bg=backG,
                                        activeforeground = primaryColor)
       
        self.menuChoiceL = tk.Menu(self.choiceLanguage,fg = primaryColor ,bg = backG,font =(fontName,14),tearoff=0)
        self.choiceLanguage["menu"] = self.menuChoiceL
        for item in ["any","french","english","spanish","arab"]:
            #print(item)    
            self.menuChoiceL.add_command(label=item.title(), command=lambda c=item.title(): self.changeLanguageChoosed(name=c))
        self.choiceLanguage.pack()

        container.pack(pady=10,anchor="center",expand = True)
        self.choiceContinent.pack(padx =19,side = "left",anchor="w")
        self.choiceLanguage.pack(pady  =5,side = "right",anchor="e")
        

        
        

        self.play = tk.Button(self,text = "Play!",font = (fontName,22,"bold"),bg = secondColor,fg = backG,activeforeground=primaryColor,activebackground=backG)
        self.play.config(command=lambda: self.playGame())
        self.play.pack(pady = 20)

        self.language = None
        self.continent = None
       
        
        
    def changeType(self,name):
            
        distance = self.currentTypePos[name]-self.currentTypePos[self.currentType]
            
        length = distance/10
            
        if self.numberOfSteps < 5:
            self.numberOfSteps+=1
            self.typeGuess.move(self.RecChoice, length, 0)
            self.after(20, self.changeType, name)  # Proper recursion with delay and passing arguments
        else:
            self.numberOfSteps = 0 # current is still the end
            self.typeGuess.itemconfig(self.currentTypeTexts[self.currentType],fill = fourthColor) 
            self.currentType = name  # Finalize the change in type 
            self.typeGuess.itemconfig(self.currentTypeTexts[self.currentType],fill = backG)
            
    
    
    
    def playGame(self):
        type_guess = self.currentType
        gamemode =  self.gameModes[self.current % len(self.gameModes)]   
        print(type_guess)
        print(gamemode)
        print(self.language)
        print(self.continent)
        print("")
        app.changeFrame("CountryQuiz")
        app.frames["CountryQuiz"].setParameters(gamemode,type_guess,self.continent,self.language)
        #self.play.config(state="disabled")
    
    
    
    def changeGamemode(self,i):
        print("in change gamemode")
        
        self.current+=i
        self.labelGamemode.config(text = self.gameModes[self.current % len(self.gameModes)])
        self.descriptionLabel.config(text = self.description[self.current  % len(self.gameModes)])

    def onDisplay(self):
        pass

    def changeContinentChoosed(self,name):
        print(name)
        self.choiceContinent.config(text = name)
        if name !="any":
            self.choiceLanguage.pack_forget()
            self.continent = name
        else:
            self.choiceLanguage.pack(side = tk.RIGHT,padx=5)
            self.choiceLanguage.config(text = "language spoken")
            self.choiceContinent.config(text = "continent")
            self.continent = None

    
    def changeLanguageChoosed(self,name):   
        print(name)
        self.choiceLanguage.config(text = name)
        if name !="Any":
            self.choiceContinent.pack_forget()
            self.language = name
        else:
            self.choiceContinent.pack(side= tk.LEFT,padx=5)
            self.choiceContinent.config(text = "continent")
            self.choiceLanguage.config(text = "language spoken")
            self.language = None
class AfficherPerformance(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(bg = backG)
        self.controller = controller
        
        style = utilitaires.getStyle()
        retour = ttk.Button(self, text="Main menu", style='CountryQuiz.TButton',command = lambda: app.changeFrame("menuPrincipal"))
        #retour = tk.Button(self,text = "Main menu",bg = backG,fg = secondColor,command = lambda: app.changeFrame("menuPrincipal"),font=(fontName,20,"bold"),width=20)
        change = ttk.Button(self, text="Change Parameters", style='CountryQuiz.TButton',command = lambda: app.changeFrame("chooseGamemode"))
        #change = tk.Button(self,text = "Change Parameters",bg = backG,fg = secondColor,command = lambda: app.changeFrame("chooseGamemode"),font=(fontName,20,"bold"),width=20)
        playAgain = ttk.Button(self, text="Play again", style='CountryQuiz.TButton',command = self.playAgain)        
        #playAgain = tk.Button(self,text = "Play again",bg = backG,fg = secondColor,command = self.playAgain  ,font=(fontName,20,"bold"),width=20)
        
        titre = tk.Label(self,text = "Your Score",fg= primaryColor,font=(fontName,55),bg = backG)
        self.point = tk.Label(self,fg= primaryColor,font=(fontName,75,"bold"),bg = backG)
        titre.pack(pady = 10)
        self.point.pack(pady = 10)
        retour.pack(pady = 10)
        change.pack(pady = 10)
        playAgain.pack(pady =10)

    def setScore(self,score):
        self.score = score
        self.point.config(text = score)
    
    def playAgain(self):
        app.changeFrame("CountryQuiz")
        app.frames["CountryQuiz"].onPlay()
    def onDisplay(self):
        pass

class CountryQuiz(tk.Frame):
    def __init__(self, parent, controller):
        
        self.color1 = "#EF5A6F"
        self.bground = "#FFF1DB"
        self.color2 = "#536493"
        self.color3 = "#D4BDAC"

        
        super().__init__(parent)
        
        self.controller = controller

        
        self.afficherScore = tk.Label(self,font=(fontName,20,"bold"),fg = self.color2,bg = backG,justify="center",text = "Current Score: 0")
        self.afficherScore.pack(anchor="nw",padx =5)

        self.frame = tk.Frame(self, bg = backG)
        self.compteur = tk.Label(self.frame,anchor="e",text="30",font=(fontName,33,"bold"),fg = self.color3,bg = backG,justify="right")
        self.compteur.pack(anchor="e",side="right")# faire que compteur est completement a droite
        self.frame.pack()
        
        self.title = tk.Label(self.frame,font=(fontName,33,"bold"),fg = self.color1,bg = backG,justify="center")
        self.title.pack(pady = 10,anchor="center",side = "right")


        self.frameP = tk.Frame(self,bg = backG)
        self.frameE = tk.Frame(self,bg = backG)
        self.frameA = tk.Frame(self,bg = backG)

        self.map = mapM.interactiveMap(self)
        self.map.pack(pady = 5)
        self.map.resize(0.7)

        self.size  =20
        self.textP = tk.Label(self.frameP,fg = self.color2,bg=backG,text = "Population",font=(fontName, self.size,"bold"))
        self.spinPopulation = tk.Spinbox(self.frameP,fg = self.color2,bg = backG,insertbackground= self.color2,font=(fontName, self.size))
        
        self.textE = tk.Label(self.frameE,fg = self.color2,bg=backG,text = "Capital",font=(fontName, self.size,"bold"))
        self.entryCapital = tk.Entry(self.frameE,fg = self.color2,bg = backG,insertbackground= self.color2,font=(fontName, self.size))

        self.spinPopulation.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=False)
        
        
        self.textA = tk.Label(self.frameA,fg = self.color2,bg=backG,text = "Area (km^2)",font=(fontName, self.size,"bold"))
        self.spinArea = tk.Spinbox(self.frameA,fg = self.color2,bg = backG,insertbackground= self.color2,font=(fontName, self.size,))
        
        
        self.textP.pack(pady = 4)
        self.spinPopulation.pack()
        
        self.textE.pack(pady = 4)
        self.entryCapital.pack()

        self.textA.pack(pady = 4)
        self.spinArea.pack()

        self.frameP.pack()
        self.frameE.pack(pady =8)
        self.frameA.pack()


        self.nextRound = tk.Button(self,text = "Next",fg = self.color1,bg = backG,font=(fontName, self.size))
        self.nextRound.config(command=lambda: self.setUI(),activeforeground=self.color3,activebackground=backG)
        self.nextRound.pack(pady = 4)
        
        #self.gameModes = ["peaceful","against the clock","best score","best score V2","big brainer"]
        #self.setParameters("best score","country",None,None)

    def updateTimer(self):
        if str(self.time) == "0":
            self.setUI()
        self.compteur.config(text = str(self.time))
        if type(self.time) == int:
            self.time-=1
        if self.displayed:
            self.after(1000,self.updateTimer)

        
    
    
    def setParameters(self,gamemode,guessType,continent ,language):
        
        

        self.gamemode =gamemode
        self.guessType = guessType
        self.continent = continent
        self.language = language
        
        
        if gamemode =="best score":
            self.originalTime = 40
            self.time = self.originalTime
            
        elif gamemode =="best score V2":
            self.originalTime = 240
            self.time = self.originalTime

        elif gamemode =="against the clock":
            self.originalTime = 150
            self.time = self.originalTime

        else:
            self.originalTime = "N/A"
            self.time = self.originalTime

        if self.guessType =="country":

            self.entryCapital.pack()
            self.textE.pack()
            self.textA.pack()
            self.spinArea.pack()
        
        else:
            self.entryCapital.pack_forget()
            self.textA.pack_forget()
            self.spinArea.pack_forget()
            self.textE.pack_forget()

        self.onPlay()
        
        
        self.nextRound.config(text = "Next")
    
    
    
    def Leave(self):
        #app.changeFrame("menuPrincipal")
        app.changeFrame("AfficherPerformance")
        self.displayed = False
        self.map.deletePoint()
        app.frames["AfficherPerformance"].setScore(self.totalScore)
        self.totalScore=0
    
    def setUI(self):
        if self.guessNumber !=-1:
            self.verifyAnswers()
        code = "countryName" if self.guessType == "country" else "name"
        self.guessNumber+=1
        if self.guessNumber == self.numberOfGuesses-1: # oui
            self.nextRound.config(text = "See Score")
        if self.guessNumber >= self.numberOfGuesses: # oui
            self.Leave()
        elif self.gamemode != "best score" and str(self.time) =="0":
            self.Leave()
        else:
            if self.gamemode == "best score":
                self.time = self.originalTime
            
            #print(self.list[self.guessNumber])
            if len(self.list[self.guessNumber][code]) >= 19:
                self.title.config(font = (fontName,20,"bold"))
                #print("too big           yes")
            else:
                self.title.config(font = (fontName,33,"bold"))
            self.title.config(text = self.list[self.guessNumber][code])
            self.map.deletePoint()
            print("title is:        ------ ",self.list[self.guessNumber][code])

        
        self.spinArea.delete(0,tk.END)
        self.entryCapital.delete(0,tk.END)
        self.spinPopulation.delete(0,tk.END)  
     
    # do spinbox for population, elevation
    # do the widget to select location of that place
    # maybe for city and capital: guess in what country it is
    # for country: guess the continent
    def verifyAnswers(self):
        data = self.list[self.guessNumber]
        population = data["population"]
        guess = self.spinPopulation.get()
        self.totalScore+=utilitaires.calculate_population_score(population,guess)
        print("score for the population answer: ",utilitaires.calculate_population_score(population,guess) )


        if self.guessType =="country":
            if self.entryCapital.get().lower() == data["capital"].lower():
                self.totalScore+=50
                area = data["areaInSqKm"]
                guess = self.spinArea.get()
                self.totalScore+=utilitaires.calculate_population_score(area,guess)
                print("score for the area answer: ",utilitaires.calculate_population_score(area,guess) )

            if self.map.point_position:
                xG,yG = self.map.point_position
                lon,lat = mapM.pixel_to_wgs84(xG,yG)
                code = utilitairesPays.get_country_code(lat,lon).strip()
                
                if data["countryCode"] ==code:
                    self.totalScore+=100
                    print("the location was guessed right")
                
        else:
            if self.map.point_position:
                xG,yG = self.map.point_position 
                lat, lng = data["latitude"],data["longitude"]
                xT,yT = mapM.wgs84_to_pixel(lng,lat)
                self.totalScore+= int(utilitaires.calculate_positions_score(xT,yT,xG,yG)/50)

        
        self.afficherScore.config(text = f'CurrentScore: {self.totalScore}')
        print("current Score:",self.totalScore)
    
    def getListOfRounds(self):
        self.numberOfGuesses = 5
        lst = list()
        if self.gamemode == "best score":
            self.numberOfGuesses =10
            print("--------------------------=----")
        elif self.gamemode == "peaceful":
            self.numberOfGuesses =30
        elif self.gamemode == "best score V2":
            self.numberOfGuesses =20
        
        funcDict  = {"city":utilitairesPays.getRandomCityInformation,
                    "capital":utilitairesPays.getRandomCapitalInformation,"country":utilitairesPays.getRandomCountryInformation}
        
        #lst.append(utilitairesPays.getSpecificCountryInformation("canada"))
        i = 0
        while i < self.numberOfGuesses:
            retourner = funcDict[self.guessType](continent=self.continent, language=self.language)
            if not retourner:
                continue
            
            lst.append(retourner)
            if self.guessType == "country":
                print(lst[i]["countryName"])  
            else:  
                print(lst[i]["name"])          
            i += 1
        
        return lst
    

      
    def onPlay(self):
        self.totalScore = 0
        self.displayed = True

        self.list = self.getListOfRounds()
        self.guessNumber = -1

        self.nextRound.config(text = "Next")
        
        self.updateTimer()
        self.setUI()

    def onDisplay(self):
        pass
    def setGamemode(self,gamemode):
        pass


class menuPrincipal(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title = tk.Label(self,text = "choose your game", font = (fontName,30,"bold"),bg = backG,fg = primaryColor)
        self.title.pack()
        
        style  =utilitaires.getStyle()
        
        self.countryQuiz = ttk.Button(self, text="Country Quiz", style='CountryQuiz.TButton')
        self.countryQuiz.config(command = lambda: self.setScene("chooseGamemode"))
        self.countryQuiz.pack(pady=35)

        self.tempQuiz = ttk.Button(self, text="temperature quiz", style='CountryQuiz.TButton')
        self.tempQuiz.config(command = lambda: self.setScene("EnterCity"))
        self.tempQuiz.pack()

        self.instructions = ttk.Button(self, text="How to play", style='CountryQuiz.TButton')
        self.instructions.config(command = lambda: self.showInstructions())
        self.instructions.pack(pady = 35)
    
        
    
    def setScene(self,name):
        app.changeFrame(name)
 
    def onDisplay(self):  
        pass 
    def showInstructions(self):
        instructions = (
        "Welcome to the Game!\n"
        "for temperature quiz:\n"
        "Enter a city for wich you want to guess the temperature\n"
        "then, guess the answer in the least amount of tries\n"
        "\n"
        "for the country quiz:\n"
        "choose the type of guess (city, capital,country)\n"
        "choose the gamemode using the arrows\n"
        "choose specific parameters for the choice of the guesses\n"

        )
        messagebox.showinfo("Game Instructions", instructions)

        


class Application(tk.Tk):
    

    def __init__(self):
        super().__init__()

        self.title("Weather Guessing Game")
        self.geometry("600x500")
        self.resizable(False, False)
            
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.cityframe = EnterCity(parent=container, controller=self)

        self.GuessFrame = GuessWindow(parent=container, controller=self)

        self.currentFrame = "EnterCity"

        self.frames = {}
        for F in (EnterCity, GuessWindow,chooseGamemode,menuPrincipal,CountryQuiz,AfficherPerformance):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.config(bg = backG)
            
        self.changeFrame("menuPrincipal")
        #self.frames["GuessWindow"].configure("rigaud",20)

        self.cityframe.tkraise
        self.center_window()

    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    
    def changeFrame(self,changeFrame):
        
        for frame in self.frames.values():

            frame.pack_forget()

        
        # Show the specified frame
        frame = self.frames[changeFrame]
        frame.pack(fill="both", expand=True)
        frame.onDisplay()
        if changeFrame == "CountryQuiz":
            self.geometry("1000x800")
        else:
            self.geometry("600x500")
    

def on_closing():
        utilitaires.writeNewFavoriteCities(favoriteCities)
        app.destroy()


app = Application()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

