days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

shirts = ["S1", "S2", "S3", "S4", "S5"]
pants = ["P1", "P2", "P3"]

shalwar_qamees = ["SQ1", "SQ2"]
shirt_pant = [(s, p) for s in shirts for p in pants]

def wardrobe_csp():
    solutions = []
    assignment = {}

    def is_valid(day, outfit):
        # Ensure uniqueness across days
        for d in assignment:
            if assignment[d] == outfit:
                return False
        return True

    def backtrack(i):
        if i == len(days):
            solutions.append(assignment.copy())
            return

        day = days[i]

        if day == "Monday" or day == "Thursday":
            domain = shirt_pant
        elif day == "Friday":
            domain = shalwar_qamees
        else:
            domain = shirt_pant + shalwar_qamees

        for outfit in domain:
            if is_valid(day, outfit):
                assignment[day] = outfit
                backtrack(i + 1)
                del assignment[day]

    backtrack(0)
    return solutions

solutions = wardrobe_csp()

print("Total schedules found:", len(solutions))
print()

for i, sol in enumerate(solutions[:5], 1):
    print(f"Schedule {i}:")
    for day in days:
        print(f"  {day}: {sol[day]}")
    print()