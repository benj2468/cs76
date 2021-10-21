# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from copy import deepcopy
from typing import List
from main import BinaryCSP, VarHeuristic, test_board, ValHeuristic
from collections import defaultdict
import names
import random
import math


class SectionTime():
    def __init__(self, str: str) -> None:
        split = str.split(" ")
        self.day = split[0]
        self.time = int(split[1])


class SectionAssignment():
    def __init__(self) -> None:
        self.assignment = {}
        self.section_tracking = defaultdict(lambda: set())
        self.leader_tracking = defaultdict(lambda: False)

    def __str__(self) -> str:
        return f"{self.assignment}"


class BuildSections(BinaryCSP):
    def __init__(self, file_name: str, **kwargs) -> None:
        self.variable_map = {}
        self.students = 0
        self.leaders = 0
        constraints = {}
        domains = defaultdict(lambda: set())
        variables = []

        def parse_time(str):
            split = str.split(" ")
            return (split[0], int(split[1]))

        with open(file_name, "r") as f:

            for i, line in enumerate(f.readlines()):
                split = line.split(": ")
                name = split[0]
                if '*' in name:
                    self.leaders += 1
                else:
                    self.students += 1
                self.variable_map[i] = name
                for time in split[1].split(', '):
                    domains[i].add(parse_time(time))
                variables.append(i)

        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                # I think there need to be more constraints
                constraints[(i, j)] = 'related'

        self.size_min = math.floor((self.students / self.leaders) - 1)
        self.size_max = math.ceil((self.students / self.leaders) + 1)

        ## Check if solution if feasible
        options_per_slot = defaultdict(lambda: 0)
        for slots in domains.values():
            for slot in slots:
                options_per_slot[slot] += 1

        valid_slots = 0
        for max_size in options_per_slot.values():
            if self.size_min <= max_size:
                valid_slots += 1
        if valid_slots < self.leaders:
            domains = defaultdict(lambda: [])

        super().__init__(variables, constraints, domains, **kwargs)

        self.default_assignment = SectionAssignment()

    def assign_one(self, var, val, assignment: SectionAssignment):
        new = deepcopy(assignment)
        new.assignment[var] = val
        new.section_tracking[val].add(var)
        if '*' in self.variable_map[var]:
            new.leader_tracking[val] = True
        for neighbor in list(self.constraint_graph[var]):
            if neighbor in assignment.assignment:
                if (neighbor, var) in self.constraints:
                    del self.constraints[(neighbor, var)]
                if (var, neighbor) in self.constraints:
                    del self.constraints[(var, neighbor)]
                self.constraint_graph[var].remove(neighbor)

        return new

    def assign_many(self, inferences: SectionAssignment,
                    assignment: SectionAssignment):
        new = deepcopy(assignment)

        for k, v in inferences.assignment.items():
            new = self.assign_one(k, v, new)
        return new

    def is_assigned(self, var, assignment):
        return super().is_assigned(var, assignment.assignment)

    def print(self, assignment, **kwargs) -> str:
        solution = [f"Assignment:"]
        if assignment == None:
            solution.append("   None")
        else:
            sections = defaultdict(lambda: [])
            for key, value in assignment.assignment.items():
                sections[value].append(self.variable_map[key])

            for i, sec in enumerate(sections):
                solution.append(f"  Section {sec}")
                for prs in sections[sec]:
                    solution.append(f"      - {prs}")

        super().print(solution, **kwargs)

    def is_complete(self, assignment: SectionAssignment):
        for section in assignment.section_tracking.values():
            if len(section) - 1 < self.size_min:
                return False
        return super().is_complete(assignment)

    def is_consistent(self, var, val, assignment: SectionAssignment):
        is_leader = lambda x: '*' in self.variable_map[x]
        total_students = len(assignment.section_tracking[val]) - (
            1 if assignment.leader_tracking[val] else 0)
        total_sections = len(assignment.section_tracking)
        if not val in assignment.section_tracking and total_sections == self.leaders:
            return False
        if total_students == self.size_max - 1 and not is_leader(var):
            return False
        if assignment.leader_tracking[val] and is_leader(var):
            return False

        return True


file_name = "cs1_b.txt"
leaders = 15
students = 150
times = [10, 11, 12, 13, 14, 15, 16, 17, 18]
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# def make_line(leader=False):
#     line = []
#     for day in random.sample(days, len(days) if leader else 5):
#         for time in random.sample(times, len(times) if leader else 9):
#             line.append(f"{day} {time}00")
#     return f"{'*' if leader else ''}{names.get_full_name()}: {', '.join(line)}"

# with open(file_name, "w") as file:
#     for _ in range(leaders):
#         file.write(f"{make_line(True)}\n")
#     for _ in range(students):
#         file.write(f"{make_line()}\n")

builder = BuildSections(f"./{file_name}", var_h=VarHeuristic.DEGREE_TIEBREAKER)
test_board(builder)
