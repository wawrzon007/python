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
import random

class Instance: 
    def __init__(self, machines=1):
        self.jobs = []
        assert(isinstance(machines, int) and machines > 0)
        self.machines = machines
    
    def generate(self, n, pmin=1, pmax=1):        
        for i in range(1, n + 1):
            self.jobs.append(Job("J" + str(len(self.jobs) + 1), random.randint(pmin, pmax)))
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
    # Konstruktor
    def __init__(self, i):
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []

class Schedule(Schedule): 
    def isFeasible(self):
        ### POCZATEK ROZWIAZANIA
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
                    

        if schedule.instance.machines > 1:
            for a in self.assignments:
                for aa in self.assignments:
                    if a.job == aa.job:
                        if a.machine != aa.machine:
                            if a.complete - a.start < a.job.p:
                                a.job.p = a.job.p - (a.complete - a.start)
                                if aa.complete - aa.start != aa.job.p:
                                    return False
        else:
            for a in self.assignments:
                if a.complete - a.start != a.job.p:
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
        ### KONIEC ROZWIAZANIA

class Schedule(Schedule): 
    def cmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        maks = 1
        for i in schedule.assignments:
            for ii in schedule.assignments:
                if i == ii:
                    maks = max(maks, max(i.complete, ii.complete))
        return maks
        ### KONIEC ROZWIAZANIA


    
    def csum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        tab = []
        suma = 0
        for i in range(len(instance.jobs)):
            for ii in range(len(schedule.assignments)):
                if schedule.assignments[i].job == schedule.assignments[ii].job:
                    if schedule.assignments[i].machine == schedule.assignments[ii].machine:
                        if schedule.assignments[i].complete != schedule.assignments[ii].complete and schedule.assignments[i].job not in tab:
                            suma += max(schedule.assignments[i].complete, schedule.assignments[ii].complete) 
                            tab.append(schedule.assignments[i].job)
                            print(f'1 {suma}')
                            print(f'dada {schedule.assignments[i]}     {schedule.assignments[ii]}   {max(schedule.assignments[i].complete, schedule.assignments[ii].complete) }')
                        elif schedule.assignments[i].complete != schedule.assignments[ii].complete and schedule.assignments[i].job in tab:
                            #suma -= tab[tab.index(schedule.assignments[i].job)].p
                            for a in tab:
                                print(f'2 {suma}')
                                if a == schedule.assignments[i].job:
                                    suma -= schedule.assignments[i].complete
                                    break
                            suma += max(schedule.assignments[i].complete, schedule.assignments[ii].complete)
                            print(f'3 {suma}')
                            print(f'plka {schedule.assignments[i]}     {schedule.assignments[ii]}   {max(schedule.assignments[i].complete, schedule.assignments[ii].complete) }')
                    elif schedule.assignments[i].machine != schedule.assignments[ii].machine:
                        if schedule.assignments[i].job not in tab:
                            suma += max(schedule.assignments[i].complete, schedule.assignments[ii].complete) 
                            tab.append(schedule.assignments[i].job)
                            print(f'4 {suma}')
                            print(f'sffsf  {schedule.assignments[i]}     {schedule.assignments[ii]}   {max(schedule.assignments[i].complete, schedule.assignments[ii].complete) }')
                        elif schedule.assignments[i].job in tab:
                            for a in tab:
                                print(f'5 {suma}')
                                if a == schedule.assignments[i].job:
                                    suma -= schedule.assignments[i].complete
                                    break
                            suma += max(schedule.assignments[i].complete, schedule.assignments[ii].complete)
                            print(f'6 {suma}')
                            print(f'zxzsf  {schedule.assignments[i]}     {schedule.assignments[ii]}   {max(schedule.assignments[i].complete, schedule.assignments[ii].complete) }')
                        
        return suma
        ### KONIEC ROZWIAZANIA
    


    
    def cwsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        waga = 0
        tab = []
        waga = 0
        for i in range(len(instance.jobs)):
            for ii in range(len(schedule.assignments)):
                if schedule.assignments[i].job == schedule.assignments[ii].job:
                    if schedule.assignments[i].complete != schedule.assignments[ii].complete and schedule.assignments[i].job not in tab:
                        waga += schedule.assignments[i].job.w * max(schedule.assignments[i].complete, schedule.assignments[ii].complete) 
                        tab.append(schedule.assignments[i].job)
                        print(f'dada {schedule.assignments[i]}     {schedule.assignments[ii]}   {max(schedule.assignments[i].complete, schedule.assignments[ii].complete) }')
                    elif schedule.assignments[i].machine == schedule.assignments[ii].machine:
                        waga += schedule.assignments[i].job.w *max(schedule.assignments[i].complete, schedule.assignments[ii].complete) 
                        print(f'dada {schedule.assignments[i]}     {schedule.assignments[ii]}   {max(schedule.assignments[i].complete, schedule.assignments[ii].complete) }')
        return waga
        ### KONIEC ROZWIAZANIA

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", w=2, p=10)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.cmax() == 10
#print(schedule.csum())
assert schedule.csum() == 30
#assert schedule.cwsum() == 40
### BEGIN HIDDEN TESTS
ja = Job("J1", w=5, p=5)
jb = Job("J2", w=4, p=10)
jc = Job("J3", w=2, p=15)
jd = Job("J4", w=1, p=20)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 3, 0, 5),
    JobAssignment(jb, 3, 5, 10),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 1, 0, 10),
    JobAssignment(jc, 1, 12, 17),
    JobAssignment(jd, 2, 5, 25),
]

