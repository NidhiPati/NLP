import sys
import math
import nltk.metrics
import nltk.classify.util
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


def main():
    for arg in sys.argv[1:]:
        print(arg)


uni_grams_list = {}
bi_grams_list = {}


def find_uni_grams():
    file_content = open(input_file, "r").readlines()
    for each_line in range(file_content.__len__()):
        line = file_content[each_line]
        # cleaning
        if line.find(','):
            line = line.replace(',', "")
        if line.find(':'):
            line = line.replace(':', "")
        if line.find('`'):
            line = line.replace('`', " ")
        if line.find('.'):
            line = line.replace('.', "")
        if line.find('- '):
            line = line.replace('- ', " ")
        if line.find("'"):
            line = line.replace("'", "")
        if line.find('"'):
            line = line.replace('"', "")
        if line.find('('):
            line = line.replace('(', "")
        if line.find(')'):
            line = line.replace(')', "")
        line = line.lower()
        temporary_array = line.split()
        for number_of_wordS_in_line in range(temporary_array.__len__()):
            uni_gram = temporary_array[number_of_wordS_in_line]
            if uni_gram not in uni_grams_list:
                uni_grams_list[uni_gram] = 0
            uni_grams_list[uni_gram] = uni_grams_list[uni_gram] + 1


def find_bi_grams():
    file_content = open(input_file, "r").readlines()
    for each_line in range(file_content.__len__()):
        line = file_content[each_line]
        # cleaning
        if line.find(','):
            line = line.replace(',', "")
        if line.find(':'):
            line = line.replace(':', "")
        if line.find('`'):
            line = line.replace('`', " ")
        if line.find('.'):
            line = line.replace('.', "")
        if line.find('- '):
            line = line.replace('- ', " ")
        if line.find("'"):
            line = line.replace("'", "")
        if line.find('"'):
            line = line.replace('"', "")
        if line.find('('):
            line = line.replace('(', "")
        if line.find(')'):
            line = line.replace(')', "")
        line = line.lower()
        temporary_array = line.split()
        for number_of_wordS_in_line in range(temporary_array.__len__()-1):
            bi_gram = temporary_array[number_of_wordS_in_line]+" "+temporary_array[number_of_wordS_in_line+1]
            if bi_gram not in bi_grams_list:
                bi_grams_list[bi_gram] = 0
            bi_grams_list[bi_gram] = bi_grams_list[bi_gram] + 1
            number_of_wordS_in_line += 2


def chi_square():
    find_bi_grams()
    output = []
    range_ = bi_grams_list.items()
    print(range_)
    print(range_.__len__())
    for key, value in range_:
        bi_gram = key
        temp_array = bi_gram.split(" ")
        first_word = temp_array[0]
        second_word = temp_array[1]
        count_of_first_word_second_word = value
        count_of_only_first_word = 0
        count_of_only_second_word = 0
        count_of_other_words = 0
        if first_word not in stopwords.words('english') and second_word not in stopwords.words('english'):
            for key1, value1 in bi_grams_list.items():
                k = key1
                split_bi_gram = k.split(" ")
                if split_bi_gram[0] == first_word and split_bi_gram[1] != second_word:
                    count_of_only_first_word = count_of_only_first_word + value1
                elif split_bi_gram[0] != first_word and split_bi_gram[1] == second_word:
                    count_of_only_second_word = count_of_only_second_word + value1
                elif split_bi_gram[0] != first_word and split_bi_gram[1] != second_word:
                    count_of_other_words = count_of_other_words + value1
            count_of_all = count_of_first_word_second_word + count_of_only_first_word + count_of_only_second_word + \
                          count_of_other_words
            try:
                score = nltk.collocations.BigramAssocMeasures.chi_sq(count_of_first_word_second_word,
                            (count_of_only_first_word, count_of_only_second_word), count_of_all)
                score = score/100
                output.append([key, score])
            except ZeroDivisionError:
                continue

    output_ = sorted(output, key=lambda output: output[1], reverse=True)
    for o in range(20):
        print(output_[o])


def take_second(element):
    return element[1]


def pmi_measure():
    find_uni_grams()
    find_bi_grams()
    output = []
    range_of_uni_grams = uni_grams_list.items()
    range_ = bi_grams_list.items()
    count_of_all_uni_grams = 0
    for k, v in range_:
        count_of_all_uni_grams = count_of_all_uni_grams + v
    count_of_all_bi_grams = 0
    for k1, v1 in range_:
        count_of_all_bi_grams = count_of_all_bi_grams + v1
    for key, value in range_:
        bi_gram = key
        temp_array = bi_gram.split(" ")
        first_word = temp_array[0]
        second_word = temp_array[1]
        count_of_first_word_second_word = value
        count_of_first_word = 0
        count_of_second_word = 0
        for key_u, value_u in range_of_uni_grams:
            k_uni = key_u
            if k_uni == first_word:
                count_of_first_word = value_u
            if k_uni == second_word:
                count_of_second_word = value_u
        probability_of_first_word = count_of_first_word/count_of_all_uni_grams
        probability_of_second_word = count_of_second_word/count_of_all_uni_grams
        probability_of_bi_gram = count_of_first_word_second_word/count_of_all_bi_grams
        score = math.log(probability_of_bi_gram/float(probability_of_first_word*probability_of_second_word), 2)
        output.append([key, score])

    output_ = sorted(output, key=lambda output: output[1], reverse=True)
    for o in range(20):
        print(output_[o])


if __name__ == "__main__":
    input_file = sys.argv[1]
    measure = sys.argv[2]
    if measure == 'chi-square':
        chi_square()
    if measure == 'pmi':
        pmi_measure()

