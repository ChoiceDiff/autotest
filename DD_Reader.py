import pandas as pd
import numpy as np
import math
import os

def getDdValMap(dd_dict):
    ddLen=len(dd_dict)
    ddMap = {}# 数据哈希表
    for i in range(0,ddLen): # 左闭右开区间
        row = dd_dict[i] # 按位置取得一行数据
        label = row["标识"]
        primaryKey = row["变量名"] # 以变量名作为主键！！！
        paraDes = row["描述"]
        paraType = row["数据类型"]
        direction = row["方向"]
        maxValue = row["最大值"] # 根据数据类型进行处理
        minValue = row["最小值"] # 根据数据类型进行处理
        defVal = row["定义值"] # 根据数据类型进行处理
        iniVal = row["初始值"] # 根据数据类型进行处理
        unit = row["单位"]
        cycle = int(row["周期_ms"])
        labelNum = row["Label号"]
        offset = row["偏移量"] # if row["偏移量"] != np.nan else ""
        length = row["长度"] # if row["长度"] != np.nan else ""
        ratio = row["分辨率"] # ？？？ <class 'float'>
        sdiExp = row["SDI预期"]
        paraRetro = row["变量追溯"]
        principle = row["原理"]
        titleLevel = int(row["标题等级"])
        possibleVal = []
        ddMap[primaryKey] = [label,paraDes,paraType,direction,maxValue,\
                                minValue,defVal,iniVal,unit,cycle,labelNum,\
                                offset,length,ratio,sdiExp,paraRetro,principle,\
                                titleLevel,possibleVal] # 数据记录
    return ddMap

def findDataByKey(dd_map,paraName):
    return dd_map[paraName]

def baseInfo(txtLines): # 读取文件名，和需求号
    line1 = txtLines[0].split(":")[1]
    line2 = txtLines[1].split(":")[1:]
    return line1,line2

def parseCondition(condition,relationDict): # 解析条件、变量对应的范围
    condRangeMap = {}
    for line in condition:
        temp = line.split(":")
        detail = temp[1].split(",")
        paraName = detail[0]
        conditionDetail = detail[1]
        veriType = detail[2]
        bound = []
        count = 0
        opType = [] # 0位置为原来的，1位置为取反，2位置为数量
        for op in relationDict:
            if op in conditionDetail:
                count = conditionDetail.count(op)
                opType.append(op)
                opType.append(relationDict[-relationDict.index(op)-1])
                opType.append(count)
                bound = conditionDetail.split(op).remove(paraName)
                break
        condRangeMap[temp[0]] = [paraName,opType,bound,veriType]
    return condRangeMap

def parseTruthTable(tt):
    pass

def getTcData(tt):
    if paraType == "离散量":
            # 根据数据类型进行数据处理
            possibleVal = [1,0]
            maxValue = 1
            minValue = 0
        elif paraType == "整型":
            maxValue = int(row["最大值"])
            minValue = int(row["最小值"])
            ratio = 1
            possibleVal.append(minValue - ratio)
            possibleVal.append(minValue)
            possibleVal.append(minValue + ratio)
            possibleVal.append(maxValue - ratio)
            possibleVal.append(maxValue)
            possibleVal.append(maxValue + ratio)
            possibleVal.append((maxValue + minValue)//2)
        elif paraType == "字符型":
            possibleVal.append(str(iniVal).split(','))
            maxValue = max(possibleVal)
            minValue = min(possibleVal)
        elif paraType == "浮点型" and maxValue != np.nan and minValue != np.nan:
            maxValue = float(row["最大值"]) # 精度不准
            minValue = float(row["最小值"]) # 精度不准
            # precisionLen = len(str(ratio))-2
            precisionLen = len(str(ratio).split('.')[1])
            possibleVal.append("{1:.{0}f}".format(precisionLen,minValue - ratio))
            possibleVal.append("{1:.{0}f}".format(precisionLen,minValue))
            possibleVal.append("{1:.{0}f}".format(precisionLen,minValue + ratio))
            possibleVal.append("{1:.{0}f}".format(precisionLen,maxValue - ratio))
            possibleVal.append("{1:.{0}f}".format(precisionLen,maxValue))
            possibleVal.append("{1:.{0}f}".format(precisionLen,maxValue + ratio))
            possibleVal.append("{1:.{0}f}".format(precisionLen,(maxValue + minValue)/2))

def generateTcFile(tt):
    pass

def main():
    # 操作类型字典
    paraMap = {'s': 'SET', 'sl': 'SELECT','w': 'WAIT', 'v': 'VERIFY', 'c': 'CHECK'}

    # 解析数字字典
    sheet=pd.read_excel('dd.xlsx',sheet_name=None) # <class 'dict'>
    sheetInfo=sheet.items() # <class 'dict_items'>
    dataInfoDict = []
    for _,dataInfo in sheetInfo: # key为sheet.keys(),<class 'dict_keys'>表单名列表
        dataInfoDict = dataInfo.to_dict(orient='records') # 表单数据转化为列表形式，不包含A,B,C,D
    ddMap=getDdValMap(dataInfoDict) # 获得“变量名-变量信息”映射map

    # 解析输入模板：
    default_dir = os.chdir(os.path.dirname(__file__))
    txtFilePath = os.path.join(default_dir,"template.txt")
    f_data = open(txtFilePath, "r", encoding='utf-8')
    txtLines = f_data.readlines()
    index = 0 # 用于跟踪索引

    # 1.文件名、需求号
    baseLines = txtLines[index:2]
    fileName,requirementNum = baseInfo(baseLines)

    # 2.条件和变量对应的范围
    lenTxt = len(txtLines)
    index = 3
    for i in range(index,lenTxt):
        if "Truth Table" in txtLines[i]:
            conditionLines = txtLines[index:i]
            index = i
            break
    relationDict = ["==","<=",">=","<",">","!="] # -index-1就可以找到相反的判断
    condData = parseCondition(conditionLines,relationDict)
    
    # 3.真值表与条件、影响变量对应
    # 4.计算对应的值
    # 5.写入新生成的TC 表格文件
    tt = 
    ttLineInfo = 
    infoByCondition = {}
    dataInfo = countTestData(infoByCondition,ddMap)
    
    #生成TC，写入Excel


if __name__=='__main__':
    main()
