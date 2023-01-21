#%%
a = [ 3, 6, 7, 1, 3 ,8, 19, 1, 2, 3]
a_s = sum(a)/len(a)
var= sum( [(a_i - a_s)**2 for a_i in a])/(len(a)-1 )
var
# %%
b = {3, 6, 7, 1, 3 ,8, 19, 1, 2, 3}


#%%
import math
def entropy(classes):
    n = sum([len(c) for c in  classes])
    result = 0
    for c in classes:
        if len(c) == 0:
            continue
        n_c = len(c)/n
        result += n_c * math.log2(n_c)
    return -result

def gain (p_nodes,c_nodes):
    n = sum(len(c) for c in p_nodes)
    result_c = 0
    for c in c_nodes:
        n_c = sum(len(c_i) for c_i in c)
        result_c += n_c/n * entropy(c)
    result = entropy(p_nodes) - result_c
    return result

def split_info(c_nodes):
    n = sum(len(c) for c in c_nodes)
    result = 0
    for c in c_nodes:
        result +=  len(c)/n * math.log2(len(c)/n)
    return -result


def gain_ratio(p_nodes,c_nodes):
    p_gain = gain(p_nodes,c_nodes)
    return p_gain / split_info(c_nodes)


parent_nodes = [[0]*10,[1]*10]
p_yes = [[0]*6,[1]*4]
p_no = [[0]*4,[1]*6]
child_nodes= [p_yes,  p_no]
print(f'own car { gain(parent_nodes,child_nodes)}' )
print(f'gain ratio {gain_ratio(parent_nodes,child_nodes)}')

p_family = [[0]*1,[1]*3]
p_sports = [[0]*8,[1]*0]
p_luxury = [[0] *1,[1]*7]

child_nodes= [p_family,  p_sports,p_luxury]
print(f'car type {gain(parent_nodes,child_nodes)}')
print(f'gain ratio {gain_ratio(parent_nodes,child_nodes)}')

child_nodes = []
for i in range(10):
    child_nodes.append([[0]*1,[1]*0])
for i in range(10):
    child_nodes.append([[0]*0,[1]*1])
print(f'student id {gain(parent_nodes,child_nodes)}')
print(f'gain ratio {gain_ratio(parent_nodes,child_nodes)}')
#1 - (10/20) * -1 *(6/10 * math.log2(6/10) + 4/10 * math.log2(4/10)) - (10/20) * -1 *(4/10 * math.log2(4/10) + 6/10 * math.log2(6/10))
#1 - (4/20) * -1 * (1/)
# %%

# %%
