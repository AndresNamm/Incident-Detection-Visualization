import matplotlib.pyplot as plt
import numpy as np



def read_acc_route_list():
    f = open("data/plot_result/label_result_list.txt")
    lines = f.readlines()
    acc_route_id_list = []
    resultDict = {}
    for line in lines:
        side1 = line.split("\t")
        acc_route_id_list.append(side1[0])
        resultDict[side1[0]]= side1[1][:-1]
        print(side1[1][:-1])
    return acc_route_id_list,resultDict


def generate_filename(route_id, fold):
    return "data/plot_result/TW_300/fold_" + str(fold) + "/detect_result_" + str(route_id) + ".txt"

acc_route_id_list, result_dic = read_acc_route_list()
curve_colors = ['b', 'g', 'c', 'r']

f = open("data/plot_result/TW_300/result.txt", "w")
fig = plt.figure()
sp = fig.add_subplot(111)

max_route_id = 0
max_area = 0
max_fold = 0
min_route_id = 0
min_area = 1
min_fold = 0

for route_id in acc_route_id_list:
    for i in range(1,2):
        DR = []
        FAR = []

        filename = generate_filename(route_id, i)
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

        # while line:
        #     line_split = line.split()
        #     if line_split[0] == "KL":
        #         while True:
        #             line = file.readline()
        #             if line.split()[0]=="Weighted":
        #                 break
        #             rates = line.split("\t")
        #             try:
        #                 DR.append(float(rates[0]))
        #                 FAR.append(float(rates[1]))
        #             except:
        #                 print(rates)
        #
        #     line = file.readline()

        area = np.trapz(list(reversed(DR)), x=list(reversed(FAR)))
        if area > max_area:
            max_area = area
            max_route_id = route_id
            max_fold = i
        if area < min_area:
            min_area = area
            min_route_id = route_id
            min_fold = i
        f.write(str(route_id)+"\t"+str(i)+"\t"+str(area)+"\t"+str(result_dic[str(route_id)])+"\n")
f.write(str(max_route_id) + "\t" + str(max_fold) + "\t" + str(max_area) + "\t"+str(result_dic[str(max_route_id)])+"\n")
f.write(str(min_route_id) + "\t" + str(min_fold) + "\t" + str(min_area) + "\t"+str(result_dic[str(min_route_id)])+"\n")

for i in range(1, 2):
    filename = generate_filename("28807991", i)
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
    sp.plot(FAR, DR, '-', color=curve_colors[i-1], label="Fold " + str(i) + "(AUC = " + str(area) + ")")
sp.set_title("Fanling Highway")
sp.set_xlabel("False Alarm Rate")
sp.set_ylabel("Detection Rate")
sp.legend(loc='lower right')
plt.show()