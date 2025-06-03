
def indicators():
    with open('indic.txt', 'r', encoding='utf-8') as file:
        lines = [line[1:line.find('\n')] if '\n' in line else line[1:] for line in file]

    return lines

def indicators_rzv():
    with open('indic_rzv.txt', 'r', encoding='utf-8') as file:
        lines = [line[1:line.find('\n')] if '\n' in line else line[1:] for line in file]
    dict = {}
    for line in lines:
        dict[line] = line.split('...')
    return lines, dict

def proceed_texts(indics, indics_rzv, parted_indics_rzv):
    
    f = open('ner_tags.txt', 'w', encoding='utf-8')


    with open('new_texts.txt', 'r', encoding='utf-8') as read_file:

        for sent in read_file:

            indic_st = []
            indic_rzv_st = {}

            for indic in indics:
                if indic in sent:
                    indic_st.append(indic)

            rzv_count = 0
            for ind_rzv in indics_rzv:
                is_ind = True
                for part_ind in parted_indics_rzv[ind_rzv]:
                    if part_ind not in sent:
                        is_ind = False
                if is_ind:
                    rzv_count +=1
                    indic_rzv_st[ind_rzv] = parted_indics_rzv[ind_rzv]
                    # print(sent)
                else:
                    indic_rzv_st[ind_rzv] = None

            if indic_st == [] and rzv_count == 0:
                continue

            sent_words = sent.split()
            for i in range(0, len(sent_words)):
                is_first = (i == 0)
                is_last = (i == len(sent_words) - 1)
                is_in_ind = False
                for ind in indic_st:
                    if sent_words[i][1:] in ind:
                        if sent_words[i] in ['в', 'и', 'на', 'ее', 'а'] and sent_words[i+1][1:] not in ind and sent_words[i-1][1:] not in ind:
                            continue
                        if ' ' not in ind:
                            sent_words[i] = f"{sent_words[i]} B-MRK"
                            is_in_ind = True
                            break
                        else:
                            first_word = ind[:ind.find(' ')]
                            if is_first and sent_words[i+1] in ind:
                                sent_words[i] = f"{sent_words[i]} B-MRK"
                                is_in_ind = True
                                break
                            elif is_last and sent_words[i-1] in ind:
                                sent_words[i] = f"{sent_words[i]} I-MRK"
                                is_in_ind = True
                                break
                            elif not is_last and sent_words[i][1:] in first_word and sent_words[i+1] in ind:
                                sent_words[i] = f"{sent_words[i]} B-MRK"
                                is_in_ind = True
                                break
                            elif 'B-MRK' in sent_words[i-1] or 'I-MRK' in sent_words[i-1]:
                                sent_words[i] = f"{sent_words[i]} I-MRK"
                                is_in_ind = True
                                break
                                


                if not is_in_ind:
                    for ind_r in indics_rzv:
                        if indic_rzv_st[ind_r] != None and not is_in_ind:
                            for k in range(0, len(indic_rzv_st[ind_r])):
                                ind = indic_rzv_st[ind_r][k]
                                if k == 0 and sent_words[i][1:] in ind:

                                    if sent_words[i] in ['в', 'и', 'на', 'ее', 'а'] and sent_words[i+1][1:] not in ind and sent_words[i-1][1:] not in ind:
                                        continue

                                    if ' ' not in ind:
                                        sent_words[i] = f"{sent_words[i]} B-MRK"
                                        is_in_ind = True
                                        break
                                    else:
                                        first_word = ind[:ind.find(' ')]
                                        if is_first and sent_words[i+1] in ind:
                                            sent_words[i] = f"{sent_words[i]} B-MRK"
                                            is_in_ind = True
                                            break
                                       
                                        elif not is_last and sent_words[i][1:] in first_word and sent_words[i+1] in ind:
                                            sent_words[i] = f"{sent_words[i]} B-MRK"
                                            is_in_ind = True
                                            break
                                        elif 'B-MRK' in sent_words[i-1] or 'I-MRK' in sent_words[i-1]:
                                            sent_words[i] = f"{sent_words[i]} I-MRK"
                                            is_in_ind = True
                                            break
                                if k == 1 and sent_words[i] in ind:
                                    if sent_words[i] in ['в', 'и', 'на', 'ее', 'а'] and sent_words[i+1] not in ind and sent_words[i-1] not in ind:
                                        continue
                                    if ' ' not in ind:
                                        sent_words[i] = f"{sent_words[i]} I-MRK"
                                        is_in_ind = True
                                        break
                                    else:
                                        if sent_words[i-1] in ind or (not is_last and sent_words[i+1] in ind):
                                            
                                            sent_words[i] = f"{sent_words[i]} I-MRK"
                                            is_in_ind = True
                                            break

                if not is_in_ind:
                     sent_words[i] = f"{sent_words[i]} O"     

            for word in sent_words:
                f.write(word)
                f.write('\n')

            f.write('\n')

def spec_marks():
    pass


def postprocess_file():
    f = open('ner_tags_train.txt', 'w', encoding='utf-8')
    f1 = open('ner_tags_test.txt', 'w', encoding='utf-8')
    lines = []
    symbols_to_delete = f"#(){{}}[]\"№."
    ord_symbols = f",!?;:"

    with open('ner_tags.txt', 'r', encoding='utf-8') as read_file:
        lines = read_file.readlines()
    
    for i in range(0, 59717):
        # if i < 189335:
        if lines[i] == '\n' and lines[i-1] == '\n':
            continue
        line = lines[i]
        for symbol in symbols_to_delete:
            line = line.replace(symbol, "")

        symbol_in = False
        for symbol in ord_symbols:
            if symbol in line:
                if 'B-MRK' in line:
                    f.write(f"{line[:line.find(symbol)]} B-MRK")
                    f.write('\n')
                    f.write(f"{symbol} I-MRK")
                    f.write('\n')
                elif 'I-MRK' in line:
                    f.write(f"{line[:line.find(symbol)]} I-MRK")
                    f.write('\n')
                    f.write(f"{symbol} I-MRK")
                    f.write('\n')
                else:
                    f.write(f"{line[:line.find(symbol)]} O")
                    f.write('\n')
                    f.write(f"{symbol} O")
                    f.write('\n')
                
                symbol_in = True
                break

        if not symbol_in:
            f.write(line)

    for i in range(59718, len(lines)):
        if lines[i] == '\n' and lines[i-1] == '\n':
            continue
        line = lines[i]
        for symbol in symbols_to_delete:
            line = line.replace(symbol, "")

        symbol_in = False
        for symbol in ord_symbols:
            if symbol in line:
                if 'B-MRK' in line:
                    f1.write(f"{line[:line.find(symbol)]} B-MRK")
                    f1.write('\n')
                    f1.write(f"{symbol} I-MRK")
                    f1.write('\n')
                elif 'I-MRK' in line:
                    f1.write(f"{line[:line.find(symbol)]} I-MRK")
                    f1.write('\n')
                    f1.write(f"{symbol} I-MRK")
                    f1.write('\n')
                else:
                    f1.write(f"{line[:line.find(symbol)]} O")
                    f1.write('\n')
                    f1.write(f"{symbol} O")
                    f1.write('\n')
                
                symbol_in = True
                break

        if not symbol_in:
            f1.write(line)
           






indics = []
indics_rzv = []
parted_indics_rzv = {}
indics = indicators()
indics_rzv, parted_indics_rzv = indicators_rzv()
proceed_texts(indics, indics_rzv, parted_indics_rzv)
postprocess_file()
