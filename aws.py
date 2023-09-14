class Job: 
    # Konstruktor
    def __init__(self, i, p1=1, p2=1):
        self.i = i # Identyfikator zadania (np. liczba lub ciąg znaków)
        assert(isinstance(p1, int) and p1 > 0)
        assert(isinstance(p2, int) and p2 > 0)
        self.p1 = p1 # Czas wykonywania operacji na pierwszym procesorze
        self.p2 = p2 # Czas wykonywania operacji na drugim procesorze
    
    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = [{self.p1}, {self.p2}]]"

import random

class Instance: 
    def __init__(self):
        self.jobs = []

class JobAssignment: 
    # Konstruktor
    def __init__(self, j, m, s, c):
        assert(isinstance(j, Job))
        assert(m == 1 or m == 2)
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
    # Konstruktor
    def __init__(self, i):
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []

class Schedule(Schedule): 
    def isFeasible(self):
        ### POCZATEK ROZWIAZANIA
        #Żadna operacja nie wykonuje się na niedostepnym procesorze.
        for a in self.assignments:
            if a.machine > 2:
                return False
        
        #Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu.
        for a in self.assignments:
            assigned = False
            for j in self.instance.jobs:
                  if j == a.job:
                    assigned = True
                    break
            if assigned == False:
                  return False
        
        #W danej chwili, na danym procesorze, wykonuje się co najwyżej jedna operacja.
        for a in self.assignments:
            for aa in self.assignments:
                if a.job != aa.job:
                    if a.machine == aa.machine:
                        if max(a.start, aa.start) < min(a.complete, aa.complete):
                              print("2")
                              return False
        
        #Każda operacja wykonuje się dokładnie tyle czasu, ile powinna.
        for a in self.assignments:
            for aa in self.assignments:
                if a.job == aa.job:
                      if a.machine == 1:
                        if a.complete - a.start != a.job.p1:
                         print("5")
                         return False
                      if aa.machine == 2:
                         if aa.complete - aa.start != aa.job.p2:
                              print("6")
                              return False
        
        #Operacje w ramach tego samego zadania nie wykonują się jednocześnie na więcej niż jednym procesorze.
        for a in self.assignments:
            for aa in self.assignments:
                if a.job == aa.job:
                    if a.machine != aa.machine:
                        if max(a.start, aa.start) < min(a.complete, aa.complete):
                              print("7")
                              return False
                        
        return True
        ### KONIEC ROZWIAZANIA

class Schedule(Schedule): 
    def cmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        return max(map(lambda x: x.complete, self.assignments))
        ### KONIEC ROZWIAZANIA

from copy import deepcopy

def LAPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    schedule.instance.jobs.sort(key=lambda x: x.p2, reverse = True)
    s1 = 0
    s2 = 0
    max1 = 0
    max2 = 0
    tab = schedule.instance.jobs.copy()
    tab1 = schedule.instance.jobs.copy()
    tab2 = []
    tab3 = []
    for x in range(11):
    #while len(tab)>0:
        czas1 = 1
        czas2 = 1
        tab.sort(key=lambda x: x.p2, reverse = True)
        for i in range(len(tab)):
            max1 = tab[i].p2
            if tab[i].p2 == max1:
                  #if czas1 > 0:
                       # if tab[i] in schedule.assignments:
                           #   print("DFsf")
                           #   if s1 + tab[i].p1 < schedule.assignments.index(tab[i].complete):
                           #         s1 = schedule.assignments.index(tab[i].complete)
                        #            print("s1")
                        schedule.assignments.append(JobAssignment(tab[i], 1, s1, s1 + tab[i].p1))
                        tab2.append(JobAssignment(tab[i], 1, s1, s1 + tab[i].p1))
                        s1 += tab[i].p1
                        tab.pop(tab.index(tab[i]))
                        break
        
        tab1.sort(key=lambda x: x.p1, reverse = True)
        for i in range(len(tab1)):
            max2 = tab1[i].p1
            if tab1[i].p1 == max2:
                if czas2 > 0:
                    if tab1[i] in schedule.assignments:
                        print("SDFSFA")
                    print("tab3",schedule.assignments)
                    for abc in schedule.assignments:
                        print(abc.job, tab1[i])
                        if tab1[i] == abc.job and abc.machine != 2:
                            print("abc.job")
                            print(tab1[i],abc)
                        #y = tab3.index(tab1[i])
                        #print(tab3[y], tab3[y+1])
                            if s2 + tab1[i].p2 < abc.complete:
                                #s2 = tab2[y + 1]
                                print("HFGHF")
                    schedule.assignments.append(JobAssignment(tab1[i], 2, s2, s2 + tab1[i].p2))
                    tab3.append(JobAssignment(tab1[i], 1, s2, s2 + tab1[i].p2))
                    s2 += tab1[i].p2
                    tab1.pop(tab1.index(tab1[i]))
                    break

    print("wynik: ",schedule.assignments)
    print(schedule.instance.jobs)
    ### KONIEC ROZWIAZANIA
    return schedule


ja = Job("J1", p1=8, p2=3)
jb = Job("J2", p1=7, p2=11)
jc = Job("J3", p1=5, p2=12)
jd = Job("J4", p1=10, p2=5)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

assert LAPT(instance).cmax() == 31

ja = Job("J1", p1=10, p2=23)
jb = Job("J2", p1=11, p2=22)
jc = Job("J3", p1=12, p2=21)
jd = Job("J4", p1=13, p2=20)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

assert LAPT(instance).cmax() == 86