import random
import pandas as pd
import plotly.express as px
from copy import deepcopy


class Job: 
    def __init__(self, i, p=1, w=1):
        assert(isinstance(p, int) and p > 0)
        self.i = i # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p # Czas wykonywania zadania
        assert(isinstance(w, int) and w > 0 and w < 140509184)
        self.w = w # wymagana pamięć zadania
    
    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}]"

class Instance: 
    def __init__(self, machines = 16, memory = 140509184):
        self.jobs = []
        assert(isinstance(machines, int) and machines > 0)
        self.machines = machines
        self.memory = memory
    
    def generate(self, a):   
        df = pd.read_csv('zapat.csv', sep=";")
        df = df.query('czas > 0 and pamiec > 0 and pamiec < 140509184')
        df = df.sample(n = a)
        for i in range(len(df)):
            self.jobs.append(Job("J" + str(len(self.jobs) + 1), int(df.iloc[i].czas), int(df.iloc[i].pamiec)))
        
class JobAssignment: 
    # Konstruktor
    def __init__(self, j, m, s, c):
        assert(isinstance(j, Job))
        assert(isinstance(m, int) and m > 0)
        assert(isinstance(s, int) and s >= 0)
        assert(isinstance(c, int) and c > s)
        self.job = j # Zadanie
        self.machine = m # Procesor, na którym zadanie się wykonuje
        self.start = s # Czas rozpoczęcia zadania
        self.complete = c # Czas zakończenia zadania
    
    # Reprezentacja przydziału zadania do procesora
    def __repr__(self):
        return f"{self.job} ~ P{self.machine}[{self.start}; {self.complete})"

class Schedule: 
    def __init__(self, i):
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []

    def cmax(self):
        assert self.isFeasible() == True
        return max(map(lambda x: x.complete, self.assignments))

class Schedule(Schedule): 
    def isFeasible(self):
        for a in self.assignments:
            for aa in self.assignments:
                if a.job != aa.job:
                    if a.machine == aa.machine:
                        if max(a.start, aa.start) < min(a.complete, aa.complete):
                            return False
                    
        for a in self.assignments:
            for aa in self.assignments:
                if a.job == aa.job:
                    if a.machine != aa.machine:
                        if max(a.start, aa.start) < min(a.complete, aa.complete):
                            return False
                    
        for a in self.assignments:
            for aa in self.assignments:
                if a.job == aa.job:
                    if a.complete - a.start < a.job.p:
                        a.job.p = a.job.p - (a.complete - a.start)
                        if aa.complete - aa.start != aa.job.p:
                            return False
            
        for a in self.assignments:
            assigned = False
            for j in self.instance.jobs:
                if j == a.job:
                    assigned = True
                    break
            if assigned == False:
                return False
            
        for a in self.assignments:
            if a.machine > self.instance.machines:
                return False
            
        return True

def wykresczas():
    df = pd.read_csv('zapat.csv', sep=";")
    fig = px.line(df, x = df.index, y = df.czas, title = 'czas')
    fig.show()
#wykresczas()

def wykrespamiec():
    df = pd.read_csv('zapat.csv', sep=";")
    fig = px.line(df, x = df.index, y = 'pamiec', title = 'pamiec')
    fig.show()
#wykrespamiec()

def LPT(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.p, reverse = True)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]  #tablica procesorów
    abc = [0 for _ in range(instance.machines)]  #tablica pamieci 
    while len(instance.jobs) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        koniec = 0
        if sum(abc) > instance.memory:
            break
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                abc[x] = 0                
                if sum(abc) + s[i].w > instance.memory:
                  for y in range(instance.machines):
                    if koniec == 1:
                        break
                    for a in range(len(s)):
                        if sum(abc) + s[a].w <= instance.memory:
                            schedule.assignments.append(JobAssignment(s[a], m + 1, tab[x], tab[x] + s[a].p))
                            tab[x] += s[a].p
                            abc[x] += s[a].w
                            s.pop(s.index(s[a]))
                            koniec = 1
                            break
                    else:
                        tab[y] += s[a].p
                        abc[y] = 0
                        tab[x] = tab[y]
                if koniec == 1:
                    break
                if sum(abc) + s[i].w <= instance.memory:
                    schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                    tab[x] += s[i].p
                    abc[x] += s[i].w
                    s.pop(s.index(s[i]))
                    break
    return schedule

def RND(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]  #tablica procesorów
    abc = [0 for _ in range(instance.machines)]  #tablica pamieci 
    while len(instance.jobs) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        koniec = 0
        if sum(abc) > instance.memory:
            break
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                abc[x] = 0                
                if sum(abc) + s[i].w > instance.memory:
                  for y in range(instance.machines):
                    if koniec == 1:
                        break
                    for a in range(len(s)):
                        if sum(abc) + s[a].w <= instance.memory:
                            schedule.assignments.append(JobAssignment(s[a], m + 1, tab[x], tab[x] + s[a].p))
                            tab[x] += s[a].p
                            abc[x] += s[a].w
                            s.pop(s.index(s[a]))
                            koniec = 1
                            break
                    else:
                        tab[y] += s[a].p
                        abc[y] = 0
                        tab[x] = tab[y]
                if koniec == 1:
                    break
                if sum(abc) + s[i].w <= instance.memory:
                    schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                    tab[x] += s[i].p
                    abc[x] += s[i].w
                    s.pop(s.index(s[i]))
                    break
    return schedule

