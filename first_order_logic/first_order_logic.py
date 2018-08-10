import time, copy
from collections import defaultdict

dic = defaultdict(list)
sentences = []
queries = []

def kb_tell(dic, sents, length = 0):
    if len(sents) == 1: 
        sents_split = sents[0].split(" | ")
        sents_split = []
        for j in sents[0].split(" | "):
            sents_split.append(j.partition("(")[0])
        sents_split = list(set(sents_split))
        for j in sents_split:
            dic[j].append(length)
    else:
        for i in range(len(sents)):
            sents_split = []
            for j in sents[i].split(" | "):
                sents_split.append(j.partition("(")[0])
            sents_split = list(set(sents_split))
            for j in sents_split:
                dic[j].append(i)

def negation(kb):
    if kb[0] == "~":
        not_kb = kb[1:]
    else:
        not_kb = "~" + kb
    return not_kb

def parameter(kb_set, temp_set_kb):
    kb_set_new = []
    for i in kb_set:
        kb_para_old = i.partition("(")[2][:-1].split() #take parameters
        kb_para = kb_para_old[0].split(",") #split parameters
        kb_para_old = "".join(kb_para_old) 
        for j in range(len(kb_para)):
            if kb_para[j] in temp_set_kb and kb_para[j].islower():
                kb_para[j] = temp_set_kb[kb_para[j]]
        kb_para = ",".join(kb_para)
        i = i.replace(kb_para_old, kb_para)
        kb_set_new.append(i)
    return kb_set_new

def unify(query, kb, intt = -1):
    temp_set_kb = {}

    queries = query.split(" | ")
    if intt >= 0:
        query = queries[intt]

    kb_set = kb.split(" | ")
    not_query = negation(query)

    kb_for_query = []
    for i in kb_set:
        if i.partition("(")[0] == not_query.partition("(")[0]:
            kb_for_query.append(i)

    for i in kb_for_query:
        kb_para = i.partition("(")[2][:-1].split()[0].split(",") #parameter of kb
        query_para = query.partition("(")[2][:-1].split()[0].split(",") #parameter of query
        breakk = False

        for j in range(len(kb_para)):
            if kb_para[j][0].isupper() and query_para[j][0].isupper() and kb_para[j] != query_para[j]: #not same constants
                breakk = True #make flag to loop for next kb_for_query

        if breakk:
            continue

        #parameter checking process
        for j in range(len(kb_para)):
            if kb_para[j][0].islower() and query_para[j][0].isupper(): #kb has variable and query has Constant
                temp_set_kb[kb_para[j]] = query_para[j]
            elif kb_para[j][0].isupper() and query_para[j][0].islower(): #query has variable and kb has Constant
                temp_set_kb[query_para[j]] = kb_para[j]
            else:
                temp_set_kb[kb_para[j]] = query_para[j]
        
        if len(queries) == 1 and len(kb_set) == 1: #check for contradiction
            kb_set_new = []   
            kb_set_old = kb_set[0]
            kb_set_new = parameter(kb_set, temp_set_kb)

            kb_set = " | ".join(kb_set_new)
            kb_para = kb_set.partition("(")[2][:-1]
            kb_para_set = kb_para.split(",")
            #all parameters check not just one parameter
            para_const = [kb_para_set[i][0].isupper() for i in range(len(kb_para_set))]                

            if (kb_set in sentences or kb_set_old in sentences):
                return 1
            else:
                return -1
        
        #if predicate:
        kb_set.remove(i)
    #if predicate:        
    queries.remove(query)

    for key in temp_set_kb: #when different constant meets
        if temp_set_kb[key][0].isupper() and key[0].isupper() and temp_set_kb[key] != key:
            return -1 


    #combining step
    kb_set_new = []   
    if kb_set and temp_set_kb:
        kb_set_new = parameter(kb_set, temp_set_kb)

    q_set_new = []
    if queries and temp_set_kb: 
        q_set_new = parameter(queries, temp_set_kb)   
        
        for i in q_set_new: # if new query is not in new kb set
            if i not in kb_set_new: 
                kb_set_new += q_set_new
        
    kb_set = " | ".join(kb_set_new)
    return kb_set

def resolution():
    flag_set = []
    sentence_length = len(sentences)
    for query in queries:
        sentence = sentences[:sentence_length]
        flag = False
        kb_stack = []
        kb_dic = copy.deepcopy(dic)
        not_query = negation(query)
        sentence.append(not_query)
        kb_stack.append([not_query, [-1]])
        kb_tell(kb_dic, [not_query], len(sentence)-1)

        while kb_stack:
            kb_set = []
            path = []
            kb_pop, path = kb_stack.pop()
            kb_set = kb_pop.split(" | ")
            for j in range(len(kb_set)):
                not_kb = negation(kb_set[j])
                sentence_index = kb_dic[not_kb.partition("(")[0]] # need to erase later
                length = len(sentence)
                sentence_comb = []
                for i in sentence_index: # i => index of sentences
                    if i not in path: #duplicate path check
                        new_kb, step = unify(kb_pop, sentence[i], j), [i]
                        if new_kb == 1: #query is true
                            kb_stack = []
                            flag = True
                            break
                        if new_kb != -1 and new_kb != "" and not new_kb in sentence:
                            sentence.append(new_kb)
                            kb_stack.append([new_kb, path+step])
                            sentence_comb.append(new_kb)
                for i, sent in enumerate(sentence_comb):
                    kb_tell(kb_dic, [sent], length+i)
        flag_set.append(flag)
    writeFile(flag_set)
    return

def writeFile(flag_set):
    f = open("output.txt", "w")
    for i in flag_set:
        if i == True:
            f.write("TRUE\n")

        else:
            f.write("FALSE\n")
    f.close()
    print(flag_set)
    return

def readFile():
    f = open("inputs.txt", "r")
    read = f.read().splitlines()
    f.close()

    for i in range(1,int(read[0])+1):
        queries.append(read[i])
    for i in range(int(read[0])+2, len(read)):
        sentences.append(read[i])
    kb_tell(dic, sentences)
    resolution()
    return

if __name__ == '__main__':
       readFile() 
    