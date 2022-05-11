import os
import re

def main():
    dir = "./1024/"
    fileNamePrefix = "page_list"
    extName = ".txt"


    # middleSplitListTest  = []

    content = ""
    for i in range(1,100,100):
        start = i
        end = i+100 -1
        if end >= 1531:
            end = 1531

        fileNmae = str(start) + "_" +str(end)
        fullPath = dir + fileNamePrefix + fileNmae + extName
        print(fullPath)
        fd = open(fullPath,mode="r",encoding="utf-8")


        key = 0
        for line in fd.readlines():
            # newLine = ""
            lineList = line.split(" , ")
            url = lineList[1].replace("state/p/13/","")
            title = lineList[2].replace("\n","").strip(" ")
            # print("key:",key, " title:",title, " len:",len(title))
            labels = ""

            patternLabel = re.compile(r'\[.*?\]')
            reFindHrefLabel = re.findall(patternLabel,title)
            if len(reFindHrefLabel) > 0 :
                for ll in reFindHrefLabel:
                    title = title.replace(ll,"")
                    labels = labels + ll + "@"

            title ,thisTags,category,brand,actor,hitsCondition = processTags(title,labels)
            print("processTags after , title: "+title+ " actor:"+actor+ "hitsCondition:",hitsCondition)
            if title == "":#有些title将 tag删除后，就会变空了直接
                continue

            S = "^"
            record = get_record_empty()
            record["page"] = str(lineList[0]).strip(" ")
            record["url"] = url.strip(" ")
            record["tags"] = thisTags.strip(" ")
            record["actor"] = actor.strip(" ")
            record["brand"] = brand.strip(" ")
            record["title"] = title.strip(" ")
            record["category"] = category.strip(" ")
            record["labels"] = labels
            record["hits"] = hitsCondition
            newLine = ""
            kk = 0
            for k,oneWord in record.items():
                if kk == len(record) - 1:
                    newLine = newLine + oneWord + os.linesep
                else:
                    newLine = newLine + oneWord + S
                    kk = kk + 1

            # print(newLine)
            # exit(3)
            # newLine =  + S +url + S + thisTags + S + actor + S + brand + S + title + S + category + os.linesep
            # print("newLine:",newLine)
            content = content + newLine
            key = key+1

    # for i in middleSplitListTest:
    #     print(i)

    outFileName = "merge.cvs"
    newFileName = dir +  outFileName

    with open(newFileName,"w",encoding="utf-8")as fp:
        fp.write(content)

    print("finish.")

def processTags(title,labels):
    print("processTags title:",title,"labels:",labels)
    thisTags = ""
    brand = ""
    actor = ""
    category = ""
    hitsCondition = "off"

    tags = ["【新片原档首发】","【新片速遞】","【歐美原創】","【歐美精選】","【欧美精选】"]
    for tag in tags :
        if title.find(tag) == -1:
            continue
        #把tag从标题中删除，方便继续分析title
        title = title.replace(tag,"").strip(" ")
        # thisTags = thisTags + tag
        thisTags = tag

        if tag == "【歐美精選】" or tag == "【欧美精选】":
            title ,category,brand,actor,hitsCondition =  processTagsBySS(title,labels)
        elif tag == "【新片原档首发】":
            title ,category,brand,actor,hitsCondition =  processTagsByNewFirst(title)

    # if title == "-Siri Dahl":
    #     print("aaaa:",actor)
    #     exit(33)

    return title ,thisTags,category,brand,actor,hitsCondition