assert schedule.cmax() == 25
print(schedule.csum())
print("cxgxgbxvxvbxxxvxvccv")
assert schedule.csum() == 57
assert schedule.cwsum() == 124
### END HIDDEN TESTS

from copy import deepcopy

def L(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]
    while len(s) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                tab[x] += s[i].p
                break
        i += 1
    ### KONIEC ROZWIAZANIA
    return schedule

from copy import deepcopy

def LPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.p, reverse = True)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]
    while len(s) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                tab[x] += s[i].p
                break
        i += 1
    ### KONIEC ROZWIAZANIA
    return schedule

from copy import deepcopy

def SPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    s = schedule.instance.jobs.copy()
    s.sort(key=lambda x: x.p)
    print(s)
    m = 0
    z = 0
    i = 0
    tab = [0 for _ in range(instance.machines)]
    while len(s) != len(schedule.assignments):
        z = min(tab)
        m = tab.index(z)
        for x in range(instance.machines):
            if tab[x] == tab[m]:  
                schedule.assignments.append(JobAssignment(s[i], m + 1, tab[x], tab[x] + s[i].p))
                tab[x] += s[i].p
                break
        i += 1
    ### KONIEC ROZWIAZANIA
    return schedule

from copy import deepcopy

def McNaughton(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    tab = [] 
    s = 0
    czas = 0
    for j in schedule.instance.jobs:
        tab.append(JobAssignment(j, 1, s, s + j.p))
        s += j.p
    s = 0
    cmax = max(map(lambda x: x.complete, tab)) // instance.machines
    tab = schedule.instance.jobs.copy()
    tab1 = tab.copy()
    for i in range(instance.machines):
        ii = 0
        while len(tab) > 0:
            if s + tab[ii].p > cmax:
                czas = tab[ii].p - (cmax - s)
                abc = deepcopy(tab[ii])
                schedule.instance.jobs.append(abc)
                if cmax - s == 0:
                    schedule.assignments.append(JobAssignment(tab[ii], i + 2, 0, tab[ii].p))
                    tab.pop(tab.index(tab[ii]))
                    break
                tab1[ii].p = (cmax - s)
                schedule.assignments.append(JobAssignment(tab1[ii], i + 1, s, cmax)) 
                abc.p = czas
                schedule.assignments.append(JobAssignment(abc, i + 2, 0, abc.p))
                s = abc.p
                tab.pop(tab.index(tab[ii]))
                tab1.pop(tab1.index(tab1[ii]))
                czas = 0
                break
            schedule.assignments.append(JobAssignment(tab[ii], i + 1, s, s + tab[ii].p))
            s += tab[ii].p
            tab.pop(tab.index(tab[ii]))
            tab1.pop(tab1.index(tab1[ii]))
    ### KONIEC ROZWIAZANIA
    return schedule

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", p=10)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.isFeasible() == True

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 105, 110),
    JobAssignment(jc, 2, 5, 10),
]

assert schedule.isFeasible() == True

# Dwa zadania wykonują się jednocześnie na pierwszym procesorze
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 4, 9),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się jednocześnie na dwóch procesorach
schedule.assignments = [
    JobAssignment(ja, 1, 20, 25),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 23, 28),
]

assert schedule.isFeasible() == False

# Niektóre zadania nie zostały ukończone
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 4),
    JobAssignment(jb, 1, 5, 9),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 3, 0, 10),
    JobAssignment(Job("X", 5), 3, 10, 15)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się na nieistniejącej maszynie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 4, 5, 10),
]

