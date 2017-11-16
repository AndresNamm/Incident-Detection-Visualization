import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import pdb;


class DataType(Enum):
    GPS = "gps"
    SP_GPS = "gps_sp"
    GPS_LONG = "gps_long"
    GPS_25 = "gps_acc25_rec25"
    SP = "sp"


class Window(Enum):
    TW_60 = "TW_60"
    TW_300 = "TW_300"
    TW_600 = "TW_600"
    TW_1800 = "TW_1800"
    TW_3600 = "TW_3600"


## DEFAULT VALUES OR GENERATING THE PLOTS AND ASSESSING AUC
default_val = "0\t0"
default_val_auc = -1
maxFold = 5


##


def main():
    # generateFullResult(Window.TW_300, DataType.SP)
    plotAUC("28807991",Window.TW_600,"Tai Po Road - Sha Tin")
    plotAUC("46765762",Window.TW_600, "Island Eastern Corridor")


def generateFullResult(windows, datatype):
    acc_route_id_list, result_dic = read_acc_route_list()
    windows = []
    for window in windows:
       windows.append(window)
    for window in windows:
        auc = getAucDic(window, result_dic, acc_route_id_list)
        folds = [[] for i in range(1, maxFold)]
        average = []
        for key in auc.keys():
            cumSum = 0
            cumAcc = 0
            cumAccRec = 0
            auc_count = 0
            for foldNr in range(1, maxFold):
                i = foldNr - 1
                auc_count += 1 if auc[key][i] != default_val_auc else 0
                cumSum += auc[key][i] if auc[key][i] != default_val_auc else  0
                cumAcc += float(result_dic[key][i].split()[1])
                cumAccRec += float(result_dic[key][i].split()[0])
                folds[i].append(key + str(foldNr) + "\t" + str(auc[key][i]) + "\t" + result_dic[key][i])
            if (auc_count == 0):
                print(auc[key])
                print(key)
            average.append(key + "\t" + str(cumSum / auc_count) + "\t" + str(cumAccRec / auc_count) + "\t" + str(
                cumAcc / auc_count) + "\t" + str(cumAccRec / cumAcc))

        f = open("data/plot_result/" + window.value + "/result.txt", "w")
        f.write("key\taverage auc\tacc recs avg\tacc avg\tacc_rec/acc avg")
        for i in range(1, maxFold):
            f.write("\tfold" + str(i) + "\tauc\trecs\tacc")
        f.write("\n")
        for i in range(len(average)):
            f.write(average[i])
            for fold in range(1, maxFold):
                j = fold - 1
                f.write("\t" + folds[j][i])
            f.write("\n")
        f.close()


def read_acc_route_list(data_type):
    acc_route_id_list = []
    resultDict = {}
    for foldNr in range(1, maxFold):

        i = foldNr - 1
        f = open("data/plot_result/" + data_type.value + "/f" + str(foldNr) + "/label_result_list.txt")
        lines = f.readlines()
        for line in lines:
            splitter = line.split("\t")
            # acc_route_id_list.append(splitter[0])
            if splitter[0] not in resultDict:
                resultDict[splitter[0]] = [default_val for j in range(1, maxFold)]
            resultDict[splitter[0]][i] = splitter[1] + "\t" + splitter[2].strip("\n")
    print(resultDict)
    for key in resultDict.keys():
        acc_route_id_list.append(key)
        # print(side1[1][:-1])
    return acc_route_id_list, resultDict


def generate_filename(route_id, fold, window_size):
    ans = "data/plot_result/" + window_size.value + "/fold_" + str(fold) + "/detect_result_" + str(route_id) + ".txt"
    # print(ans)
    return ans


def getAucDic(window, result_dic, acc_route_id_list):
    auc = {}
    default_val_auc = 0.0
    print(window.value)
    for route_id in acc_route_id_list:
        auc[route_id] = [default_val_auc for i in range(1, maxFold)]
        for foldNr in range(1, maxFold):
            i = foldNr - 1
            DR = []
            FAR = []
            filename = generate_filename(route_id, foldNr, window)
            if result_dic[route_id][i] != default_val:
                file = open(filename)
                line = file.readline()
                while line:
                    line_split = line.split()
                    if line_split[0] == "Weighted":
                        while True:
                            line = file.readline()
                            if not line:
                                break
                            rates = line.split("\t")
                            try:
                                DR.append(float(rates[0]))
                                FAR.append(float(rates[1]))
                            except:
                                print(rates)

                    line = file.readline()
                area = np.trapz(list(reversed(DR)), x=list(reversed(FAR)))  # integration
                auc[route_id][i] = area
    return auc




def plotAUC(way_id, window_size, fileName):
    curve_colors = ['b', 'g', 'c', 'r']
    fig = plt.figure()
    sp = fig.add_subplot(111)
    for i in range(1, maxFold):
        filename = generate_filename(way_id, i, window_size)
        try:
            file = open(filename)
            line = file.readline()

            DR = []
            FAR = []

            while line:
                line_split = line.split()
                if line_split[0] == "Weighted":
                    while True:
                        line = file.readline()
                        if not line:
                            break
                        rates = line.split("\t")
                        DR.append(float(rates[0]))
                        FAR.append(float(rates[1]))
                line = file.readline()

            area = np.round(np.trapz(list(reversed(DR)), x=list(reversed(FAR))), 3)
            sp.plot(FAR, DR, '-', color=curve_colors[i - 1], label="Fold " + str(i) + "(AUC = " + str(area) + ")")
        except:
            print("not")
    sp.set_title(fileName)
    sp.set_xlabel("False Alarm Rate")
    sp.set_ylabel("Detection Rate")
    sp.legend(loc='lower right')
    plt.show()

if __name__ == "__main__": main()