def processTagsBySS(title,labels):
    brand = ""
    actor = ""
    category = ""
    hitsCondition = "off"

    brand_list = ["Evil Angel","Digital Sin","Tushy","Elegant Angel","21 Sextury","Dane Jones","Blacks On Blondes",
                  "Pure Taboo","Brazzers","Deeper","Private","Reality Kings","BANG","BJRaw","Team Skeet",
                  "Arch Angel","Porn Pros","Bang Bros","MOFOS","Vision Films","Reality Kings","Property Sex",
                  "Naughty America","Spizoo","Crave Media","Babes","PornFidelity","MYLF"]

    #查找(category)
    patternCategory = re.compile(r'\(.*?\)')
    reCategory = re.findall(patternCategory,title)
    if len(reCategory) > 0 :
        #替换(category)
        category = reCategory[0]
        title = title.replace(reCategory[0],"").strip(" ")
        # print(category,title)
    #删除标题中的首字符： -
    if title[0:1] == "-":
        title = title[1:].strip(" ")

    #title抓取的时候，有些字符串过长，被关切了，如[vip123] (xxxxx) 这些，得处理掉
    if title.find("[") != -1 :
        title = title[0:title.find("[")].strip(" ")

    if title.find("(") != -1 :
        title = title[0:title.find("(")].strip(" ")



    #第一轮，筛选，根据： -
    middleSplitList = title.split(" - ")
    if len(middleSplitList) == 1:
        spaceSplitList = title.split(" ")
        if len(spaceSplitList ) == 2:#只有一个空格
            actor = title
            hitsCondition = "middle 1"
            return title ,category,brand,actor,hitsCondition

    elif len(middleSplitList) == 2:
        # print("middleSplitList len == 2" ,middleSplitList[1])
        actor = middleSplitList[1]
        brand = middleSplitList[0]

        hitsCondition = "middle 2"
        return title ,category,brand,actor,hitsCondition

    elif len(middleSplitList) == 3:
        # print("middleSplitList len == 3" ,middleSplitList[1])
        actor = middleSplitList[1]
        brand = middleSplitList[0]

        hitsCondition = "middle 3"
        return title ,category,brand,actor,hitsCondition
    else:
        print("err middleSplitList len == ",len(middleSplitList))

    #查找title中包含 .
    pointSplitList =    title.split(".")
    if len(pointSplitList) >= 2 :
        print("pointSplitList title:",title)
        if pointSplitList[0] == "Thicc18" or pointSplitList[0] == "thicc18":
            brand = "thicc18"
            actor = str(pointSplitList[2:])
            hitsCondition = "point 1"
            return title ,category,brand,actor,hitsCondition

        if pointSplitList[1][0:2] == "20" or pointSplitList[1][0:2] == "21" or pointSplitList[1][0:2] == "22":
            brand = pointSplitList[0]
            if len(pointSplitList) >= 3:
                actor = pointSplitList[1][2:] + " " + pointSplitList[2]
            else:
                actor = pointSplitList[1][2:]

            hitsCondition = "point 2"
            return title ,category,brand,actor,hitsCondition

    # print("netx brand_list labels")
    for bb in brand_list:
        # print("im in brand_list:")
        if labels.find(bb) == -1:
            continue
        # print("brand:",bb,"title:",title)
        # if title.find("_") != -1 or title.find("-") != -1 or title.find(".") != -1:
        if title.find("_") != -1 or title.find("-") != -1 :
            continue

        spaceTitleList  = title.split(" ")
        actor =  spaceTitleList[len(spaceTitleList)-2:len(spaceTitleList)]
        actor = "".join(actor)
        # print("spaceTitleList:",spaceTitleList, " actor:",actor)
        # exit(3)

        hitsCondition = "brand_list 1" + bb
        return title ,category,brand,actor,hitsCondition

    return title ,category,brand,actor,hitsCondition

def processTagsByNewFirst(title):
    brand = ""
    actor = ""
    category = ""
    hitsCondition = "off"

    titleList = title.split("-")
    if len(titleList) == 2:
        brand = titleList[0]
        aa_index = titleList[1].find("(")
        actor = titleList[1][0:aa_index]
        category = titleList[1][aa_index:]
        title = title.replace(category,"")

        hitsCondition = "middle 2"

    elif len(titleList) == 1:
        aa_index = titleList[0].find("(")
        actor = titleList[0][0:aa_index]
        category = titleList[0][aa_index:]
        title = title.replace(category,"")

        hitsCondition = "middle 1"
    elif len(titleList) == 3:
        # brand = titleList[]
        aa_index = titleList[2].find("(")
        actor = titleList[2][0:aa_index]
        category = titleList[2][aa_index:]
        title = title.replace(category,"")

        hitsCondition = "middle 3"
    else:
        print("has error")
        exit(1)

    return title ,category,brand,actor,hitsCondition

def get_record_empty():
    r = {
        "page":0,
        'url':"",
        'actor':"",
        'brand':"",
        'title':"",
        'category':"",
        'tags':"",
        "labels":"",
        "hits":"",
    }
    return r

if  __name__ == "__main__" :
    main()