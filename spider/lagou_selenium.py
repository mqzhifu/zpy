from selenium import webdriver

from selenium.webdriver.common.by import By

import time
import util.common as uc
from lxml import etree

class LagouSelenium:
    data_path = ""
    drive = None
    domain = "https://www.lagou.com/wn/jobs?pn={page_index}&cl=false&fromSearch=true&kd={keyword}"
    def __init__(self,data_path):
        self.data_path = data_path

    def start(self):
        domain = self.domain.replace("{keyword}","前端")

        # options.add_argument('lang=zh_CN.UTF-8')
        # options.add_argument('Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        # options.add_argument("Accept-Language: zh-CN,zh;q=0.9")
        # Referer: https://www.lagou.com/
        # options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"')

        self.drive = webdriver.Chrome( executable_path="/usr/local/opt/python/Frameworks/Python.framework/Versions/3.9/chromedriver")
        # options = webdriver.ChromeOptions()
        # self.drive = webdriver.Chrome(chrome_options=options,executable_path="/usr/local/opt/python/Frameworks/Python.framework/Versions/3.9/chromedriver")
        dataList = []
        # for i in range(1,31):
        url = domain.replace("{page_index}",str( 1 ))
        onePageData = self.get_onde(url)

        # onePageData = [{'job_title': '前端开发工程师', 'city': '上海', 'area': '青浦区', 'date': '19:41发布', 'salary': '15k-30', 'experience': '经验不限', 'educational_background': '本科', 'company_title': '申通快递', 'company_desc': '“平台稳定，技术氛围好，团队融洽，发展空间大”', 'company_people': ' 2000人以上', 'company_category': '物流｜运输 ', 'company_finance': ' 上市公司 ', 'labels': ['物流｜运输', 'React']}, {'job_title': '前端开发工程师', 'city': '北京', 'area': '海淀区', 'date': '21:51发布', 'salary': '15k-20', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '拉勾集团', 'company_desc': '“技术大牛多，福利待遇好”', 'company_people': ' 500-2000人', 'company_category': '工具类产品,在线教育 ', 'company_finance': ' D轮及以上 ', 'labels': ['IT技术服务｜咨询', '数据服务｜咨询', 'Vue', 'Web前端开发', 'HTML']}, {'job_title': '前端工程师', 'city': '杭州', 'area': '拱墅区', 'date': '15:09发布', 'salary': '15k-30', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '拉勾集团', 'company_desc': '“双休，大平台”', 'company_people': ' 500-2000人', 'company_category': '工具类产品,在线教育 ', 'company_finance': ' D轮及以上 ', 'labels': ['工具类产品', '在线教育', 'React', 'Vue', 'Angular']}, {'job_title': '前端开发工程师', 'city': '武汉', 'area': '', 'date': '22:41发布', 'salary': '20k-35', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '论答', 'company_desc': '“美国技术团队，出海业务”', 'company_people': ' 150-500人', 'company_category': 'IT技术服务｜咨询 ', 'company_finance': ' B轮 ', 'labels': ['人工智能服务', '软件服务｜咨询', 'TypeScript', 'React']}, {'job_title': '前端开发工程师', 'city': '苏州', 'area': '虎丘区', 'date': '20:56发布', 'salary': '15k-18', 'experience': '经验3-5年', 'educational_background': '大专', 'company_title': '微创软件', 'company_desc': '“六险一金”', 'company_people': ' 2000人以上', 'company_category': 'IT技术服务｜咨询 ', 'company_finance': ' 不需要融资 ', 'labels': ['IT技术服务｜咨询', '人工智能服务', 'Web前端开发']}, {'job_title': '前端开发工程师', 'city': '广州', 'area': '龙溪', 'date': '20:33发布', 'salary': '12k-20', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '蓝深科技', 'company_desc': '“员工餐厅、年终奖、周末双休、大平台”', 'company_people': ' 500-2000人', 'company_category': '电商平台 ', 'company_finance': ' A轮 ', 'labels': ['电商平台', '新零售', 'JavaScript', 'HTML', 'React']}, {'job_title': '前端开发工程师', 'city': '杭州', 'area': '余杭区', 'date': '19:23发布', 'salary': '8k-12', 'experience': '经验1-3年', 'educational_background': '本科', 'company_title': '学能科技', 'company_desc': '“前景好，公司氛围很nice、小零食、下午茶”', 'company_people': ' 15-50人', 'company_category': '教育 ', 'company_finance': ' 天使轮 ', 'labels': ['在线教育', '教育｜培训', 'CSS', 'JavaScript', 'HTML']}, {'job_title': '前端开发工程师', 'city': '杭州', 'area': '余杭区', 'date': '19:23发布', 'salary': '12k-16', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '学能科技', 'company_desc': '“政府项目前景好，公司氛围nice、小零食下午茶”', 'company_people': ' 15-50人', 'company_category': '教育 ', 'company_finance': ' 天使轮 ', 'labels': ['在线教育', '教育｜培训', 'JavaScript', 'CSS', 'HTML']}, {'job_title': '前端开发工程师', 'city': '珠海', 'area': '香洲区', 'date': '19:03发布', 'salary': '10k-15', 'experience': '经验3-5年', 'educational_background': '大专', 'company_title': '博悦科创', 'company_desc': '“团队氛围好 五险一金 下午茶 大牛多”', 'company_people': ' 500-2000人', 'company_category': 'IT技术服务｜咨询 ', 'company_finance': ' 不需要融资 ', 'labels': ['物联网', 'Vue', 'CSS', 'javaScript', 'HTML5']}, {'job_title': '前端开发工程师', 'city': '深圳', 'area': '福田区', 'date': '18:44发布', 'salary': '12k-18', 'experience': '经验1-3年', 'educational_background': '本科', 'company_title': '博悦科创', 'company_desc': '“公司氛围好 人性化管理 福利丰厚 上升空间多”', 'company_people': ' 500-2000人', 'company_category': 'IT技术服务｜咨询 ', 'company_finance': ' 不需要融资 ', 'labels': ['科技金融', 'Web前端开发', 'Vue', 'JavaScript', 'Es6']}, {'job_title': '前端开发工程师', 'city': '武汉', 'area': '水果湖', 'date': '18:02发布', 'salary': '6k-10', 'experience': '经验3-5年', 'educational_background': '大专', 'company_title': '楚天龙', 'company_desc': '“上市公司，行业好，业务稳定”', 'company_people': ' 500-2000人', 'company_category': '信息安全 ', 'company_finance': ' 上市公司 ', 'labels': ['智能硬件', '软件服务｜咨询', 'JavaScript', 'Web前端开发', 'VUE']}, {'job_title': '前端开发工程师', 'city': '深圳', 'area': '南山区', 'date': '23:10发布', 'salary': '12k-23', 'experience': '经验1-3年', 'educational_background': '本科', 'company_title': 'AfterShip', 'company_desc': '“技术大牛 国际化团队 高速增长 极客文化”', 'company_people': ' 150-500人', 'company_category': '软件服务｜咨询,营销服务｜咨询,数据服务｜咨询 ', 'company_finance': ' B轮 ', 'labels': ['软件服务｜咨询', 'TypeScript', 'Angular', 'Node.js']}, {'job_title': '前端开发工程师', 'city': '成都', 'area': '锦江区', 'date': '22:56发布', 'salary': '10k-18', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '成都爱找我科技有限公司', 'company_desc': '“入职五险一金；网红办公地；大平台”', 'company_people': ' 150-500人', 'company_category': '消费生活 ', 'company_finance': ' A轮 ', 'labels': ['JavaScript', 'HTML', 'CSS', 'Vue', '互联网公司']}, {'job_title': '前端开发工程师', 'city': '南京', 'area': '奥体', 'date': '17:29发布', 'salary': '10k-20', 'experience': '经验3-5年', 'educational_background': '本科', 'company_title': '紫金保险', 'company_desc': '“核心系统技术新颖”', 'company_people': ' 2000人以上', 'company_category': '金融业 ', 'company_finance': ' 不需要融资 ', 'labels': ['金融业', 'Vue']}, {'job_title': '前端开发工程师', 'city': '北京', 'area': '大山子', 'date': '22:46发布', 'salary': '18k-25', 'experience': '经验1-3年', 'educational_background': '本科', 'company_title': '蓝标传媒', 'company_desc': '“上市广告公司，晋升发展透明”', 'company_people': ' 500-2000人', 'company_category': '营销服务｜咨询 ', 'company_finance': ' 不需要融资 ', 'labels': ['营销服务｜咨询', '文化传媒', 'CSS', 'JavaScript', 'Vue']}]
        # uc.ppp("onePageData:",onePageData)
        for row in onePageData:
            rowStr = ""
            for num,key in enumerate (row ) :
                # print(key,row[key])
                if key != "labels":
                    rowStr = rowStr +  row[key] + ","
                else:
                    rowStr = rowStr + "!".join( row[key])+ ","

            rowStr = rowStr[0:len(rowStr)-1]
            # print(rowStr)
            dataList.append(rowStr)
        time.sleep(2)

        data = ""
        for row in dataList:
            data = data + row + "\n"

        # uc.ppp(data)
        fd = open("test.txt", "a")
        fd.write(data)

        self.drive.quit()

    def get_onde(self,url):
        #开启 浏览器 打开网扯
        self.drive.get(url)

        time.sleep(5)
        #查找 所有 label
        labelListSearch = self.drive.find_elements(By.XPATH,"//div[ contains(@class, 'ir___QwEG')]")
        labelList = []
        print("start process labels.")
        for k, item in enumerate(labelListSearch):
            # print("-----" * 10)
            ll = item.find_elements(By.XPATH,"./span")
            itemLabels = []
            for la in ll:
                itemLabels.append(la.text)

            labelList.append(itemLabels)

        print("labelList",labelList)
        #查找每一条记录
        jobList = self.drive.find_elements(By.XPATH,"//div[ contains(@class, 'em__10RTO')]")
        print("jobList：",len(jobList))

        finalDataList = []
        # 开始处理每一条记录
        for k,job in enumerate(jobList):
            line = job.text.split("\n")
            print(line)
            print("---"* 5)
            row = self.get_empty_record()

            job_split_index = line[0].find("[")

            job_title = line[0][0:job_split_index]
            job_area_desc = line[0][job_split_index+1:]
            job_area_desc = job_area_desc[ 0 : len(job_area_desc)-1]

            job_area_info = job_area_desc.split("·")

            row["job_title"] = job_title
            row["city"] = job_area_info[0]
            if len(job_area_info) == 2:
                row["area"] = job_area_info[1]

            row["date"] =line[1]

            salaryIndex = line[2].rindex("k")
            row["salary"] = line[2][0:salaryIndex]

            experience_educational_str = line[2][salaryIndex+1:]
            experience_educational_str_arr  = experience_educational_str.split("/")
            row["experience"] = experience_educational_str_arr[0].strip(" ")
            row["educational_background"] = experience_educational_str_arr[1].strip(" ")

            row["company_title"] = line[3].strip(" ")
            # if len(line) == 7
            company_desc_arr =line[4].split("/")

            row["company_category"] = company_desc_arr[0].strip(" ")
            row["company_finance"] = company_desc_arr[1].strip(" ")
            row["company_people"] = company_desc_arr[2].strip(" ")


            row["company_desc"] = line[6].strip(" ")
            row["labels"] = labelList[k]
            print(row)
            # uc.ppp(row)
            print("*"* 50)
            finalDataList.append(row)

        print("one page finish.","-"*30)
        return finalDataList



    def get_empty_record(self):
        return  {
            "job_title":"",
            "city":"",
            "area":"",
            "date":"",
            "salary":"",
            "experience":"",
            "educational_background":"",
            "company_title":"",
            "company_desc":"",
            "company_people":"",
            "company_category":"",
            "company_finance":"",
            "labels":[],
        }

    def test(self):
        f = open("./lagou.html",'r')
        info = f.read()

        htmlTree = etree.HTML(info)
        # threadTablelistHtml = htmlTree.xpath("//div[@class='em__10RTO']")
        joblist = htmlTree.xpath("//div[ contains(@class, 'em__10RTO')]")

        # for item in joblist:
        #     print(33)
        #
        # print(threadTablelistHtml)
        # print(len(threadTablelistHtml))

