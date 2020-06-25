import sys
import math

mid = sys.stdin.readlines()
res = list(map(lambda a: str.replace(a, "\n", ""), mid))
all = []
for i in res:
    all.append(i.split())
np = all.pop(0)
n,k = int(np[0]),int(np[1])

def identity(n):
  m = [[0 for i in range(n)] for j in range(n)]
  for q in range(0,n):
    m[q][q]=1
  return m

data =[list(map(float, m)) for m in all[0:n]]

parameter = [[list(map(float, m)) for m in all[n:]], [identity(2) for i in range(k)], [1/n for i in range(k)]]



def determinant(m):
  return m[0][0]*m[1][1]-m[0][1]*m[1][0]


def inverse(m):
  detm = determinant(m)
  return [[m[1][1]/detm, -1*m[0][1]/detm],
          [-1*m[1][0]/detm, m[0][0]/detm]]

def Normal(x,mu,cov):
  covinv = inverse(cov)
  xmmu = [x[i]-mu[i] for i in range(len(mu))]
  p = 1 / math.sqrt(2 * math.pi**n *determinant(cov)) * math.exp(-(xmmu[1]**2*covinv[1][1] + xmmu[1]*xmmu[0]*covinv[0][1] +
                                                       xmmu[0]**2*covinv[0][0] + xmmu[0]*xmmu[1]*covinv[1][0])/2)
  return p



def Estep(x,para):
  mu_i = para[0]
  cov_i = para[1]
  w_j = para[2]
  w_ij=[]
  for j in range(k):
    w_i=[]
    for i in range(n):
      w_i.append(w_j[j]*Normal(x[i],mu_i[j],cov_i[j]))
    w_ij.append(w_i)
  den =[]
  for i in range(n):
    sum = 0
    for j in range(k):
      sum += w_ij[j][i]
    den.append(sum)
  r = []
  for j in range(k):
    r.append([w_ij[j][i]/den[i] for i in range(n)])

  return r


def Mstep(w_ij, x):
    mu_j = []
    cov_j = []
    w_j = []
    for j in range(k):
        mu_no_0 = 0
        mu_no_1 = 0
        mu_deno = sum(w_ij[j])
        for i in range(n):
            mu_no_0 += w_ij[j][i] * x[i][0]
            mu_no_1 += w_ij[j][i] * x[i][1]
        mu_j.append([mu_no_0 / mu_deno, mu_no_1 / mu_deno])

        sig_no_00 = 0
        sig_no_01 = 0
        sig_no_10 = 0
        sig_no_11 = 0
        for i in range(n):
            xmmu = [x[i][q] - mu_j[j][q] for q in range(len(mu_j[j]))]
            sig_no_00 += w_ij[j][i] * xmmu[0] * xmmu[0]
            sig_no_01 += w_ij[j][i] * xmmu[0] * xmmu[1]
            sig_no_10 += w_ij[j][i] * xmmu[1] * xmmu[0]
            sig_no_11 += w_ij[j][i] * xmmu[1] * xmmu[1]
        cov_j.append([[sig_no_00 / mu_deno, sig_no_01 / mu_deno], [sig_no_10 / mu_deno, sig_no_11 / mu_deno]])

        w_j.append(mu_deno / n)
    return ([mu_j, cov_j, w_j])



def EM(x, para):
    post_prob = Estep(x, para)
    para = Mstep(post_prob, x)
    return para

def predict(data, p):
    final_p = []
    c = []
    for j in range(k):
        p_j = [p[2][j] * Normal(data[q], p[0][j], p[1][j]) for q in range(n)]
        final_p.append(p_j)

    r = []
    for i in range(n):
        r_i = []
        for j in range(k):
            r_i.append(final_p[j][i])
        r.append(r_i)

    for i in r:
        c.append(i.index(max(i)))
    return c


cluster = EM(data, parameter)
label = predict(data, cluster)

for i in label:
    print(i)
