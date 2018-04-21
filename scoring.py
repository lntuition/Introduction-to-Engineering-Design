import os
import subprocess
import csv

# -------------------------------- Usage -------------------------------
# question_cnt : number of problems
# testcase : input/output with key/value 

studentId = 
[ "20151589","20151614","20171618","20171624","20171628","20171708","20172049","20181588","20181591","20181596","20181600","20181601","20181608",
  "20181613","20181614","20181617","20181618","20181622","20181623","20181628","20181631","20181632","20181633","20181637","20181642","20181643",
  "20181647","20181656","20181660","20181661","20181664","20181668","20181669","20181671","20181672","20181675","20181676","20181687","20181688",
  "20181696","20181699","20181706" ]
question_cnt = 4
testcase = [
    [], # dummy
    [{"0 0 0 0 0" : "0.00 good"}],
    [],
    [],
    []
]

csv_content = []
temp_csv = ["studentId"]
for q_num in range(1, 1 + question_cnt):
    for t_num in range(1, 1 + len(testcase[q_num])):
        temp_csv.append("Q" + str(q_num) + "_testcase" + str(t_num))
csv_content.append(temp_csv)

# compile c file
for directory in studentId:
    if os.path.isdir('./' + directory) is True:
        os.chdir(directory + '/')

        temp_csv = [directory]
        for q_num in range(1, 1 + question_cnt):
            string = 'c' + str(q_num) + '_' + directory
            os.system('cl ' + string + '.c')
            if os.path.isfile(string + '.exe') is True: # question
                for t in testcase[q_num]:
                    for key, value in t.items():
                        if subprocess.check_output('./' + string + '.exe', input=key, encoding='UTF-8').strip() == value is True:
                            temp_csv.append(1)
                        else:
                            temp_csv.append(0)
            else:
                for t in testcase[q_num]:
                    temp_csv.append(0)
                    
        csv_content.append(temp_csv)
        os.chdir('..')

# make csv file
csvfile = open('score.csv', 'w', newline='')
writer = csv.writer(csvfile)
for row in csv_content:
    writer.writerow(row)
csvfile.close()
