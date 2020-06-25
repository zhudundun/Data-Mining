import sys
# c1, create frequent-1 itemset
def create_c1(transaction_table):
    c1 = {}
    for p in transaction_table:
        for item in p:
            item = tuple(item,)
            if item not in c1:
                c1[item] = 1
            else:
                c1[item] += 1
    return c1


# f1, create frequent-1 itemset meeting constraint
def create_f1(c1):
    f1 = {k: v for (k, v) in c1.items() if v >= minsup}
    sorted_f1 = dict(sorted(f1.items(), key=lambda f1: f1[1], reverse=True))
    return sorted_f1


# create ck, generate frequent k+1 itemset using frequent k itemset
def create_ck(f_km1, k):
    ck = []
    len_f_km1 = len(f_km1.keys())
    *f_km1_key, = f_km1
    f_km1_key.sort()
    for i in range(len_f_km1):
        for j in range(i+1, len_f_km1):
            a1 = f_km1_key[i]
            a2 = f_km1_key[j]
            if a1[0:k-2] == a2[0:k-2]:
                ck.append(sorted(list(set(f_km1_key[i]) | set(f_km1_key[j]))))

    return ck


# check ck, get support for frequent k+1 itemset
def check_ck(ck):
    ckf = {}
    for j in ck:
        for i in trans:
            if len(set(j).intersection(set(i))) == len(j):
                if tuple(j) not in ckf:
                    ckf[tuple(j)] = 1
                else:
                    ckf[tuple(j)] += 1
    return ckf


# create fk,delete item set doesn't meet constraint
def create_fk(ckf):
    for (l, v) in list(ckf.items()):
        if v < minsup:
            del(ckf[l])
    return ckf


def freq_item(transaction_table):
    freq_item = {}
    c1 = create_c1(transaction_table)
    fkm1 = create_f1(c1)
    freq_item.update(fkm1)
    k = 2
    while fkm1:
        ck = create_ck(fkm1, k)
        cfk = check_ck(ck)
        fk = create_fk(cfk)
        freq_item.update(fk)
        k = k+1
        fkm1 = fk
    tt = [(k, v) for k, v in freq_item.items()]
    return tt


def closed_item (transaction_table):
    fi = freq_item(transaction_table)
    m = set()

    for i in fi:
        for j in fi:
            if i[1] == j[1] and (set(i[0]).issubset(set(j[0]))) and (i!=j):
                m.add(i)
                break
    return(list(set(fi)-m))

def max_item(transaction_table):
    fi = freq_item(transaction_table)
    m = set()

    for i in fi:
        for j in fi:
            if (set(i[0]).issubset(set(j[0]))) and (i != j):
                m.add(i)
                break
    return(list(set(fi) - m))


# output the result
def out(result):
    result.sort(key=lambda x:x[0])
    result.sort(key=lambda x:x[1], reverse=True)
    for i in result:
        print(str(i[1]) + ':', *i[0])


# input
minsup = int(input())

mid = sys.stdin.readlines()
res = list(map(lambda a: str.replace(a, "\n", ""), mid))
trans = []
for i in res:
    trans.append(i.split(' '))


# output q1 result
out(freq_item(trans))
print("")

# output q2 result
out(closed_item(trans))
print("")

# output q3 result
out(max_item(trans))
