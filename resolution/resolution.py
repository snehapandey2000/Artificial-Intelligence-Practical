import sys
import re

queries = list()
kb = list()
nq = 0
ns = 0


def get_input():
    fin = "input.txt"
    output_file = "output.txt"
    global queries
    global kb
    global nq
    global ns

    try:
        input_file = open(fin, 'r')
        lines = input_file.readlines()
        for index, line in enumerate(lines):
            if index == 0:
                nq = int(lines[index].strip("\n"))
                for i in range(1, nq + 1):
                    queries.append(lines[i].strip("\n"))
                ns = int(lines[nq+1].strip("\n"))
                for i in range(nq + 2, nq + ns + 2):
                    kb.append(lines[i].strip("\n"))
                break
        input_file.close()
        return queries, kb

    except IOError:
        fo = open(output_file, 'w')
        fo.write("File not found: {}".format(fin))
        fo.close()
        sys.exit()


def parseKB(kb):
    negativeKB = dict()
    positiveKB = dict()

    for item in kb:
        data = item.split('|')
        for i in data:
            i = i.replace(' ', '')
            if i[0] == '~':
                b = i[1:]
                b = b.partition("(")[0]
                try:
                    negativeKB[b].append(item)
                except KeyError:
                    negativeKB[b] = [item]
            else:
                i = i.partition("(")[0]
                try:
                    positiveKB[i].append(item)
                except KeyError:
                    positiveKB[i] = [item]

    return negativeKB, positiveKB


def extract_constants(query):
    variable = re.search(r'\((.*?)\)', query).group(1)
    return variable


def checkSentence(kb):
    if "|" in kb:
        return False
    const_list = re.search(r'\((.*?)\)', kb).group(1)
    const = const_list.split(",")
    for val in const:
        if val[0].isupper():
            continue
        else:
            return False
    return True


def unification(query, left_over, positiveKB, negativeKB, can_simplyfy):
    #print("In unification")
    if query[0] != '~':
        tomatch = query.partition("(")[0]
        try:
            value = negativeKB[tomatch]
        except KeyError:
            return False

        for sentence in value:
            try:
                left_over_temp = left_over
                query_temp = query

                if sentence in can_simplyfy:
                    ret1, l1 = remove(left_over_temp, sentence[1:])
                    ret2 = 1
                    l2 = ""
                else:
                    ret1, l1 = remove(left_over_temp, query_temp)
                    ret2, l2 = remove(sentence, "~" + query_temp)
                if ret1 == 0 or ret2 == 0:
                    continue
                else:
                    if l1 == '' and l2 != '':
                        left_over_temp = l2
                    elif l2 == '' and l1 != '':
                        left_over_temp = l1
                    elif l1 == '' and l2 == '':
                        left_over_temp = ''
                    else:
                        left_over_temp = l2 + " | " + l1

                    if left_over_temp == '':
                        return True
                    else:
                        if "|" in left_over_temp:
                            data = left_over_temp.split("|")
                            for i in data:
                                i = i.replace(" ", "")
                                if unification(i, left_over_temp, positiveKB, negativeKB, can_simplyfy):
                                    return True
                                else:
                                    break
                        else:
                            if unification(left_over_temp, left_over_temp, positiveKB, negativeKB, can_simplyfy):
                                return True
                            else:
                                continue
            except RuntimeError as re:
                if re.args[0] == 'maximum recursion depth exceeded':
                    return False

        return False

    else:
        tomatch = query.partition("(")[0]
        try:
            value = positiveKB[tomatch[1:]]
        except KeyError:
            return False
        for sentence in value:
            try:
                left_over_temp = left_over
                query_temp = query
                if sentence in can_simplyfy:
                    ret_val1, l1 = remove(left_over_temp, "~" + sentence)
                    ret_val2 = 1
                    l2 = ""
                else:
                    ret_val1, l1 = remove(left_over_temp, query_temp)
                    ret_val2, l2 = remove(sentence, query_temp[1:])
                if ret_val1 == 0 or ret_val2 == 0:
                    continue
                else:
                    if l1 == '' and l2 != '':
                        left_over_temp = l2
                    elif l2 == '' and l1 != '':
                        left_over_temp = l1
                    elif l1 == '' and l2 == '':
                        left_over_temp = ''
                    else:
                        left_over_temp = l2 + " | " + l1

                    if left_over_temp == '':
                        return True
                    else:
                        if "|" in left_over_temp:
                            data = left_over_temp.split("|")
                            for i in data:
                                i = i.replace(" ", "")
                                if unification(i, left_over_temp, positiveKB, negativeKB, can_simplyfy):
                                    return True
                                else:
                                    break
                        else:
                            if unification(left_over_temp, left_over_temp, positiveKB, negativeKB, can_simplyfy):
                                return True
                            else:
                                continue
            except RuntimeError as re:
                if re.args[0] == 'maximum recursion depth exceeded':
                    return False
        return False