assert schedule.isFeasible() == False
### BEGIN HIDDEN TESTS
ja = Job("J1", p=5)
jb = Job("J2", p=10)
jc = Job("J3", p=15)
jd = Job("J4", p=20)

instance = Instance(machines=4)
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 25, 35),
]

assert schedule.isFeasible() == True

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 1025, 1035),
]

assert schedule.isFeasible() == True

# Dwa zadania wykonują się jednocześnie na pierwszym procesorze
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 1, 4, 14),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się jednocześnie na dwóch procesorach
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 4, 5, 15),
]

assert schedule.isFeasible() == False

# Niektóre zadania nie zostały ukończone
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 25, 34),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 25, 35),
    JobAssignment(Job("X", 5), 3, 1010, 1015)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się na nieistniejącej maszynie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 5, 0, 10),
    JobAssignment(jd, 2, 25, 35),
]

assert schedule.isFeasible() == False
### END HIDDEN TESTS

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", w=2, p=10)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.cmax() == 10
print(schedule.csum())
assert schedule.csum() == 30
#assert schedule.cwsum() == 40
### BEGIN HIDDEN TESTS
ja = Job("J1", w=5, p=5)
jb = Job("J2", w=4, p=10)
jc = Job("J3", w=2, p=15)
jd = Job("J4", w=1, p=20)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 3, 0, 5),
    JobAssignment(jb, 3, 5, 10),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 1, 0, 10),
    JobAssignment(jc, 1, 12, 17),
    JobAssignment(jd, 2, 5, 25),
]

assert schedule.cmax() == 25
print(schedule.csum())
assert schedule.csum() == 57
assert schedule.cwsum() == 124
### END HIDDEN TESTS

random.seed(1234567890)

instance = Instance()
instance.generate(50, 1, 100)

instance.machines = 1
schedule = L(instance)
assert schedule.cmax() == 2333

instance.machines = 2
schedule = L(instance)
assert schedule.cmax() == 1170

instance.machines = 5
schedule = L(instance)
assert schedule.cmax() == 495
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)

instance.machines = 1
schedule = L(instance)
assert schedule.cmax() == 4728

instance.machines = 2
schedule = L(instance)
assert schedule.cmax() == 2391

instance.machines = 5
schedule = L(instance)
assert schedule.cmax() == 996
### END HIDDEN TESTS

random.seed(1234567890)

instance = Instance()
instance.generate(50, 1, 100)

instance.machines = 1
assert L(instance).cmax() == 2333
assert LPT(instance).cmax() == 2333

instance.machines = 2
assert L(instance).cmax() == 1170
assert LPT(instance).cmax() == 1167

instance.machines = 5
assert L(instance).cmax() == 495
assert LPT(instance).cmax() == 471
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)

instance.machines = 1
assert LPT(instance).cmax() == 4728

instance.machines = 3
assert LPT(instance).cmax() == 1578

instance.machines = 5
assert LPT(instance).cmax() == 946

instance.machines = 10
assert LPT(instance).cmax() == 475
### END HIDDEN TESTS

random.seed(1234567890)

instance = Instance()
instance.generate(50, 1, 100)

instance.machines = 1
assert L(instance).csum() == 60506
assert SPT(instance).csum() == 39761

instance.machines = 2
assert L(instance).csum() == 30653
assert SPT(instance).csum() == 20478

instance.machines = 5
assert L(instance).csum() == 12659
assert SPT(instance).csum() == 8920
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)

instance.machines = 1
assert SPT(instance).csum() == 157876

instance.machines = 3
assert SPT(instance).csum() == 54225

instance.machines = 5
assert SPT(instance).csum() == 33505

instance.machines = 10
assert SPT(instance).csum() == 17990
### END HIDDEN TESTS

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", p=10)

instance = Instance()
instance.machines = 2
instance.jobs = [ja, jb, jc]

assert LPT(instance).cmax() == 20
assert McNaughton(instance).cmax() == 15

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(200, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100
instance.machines = 7

assert LPT(instance).cmax() == 1418
assert McNaughton(instance).cmax() == 1417

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(200, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100
instance.jobs.append(Job("J", p = 1420))
instance.machines = 8

assert LPT(instance).cmax() == 1420
assert McNaughton(instance).cmax() == 1420
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(120, 1, 100)
instance.machines = 3

assert McNaughton(instance).cmax() == 1932

random.seed(1234567890)

instance = Instance()
instance.generate(120, 1, 100)
instance.jobs.append(Job("J", p = 1933))
instance.machines = 4

assert McNaughton(instance).cmax() == 1933
### END HIDDEN TESTS