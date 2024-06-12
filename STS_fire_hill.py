import random
import math
import matplotlib.pyplot as plt

score_list = []

def generate_initial_solution(n):
    triples = []
    elements = list(range(1, n + 1))
    while len(triples) < n * (n - 1) // 6:
        triple = random.sample(elements, 3)
        if triple not in triples:
            triples.append(triple)
    return triples

def evaluate_solution(triples, n):
    pair_count = {}
    for triple in triples:
        for i in range(3):
            for j in range(i + 1, 3):
                pair = (min(triple[i], triple[j]), max(triple[i], triple[j]))
                if pair not in pair_count:
                    pair_count[pair] = 0
                pair_count[pair] += 1

    score = 0
    penalty = 0
    for count in pair_count.values():
        if count == 1:
            score += 1
        else:
            penalty += (count - 1) ** 2

    expected_pairs = n * (n - 1) // 2
    if len(pair_count) != expected_pairs:
        penalty += abs(expected_pairs - len(pair_count)) * 20

    unique_triples = [tuple(sorted(triple)) for triple in triples]
    if len(unique_triples) != len(set(unique_triples)):
        penalty += (len(unique_triples) - len(set(unique_triples))) * 50

    return score - penalty

def generate_neighborhood(triples, n):
    neighborhood = []
    for i in range(len(triples)):
        for j in range(3):
            for k in range(1, n + 1):
                if k not in triples[i]:
                    new_triple = triples[i][:]
                    new_triple[j] = k
                    new_triples = triples[:]
                    new_triples[i] = new_triple
                    neighborhood.append(new_triples)
    return neighborhood

def simulated_annealing(n, initial_temp=10000, cooling_rate=0.8, max_iterations=5000):
    current_solution = generate_initial_solution(n)
    current_score = evaluate_solution(current_solution, n)
    temperature = initial_temp

    best_solution = current_solution
    best_score = current_score

    for iteration in range(max_iterations):
        temperature *= cooling_rate
        if temperature <= 0:
            break

        neighborhood = generate_neighborhood(current_solution, n)
        next_solution = random.choice(neighborhood)
        next_score = evaluate_solution(next_solution, n)

        if next_score > current_score:
            current_solution = next_solution
            current_score = next_score
        else:
            acceptance_probability = math.exp((next_score - current_score) / temperature)
            if random.random() < acceptance_probability:
                current_solution = next_solution
                current_score = next_score

        if current_score > best_score:
            best_solution = current_solution
            best_score = current_score

        print(best_score)
        score_list.append(best_score)
    return best_solution, best_score

def is_valid_sts(triples, n):
    unique_triples = [tuple(sorted(triple)) for triple in triples]
    if len(unique_triples) != len(set(unique_triples)):
        return False

    pair_count = {}
    for triple in unique_triples:
        for i in range(3):
            for j in range(i + 1, 3):
                pair = (min(triple[i], triple[j]), max(triple[i], triple[j]))
                if pair not in pair_count:
                    pair_count[pair] = 0
                pair_count[pair] += 1

    for count in pair_count.values():
        if count != 1:
            return False

    expected_pairs = n * (n - 1) // 2
    if len(pair_count) != expected_pairs:
        return False

    return True

# Example usage
n = 13  # Should be of the form 6k+1 or 6k+3
score = 0
while score < 70:
    solution, score = simulated_annealing(n)
print("Solution:")
for triple in solution:
    print(triple)
print("Score:", score)
print("Is valid STS:", is_valid_sts(solution, n))

# 创建图表
plt.plot(score_list)

# 添加标题和标签
# plt.title('Sample Plot')
plt.xlabel('Step')
plt.ylabel('Score')
plt.grid(True)
plt.show()