def remove(k, query):
    __int, newq, news = substitution(k, query)
    if __int == 1:
        if newq in news:
            news1 = news.replace(newq, "")
        else:
            start = news.find(query.partition("(")[0])
            end = news.find(')', start)
            to_del = news[start:end + 1]
            news1 = news.replace(to_del, "")
        if " |  | " in news1:
            news2 = news1.replace(" |  | ", " | ")
            return 1, news2
        elif news1[:3] == " | ":
            news2 = news1[3:]
            return 1, news2
        elif news1[-3:] == " | ":
            news2 = news1[:-3]
            return 1, news2
        else:
            return 1, news1
    else:
        return 0, news


def substitution(sentence, query):
    predicate = query.partition("(")[0]

    constant = extract_constants(query)
    cons_list = constant.split(",")
    count = 0

    data = sentence.split("|")
    flag = 0
    for i in data:
        m = i.partition("(")[0]
        m = m.replace(' ', '')
        if m == predicate:
            __vars = re.search(r'\((.*?)\)', i).group(1)
            var_list = __vars.split(",")
            for j in var_list:
                if j[0].isupper() and cons_list[count][0].islower():
                    query = test(cons_list[count], query, j)
                    flag = 1
                    count += 1
                elif j[0].islower() and cons_list[count][0].isupper():
                    sentence = test(j, sentence, cons_list[count])
                    flag = 1
                    count += 1
                elif j[0].isupper() and cons_list[count][0].isupper():
                    if j == cons_list[count]:
                        query = query
                        sentence = sentence
                        flag = 1
                    else:
                        flag = 0
                        break
                    count += 1
                elif j[0].islower() and cons_list[count][0].islower():
                    # print("both variables")
                    if not (j == cons_list[count]):
                        # add code here
                        sentence = test(j, sentence, cons_list[count])
                        query = query
                        flag = 1
                    else:
                        sentence = sentence
                        query = query
                        flag = 1
                    count += 1
            if flag == 1:
                break
    if flag == 0:
        return 0, query, sentence
    else:
        return 1, query, sentence


def test(word, to_replace, with_replace):
    big_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, word)))
    a = big_regex.sub(with_replace, to_replace)
    return(a)


def main():
    output_file = "output.txt"
    fo = open(output_file, 'w')
    query_list, sentences = get_input()
    negativeKB, positiveKB = parseKB(sentences)
    can_simplyfy = []
    for a in sentences:
        if checkSentence(a):
            can_simplyfy.append(a)

    for query in query_list:
        if query[0] == '~':
            new_query = query[1:]
            if unification(new_query, new_query, positiveKB, negativeKB, can_simplyfy):
                fo.write("TRUE" + "\n")
            else:
                fo.write("FALSE" + "\n")

        else:
            new_query = "~" + query
            if unification(new_query, new_query, positiveKB, negativeKB, can_simplyfy):
                fo.write("TRUE" + "\n")
            else:
                fo.write("FALSE" + "\n")
    fo.close()


if __name__ == '__main__':
    main()
