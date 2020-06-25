import sys
import math
mid = sys.stdin.readlines()
res = list(map(lambda a: str.replace(a, "\n", ""), mid))

df=[]
df_test=[]
df_train=[]

for j in res:
    df.append(j.split(' '))
for i in df:
    temp=[]
    for k in i[1:]:
        temp.append(k[2:])
    temp.append(i[0])
    if i[0]=='-1':
        df_test.append(temp)
    else: 
        df_train.append(temp)
            
n_attr=len(df_train[0])-1
attributes =  list(range(n_attr))

def get_attribute(df, attr_index):
    label_list=[]
    for i in range(len(df)):
        label_list.append(df[i][attr_index])
    return label_list

def num_class(df, predict_attr):
    label=get_attribute(df,predict_attr)
    class_num=dict.fromkeys(set(label),0)
    for item in label:
        class_num[item]+=1
           

    return class_num


def select_threshold(df, attribute, predict_attr):
    # Convert dataframe column to a list and round each value
    values = get_attribute(df, attribute)
    values = [ float(x) for x in values]
    # Remove duplicate values by converting the list to a set, then sort the set
    values = set(values)
    values = list(values)
    values.sort()
    max_ig = float("-inf")
    thres_val = 0
    # try all threshold values that are half-way between successive values in this sorted list
    for i in range(0, len(values) - 1):
        thres = (values[i] + values[i+1])/2
        ig = info_gain(df, attribute, predict_attr, thres)
        if ig > max_ig:
            max_ig = ig
            thres_val = thres
    # Return the threshold value that maximizes information gained
    return thres_val

def info_gain(df, attribute, predict_attr, threshold):
    attribute_list=get_attribute(df,attribute)
    sub1_index=[i for i in range(len(attribute_list)) if float(attribute_list[i])<=threshold]
    sub2_index=[i for i in range(len(attribute_list)) if float(attribute_list[i])>threshold]

    sub_1 = [df[i] for i in sub1_index]
    sub_2 = [df[i] for i in sub2_index]
    # Determine information content, and subract remainder of attributes from it
    ig = info_entropy(df, predict_attr) - remainder(df, [sub_1, sub_2], predict_attr)
    return ig

def info_entropy(df, predict_attr):
    # Dataframe and number of positive/negatives examples in the data
    label_count=num_class(df,predict_attr)   
    # Calculate entropy
    I=0
    if 0 in label_count.values():
        I = 0
    else:
        sum_count=sum(label_count.values())
        for i in label_count.values():
            I = I + ((-1*i)/(sum_count))*math.log(i/(sum_count), 2) 
    return I

def remainder(df, df_subsets, predict_attr):
    # number of test data
    num_data = len(df)
    remainder = float(0)
    for df_sub in df_subsets:
        if len(df_sub) > 1:
            remainder += float(len(df_sub)/num_data)*info_entropy(df_sub, predict_attr)
    return remainder

def choose_attr(df, attributes, predict_attr):
    max_info_gain = float("-inf")
    best_attr = None
    threshold = 0
    # Test each attribute (note attributes maybe be chosen more than once)
    for attr in attributes:
        thres = select_threshold(df, attr, predict_attr)
        ig = info_gain(df, attr, predict_attr, thres)
        if ig > max_info_gain:
            max_info_gain = ig
            best_attr = attr
            threshold = thres
    return best_attr, threshold

def build_tree(df, cols, predict_attr,depth):
    # Get the number of positive and negative examples in the training data
    label_count = num_class(df, predict_attr)
    # If train data has all positive or all negative values
    # then we have reached the end of our tree
    if len(df) in label_count.values():
        # Create a leaf node indicating it's prediction
        leaf = Node(None,None)
        leaf.leaf = True
        for key, value in label_count.items():
            if value==len(df):
                leaf.predict=key
            
        return leaf
    else:
        # Determine attribute and its threshold value with the highest
        # information gain
        best_attr, threshold = choose_attr(df, cols, predict_attr)
        # Create internal tree node based on attribute and it's threshold
        tree = Node(best_attr, threshold)
        attribute_list=get_attribute(df,best_attr)

        sub1_index=[i for i in range(len(attribute_list)) if float(attribute_list[i])<=threshold]
        sub2_index=[i for i in range(len(attribute_list)) if float(attribute_list[i])>threshold]

        sub_1 = [df[i] for i in sub1_index]
        sub_2 = [df[i] for i in sub2_index]

        #depth+=1
        if depth==2:
            tree.leaf=True
            for key, value in label_count.items():
                if value==max(label_count.values()):
                    tree.predict=key
            return tree            
        # Recursively build left and right subtree
        depth+=1
        tree.left = build_tree(sub_1, cols, predict_attr,depth)
        tree.right = build_tree(sub_2, cols, predict_attr,depth)
        return tree
    

def predict(node, row_df):
   
    # If we are at a leaf node, return the prediction of the leaf node
    if node.leaf:
        return node.predict
    # Traverse left or right subtree based on instance's data
    if float(row_df[node.attr]) <= node.thres:
        return predict(node.left, row_df)
    elif float(row_df[node.attr])> node.thres:
        return predict(node.right, row_df)

    
def test_predictions(root, df):
    num_data = len(df)
    result = []
    for i in range(num_data):
        result.append(predict(root, df[i]))
     
    return result

class Node(object):
    def __init__(self, attribute, threshold):
        self.attr = attribute
        self.thres = threshold
        self.left = None
        self.right = None
        self.leaf = False
        self.predict = None
        
root=build_tree(df_train,attributes , n_attr,0)
result=test_predictions(root,df_test)
#print(test_predictions(root,df_test))
#print(df_test)
for i in result:
        print(i)
#print(df_train[0])
