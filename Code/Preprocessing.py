import csv

def launchPreProcessing():

    addLabelToActionA()
    addLabelToActionB()
    writeTxtToCsv("A")
    writeTxtToCsv("B")
    print("PREPROCESSING DONE")

def loadFileInDictionary(file):

    fileDict = dict()
    nLine = 0

    skipLine = 2

    for line in file:
        if skipLine > 0:
            skipLine -= 1
            continue
        line = line.split()
        fileDict[nLine] = line
        nLine += 1

    return fileDict

def writeTxtToCsv(home):

    txtLabeledB = open("./Dataset/datasetTXT/labeledData"+home+".txt", "r")
    skipLine = 1
    nLine = 1

    with open("./Dataset/datasetCSV/labeled"+home+".csv", mode='w') as activityA:
        activity_writer = csv.writer(activityA, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        activity_writer.writerow(['NUMBER', 'ACTIVITY', 'LOCATION', 'TYPE', 'PLACE'])

        for line in txtLabeledB:
            if skipLine > 0:
                skipLine -= 1
                continue
            line = line.split()
            
            activity_writer.writerow([nLine, str(line[0]), str(line[1]), str(line[2]), str(line[3])])
            nLine += 1

    skipLine = 2
    nLine = 1


def addLabelToActionA():

    activityA = open("./Dataset/datasetTXT/OrdonezA_ADLs.txt", "r")
    actionA = open("./Dataset/datasetTXT/OrdonezA_Sensors.txt", "r")
    final = open("./Dataset/datasetTXT/labeledDataA.txt", "w")

    activityADict = loadFileInDictionary(activityA)
    actionADict = loadFileInDictionary(actionA)

    coupled = False
    out = False
    skip = False

    # print(len(activityADict))
    # print(len(actionADict))

    start = 0
    end = 0

    actionIndex = 0

    for nActivity in activityADict:
        if nActivity == 0:
            line = "{:<17}{:<10}{:<10}{:<10}".format("ACTIVITY", "LOCATION", "TYPE", "PLACE")
            final.write(line)
            final.write("\n")
        # print("ACTIVITY: ", activityADict[nActivity])
        out = False
        while actionIndex < len(actionADict) and not out == True:
            coupled = False
            skip = False
            # print(activityADict[nActivity])
            # print(actionADict[nAction])
            # print("ACTION: ", actionADict[actionIndex])

            ###### MONTH 
            startMonthActivity = int(activityADict[nActivity][0][5:7])
            endMonthActivity = int(activityADict[nActivity][2][5:7])
            startMonthAction = int(actionADict[actionIndex][0][5:7])
            endMonthAction = int(actionADict[actionIndex][2][5:7])

            ###### DAY
            startDayActivity = int(activityADict[nActivity][0][8:])
            endDayActivity = int(activityADict[nActivity][2][8:])
            startDayAction = int(actionADict[actionIndex][0][8:])
            endDayAction = int(actionADict[actionIndex][2][8:])   

            ##### HOUR
            startHourActivity = int(activityADict[nActivity][1][:2])
            endHourActivity = int(activityADict[nActivity][3][:2])
            startHourAction = int(actionADict[actionIndex][1][:2])
            endHourAction = int(actionADict[actionIndex][3][:2])

            ##### MINUTE
            startMinuteActivity = int(activityADict[nActivity][1][3:5])
            endMinuteActivity = int(activityADict[nActivity][3][3:5])
            startMinuteAction = int(actionADict[actionIndex][1][3:5])
            endMinuteAction = int(actionADict[actionIndex][3][3:5])

            ##### SECOND
            startSecondActivity = int(activityADict[nActivity][1][6:])
            endSecondActivity = int(activityADict[nActivity][3][6:])
            startSecondAction = int(actionADict[actionIndex][1][6:])
            endSecondAction = int(actionADict[actionIndex][3][6:])

            ##### TIME
            startTimeActivity = startHourActivity * 3600 + startMinuteActivity * 60 + startSecondActivity
            endTimeActivity = endHourActivity * 3600 + endMinuteActivity * 60 + endSecondActivity
            startTimeAction = startHourAction * 3600 + startMinuteAction * 60 + startSecondAction
            endTimeAction = endHourAction * 3600 + endMinuteAction * 60 + endSecondAction

            ##### LOCATION
            if actionIndex > 0 and start < end:
                locationActionBefore = actionADict[actionIndex - 1][6]
                locationAction = actionADict[actionIndex][6]
            else:
                locationActionBefore = "EARLY"
                locationAction = "EARLY"

            # print("START TIME ACTIVITY: ", startTimeActivity)
            # print("START TIME ACTION: ", startTimeAction)
            # print("--------------------")
            # print("END TIME ACTIVITY: ", endTimeActivity)
            # print("END TIME ACTION: ", endTimeAction)

            # perfect situation
            if startTimeActivity <= startTimeAction and endTimeActivity + 2 >= endTimeAction - 51:
                # print("I AM INSIDE FIRST")
                if endDayActivity != endDayAction:
                    # print("NOT SAME DAY")
                    coupled = False
                elif locationActionBefore != locationAction:
                    # print("NOT SAME LOCATION")
                    # print(locationActionBefore)
                    # print(locationAction)
                    coupled = False
                else:
                    coupled = True
            elif startTimeActivity <= startTimeAction + 48 and endTimeActivity >= endTimeAction:
                coupled = True

            # riding day before
            elif startTimeActivity <= startTimeAction and endDayAction == endDayActivity - 1:
                # print("I AM INSIDE SECOND")
                coupled = True
            
            # riding day after
            elif endTimeActivity >= endTimeAction and startDayAction == startDayActivity + 1:
                # print("I AM INSIDE THIRD")
                coupled = True

            # riding month before
            elif startTimeActivity <= startTimeAction and endDayActivity == 1 and endMonthAction == endMonthActivity - 1:
                # print("I AM INSIDE FOURTH")
                coupled = True
            
            # riding month after
            elif endTimeActivity >= endTimeAction and endDayActivity == 1 and endDayAction == 1 and startMonthAction == startMonthActivity +1:
                # print("I AM INSIDE FIFTH")
                coupled = True

            # jump no labeled action
            elif endTimeAction < startTimeActivity and not startDayActivity < startDayAction and not startDayAction == 1:
                # print("I AM IN THE SKIP")
                skip = True

            else:
                coupled = False
                                
            if coupled == True:
                end += 1
                actionIndex += 1
                # print("I MOVED END, NOW IS: ", end + 3)
            elif skip == True:
                # print("I AM SKIPPING")
                start += 1
                end += 1
                actionIndex += 1
            else:
                # print("START ACTION: ", start + 3)
                # print("END ACTION: ", end + 3)
                # print("I USE THIS ACTIVITY: ", activityADict[nActivity][4])
                for i in range(start, end):
                    line = "{:<17}{:<10}{:<10}{:<10}".format(activityADict[nActivity][4], actionADict[i][4],
                    actionADict[i][5], actionADict[i][6])
                    # print("I ADDED THIS LINE: ", line)
                    final.write(line)
                    final.write("\n")
                start = end 
                out = True

            if actionIndex == len(actionADict) and coupled:
                for i in range(start, end):
                    line = "{:<17}{:<10}{:<10}{:<10}".format(activityADict[nActivity][4], actionADict[i][4],
                    actionADict[i][5], actionADict[i][6])
                    # print("I ADDED THIS LINE: ", line)
                    final.write(line)
                    final.write("\n")
            # print("")

def addLabelToActionB():

    activityA = open("./Dataset/datasetTXT/OrdonezB_ADLs.txt", "r")
    actionA = open("./Dataset/datasetTXT/OrdonezB_Sensors.txt", "r")
    final = open("./Dataset/datasetTXT/labeledDataB.txt", "w")

    activityADict = loadFileInDictionary(activityA)
    actionADict = loadFileInDictionary(actionA)

    coupled = False
    out = False
    skip = False

    # print(len(activityADict))
    # print(len(actionADict))

    start = 0
    end = 0

    actionIndex = 0

    for nActivity in activityADict:
        if nActivity == 0:
            line = "{:<17}{:<10}{:<10}{:<10}".format("ACTIVITY", "LOCATION", "TYPE", "PLACE")
            final.write(line)
            final.write("\n")
        # print("ACTIVITY: ", activityADict[nActivity])
        out = False
        while actionIndex < len(actionADict) and not out == True:
            coupled = False
            skip = False
            # print(activityADict[nActivity])
            # print(actionADict[nAction])
            # print("ACTION: ", actionADict[actionIndex])

            ###### MONTH 
            startMonthActivity = int(activityADict[nActivity][0][5:7])
            endMonthActivity = int(activityADict[nActivity][2][5:7])
            startMonthAction = int(actionADict[actionIndex][0][5:7])
            endMonthAction = int(actionADict[actionIndex][2][5:7])

            ###### DAY
            startDayActivity = int(activityADict[nActivity][0][8:])
            endDayActivity = int(activityADict[nActivity][2][8:])
            startDayAction = int(actionADict[actionIndex][0][8:])
            endDayAction = int(actionADict[actionIndex][2][8:])   

            ##### HOUR
            startHourActivity = int(activityADict[nActivity][1][:2])
            endHourActivity = int(activityADict[nActivity][3][:2])
            startHourAction = int(actionADict[actionIndex][1][:2])
            endHourAction = int(actionADict[actionIndex][3][:2])

            ##### MINUTE
            startMinuteActivity = int(activityADict[nActivity][1][3:5])
            endMinuteActivity = int(activityADict[nActivity][3][3:5])
            startMinuteAction = int(actionADict[actionIndex][1][3:5])
            endMinuteAction = int(actionADict[actionIndex][3][3:5])

            ##### SECOND
            startSecondActivity = int(activityADict[nActivity][1][6:])
            endSecondActivity = int(activityADict[nActivity][3][6:])
            startSecondAction = int(actionADict[actionIndex][1][6:])
            endSecondAction = int(actionADict[actionIndex][3][6:])

            ##### TIME
            startTimeActivity = startHourActivity * 3600 + startMinuteActivity * 60 + startSecondActivity
            endTimeActivity = endHourActivity * 3600 + endMinuteActivity * 60 + endSecondActivity
            startTimeAction = startHourAction * 3600 + startMinuteAction * 60 + startSecondAction
            endTimeAction = endHourAction * 3600 + endMinuteAction * 60 + endSecondAction

            ##### LOCATION
            if actionIndex > 0 and start < end:
                locationActionBefore = actionADict[actionIndex - 1][6]
                locationAction = actionADict[actionIndex][6]
            else:
                locationActionBefore = "EARLY"
                locationAction = "EARLY"

            # print("START TIME ACTIVITY: ", startTimeActivity)
            # print("START TIME ACTION: ", startTimeAction)
            # print("--------------------")
            # print("END TIME ACTIVITY: ", endTimeActivity)
            # print("END TIME ACTION: ", endTimeAction)

            # perfect situation
            if startTimeActivity <= startTimeAction and endTimeActivity>= endTimeAction - 28:
                # print("I AM INSIDE FIRST")
                if endDayActivity != endDayAction:
                    # print("NOT SAME DAY")
                    coupled = False
                # elif locationActionBefore != locationAction:
                #    print("NOT SAME LOCATION")
                #    print(locationActionBefore)
                #    print(locationAction)
                #    coupled = False
                else:
                    coupled = True
            #elif startTimeActivity <= startTimeAction + 48 and endTimeActivity >= endTimeAction:
            #    coupled = True

            # riding day before
            elif startTimeActivity <= startTimeAction and endDayAction == endDayActivity - 1:
                # print("I AM INSIDE SECOND")
                coupled = True
            
            # riding day after
            elif endTimeActivity >= endTimeAction and startDayAction == startDayActivity + 1:
                # print("I AM INSIDE THIRD")
                coupled = True

            # riding month before
            elif startTimeActivity <= startTimeAction and endDayActivity == 1 and endMonthAction == endMonthActivity - 1:
                # print("I AM INSIDE FOURTH")
                coupled = True
            
            # riding month after
            elif endTimeActivity >= endTimeAction and endDayActivity == 1 and endDayAction == 1 and startMonthAction == startMonthActivity +1:
                # print("I AM INSIDE FIFTH")
                coupled = True
            

            # jump no labeled action

            elif endTimeAction < startTimeActivity and not startDayActivity < startDayAction and not startDayAction == 1:
                # print("I AM IN THE SKIP")
                skip = True

            else:
                coupled = False
                                
            
            if coupled == True:
                end += 1
                actionIndex += 1
                # print("I MOVED END, NOW IS: ", end + 3)
            elif skip == True:
                # print("I AM SKIPPING")
                start += 1
                end += 1
                actionIndex += 1
            else:
                # print("START ACTION: ", start + 3)
                # print("END ACTION: ", end + 3)
                # print("I USE THIS ACTIVITY: ", activityADict[nActivity][4])
                for i in range(start, end):
                    line = "{:<17}{:<10}{:<10}{:<10}".format(activityADict[nActivity][4], actionADict[i][4],
                    actionADict[i][5], actionADict[i][6])
                    # print("I ADDED THIS LINE: ", line)
                    final.write(line)
                    final.write("\n")
                start = end 
                out = True

            if actionIndex == len(actionADict) and coupled:
                for i in range(start, end):
                    line = "{:<17}{:<10}{:<10}{:<10}".format(activityADict[nActivity][4], actionADict[i][4],
                    actionADict[i][5], actionADict[i][6])
                    # print("I ADDED THIS LINE: ", line)
                    final.write(line)
                    final.write("\n")
            # print("")