import sys

dataset = sys.stdin.readlines()

for i in range(len(dataset)):
    dataset[i] = dataset[i].replace('\n', '')
    dataset[i] = dataset[i].split(',')
features = dataset[0]
class_label = dataset[0].index("class_type")

N = 0
dataset_by_class = dict()
for i in range(1, 8):
    dataset_by_class[str(i)] = list()
for i, train in enumerate(dataset):
    if i > 0 and train[class_label] != "-1":
        dataset_by_class[train[class_label]].append(train)
        N += 1

C = 7
prior_probs = dict()
for class_type, data in dataset_by_class.items():
    prior_probs[class_type] = (len(dataset_by_class[class_type]) + 0.1) / (N + 0.1 * C)

for i, test in enumerate(dataset):
    if i > 0 and test[class_label] == "-1":
        probs = dict()
        for k in range(1, 8):
            probs[str(k)] = 0
        for class_type, prob in probs.items():
            probs[class_type] = prior_probs[class_type]
            for j, f in enumerate(test):
                if j != 0 and j != class_label:
                    count = 0
                    for same_class_example in dataset_by_class[class_type]:
                        if same_class_example[j] == f:
                            count += 1
                    D = 2
                    if features[j] == "legs":
                        D = 6
                    probs[class_type] *= (count + 0.1) / (len(dataset_by_class[class_type]) + 0.1 * D)
        print(max(probs, key=probs.get))
