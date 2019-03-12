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
        temporary = file_content[each_line].replace(",/,", "").replace("''/''", ""). \
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
                tag_and_pair = beginning_of_sentence + "_" + pos_tag
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
    for index, line in enumerate(_sentence_tags.keys()):
        predictions_of_tags = [''] * len(line)
        for counter, w in enumerate(line):
            if w in words_list:
                temp = _all_unique_words[w]
                _max = max(temp, key=temp.get)
            else:
                _max = 'NN'

            predictions_of_tags[counter] = _max
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

    percentage_of_accuracy = (float(right_count / total_number_of_tags)) * 100
    print("Simple Baseline Accuracy: ", percentage_of_accuracy)


if __name__ == "__main__":
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    function_(train_file, test_file)
