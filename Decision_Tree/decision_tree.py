import numpy as np
import operator

dataset = [[1, 1, 1],
           [1, 1, 1],
           [1, 0, 0],
           [0, 1, 0],
           [0, 1, 0]]

labels = ['no surfacing','flippers']
dataset = np.array(dataset)


def cal_entropy(dataset):
    '''
    calculate entropy
    the formula is H(X) = - ∑(i to n) pi * log(pi)
    '''
    entropy = 0.0
    observations_count = dataset.shape[0]
    labels_count = {}
    for observation in dataset:
        current_label = observation[-1]
        if current_label not in labels_count.keys():
            labels_count[current_label] = 0
        labels_count[current_label] += 1
    for label in labels_count:
        proba = labels_count[label] / float(observations_count)
        entropy -= proba * np.log(proba)
    return entropy


def split_dataset(dataset, axis, value):
    '''
    split dataset by one selected feature
    axis : the index of selected feature
    value : the value of selected feature
    '''
    retDataSet = None
    for featVec in dataset:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec = np.concatenate((reducedFeatVec, featVec[axis+1:]))
            if retDataSet is None:
                retDataSet = reducedFeatVec[np.newaxis, :]
            else:
                retDataSet = np.vstack((retDataSet, reducedFeatVec))
    return retDataSet


def choose_feature(dataset):
    '''
    suppose there is k class Ck, |Ck| is the number of observations labeled k.
    suppose there is sub dataset D1 to Dn divided by feature A, |Di| is the number of sub dataset divided by A
    |Dik| is the number of sub dataset Di which labeld as Ck
    '''
    number_of_features = dataset.shape[1] -1
    # calculate the entropy of H(Dataset) = - ∑(k to K) p * log p, p is the probability of class k
    # p = |Ck| / |Dataset|, the number of data labeled class k compared with total number of dataset
    base_entropy = cal_entropy(dataset)

    highest_info_gain = 0.0
    index_of_selected_feature = -1
    # iterate over all the features
    for i in range(number_of_features):
        # get a set of unique values of specific features, for every data
        unique_values_set = set([observation[i] for observation in dataset])
        new_entropy = 0.0
        for value in unique_values_set:
            splited_dataSet = split_dataset(dataset, i, value)
            # calculate H(D|A), =  ∑(i to n) |Di|/|D| * H(Di)
            # = -∑(i to n) |Di|/|D| * ∑(k to K) |Dik|/|Di| * log( |Dik|/|Di| )
            proba_of_value = len(splited_dataSet) / float(len(dataset))
            new_entropy += proba_of_value * cal_entropy(splited_dataSet)
        info_gain = base_entropy - new_entropy  # calculate the info gain; ie reduction in entropy
        if (info_gain > highest_info_gain):  # compare this to the best gain so far
            highest_info_gain = info_gain  # if better than current best, set to best
            best_feature = i
    return best_feature  # returns index of best feature


def get_majority_label(class_list):
    '''
    get the most frequent label, will be used to label a node.
    '''
    class_count={}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        else:
            class_count[vote] += 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

def createTree(dataset, labels):
    class_list = [observation[-1] for observation in dataset]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]#stop splitting when all of the classes are equal
    if len(dataset[0]) == 1: #stop splitting when there are no more features in dataSet
        return get_majority_label(class_list)
    best_feature = choose_feature(dataset)
    best_feature_label = labels[best_feature]
    decision_tree = {best_feature_label:{}}
    del(labels[best_feature])
    # get a set of unique values of selected best features, for every data
    unique_values_set = set([observation[best_feature] for observation in dataset])
    for value in unique_values_set:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        decision_tree[best_feature_label][value] = createTree(split_dataset(dataset, best_feature, value),subLabels)
    return decision_tree


print(createTree(dataset, labels))