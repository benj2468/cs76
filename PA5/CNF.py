# Benjamin Cape - 21F - CS76
# PA5
# 10.24.21

from collections import defaultdict
from typing import Generator, List, Mapping, Set, Mapping
from copy import copy
from enum import Enum

Model = Mapping[int, bool]


class Satisfied(Enum):
    '''
    Useful helper for checking satisfied
    '''
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