def LMR(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.w)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]  #tablica procesorów
    abc = [0 for _ in range(instance.machines)]  #tablica pamieci 
    while len(instance.jobs) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        koniec = 0
        if sum(abc) > instance.memory:
            break
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                abc[x] = 0                
                if sum(abc) + s[i].w > instance.memory:
                  for y in range(instance.machines):
                    if koniec == 1:
                        break
                    for a in range(len(s)):
                        if sum(abc) + s[a].w <= instance.memory:
                            schedule.assignments.append(JobAssignment(s[a], m + 1, tab[x], tab[x] + s[a].p))
                            tab[x] += s[a].p
                            abc[x] += s[a].w
                            s.pop(s.index(s[a]))
                            koniec = 1
                            break
                    else:
                        tab[y] += s[a].p
                        abc[y] = 0
                        tab[x] = tab[y]
                if koniec == 1:
                    break
                if sum(abc) + s[i].w <= instance.memory:
                    schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                    tab[x] += s[i].p
                    abc[x] += s[i].w
                    s.pop(s.index(s[i]))
                    break
    return schedule

def HMR(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.w, reverse = True)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]  #tablica procesorów
    abc = [0 for _ in range(instance.machines)]  #tablica pamieci 
    while len(instance.jobs) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        koniec = 0
        if sum(abc) > instance.memory:
            break
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                abc[x] = 0                
                if sum(abc) + s[i].w > instance.memory:
                  for y in range(instance.machines):
                    if koniec == 1:
                        break
                    for a in range(len(s)):
                        if sum(abc) + s[a].w <= instance.memory:
                            schedule.assignments.append(JobAssignment(s[a], m + 1, tab[x], tab[x] + s[a].p))
                            tab[x] += s[a].p
                            abc[x] += s[a].w
                            s.pop(s.index(s[a]))
                            koniec = 1
                            break
                    else:
                        tab[y] += s[a].p
                        abc[y] = 0
                        tab[x] = tab[y]
                if koniec == 1:
                    break
                if sum(abc) + s[i].w <= instance.memory:
                    schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                    tab[x] += s[i].p
                    abc[x] += s[i].w
                    s.pop(s.index(s[i]))
                    break
    return schedule

def ALFA(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.p)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]  #tablica procesorów
    abc = [0 for _ in range(instance.machines)]  #tablica pamieci 
    while len(instance.jobs) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        koniec = 0
        if sum(abc) > instance.memory:
            break
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                abc[x] = 0                
                if sum(abc) + s[i].w > instance.memory:
                  for y in range(instance.machines):
                    if koniec == 1:
                        break
                    for a in range(len(s)):
                        if sum(abc) + s[a].w <= instance.memory:
                            schedule.assignments.append(JobAssignment(s[a], m + 1, tab[x], tab[x] + s[a].p))
                            tab[x] += s[a].p
                            abc[x] += s[a].w
                            s.pop(s.index(s[a]))
                            koniec = 1
                            break
                    else:
                        tab[y] += s[a].p
                        abc[y] = 0
                        tab[x] = tab[y]
                if koniec == 1:
                    break
                if sum(abc) + s[i].w <= instance.memory:
                    schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                    tab[x] += s[i].p
                    abc[x] += s[i].w
                    s.pop(s.index(s[i]))
                    break
    return schedule

def BETA(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.p / x.w)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]  #tablica procesorów
    abc = [0 for _ in range(instance.machines)]  #tablica pamieci 
    while len(instance.jobs) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        koniec = 0
        if sum(abc) > instance.memory:
            break
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                abc[x] = 0                
                if sum(abc) + s[i].w > instance.memory:
                  for y in range(instance.machines):
                    if koniec == 1:
                        break
                    for a in range(len(s)):
                        if sum(abc) + s[a].w <= instance.memory:
                            schedule.assignments.append(JobAssignment(s[a], m + 1, tab[x], tab[x] + s[a].p))
                            tab[x] += s[a].p
                            abc[x] += s[a].w
                            s.pop(s.index(s[a]))
                            koniec = 1
                            break
                    else:
                        tab[y] += s[a].p
                        abc[y] = 0
                        tab[x] = tab[y]
                if koniec == 1:
                    break
                if sum(abc) + s[i].w <= instance.memory:
                    schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                    tab[x] += s[i].p
                    abc[x] += s[i].w
                    s.pop(s.index(s[i]))
                    break
    return schedule

def wykres():
    instance = Instance()
    dic = pd.DataFrame()
    for aa in range(30):   
        instance.generate(5000)
        suma = 0
        suma2 = 0
        for i in range(len(instance.jobs)):
            suma += instance.jobs[i].p / 16
            suma2 += instance.jobs[i].p * (instance.jobs[i].w / instance.memory)
        rnd_dz = RND(instance).cmax() / max(suma, suma2)
        lmr_dz = LMR(instance).cmax() / max(suma, suma2)
        hmr_dz = HMR(instance).cmax() / max(suma, suma2)
        lpt_dz = LPT(instance).cmax() / max(suma, suma2)
        alfa_dz = ALFA(instance).cmax() / max(suma, suma2)
        beta_dz = BETA(instance).cmax() / max(suma, suma2)
        data = {'RND': [rnd_dz],'LMR':[lmr_dz],'HMR':[hmr_dz],'LPT':[lpt_dz],'ALFA':[alfa_dz],'BETA':beta_dz}
        dic2 = pd.DataFrame(data)
        dic = dic.append(dic2)
        instance.jobs = []
        print(aa)
    print(dic)
    fig = px.box(dic)
    fig.show()
wykres()