import os
import re

def main():
    dir = "./1024/"
    fileNamePrefix = "page_list"
    extName = ".txt"

    content = ""
    for i in range(1,200,100):
        start = i
        end = i+100 -1
        if end >= 1531:
            end = 1531

        fileNmae = str(start) + "_" +str(end)
        fullPath = dir + fileNamePrefix + fileNmae + extName
        print(fullPath)
        fd = open(fullPath,mode="r",encoding="utf-8")


        tags = ["【新片原档首发】","【新片速遞】","【歐美原創】","【歐美精選】","【欧美精选】"]
        key = 0
        for line in fd.readlines():
            # newLine = ""
            lineList = line.split(" , ")
            url = lineList[1].replace("state/p/13/","")
            title = lineList[2].replace("\n","")
            print("key:",key, " title:",title)
            thisTags = ""
            brand = ""
            actor = ""
            category = ""
            labels = ""


            patternLabel = re.compile(r'\[.*?\]')
            reFindHrefLabel = re.findall(patternLabel,title)
            if len(reFindHrefLabel) > 0 :
                for ll in reFindHrefLabel:
                    title = title.replace(ll,"")
                    labels = labels + ll + "@"

            for tag in tags :
                if title.find(tag) != -1:
                    title = title.replace(tag,"")
                    # thisTags = thisTags + tag + "/"
                    thisTags = thisTags + tag

                    if tag == "【歐美精選】" or tag == "【欧美精选】" :
                        patternCategory = re.compile(r'\(.*?\)')
                        reCategory = re.findall(patternCategory,title)
                        if len(reCategory) > 0 :
                            category = reCategory[0]
                            title = title.replace(reCategory[0],"")
                            print(category,title)

                    if tag == "【新片原档首发】":
                        if title == "":
                            break

                        titleList = title.split("-")
                        if len(titleList) == 2:
                            brand = titleList[0]
                            aa_index = titleList[1].find("(")
                            actor = titleList[1][0:aa_index]
                            category = titleList[1][aa_index:]
                            title = title.replace(category,"")
                        elif len(titleList) == 1:
                            aa_index = titleList[0].find("(")
                            actor = titleList[0][0:aa_index]
                            category = titleList[0][aa_index:]
                            title = title.replace(category,"")
                        elif len(titleList) == 3:
                            # brand = titleList[]
                            aa_index = titleList[2].find("(")
                            actor = titleList[2][0:aa_index]
                            category = titleList[2][aa_index:]
                            title = title.replace(category,"")
                        else:
                            print("has error")
                            exit(1)

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
            content = content + newLine
            key = key+1


    outFileName = "merge.cvs"
    newFileName = dir +  outFileName

    with open(newFileName,"w",encoding="utf-8")as fp:
        fp.write(content)

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
    }
    return r

if  __name__ == "__main__" :
    main()