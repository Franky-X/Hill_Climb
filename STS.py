import random
import matplotlib.pyplot as plt

score_list = []

def generate_initial_solution(n):
    # Generate an initial solution with random triples
    triples = []
    elements = list(range(1, n + 1))
    while len(triples) < n * (n - 1) // 6:
        triple = random.sample(elements, 3)
        if triple not in triples:
            triples.append(triple)
    return triples

# def evaluate_solution(triples, n):
#     # Evaluate the solution by counting the number of covered pairs
#     covered_pairs = set()
#     for triple in triples:
#         for i in range(3):
#             for j in range(i + 1, 3):
#                 covered_pairs.add((min(triple[i], triple[j]), max(triple[i], triple[j])))
#     return len(covered_pairs)

# def evaluate_solution(triples, n):
#     # Evaluate the solution with penalties for over-covered pairs
#     pair_count = {}
#     for triple in triples:
#         for i in range(3):
#             for j in range(i + 1, 3):
#                 pair = (min(triple[i], triple[j]), max(triple[i], triple[j]))
#                 if pair not in pair_count:
#                     pair_count[pair] = 0
#                 pair_count[pair] += 1

#     # Calculate score with penalties for over-covered pairs
#     score = 0
#     for count in pair_count.values():
#         if count == 1:
#             score += 1  # Good, pair covered exactly once
#         else:
#             score -= (count - 1)  # Penalty for over-covered pairs

#     return score

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
            score += 1  # Good, pair covered exactly once
        else:
            penalty += (count - 1) ** 2  # Penalty for over-covered pairs (quadratic penalty)

    # Ensure that the solution covers exactly the required number of unique pairs
    expected_pairs = n * (n - 1) // 2
    if len(pair_count) != expected_pairs:
        penalty += abs(expected_pairs - len(pair_count)) * 10

    return score - penalty

def generate_neighborhood(triples, n):
    # Generate neighboring solutions by swapping elements in triples
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

def hill_climbing(n):
    current_solution = generate_initial_solution(n)
    current_score = evaluate_solution(current_solution, n)
    iter = 0
    while True:
        iter = iter + 1
        # print(iter)
        neighborhood = generate_neighborhood(current_solution, n)
        next_solution = None
        next_score = current_score
        for solution in neighborhood:
            score = evaluate_solution(solution, n)
            if score > next_score:
                next_solution = solution
                next_score = score

        if next_solution == None:
            break
        current_solution = next_solution
        current_score = next_score
        print(current_score)
        score_list.append(current_score)
    return current_solution, current_score

def is_valid_sts(triples, n):
    # Check if there are any duplicate triples
    unique_triples = [tuple(sorted(triple)) for triple in triples]
    if len(unique_triples) != len(set(unique_triples)):
        return False
    
    # Check if each pair appears exactly once in the triples
    pair_count = {}
    for triple in unique_triples:
        for i in range(3):
            for j in range(i + 1, 3):
                pair = (min(triple[i], triple[j]), max(triple[i], triple[j]))
                if pair not in pair_count:
                    pair_count[pair] = 0
                pair_count[pair] += 1

    # Verify that every pair appears exactly once
    for count in pair_count.values():
        if count != 1:
            return False
    
    # Check if the number of unique pairs matches the expected number
    expected_pairs = n * (n - 1) // 2
    if len(pair_count) != expected_pairs:
        return False

    return True

# Example usage
k = 2
n = 6*k+1  # Should be of the form 6k+1 or 6k+3
score = 0
while score < 70:
    solution, score = hill_climbing(n)
print("Solution:")
for triple in solution:
    print(triple)
print("Score:", score)
print("Is valid STS:", is_valid_sts(solution, n))

# 示例数据
# data = [1, 4, 2, 5, 7, 8, 6]

# 创建图表
plt.plot(score_list)

# 添加标题和标签
# plt.title('Sample Plot')
plt.xlabel('Step')
plt.ylabel('Score')
plt.grid(True)
plt.show()
