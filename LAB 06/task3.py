import random
ITEMS =[
    {"item": "Sleeping bag",      "weight": 15, "sp": 15},
    {"item": "Rope",              "weight": 3,  "sp": 7},
    {"item": "Knife",             "weight": 2,  "sp": 10},
    {"item": "Torch",             "weight": 5,  "sp": 5},
    {"item": "Bottle",            "weight": 9,  "sp": 8},
    {"item": "Glucose",           "weight": 20, "sp": 17},
]
MAX_WEIGHT = 30
N = len(ITEMS)
POP_SIZE      = 30
NUM_GEN       = 100
CROSSOVER_RATE = 0.80
MUTATION_RATE  = 0.10
ELITE_COUNT    = 2

def random_chromosome():
    """Binary string: 1 = take the item, 0 = leave it."""
    return [random.randint(0, 1) for _ in range(N)]

def fitness(chrom):
    """
    Total survival points if weight ≤ MAX_WEIGHT, else 0 (hard penalty).
    """
    total_w = sum(ITEMS[i]["weight"] for i in range(N) if chrom[i])
    total_sp = sum(ITEMS[i]["sp"]     for i in range(N) if chrom[i])
    return total_sp if total_w <= MAX_WEIGHT else 0

def roulette_select(population, fitnesses):
    """Fitness-proportionate (roulette wheel) selection."""
    total = sum(fitnesses)
    if total == 0:
        return random.choice(population)
    pick = random.uniform(0, total)
    cumulative = 0
    for chrom, f in zip(population, fitnesses):
        cumulative += f
        if cumulative >= pick:
            return chrom
    return population[-1]

def single_point_crossover(parent_a, parent_b):
    """Swap tails at a random cut-point."""
    if random.random() > CROSSOVER_RATE:
        return list(parent_a)        
    point = random.randint(1, N - 2)
    return parent_a[:point] + parent_b[point:]

def mutate(chrom):
    """Flip each bit independently with probability MUTATION_RATE."""
    return [1 - g if random.random() < MUTATION_RATE else g for g in chrom]

def genetic_algorithm():
    population = [random_chromosome() for _ in range(POP_SIZE)]
    best_chrom, best_fit = None, 0

    for generation in range(1, NUM_GEN + 1):
        fitnesses = [fitness(c) for c in population]

        gen_best_fit = max(fitnesses)
        gen_best_chrom = population[fitnesses.index(gen_best_fit)]
        if gen_best_fit > best_fit:
            best_fit = gen_best_fit
            best_chrom = list(gen_best_chrom)

        sorted_pop = sorted(zip(fitnesses, population), key=lambda x: -x[0])
        new_pop = [list(c) for _, c in sorted_pop[:ELITE_COUNT]]

        while len(new_pop) < POP_SIZE:
            parent_a = roulette_select(population, fitnesses)
            parent_b = roulette_select(population, fitnesses)
            child    = single_point_crossover(parent_a, parent_b)
            child    = mutate(child)
            new_pop.append(child)

        population = new_pop

        if generation % 10 == 0 or generation == 1:
            print(f"Gen {generation:3d} | Best SP so far: {best_fit}")

    return best_chrom, best_fit

best_chrom, best_sp = genetic_algorithm()

selected   = [ITEMS[i] for i in range(N) if best_chrom[i]]
total_w    = sum(it["weight"] for it in selected)

print("\n" + "="*50)
print("  OPTIMAL SELECTION")
print("="*50)
print(f"{'Item':<22} {'Weight':>8}  {'SP':>5}")
print("-"*40)
for it in selected:
    print(f"{it['item']:<22} {it['weight']:>7.1f}  {it['sp']:>5}")
print("-"*40)
print(f"{'TOTAL':<22} {total_w:>7.1f}  {best_sp:>5}")
print(f"\nCapacity used: {total_w:.1f} / {MAX_WEIGHT} kg")