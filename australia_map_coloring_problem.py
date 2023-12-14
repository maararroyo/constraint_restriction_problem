from collections import defaultdict, deque

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def solve(self):
        assignment = {}
        self.ac3()
        return self.backtracking(assignment)

    def backtracking(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtracking(assignment)
                if result is not None:
                    return result
                assignment.pop(var, None)

        return None

    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for (var2, constraint) in self.constraints[var]:
            if var2 in assignment and not constraint(value, assignment[var2]):
                return False
        return True

    def ac3(self):
        queue = deque([(var1, var2) for var1 in self.constraints for var2, _ in self.constraints[var1]])
        while queue:
            (var1, var2) = queue.popleft()
            if self.revise(var1, var2):
                if len(self.domains[var1]) == 0:
                    return False
                for var3, _ in self.constraints[var1]:
                    if var3 != var2:
                        queue.append((var3, var1))
        return True

    def revise(self, var1, var2):
        revised = False
        for value in self.domains[var1]:
            if all(not constraint(value, value2) for value2 in self.domains[var2] for _, constraint in self.constraints[var1] if constraint == self.constraints[var2][0][1]):
                self.domains[var1].remove(value)
                revised = True
        return revised

# Definición de las variables, los dominios y las restricciones para el problema del coloreado del mapa de Australia

variables = ["Western Australia", "Northern Territory", "South Australia", "Queensland", "New South Wales", "Victoria", "Tasmania"]

domains = {variable: ["red", "green", "blue"] for variable in variables}

def different_colors(value1, value2):
    return value1 != value2

constraints = {
    "Western Australia": [("Northern Territory", different_colors), ("South Australia", different_colors)],
    "Northern Territory": [("Western Australia", different_colors), ("South Australia", different_colors), ("Queensland", different_colors)],
    "South Australia": [("Western Australia", different_colors), ("Northern Territory", different_colors), ("Queensland", different_colors), ("New South Wales", different_colors), ("Victoria", different_colors)],
    "Queensland": [("Northern Territory", different_colors), ("South Australia", different_colors), ("New South Wales", different_colors)],
    "New South Wales": [("South Australia", different_colors), ("Queensland", different_colors), ("Victoria", different_colors)],
    "Victoria": [("South Australia", different_colors), ("New South Wales", different_colors)],
    "Tasmania": []
}

# Solución del problema

csp = CSP(variables, domains, constraints)
solution = csp.solve()
print(solution)
