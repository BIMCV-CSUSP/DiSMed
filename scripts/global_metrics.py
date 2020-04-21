"""
Python 3

Compute global metrics of the de-identification method
"""

# Generic/Built-in
import os
import re
import multiprocessing as mp
import time


def compare_lines(gt_line, pred_line, score_dict, tags):
    """
    Compare a line from the ground truth file to another of the predicted file
    and compute the number of TP, FP and FN obtained

    inputs:
        gt_line     line of the ground truth file
        pred_line   line of the predicted file
        score_dict  dictionary with the keys 'TP', 'FP' and 'FN'
        tags        list of tags to compute as positives
    
    output: 
        modifies the global variable score_dict

    """
    regex_tag = re.compile(r"(\<(?P<tag>.+?)(?<!\/)\>)(?P<content>.+?)(\<\/(.+?)\>)")
    gt_words = gt_line.strip().split()
    pred_words = pred_line.strip().split()

    for i in range(len(pred_words)):
        # Check if the word has a predicted tag contained in the tag list
        pred_match = regex_tag.search(pred_words[i])
        if pred_match:
            pred_tag = pred_match.group("tag")
            if pred_tag in tags:
                pred_val = 1
            else:
                pred_val = 0
        else:
            pred_val = 0

        # Check if the word has a ground truth tag contained in the tag list
        gt_match = regex_tag.search(gt_words[i])
        if gt_match:
            gt_tag = gt_match.group("tag")
            if gt_tag in tags:
                gt_val = 1
            else:
                gt_val = 0
        else:
            gt_val = 0
        
        # Compare values to assess if it is a TP, FP or FN
        if (gt_val == 1) and (pred_val == 1):
                score_dict["TP"] += 1
        elif (pred_val == 1) and (gt_val == 0):
            score_dict["FP"] += 1
        elif (pred_val == 0) and (gt_val == 1):
            score_dict["FN"] += 1


def calc_precision(score_dict):
    """
    Compute precision metric from the score dictionary

    inputs:
        score_dict  dictionary with the keys 'TP', 'FP' and 'FN'
    
    output: 
        precision   float with the precision value

    """
    precision = float(score_dict["TP"]) / float(score_dict["TP"] + score_dict["FP"])
    return precision

def calc_recall(score_dict):
    """
    Compute recall metric from the score dictionary

    inputs:
        score_dict  dictionary with the keys 'TP', 'FP' and 'FN'
    
    output: 
        recall   float with the recall value

    """
    recall = float(score_dict["TP"]) / float(score_dict["TP"] + score_dict["FN"])
    return recall

def calc_f1(precision, recall):
    """
    Compute F1 metric from the score dictionary

    inputs:
        precision   float with the precision value
        recall      float with the recall value
    
    output: 
        f1   float with the F1 value

    """
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def main(gt_dir, pred_dir, tags):

    score_dict = {
        "TP" : 0,
        "FP" : 0,
        "FN" : 0   
    }

    with open(gt_dir, "r") as gt:
        groundTruth = gt.readlines()
    
    with open(pred_dir, "r") as pred:
        predicted = pred.readlines()
    
    for j in range(len(predicted)):
        print(groundTruth[j])
        print(predicted[j])
        compare_lines(groundTruth[j], predicted[j], score_dict, tags)

    precision = calc_precision(score_dict)
    recall = calc_recall(score_dict)
    f1 = calc_f1(precision, recall)

    print("Precision: \t" + str(precision))
    print("Recall: \t" + str(recall))
    print("F1-score: \t" + str(f1))


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-gt', '--groundtruth',  type = str ,default='../data/ground_truth.txt', help='Path of the file containing the ground truth')
    parser.add_argument('-p', '--predicted',  type = str, default='../data/predicted.txt', help='Path of the file containing the predictions')
    parser.add_argument('-t', '--tags',  type=str, nargs='+', default=["NAME", "DIR", "LOC", "NUM", "FECHA", "INST"], help='List of tags that mark words to de-identify')

    args = parser.parse_args()

    main(gt_dir=args.groundtruth, pred_dir=args.predicted, tags=args.tags)
