# follow path from 2-letter word by choosing random extension index
# at each level, and using only edges of weight one.

# run with:  python path1.py XX

import sys
import random

print("Argument List:", str(sys.argv))
args = len(sys.argv)

alpha1 = sys.argv[1]

def import_alphas(file):
    alphas = []
    with open(file, 'r') as f:
        alphas = f.readlines()
        f.close()
    n = len(alphas)
    for i in range(n):
        alphas[i] = alphas[i].strip()
    return alphas

# form arrays of k-nodes
        
def load_nodes() :
    knodes = []
    for i in range(16) :
        if i < 2 :
            nodes = []
            knodes.append(nodes)
            continue
        file = "../nodes/" + str(i) + "nodes.txt"
        nodes = import_alphas(file)
        knodes.append(nodes)
    return knodes

knodes = load_nodes()
# array knodes[i] is from file knodes.txt with k = i

def load_words() :
    kwords = []
    for i in range(16) :
        if i < 2 :
            words = []
            kwords.append(words)
            continue
        file = "../nodes/" + str(i) + "words.txt"
        words = import_alphas(file)
        kwords.append(words)
    return kwords

kwords = load_words()
# array kwords[i] is from file kwords.txt with k = i

def iof_word(alpha, words):
    low = 0
    high = len(words)-1
    while (low <= high):
        guess = (low + high) // 2
        if words[guess] == alpha:
            return guess
        elif words[guess] < alpha:
            low = guess + 1
        else:
            high = guess - 1
    return -1

# all_edges[i,j] contains edges from file i-j-edges.txt
# i ranges 2 to 14, and j goes i+1 to 15

def load_edges() :
    all_edges = []
    for i in range(15) :
        some_edges = []
        if i < 2 :
            edges = []
            some_edges.append(edges)
            all_edges.append(some_edges)
            continue
        for j in range(16) :
            if j < i+1 :
                edges = []
                some_edges.append(edges)
                continue
            file = "../edges/" + str(i) + "-" + str(j) + "-" + "edges.txt"
            edges = import_alphas(file)
            some_edges.append(edges)
        all_edges.append(some_edges)
    return all_edges

all_edges = load_edges()

def load_indices() :
    all_indices = []
    for i in range(15) :
        some_indices = []
        if i < 2 :
            indices = []
            some_indices.append(indices)
            all_indices.append(some_indices)
            continue
        for j in range(16) :
            if j < i+1 :
                indices = []
                some_indices.append(indices)
                continue
            file = "../edges/" + str(i) + "-" + str(j) + "-" + "indices.txt"
            indices = import_alphas(file)
            some_indices.append(indices)
        all_indices.append(some_indices)
    return all_indices

all_indices = load_indices()

def gen_path(alpha1, weight) :
    k = iof_word(alpha1, knodes[2])
    line = all_edges[2][3][k]
    array = line.split(";")
    alpha = array[0]
    adds = array[1].split(",")
    numadds = len(adds)
    r = random.randint(0, numadds-1)
    add = adds[r]
    beta = alpha + add
    beta = "".join(sorted(beta))


# n = length of alpha node, k = index in nodes array
# output is index into nodes array of length n + 1
def gen_step1(n, k) :  
    line = all_indices[n][n+1][k]
    array = line.split(";")
    if len(array[1]) > 0 :
        alpha = array[0]
        indices = array[1].split(",")
        num = len(indices)
        r = random.randint(0, num-1)
        index = int(indices[r])
        beta = knodes[n+1][index]
        # print(beta)
        return index
    return -1

print(alpha1)

def search_paths(alpha1) :
    counter = 0
    while 1 :
        n = len(alpha1)
        k = iof_word(alpha1, knodes[n])
        path = alpha1
        while n < 15 :
            k = gen_step1(n, k)
            if k == -1 :
                break
            new = kwords[n+1][k].split(";")
            words = new[1]
            path += " --> " + words
            n += 1
        if n == 15 :
            print(path)
            print("path length:  ", n-1)
        counter += 1
        if counter > 1000 :
            break

search_paths(alpha1)


