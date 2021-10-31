# Benjamin Cape - 21F - CS76
# PA5
# 10.24.21

from collections import defaultdict
import random
from CNF import Model, CNF, Disjunction, Variable
import time
from copy import copy

# Golden Number
GOLDEN_NUMBER = 0.7

# Maximum iterations for WALK-SAT
MAXIMUM_ITERATIONS = 100000


class SAT():
    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle
        self.vars = set()
        self.variables = {}
        self.variables_back = {}

        disjunctions = []

        def try_add(i, var):
            '''
            Try to add a new variable to our set of variables, and the respective maps
            '''
            if not var in self.vars:
                self.vars.add(var)
                self.variables[i] = var
                self.variables_back[var] = i
                i += 1
            return i

        i = 0
        # This is for parsing the puzzle
        with open(puzzle) as file:
            for line in file.readlines():
                line_vars = []
                for var in line.strip().split(' '):
                    if var[0] == '-':
                        true_var = var[1:]
                        i = try_add(i, true_var)
                        line_vars.append(
                            Variable(False, self.variables_back[true_var]))
                    else:
                        i = try_add(i, var)
                        line_vars.append(
                            Variable(True, self.variables_back[var]))

                disjunctions.append(Disjunction(line_vars))

        self.cnf = CNF(disjunctions)

    def stats(self) -> str:
        return f"""
-------
Name: {self.puzzle}
Threshold: {GOLDEN_NUMBER}
Sentences: {len(self.cnf.sentences)}
Constants: {len(self.cnf.constants)}
Variables: {len(self.variables)}
-------
"""

    def gsat(self) -> Model:
        '''
        GSAT Algorithm.
        '''
        model: Model = {}
        for var in self.variables:
            model[var] = False if random.randint(0, 1) == 0 else True

        i = 0
        while not self.cnf.is_satisfied(model) and i < 3000:
            # Find a random one to flip if we pass
            if random.random() >= GOLDEN_NUMBER:
                rand_var = random.sample(list(model), 1)[0]
                model[rand_var] = not model[rand_var]
            else:
                # Flip the one with the maximum score
                scores = defaultdict(lambda: [])
                m = 0
                for var in self.variables:
                    new_model = copy(model)
                    new_model[var] = not model[var]
                    count = self.cnf.count_satisfied(new_model)
                    scores[count].append(var)
                    m = max(m, count)

                rand_var = random.sample(list(scores[m]), 1)[0]
                model[rand_var] = not model[rand_var]
            i += 1

        if self.cnf.is_satisfied(model):
            self.solution = model
            return i, True
        return i, False

    def walksat(self) -> bool:
        '''
        WalkSAT Algorithm.
        '''
        model: Model = {}
        for var in self.variables:
            model[var] = False if random.randint(0, 1) == 0 else True

        i = 0

        while not self.cnf.is_satisfied(model) and i < MAXIMUM_ITERATIONS:
            # Using randomness, swap one random variable, or swap an enhancing variable.
            if random.random() >= GOLDEN_NUMBER:
                rand_var = random.sample(list(model), 1)[0]
                model[rand_var] = not model[rand_var]
            else:
                scores = defaultdict(lambda: [])
                m = 0
                unsatisfied_clause = random.sample(
                    list(self.cnf.unsatisfied_clauses(model)), 1)[0]
                # Find a variable that, when swapped, creates the most number of satisfied sentences.
                for var in map(lambda x: x.var, unsatisfied_clause.vars):
                    new_model = copy(model)
                    new_model[var] = not model[var]
                    count = self.cnf.count_satisfied(new_model)
                    scores[count].append(var)
                    m = max(m, count)

                # Swap that variable
                rand_var = random.sample(list(scores[m]), 1)[0]
                model[rand_var] = not model[rand_var]
            i += 1

        if self.cnf.is_satisfied(model):
            self.solution = model
            return i, True
        return i, False

    def walksat_enhanced(self,
                         golden_number=GOLDEN_NUMBER,
                         result=None,
                         status=None,
                         shared_visited=set()) -> bool:
        '''
        An enhanced version of the walksat that uses a form of caching to determine the number of satisfied sentences given a value swap.
        '''
        start = time.time()
        model: Model = [False] * len(self.variables)
        checked_models = shared_visited
        for var in self.variables:
            # Set all of our constants to their constant values
            if var in self.cnf.constants:
                model[var] = self.cnf.constants[var]
            else:
                model[var] = False if random.randint(0, 1) == 0 else True

        def update_model(l):
            '''
            Helper for updating the model, tried to find one that we haven't already tried 
            so that we don't check satisfied (a slow process) multiple times
            '''
            i = 0
            if len(l) == 0:
                return False
            l = copy(l)
            random.shuffle(l)
            flipped = False
            while str(model) in checked_models:
                if flipped:
                    model[l[i - 1]] = not model[l[i - 1]]
                if not l[i] in self.cnf.constants:
                    model[l[i]] = not model[l[i]]
                    flipped = True
                else:
                    flipped = False
                i += 1
                if i == len(l):
                    # If we've checked all the possible values, then return false, we've tried all of these before...
                    # We will default to picking a random one if this doesn't work
                    # This helps stay out of the local minimums
                    return False

            return True

        i = 0
        while (str(model) in checked_models or not self.cnf.is_satisfied(model)
               ) and len(checked_models) < 2**(len(self.variables) - len(
                   self.cnf.constants)) and i < MAXIMUM_ITERATIONS:
            i += 1
            if str(model) in checked_models or random.random() > golden_number:
                update_model(list(self.variables))
            else:
                checked_models.add(str(model))
                scores = defaultdict(lambda: [])
                m = 0
                unsatisfied_clause = random.sample(
                    list(self.cnf.unsatisfied_clauses(model)), 1)[0]
                satisfied = self.cnf.get_satisfied(model)
                for var in map(lambda x: x.var, unsatisfied_clause.vars):
                    if var in self.cnf.constants:
                        continue
                    # Use the unsatisfied diff helper to speed up calcs
                    count = len(satisfied) + self.cnf.count_satisfied_diff(
                        satisfied, model, var)
                    if m <= count:
                        scores[count].append(var)
                        m = count

                # Print a running count of the iterations we've made
                print(i, end="\r")

                if status != None:
                    status[golden_number] = m

                if not update_model(list(scores[m])):
                    update_model(list(self.variables))

        if result != None:
            result[time.time() - start] = golden_number

        if self.cnf.is_satisfied(model):
            self.solution = model
            return i, True
        return i, None

    def threaded_walksat(self):
        import threading
        times = {}
        status = {}
        shared_visited = set()
        attempts = 10
        for golden_number in range(1, attempts):
            # Spawn a thread for each golden number
            t = threading.Thread(target=self.walksat_enhanced,
                                 args=(
                                     golden_number / attempts,
                                     times,
                                     status,
                                     shared_visited,
                                 ),
                                 daemon=True)

            t.start()

        # Wait until one of the threads has completed
        while not len(times):
            pass

        # Wait a second, because it might have taken some time to start the last one and it might finish before the first one
        time.sleep(0.1)

        times = list(times.items())
        # Sort them and output the smallest
        times = sorted(times, key=lambda x: x[0])

        return times[0]

    def write_solution(self, file_name) -> None:
        with open(file_name, 'w') as file:
            for k in range(len(list(self.solution))):
                v = self.solution[k]
                file.write(f"{'-' if not v else ''}{self.variables[k]}\n")