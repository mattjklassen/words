from collections import Counter as C 
def subset(a,b): 
    return all(a[k]<=b[k] for k in a) with open('words2.txt') as f2, open('words3.txt') as f3, open('words4.txt') as f4: w2, w3, w4 = (f.read().split() for f in (f2,f3,f4)) G = {w:[] for w in [*w2,*w3,*w4]} for A,B in ((w2,w3),(w3,w4)): for x in A: cx = C(x) G[x].extend([y for y in B if subset(cx, C(y))]) for k, v in G.items(): print(k, '->', v)
