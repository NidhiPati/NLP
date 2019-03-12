import sys


def main():
    for arg in sys.argv[1:]:
        print(arg)


def function_(input_one, input_two):
    right_count = 0
    total_number_of_tags = 0
    wrong_ = []
    _tags_list = []
    _freq_and_tags = {}
    english_word = ''
    pos_tag = ''
    _pair_of_tag_and_freq = {}
    _all_unique_words = {}
    _sentence_tags = {}
    file_content = open(input_one, "r").readlines()
    for each_line in range(file_content.__len__()):
        temporary = file_content[each_line].replace(",/,", "").replace("''/''", "").\
            replace(":/:", "")
        beginning_of_sentence = "start"
        temporary_array1 = temporary.split()
        for loop in range(temporary_array1.__len__()):
            temporary_array2 = temporary_array1[loop]
            if temporary_array2.__contains__("/"):
                temp = str(temporary_array2).split("/")
                english_word = temp[0]
                pos_tag = temp[1]
                if pos_tag not in _tags_list:
                    _tags_list.append(pos_tag)
                    _freq_and_tags[pos_tag] = 1
                else:
                    _freq_and_tags[pos_tag] = _freq_and_tags[pos_tag] + 1
                tag_and_pair = beginning_of_sentence+"_"+pos_tag
                list_of_keys = _pair_of_tag_and_freq.keys()
                if tag_and_pair not in list_of_keys:
                    _pair_of_tag_and_freq[tag_and_pair] = 1
                else:
                    _pair_of_tag_and_freq[tag_and_pair] = _pair_of_tag_and_freq[tag_and_pair] + 1
                beginning_of_sentence = pos_tag

    file_content = open(input_one, "r").readlines()
    for each_line in range(file_content.__len__()):
        temporary = file_content[each_line].replace(",/,", "").replace("''/''", ""). \
            replace(":/:", "")
        temporary_array1 = temporary.split()
        for loop in range(temporary_array1.__len__()):
            temporary_array2 = temporary_array1[loop]
            if temporary_array2.__contains__("/"):
                temp = str(temporary_array2).split("/")
                english_word = temp[0]
                pos_tag = temp[1]
                list_of_unique_word_keys = _all_unique_words.keys()
                if english_word not in list_of_unique_word_keys:
                    _all_unique_words[english_word] = dict.fromkeys(_tags_list, 0)
                    _all_unique_words[english_word][pos_tag] += 1
                else:
                    _all_unique_words[english_word][pos_tag] += 1

    # test file
    file_content = open(input_two, "r").readlines()
    for each_line in range(file_content.__len__()):
        temporary = file_content[each_line].replace(",/,", "").replace("''/''", ""). \
            replace(":/:", "")
        temporary_array1 = temporary.split()
        words_of_a_sentence = []
        tags_of_a_sentence = []
        for loop in range(temporary_array1.__len__()):
            temporary_array2 = temporary_array1[loop]
            temp = str(temporary_array2).split("/")
            english_word = temp[0]
            pos_tag = temp[1]
            words_of_a_sentence.append(english_word)
            tags_of_a_sentence.append(pos_tag)
        _sentence_tags[tuple(words_of_a_sentence)] = tags_of_a_sentence

    words_list = _all_unique_words.keys()
    predictions_for_sentence_tags = {}
    tag_word = []
    for each_word in words_list:
        for each_tag in _tags_list:
            tag_word.append((each_tag, each_word))

    for index, line in enumerate(_sentence_tags.keys()):
        predictions_of_tags = [''] * len(line)
        score_of_prob = dict.fromkeys(tag_word, 0)
        pointer_back_tag = dict.fromkeys(tag_word, 0)
        sentence_word = line[0]
        for every_tag in _tags_list:
            if sentence_word in _all_unique_words:
                word_and_tag_freq = _all_unique_words[sentence_word][every_tag]
                total_freq_of_tag = _freq_and_tags[every_tag]
                word_tag_probability = float(word_and_tag_freq / total_freq_of_tag)
            else:
                word_tag_probability = float(1 / len(_freq_and_tags.keys()))
            n = "start" + '_' + every_tag
            if n in _pair_of_tag_and_freq:
                count_tag_pair = _pair_of_tag_and_freq[n]
                total_tag_pair_count = sum(_pair_of_tag_and_freq.values())
                tag_tag_probability = float(count_tag_pair / total_tag_pair_count)
            else:
                tag_tag_probability = float(1 / len(_pair_of_tag_and_freq.keys()))
            score_of_prob[(every_tag, sentence_word)] = word_tag_probability * tag_tag_probability
            pointer_back_tag[(every_tag, sentence_word)] = None

        previous_word = sentence_word
        for x in line[1:]:
            for e in _tags_list:
                maximum_prob = 0
                maximum_prob_tag = ''
                for each_tag in _tags_list:
                    n = each_tag + '_' + e
                    if n in _pair_of_tag_and_freq:
                        count_tag_pair = _pair_of_tag_and_freq[n]
                        total_tag_pair_count = sum(_pair_of_tag_and_freq.values())
                        tag_tag_probability = float(count_tag_pair / total_tag_pair_count)
                    else:
                        tag_tag_probability = float(1 / len(_pair_of_tag_and_freq.keys()))
                    temp_prob = score_of_prob[(each_tag, previous_word)] * tag_tag_probability
                    if temp_prob > maximum_prob:
                        maximum_prob = temp_prob
                        maximum_prob_tag = each_tag
                if x in _all_unique_words:
                    word_and_tag_freq = _all_unique_words[x][e]
                    total_freq_of_tag = _freq_and_tags[e]
                    word_tag_probability = float(word_and_tag_freq / total_freq_of_tag)
                else:
                    word_tag_probability = float(1 / len(_freq_and_tags.keys()))
                score_of_prob[(e, x)] = maximum_prob * word_tag_probability
                pointer_back_tag[(e, x)] = maximum_prob_tag
            previous_word = x

        last = line[(line.__len__()-1)]
        if last in words_list:
            maxP = 0
            last_word_tag = ''
            for t in _tags_list:
                tempP = score_of_prob[(t, last)]
                if tempP >= maxP:
                    maxP = tempP
                    last_word_tag = t
        else:
            last_word_tag = 'NN'

        predictions_of_tags[(line.__len__()-1)] = last_word_tag
        for counter, w in enumerate(reversed(line[:-1])):
            next_tag_predict = ''
            next_ = line[len(line) - 1 - counter]
            if next_ in words_list:
                mp = 0
                tp = ''
                for h in _tags_list:
                    tp = score_of_prob[(h, next_)]
                    if tp >= mp:
                        mp = tp
                        next_tag_predict = h
            else:
                next_tag_predict = 'NN'
            predicted_tag = pointer_back_tag[(next_tag_predict, next_)]
            predictions_of_tags[(line.__len__() - 2 - counter)] = str(predicted_tag)
        predictions_for_sentence_tags[tuple(line)] = predictions_of_tags

    for line in predictions_for_sentence_tags.keys():
        true = _sentence_tags[line]
        predicted = predictions_for_sentence_tags[line]
        for a, (b, c) in enumerate(zip(true, predicted)):
            total_number_of_tags += 1
            if c == b:
                right_count += 1
            else:
                wrong_.append([line[a], c, b])

    output = "POS_large.test.out"
    f = open(output, "w")
    for line, t in predictions_for_sentence_tags.items():
        for w, y in zip(line, t):
            f.write(w + '/' + y)
            f.write('\n')
        f.write('\n')
    f.close()

    percentage_of_accuracy = (float(right_count / total_number_of_tags)) * 100
    print("Viterbi accuracy: ", percentage_of_accuracy)


if __name__ == "__main__":
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    function_(train_file, test_file)
