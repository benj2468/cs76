# Benjamin Cape - 21F - CS76
# PA5
# 10.24.21

from collections import defaultdict
import random
from typing import Generator, List, Mapping, Set
import time
from copy import copy
from enum import Enum

Model = Mapping[int, bool]

GOLDEN_NUMBER = 0.7
MAXIMUM_ITERATIONS = 100000


class Satisfied(Enum):
    Satisfied = True
    UnSatisfied = False
    Unknown = -1


class Variable():
    '''
    Contains information regarding a variable within a CNF, and whether it is negated or not
    '''
    def __init__(self, true: bool, var: int) -> None:
        self.true = true
        self.var = var

    def satisfied(self, model: Model) -> Satisfied:
        '''
        Given an model, is this variable true or not?
        '''
        try:
            assign = model[self.var]
        except:
            assign = model.get(self.var)
        if assign == None:
            return Satisfied.Unknown
        return Satisfied(assign) if self.true else Satisfied(not assign)

    def __str__(self) -> str:
        return f"{'' if self.true else '-'}{self.var}"


class Disjunction():
    '''
    A Disjunction is a list of variables that are linked with or values
    '''
    def __init__(self, vars: List[Variable]) -> None:
        self.vars = vars

    def satisfied(self, model: Model) -> Satisfied:
        '''
        Checks whether the disjunction is true, given an model of all variables.

        Since this is a disjunction, we can return True as soon as we find a variable that is true
        '''
        unknown = False
        for var in self.vars:
            if var.satisfied(model) == Satisfied.Satisfied:
                return Satisfied.Satisfied
            elif var.satisfied(model) == Satisfied.Unknown:
                unknown = True
        return Satisfied.Unknown if unknown else Satisfied.UnSatisfied

    def is_satisfied(self, model: Model):
        '''
        Help determine if a disjunction is satisfied.
        '''
        return self.satisfied(model) == Satisfied.Satisfied

    def find_constant(self, model: Model) -> Variable:
        unknowns = []
        for var in self.vars:
            sat = var.satisfied(model)
            if sat == Satisfied.Unknown:
                unknowns.append(var)

        if len(unknowns) == 1:
            return unknowns[0]

    def __str__(self) -> str:
        return ",".join(map(str, self.vars))


class CNF():
    '''
    A CNF is a conjunction of disjunctions, so the list here is joined by a series of AND operators
    '''
    def __init__(self, sentences: List[Disjunction]) -> None:
        self.sentences = sentences
        self.variables_to_sentences: Mapping[int, Disjunction] = defaultdict(
            lambda: [])
        self.constants = {}
        for sentence in sentences:
            for var in sentence.vars:
                self.variables_to_sentences[var.var].append(sentence)
            if len(sentence.vars) == 1:
                var = sentence.vars[0]
                self.constants[var.var] = var.true

        while True:
            found_constant = False
            for var in list(self.constants):
                for sentence in self.variables_to_sentences[var]:
                    constant = sentence.find_constant(self.constants)
                    if constant:
                        self.constants[constant.var] = constant.true
                        found_constant = True
            if not found_constant:
                break

    def satisfied(self, model: Model) -> Satisfied:
        '''
        In order for a CNF to be satisfied ALL sentences must be true under an model. 
        Therefore, the only can return quickly if we find a sentence that is NOT satisfied.
        This is a FAST way of checking if we are not satisfied. We want this to make sure that we can check fast in the loop.
        '''
        unknown = False
        for sentence in self.sentences:
            res = sentence.satisfied(model)
            if res == Satisfied.UnSatisfied:
                return Satisfied.UnSatisfied
            elif res == Satisfied.Unknown:
                unknown = True
        return Satisfied.Unknown if unknown else Satisfied.Satisfied

    def is_satisfied(self, model: Model) -> Satisfied:
        '''
        Help determine if a cnf is satisfied.
        '''
        return self.satisfied(model) == Satisfied.Satisfied

    def count_satisfied(self, model: Model) -> int:
        """
        This is a more costly check - checks the count of satisfied sentences given the model
        """
        count = 0
        for sentence in self.sentences:
            if sentence.is_satisfied(model):
                count += 1
        return count

    def get_satisfied(self, model: Model) -> Set[Disjunction]:
        '''
        Get all the satisfied sentences
        '''
        satisfied = set()
        for sentence in self.sentences:
            if sentence.is_satisfied(model):
                satisfied.add(sentence)
        return satisfied

    def count_satisfied_diff(self, satisfied, model: Model, var) -> int:
        '''
        Count the difference between sentences satisfied in the model, and the sentences satisfied in the model with var switched.

        This is made efficient by keeping a map from variables to the sentences that include them, 
        so we only need to check some sentences, not all of them. 
        '''
        diff = 0

        for sentence in self.variables_to_sentences[var]:
            new_model = copy(model)
            new_model[var] = not model[var]
            now_satisfied = sentence.is_satisfied(new_model)
            if not sentence in satisfied and now_satisfied:
                diff += 1
            elif sentence in satisfied and not now_satisfied:
                diff -= 1
        return diff

    def unsatisfied_clauses(self, model: Model) -> Generator:
        '''
        Extract all the unsatisfied clauses from the cnf and the model
        '''
        for sentence in self.sentences:
            if not sentence.is_satisfied(model):
                yield sentence


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
        while not self.cnf.is_satisfied(model) and i < MAXIMUM_ITERATIONS:
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
            if var in self.cnf.constants:
                model[var] = self.cnf.constants[var]
            else:
                model[var] = False if random.randint(0, 1) == 0 else True

        def update_model(l):
            i = 0
            l = copy(l)
            random.shuffle(l)
            flipped = False
            while str(model) in checked_models and len(
                    checked_models) < 2**len(self.variables):
                if flipped:
                    model[l[i - 1]] = not model[l[i - 1]]
                rand_var = l[i]
                if not rand_var in self.cnf.constants:
                    model[rand_var] = not model[rand_var]

                    flipped = True
                else:
                    flipped = False
                i += 1

                if i == len(l):
                    # print('checked all variables...')
                    return False

            return True

        i = 0
        while str(model) in checked_models or not self.cnf.is_satisfied(
                model) and len(checked_models) < 2**len(
                    self.variables) and i < MAXIMUM_ITERATIONS:

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
                    count = len(satisfied) + self.cnf.count_satisfied_diff(
                        satisfied, model, var)
                    if m <= count:
                        scores[count].append(var)
                        m = count

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
            t = threading.Thread(target=self.walksat_enhanced,
                                 args=(
                                     golden_number / attempts,
                                     times,
                                     status,
                                     shared_visited,
                                 ),
                                 daemon=True)

            t.start()

        while not len(times):
            time.sleep(0.0001)

        time.sleep(0.1)

        times = list(times.items())
        times = sorted(times, key=lambda x: x[0])

        return times[0]

    def write_solution(self, file_name) -> None:
        with open(file_name, 'w') as file:
            for k in range(len(list(self.solution))):
                v = self.solution[k]
                file.write(f"{'-' if not v else ''}{self.variables[k]}\n")