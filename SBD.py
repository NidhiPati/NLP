import sys
import pandas as p
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def main():
    for arg in sys.argv[1:]:
        print(arg)


def train_classifier(train_file, test_file):
    feature_vector = p.DataFrame([], columns=['Left_Word', 'Right_Word', 'Is_Len_Of_L_Less_Than_3',
                                               'Is_L_Capital', 'Is_R_Capital', 'Is_Len_Of_R_Less_Than_4',
                                               'IS_R_Single_Quote', 'IS_R_Double_Quote', 'Class'])

    file_content = open(train_file, "r").readlines()
    for each_line in range(file_content.__len__()):
        line = file_content[each_line]
        if line.__contains__("."):
            temporary_array = file_content[each_line].split()

            if temporary_array[2].__ne__("TOK") and each_line < file_content.__len__() - 1:
                next_temporary_array = file_content[each_line + 1].split()
                left_word = temporary_array[1].replace(".", "")
                right_word = next_temporary_array[1]

                length_of_left_word = (len(temporary_array[1])-1)      # ignoring the period for length
                if length_of_left_word < 3:
                    is_len_of_l_less_than_3 = 1
                else:
                    is_len_of_l_less_than_3 = 0

                if temporary_array[1].istitle():
                    is_l_capital = 1
                else:
                    is_l_capital = 0

                if next_temporary_array[1].istitle():
                    is_r_capital = 1
                else:
                    is_r_capital = 0

                class_definition = temporary_array[2]

                # additional features
                length_of_right_word = (len(next_temporary_array[1]))
                if length_of_right_word < 4:
                    is_len_of_r_less_than_4 = 1
                else:
                    is_len_of_r_less_than_4 = 0

                if next_temporary_array[1].__eq__("'"):
                    is_r_single_quote = 1
                else:
                    is_r_single_quote = 0

                if next_temporary_array[1].__eq__('"'):
                    is_r_double_quote = 1
                else:
                    is_r_double_quote = 0

                row = p.Series([left_word, right_word, is_len_of_l_less_than_3,
                                               is_l_capital, is_r_capital, is_len_of_r_less_than_4,
                                is_r_single_quote, is_r_double_quote, class_definition],
                                index=['Left_Word', 'Right_Word', 'Is_Len_Of_L_Less_Than_3',
                                               'Is_L_Capital', 'Is_R_Capital', 'Is_Len_Of_R_Less_Than_4',
                                               'IS_R_Single_Quote', 'IS_R_Double_Quote', 'Class'])
                feature_vector = feature_vector.append(row, ignore_index=1)

            if each_line >= file_content.__len__() - 1:     # last line and definitely EOS
                print(temporary_array[1], "EOS")
                row = p.Series(['Not Applicable', temporary_array[1].replace(".", ""), 0,
                                 0, 0, 0,
                                 0, 0, 'EOS'],
                                index=['Left_Word', 'Right_Word', 'Is_Len_Of_L_Less_Than_3',
                                               'Is_L_Capital', 'Is_R_Capital', 'Is_Len_Of_R_Less_Than_4',
                                               'IS_R_Single_Quote', 'IS_R_Double_Quote', 'Class'])
                feature_vector = feature_vector.append(row, ignore_index=1)

    feature_set = feature_vector.values[:, 2:7]
    target_class = feature_vector.values[:, 8]
    print(feature_set)
    print(target_class)
    # test
    feature_set_test, target_set_test = test_classifier(test_file)

    info_gain = DecisionTreeClassifier(criterion='entropy')

    classifier_entropy = info_gain.fit(feature_set, target_class)
    print(classifier_entropy)

    predicting_test = info_gain.predict(feature_set_test)
    print(predicting_test)

    accuracy = accuracy_score(target_set_test, predicting_test)
    accuracy_percent = accuracy * 100
    print("Accuracy: ", accuracy_percent)


def test_classifier(test_file):
    feature_vector = p.DataFrame([], columns=['Left_Word', 'Right_Word', 'Is_Len_Of_L_Less_Than_3',
                                               'Is_L_Capital', 'Is_R_Capital', 'Is_Len_Of_R_Less_Than_4',
                                               'IS_R_Single_Quote', 'IS_R_Double_Quote', 'Class'])
    output_vector = p.DataFrame(columns=["Left_Word", "Right_Word", "Class"])

    file_content = open(test_file, "r").readlines()
    for each_line in range(file_content.__len__()):
        line = file_content[each_line]
        if line.__contains__("."):
            temporary_array = file_content[each_line].split()

            if temporary_array[2].__ne__("TOK") and each_line < file_content.__len__() - 1:
                next_temporary_array = file_content[each_line + 1].split()
                left_word = temporary_array[1].replace(".", "")
                right_word = next_temporary_array[1]

                length_of_left_word = (len(temporary_array[1])-1)      # ignoring the period for length
                if length_of_left_word < 3:
                    is_len_of_l_less_than_3 = 1
                else:
                    is_len_of_l_less_than_3 = 0

                if temporary_array[1].istitle():
                    is_l_capital = 1
                else:
                    is_l_capital = 0

                if next_temporary_array[1].istitle():
                    is_r_capital = 1
                else:
                    is_r_capital = 0

                class_definition = temporary_array[2]

                # additional features
                length_of_right_word = (len(next_temporary_array[1]))
                if length_of_right_word < 4:
                    is_len_of_r_less_than_4 = 1
                else:
                    is_len_of_r_less_than_4 = 0

                if next_temporary_array[1].__eq__("'"):
                    is_r_single_quote = 1
                else:
                    is_r_single_quote = 0

                if next_temporary_array[1].__eq__('"'):
                    is_r_double_quote = 1
                else:
                    is_r_double_quote = 0

                row = p.Series([left_word, right_word, is_len_of_l_less_than_3,
                                is_l_capital, is_r_capital, is_len_of_r_less_than_4,
                                is_r_single_quote, is_r_double_quote, class_definition],
                                index=['Left_Word', 'Right_Word', 'Is_Len_Of_L_Less_Than_3',
                                               'Is_L_Capital', 'Is_R_Capital', 'Is_Len_Of_R_Less_Than_4',
                                               'IS_R_Single_Quote', 'IS_R_Double_Quote', 'Class'])
                feature_vector = feature_vector.append(row, ignore_index=1)
                output_row = p.Series([left_word, right_word, class_definition],
                               index=['Left_Word', 'Right_Word', 'Class'])
                output_vector = output_vector.append(output_row, ignore_index=1)

            if each_line >= file_content.__len__() - 1:     # last line and definitely EOS
                print(temporary_array[1], "EOS")
                row = p.Series(['Not Applicable', temporary_array[1].replace(".", ""), 0,
                                 0, 0, 0,
                                 0, 0, 'EOS'],
                                index=['Left_Word', 'Right_Word', 'Is_Len_Of_L_Less_Than_3',
                                               'Is_L_Capital', 'Is_R_Capital', 'Is_Len_Of_R_Less_Than_4',
                                               'IS_R_Single_Quote', 'IS_R_Double_Quote', 'Class'])
                feature_vector = feature_vector.append(row, ignore_index=1)

    test_feature_set = feature_vector.values[:, 2:7]
    test_target_class = feature_vector.values[:, 8]
    print(test_feature_set)
    output_vector.to_csv("SBD.test.out", sep='\t')
    return test_feature_set, test_target_class


if __name__ == "__main__":
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    train_classifier(train_file, test_file)


