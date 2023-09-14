class Job: 
    # Konstruktor
    def __init__(self, i, p=1, w=1):
        assert(isinstance(p, int) and p > 0)
        self.i = i # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p # Czas wykonywania zadania
        assert(isinstance(w, int) and w > 0)
        self.w = w # Waga zadania
    
    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}]"


class Job(Job): 
    # Konstruktor
    def __init__(self, i, p=1, w=1, r=0, d=0):
        super().__init__(i, p, w)
        assert(isinstance(r, int))
        self.r = r # Czas gotowości zadania (domyślnie 0), może być też wartością ujemną
        assert(isinstance(d, int))
        self.d = d # Pożądany czas zakończenia zadania (domyślnie 0), może być też wartością ujemną
    
    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}, r = {self.r}, d = {self.d}]"


import random

class Instance: 
    def __init__(self):
        self.jobs = []
    
    def generate(self, n, pmin=1, pmax=1):        
        for i in range(1, n + 1):
            self.jobs.append(Job("J" + str(len(self.jobs) + 1), random.randint(pmin, pmax)))

class JobAssignment: 
    # Konstruktor
    def __init__(self, j, s, c):
        assert(isinstance(j, Job))
        assert(isinstance(s, int) and s >= 0)
        assert(isinstance(c, int) and c > s)
        self.job = j # Zadanie
        self.start = s # Czas rozpoczęcia zadania
        self.complete = c # Czas zakończenia zadania
    
    # Reprezentacja przydziału zadania do procesora
    def __repr__(self):
        return f"{self.job} ~ [{self.start}; {self.complete})"

class Schedule: 
    # Konstruktor
    def __init__(self, i):
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []

    def isFeasible(self):
        if(len(self.instance.jobs) != len(self.assignments)):
            print("1")
            return False
        
        # Każde zadanie zostało przydzielone dokładnie raz
        for j in self.instance.jobs:
            assigned = 0
            for a in self.assignments:
                if j == a.job:
                    assigned += 1
            if assigned != 1:
                print("2")
                return False
        
        # Każdy przydział dotyczy istniejącego zadania
        for a in self.assignments:
            assigned = False
            for j in self.instance.jobs:
                if j == a.job:
                    assigned = True
                    break
            if assigned == False:
                print("3")
                return False
        
        # Każde zadanie wykonuje się dokładnie tyle ile powinno
        for a in self.assignments:
            if a.complete - a.start != a.job.p:
                print("4")
                return False
        
        # W danej chwili wykonuje się co najwyżej jedno zadanie
        for a in self.assignments:
            for aa in self.assignments:
                if a.job != aa.job:
                    if max(a.start, aa.start) < min(a.complete, aa.complete):
                        print("5")
                        return False
            
        return True

class Schedule(Schedule): 
    def usum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        spoznienia=0
        for a in self.assignments:
            if a.job.d < a.complete:
                spoznienia += 1
        return spoznienia
        ### KONIEC ROZWIAZANIA
        


def Spr(s):
    start = 0
    for x in s:
        if x.d > start + x.p:
            return False
        start += x.p
    return True
from copy import deepcopy

def HodgesonMoore(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    zakoncz = False
    start = 0
    #maks = 0
    k = len(s)
    for i in range(len(s)):
            #    schedule.assignments.append(JobAssignment(s[i], start, start + s[i].p))
            start += s[i].p
            #print(schedule.assignments)
            #break
    koniec = start
    start = 0
    while len(s) > 0 and zakoncz == False:
        maks = 0
        #if Spr(s) == True:
        #for x in s:
            #if x.d > start + x.p:
             #   zakoncz = True
                #break
            #start += x.p
        #if zakoncz == True:
        zakoncz = Spr(s)
        print(zakoncz)
        
        
        for i in range(len(s)):
            if s[i].d > start + s[i].p:
                k = i
                print(f"k'{k}'")
                break
        if k == 0:
            schedule.assignments.append(JobAssignment(s[k], koniec - s[k].p, koniec))
            koniec -= s[k].p
            start += s[k].p
            s.pop(s.index(s[i]))
        print(f'len {len(s)}')
        if k > 0:
            for i in range(k):
                print(f'i {i}')
                if s[i].p > maks:
                    maks = s[i].p
                    print(f'maks {maks}')
        #koniec = start
            for i in range(k):
                if s[i].p == maks:
                    print("koniec")
                    print (koniec)
                    schedule.assignments.append(JobAssignment(s[i], koniec - s[i].p, koniec))
                    koniec -= s[i].p
                    start += s[i].p
                    s.pop(s.index(s[i]))
                #break
        print (schedule.assignments)
        #zakoncz = False
        #break
    if zakoncz == True:
        for i in s:
            schedule.assignments.append(JobAssignment(i, start, start + i.p))
            start += i.p
        
    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(100, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100

# Każdemu z zadań przypisz losowy pożądany czas zakończenia
for i in instance.jobs:
    i.d = random.randint(50, 200)
    
hm = HodgesonMoore(instance)
print(hm.usum())
#assert hm.usum() == 82