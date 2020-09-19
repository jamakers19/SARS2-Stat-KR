import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from util.form import form
import platform, json, re
from time import sleep
import time
dir_name = "util"

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}

class Seoul():
    def __init__(self):
#        options = webdriver.ChromeOptions()
#        options.add_argument('headless')
#        f_driver = ''
#        if platform.system() == 'Linux':
#            f_driver = '%s/chromedriver'%(dir_name)
#        elif platform.system() == 'Darwin':
#            f_driver = '%s/chromedriver_darwin'%(dir_name)
#        else:
#            f_driver = '%s/chromedriver.exe'%(dir_name)
#        self.driver = webdriver.Chrome(f_driver, chrome_options=options)
        self.db = {
            '지역'          :  0,
            '확진자'        :  0,
            '격리자'        :  0,
            '사망'        :  0,
            '의심환자'      :  0,
            '검사중'        :  0,
            '결과음성'      :  0,
            '자가격리자'    :  0,
            '감시중'        :  0,
            '감시해제'      :  0,
            '퇴원'          :  0,
            }

    def gangnam_gu(self):
        driver = webdriver.Chrome('C:/Users/Choi yeojun/OneDrive/문서/GitHub/SARS2-Stat-KR/util/chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get('http://www.gangnam.go.kr/index.htm')
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find('div', class_='confirm_info').find_all('strong')
        
        confirmed = int(str(table[0].text.replace(",","")))
        self.db['확진자'] += confirmed
        #self.db['확진자'] += int(table[0].text.replace(",","")) # 강남 확진자
        # 자가격리  |  의심환자
        self.db['자가격리자'] += int(str(table[1].text.replace(",",""))) # 강남 자가격리자
        self.db['의심환자'] += int(str(table[2].text.replace(",",""))) # 강남 능동감시자
        
        print(u"# 강남구 : %d"%(confirmed))

    def gangdong_gu(self):
        res = requests.get('https://www.gangdong.go.kr/site/contents/corona/', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')

        
        self.db['확진자'] += int(soup.find('li', 'red').find('strong').text.replace(",","")) # 강동 확진자
        self.db['퇴원'] += int(soup.find('li', 'green').find('strong').text.replace(",","")) # 강동 퇴원자
        self.db['자가격리자'] += int(soup.find('li', 'blue').find('strong').text.replace(",","")) # 강동 자가격리자
        self.db['사망'] += int(soup.find('li', 'blue').find('strong').text.replace(",","")) # 강동 사망자
        print(u"# 강동구 : %d"%(int(soup.find('li', 'red').find('strong').text)))

    def gangbuk_gu(self):
        driver = webdriver.Chrome('C:/Users/Choi yeojun/OneDrive/문서/GitHub/SARS2-Stat-KR/util/chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get('http://www.gangbuk.go.kr/intro_gb.jsp')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        temp = soup.find('ul', class_='clearfix')
        table = re.findall(u'<p class="text">(.*?)</p>',str(temp))
        

        self.db['확진자'] += int(table[0].replace(',','')) # 강북 확진자
        self.db['자가격리자'] += int(table[1].replace(',','')) # 강북 자가격리자
        self.db['퇴원'] += int(table[2].replace(',','')) # 강북 능동감시자

        print(u"# 강북구 : %d"%(int(table[0].replace(',',''))))

    def gangseo_gu(self):
        res = requests.get('http://www.gangseo.seoul.kr/new_portal/index.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  능동감시자
        table = soup.find('div', class_='covid_table').find('tbody').find('tr').get_text().split('\n')
    
        self.db['확진자'] += int(table[1].replace(",","")) # 강서 확진자
        self.db['격리자'] += int(table[2].replace(",",""))
        self.db['퇴원'] += int(table[3].replace(",",""))
        self.db['사망'] += int(table[4].replace(",",""))
        self.db['감시중'] += int(table[5].replace(",","")) # 강서 능동감시자
        print(u"# 강서구 : %d"%(int(table[1])))

    def gwanak_gu(self):
        driver = webdriver.Chrome('C:/Users/Choi yeojun/OneDrive/문서/GitHub/SARS2-Stat-KR/util/chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get('http://www.gwanak.go.kr/site/gwanak/main.do')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # 확진자  |  자가격리자  |  능동감시자
        table1 = soup.find('div', 'corona_con').find_all('td')
        table2 = soup.find('div', 'corona_con').find_all('strong')
        self.db['확진자'] += int(table1[0].text.replace(",","").split("명")[0].replace("명", ""))
        self.db['격리자'] += int(table1[1].text.replace(",","").split("명")[0].replace("명", ""))
        self.db['퇴원'] += int(table1[2].text.replace(",","").split("명")[0].replace("명", ""))
        self.db['자가격리자'] += int(table2[0].text.replace(",","").split("명")[0].replace("명", ""))
        self.db['감시중'] += int(table2[1].text.replace(",","").split("명")[0].replace("명", ""))

        print(u"# 관악구 : %d"%(int(table1[0].text.replace(",","").split("명")[0].replace("명", ""))))

    def gwangjin_gu(self):
        res = requests.get('https://www.gwangjin.go.kr/index1.html', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 위기경보단계  |  확진환자  |  자가격리&능동감시자
        # 자가격리자와 능동감시자와 별개로 분류되어 있지 않으므로 자가격리자로 취급
        table1 = soup.find('div', 'table w').find_all('th')
        table2 = soup.find('div', 'table w').find_all('strong')

        self.db['확진자'] += int(table1[0].text.replace(",","").replace('확진자(', '').replace(')', ''))
        self.db['자가격리자'] += int(table1[1].text.replace(",","").replace('자가격리(', '').replace(')', ''))
        self.db['격리자'] += int(table2[0].text.replace(",",""))
        self.db['퇴원'] += int(table1[0].text.replace(",","").replace('확진자(', '').replace(')', '')) - int(table2[0].text.replace(",",""))

        print(u"# 광진구 : %d"%(int(table1[0].text.replace(",","").replace('확진자(','').replace(')', ''))))

    def guro_gu(self):
        res = requests.get('http://www.guro.go.kr/corona2.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 구분  |  확진자  |  자가격리자  |  능동감시자
        table = soup.find('table', class_='table_A').find('tbody').find_all('td')
         # 확진자 수 뒤에 붙어있는 '강조' 텍스트 제거

        self.db['확진자'] += int(table[0].text.replace(",",""))
        self.db['격리자'] += int(table[1].text.replace(",",""))
        self.db['퇴원'] += int(table[2].text.replace(",",""))
        self.db['자가격리자'] += int(table[3].text.replace(",",""))
        self.db['감시중'] += int(table[4].text.replace(",",""))

        print(u"# 구로구 : %d"%(int(int(table[0].text.replace(",","")))))

    def geumcheon_gu(self):
        res = requests.get('https://www.geumcheon.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 구분  |  확진자  |  능동감시자(자가격리자)
        value1 = soup.find('li', class_='pink_line clearfix')
        table = re.findall('(.*?)명', value1.text)

        confirmed = int(table[0].replace(',', ''))
        quarantined = int(table[1].replace(',', ''))
        cared = int(table[2].replace(',', ''))

        self.db['확진자'] += confirmed
        # 능동감시자와 자가격리자가 N명(M명) 의 형태로 표기되어 있어 별도로 분리
        #self.db['감시중'] += int(value2[0].replace(' ', ''))
        #self.db['자가격리자'] += int(value2[1].replace('(','').replace(' ', ''))

        print(u"# 금천구 : %d"%(confirmed))

    def nowon_gu(self):
        res = requests.get('http://www.nowon.kr', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  의심환자  |  유증상자  |  자가격리자
        # 유증상자는 별도로 집계하지 않음
        table = soup.find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text[:-1].replace(' ', '').replace('\n', '').replace(',', '').split("명")[0].replace("명", ""))
        self.db['퇴원'] += int(table[1].text[:-1].replace(' ', '').replace('\w', '').replace(',', '').split("명")[0].replace("명", ""))
        self.db['격리자'] += int(table[3].text[:-1].replace(' ', '').replace('\n', '').replace(',', '').split("명")[0].replace("명", ""))
        self.db['의심환자'] += int(table[2].text[:-1].replace(' ', '').replace('\n', '').replace(',', '').split("명")[0].replace("명", ""))
        self.db['감시중'] += int(table[4].text[:-1].replace(' ', '').replace('\n', '').replace(',', '').split("명")[0].replace("명", ""))
        self.db['자가격리자'] += int(table[4].text[:-1].replace(' ', '').replace('\n', '').replace(',', '').split("명")[0].replace("명", ""))

        print(u"# 노원구 : %d"%(int(table[0].text[:-1].replace(' ', '').replace('\n', '').replace(',', '').split("명")[0].replace("명", ""))))

    def dobong_gu(self):
        res = requests.get('http://www.dobong.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('div', class_='mt10').find_all('dd')
        self.db['확진자'] += int(table[0].text.replace(' ', '').replace(',', ''))
        self.db['격리자'] += int(table[1].text.replace(' ', '').replace(',', ''))
        self.db['자가격리자'] += int(table[4].text.replace(' ', '').replace(',', '')) - int(table[5].text.replace(' ', '').replace(',', ''))
        self.db['감시중'] += int(table[4].text.replace(' ', '').replace(',', ''))
        self.db['감시해제']+= int(table[5].text.replace(' ', '').replace(',', ''))
        self.db['퇴원'] += int(table[2].text.replace(' ', '').replace(',', ''))
        self.db['사망'] += int(table[3].text.replace(' ', '').replace(',', ''))
        
        print(u"# 도봉구 : %d"%(int(table[0].text.replace(' ', '').replace(',', ''))))

    def dongdaemun_gu(self):
        res = requests.get('http://www.ddm.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  검사중  |  결과음성
        table = soup.find('tbody').find_all('strong')
        self.db['확진자'] += int(table[0].text.replace(' ', ''))
        self.db['감시중'] += int(table[1].text.replace(' ', ''))
        self.db['감시해제'] += int(table[2].text.replace(' ', ''))

        print(u"# 동대문구 : %d"%(int(table[0].text.replace(' ', ''))))

    def dongjak_gu(self):
        res = requests.get('https://www.dongjak.go.kr/')#, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  능동감시자
        table = soup.find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text.replace(',', '').replace("번", ""))
        self.db['자가격리자'] += int(table[1].text.replace(',', '').replace("명", ""))
        self.db['퇴원'] += int(table[2].text.replace(',', '').replace("명", ""))
        self.db['격리자'] += int(table[0].text.replace(',', '').replace("번", "")) - int(table[2].text.replace(',', '').replace("명", ""))
        print(u"# 동작구 : %d"%(int(table[0].text.replace(' ', '').replace("번", ""))))

    def mapo_gu(self):
        res = requests.get('http://www.mapo.go.kr/html/corona/intro.htm')#, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('tbody').find_all('tr')[1].find_all('td')
        quarantined = int(table[0].text.replace(' ', ''))
        cared = int(table[1].text.replace(' ', ''))
        confirmed = quarantined + cared
        self.db['확진자'] += confirmed
        #self.db['자가격리자'] += int(table[1].text.replace(' ', ''))
        #self.db['감시중'] += int(table[2].text.replace(' ', ''))

        print(u"# 마포구 : %d"%(confirmed))

    def seodaemun_gu(self):
        res = requests.get('http://www.sdm.go.kr/index.do', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  퇴원자  |  자가격리자
        table = soup.find('ul', class_='corona-popup-number-box').find_all('span') 
        self.db['확진자'] += int(table[0].text.replace(' ', ''))
        self.db['퇴원'] += int(table[1].text.replace(' ', ''))
        self.db['자가격리자'] += int(table[2].text.replace(' ', ''))

        print(u"# 서대문구 : %d"%(int(table[0].text.replace(' ', ''))))

    def seocho_gu(self):
        res = requests.get('http://www.seocho.go.kr/site/seocho/main.do', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        # 확진자  |  능동감시자
        table = soup.find('div', id='virusPopup').find('table').find('tbody').find_all('td')
    
        treatmentkr = int(table[0].text[:-1].replace(',',''))
        treatmentfr = int(table[1].text[:-1].replace(',',''))
        cured = int(table[2].text[:-1].replace(',',''))
        selfquarantinekr = int(table[3].text[:-1].replace(',',''))
        selfquarantinefr = int(table[4].text[:-1].replace(',',''))
        self.db['확진자'] += treatmentkr + treatmentfr + cured
        self.db['퇴원'] += cured
        self.db['자가격리자'] += selfquarantinekr + selfquarantinefr
        print(u"# 서초구 : %d"%(treatmentkr + treatmentfr + cured))

    def seongdong_gu(self):
        res = requests.get('http://www.sd.go.kr/sd/intro.do', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        temp = soup.find('ul', class_='status_list')
        table = re.findall('<em>(.*?)명</em>',str(temp))
        table2 = re.findall('<span class="stat_txt">(.*?)명</span>',str(temp))
        # 확진자  |  의심환자  |  능동감시자  |  자가격리자  |  유증상자
        # 유증상자는 별도로 집계 안함
        quarantined = int(table[0].replace(',','').replace("명", ""))
        cared = int(table[1].replace(',','').replace("명", ""))
        confirmed = quarantined + cared
        dead = int(table[2].replace('.','').replace("명", ""))
        self.db['확진자'] += confirmed
        self.db['격리자'] += quarantined
        self.db['사망'] += dead
        #self.db['의심환자'] += int(table[1].text[:-1].replace(',',''))
        self.db['퇴원'] += cared
        #self.db['자가격리자'] += int(table[3].text[:-1].replace(',',''))
        self.db['자가격리자'] += int(table2[0].replace(',','').replace("명", ""))
        self.db['감시중'] += int(table2[1].replace(',','').replace("명", ""))
        print(u"# 성동구 : %d"%(confirmed))

    # 성북구는 텍스트로 된 자료를 제공하지 않아 크롤링 불가
    def seongbuk_gu(self):
        res = requests.get('http://www.sb.go.kr/')
        soup = BeautifulSoup(res.content, 'lxml')
        # 퇴원  |  격리자  |  자가격리 능동감시자
        
        table = soup.find('div', class_='box1 clearfix').find_all('span', class_='num')
        table2 = soup.find('div', class_='d-button').find_all('p')
        self.db['퇴원'] += int(table[2].text.replace(',', ''))
        self.db['격리자'] += int(table[1].text.replace(',', ''))
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['자가격리자'] += int(table2[1].text.replace(',', '').split('자가격리 ')[1].replace('\n			', ''))
        #self.db['자가격리자'] += # int(table[2].text.replace(',', ''))
        print(u"# 성북구 : %d"%(int(table[0].text.replace(',', ''))))

    def songpa_gu(self):
        res = requests.get('http://www.songpa.go.kr/index.jsp', verify=True, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        init = soup.find('tbody')
        table = re.findall('\n(.*?)명', init.text)
        confirmed = int(table[0].replace(',', ''))
        quarantined = int(table[1].replace(',', ''))
        cared = int(table[2].replace(',', ''))
        selfquarantinekr = int(table[4][:-1].replace(',',''))
        selfquarantinefr = int(table[5][:-1].replace(',',''))
        
        # 확진자  |  퇴원(확진해제자)  |  자가격리  
        
        self.db['확진자'] += confirmed
        self.db['퇴원'] += cared
        self.db['격리자'] += quarantined
        self.db['자가격리자'] += selfquarantinekr + selfquarantinefr
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        print(u"# 송파구 : %d"%(confirmed))

    def yangcheon_gu(self):
        res = requests.get('http://www.yangcheon.go.kr/site/yangcheon/coronaStatusList.do') #, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        confirmed = int(soup.find('tbody').find_all('td')[1].text.split('명')[0].replace(',', ''))
        ## 전국  |  양천구  
        
        self.db['확진자'] += confirmed
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        #self.db['자가격리자'] += 
        print(u"# 양천구 : %d"%(confirmed))

    def yeongdeungpo_gu(self):
        res = requests.post('https://www.ydp.go.kr/selectDissInfoJSON.do', verify=False, headers=headers)
        table = json.loads(res.content)['dissInfo']

        quarantined = int(table['cnt1'])
        cared = int(table['cnt4'])
        confirmed = quarantined + cared
        self.db['확진자'] += confirmed
        self.db['격리자'] += quarantined # 확진자
        self.db['자가격리자'] += int(table['cnt2']) # 자가격리자
        self.db['퇴원'] += cared # 능동감시자

        print(u"# 영등포구 : %d"%(confirmed))
    
    def yongsan_gu(self):
        res = requests.get('http://www.yongsan.go.kr/site/kr/index.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table_init = soup.find('tbody')
        # 확진자  |  퇴원자  |  격리 |  자가격리/능동감시(자가격리자)
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ') 

        self.db['확진자'] += int(table[0][:-1]) # 확진자
        self.db['자가격리자'] += int(table[1][:-1]) # 확진자

        print(u"# 용산구 : %d"%(int(table[0][:-1])))
    
    def eunpyeong_gu(self):
        res = requests.get('https://www.ep.go.kr/CmsWeb/viewPage.req?idx=PG0000004918')#, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find_all('tbody')[1].find_all('td')

        confirmed = int(table[0].text.split('명')[0].replace(',',''))
        self.db['확진자'] += confirmed  # 확진자
        #self.db['추가확진자'] += int(table[0][:-1]) # 
        #self.db['퇴원'] += 
        #self.db['자가격리자'] += int(table[2].text[:-1].replace(',',''))
        
        print(u"# 은평구 : %d"%(confirmed))
        
    def jongno_gu(self):
        res = requests.get('http://www.jongno.go.kr/portalMain.do;jsessionid=edgF6qdhxN6YfuSesu3MBWaoxB1zxK13M4zajh2nSIWcitqm4UVSX7ITFaNU1Rdb.was_servlet_engine1', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        # 확진자  |  퇴원자  |  격리  |  자가격리/능동감시(자가격리자)
        table = soup.find('div', 'coronal-table').find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text[:-1]) # 확진자
        self.db['퇴원'] += int(table[1].text[:-1]) # 퇴원자
        self.db['격리자'] += int(table[2].text[:-1]) # 치료중
        self.db['자가격리자'] += int(table[3].text[:-1]) # 자가격리자

        print(u"# 종로구 : %d"%(int(table[0].text[:-1])))
        
    def jung_gu(self):
        res = requests.get('http://www.junggu.seoul.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('div', class_='sub_table1 popup_table').find('table').find('tbody').find_all('td')
    
        treatment = int(table[0].text.replace(',',''))
        cured = int(table[1].text.replace(',',''))
        selfquarantinekr = int(table[2].text.replace(',',''))
        selfquarantinefr = int(table[3].text.replace(',',''))
        self.db['확진자'] += treatment + cured
        self.db['자가격리자'] += selfquarantinekr + selfquarantinefr
        self.db['격리자'] +=  treatment
        self.db['퇴원'] += cured

        print(u"# 중구 : %d"%(treatment + cured))
    
    def jungnang_gu(self):
        driver = webdriver.Chrome('C:/Users/Choi yeojun/OneDrive/문서/GitHub/SARS2-Stat-KR/util/chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get('https://www.jungnang.go.kr/intro.jsp')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        temp = soup.find('b', 'num1')
        table = soup.find('ul', 'num_board').find('li').find('b', 'num1')
        table2 = re.findall('<span class="fc_blue">((.*?))</span>', temp.text)
        print(table)
        print(table2)
        
        # 전국  |  북구  |  자가격리
        self.db['확진자'] += int(table[0].replace(',', '').split(' '))
        self.db['격리자'] += int(table[0].replace(',', '').split(' ')) - int(table2[0].replace(',', ''))
        self.db['퇴원'] += int(table2[0].replace(',', ''))
        self.db['자가격리자'] += int(table[1].replace(',', ''))
        self.db['의심환자'] += int(table[2].replace(',', ''))

        print(u"# 중랑구 : %d"%(int(table[0].replace(',', ''))))
        
    def collect(self):
        res = requests.get('http://www.seoul.go.kr/coronaV/coronaStatus.do?menu_code=01', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        li_num = soup.find_all('p', class_='counter')
        li_txt = soup.find_all('p', class_='txt')

        li_txt = [txt.text for txt in li_txt]
        li_num = [num.text for num in li_num]

        others = int(soup.find('span', class_='district district26').find('span', class_='num').text.replace(',', ''))

        stat = copy.copy(form)
        for i in range(0, len(li_txt)-4):
            stat[li_txt[i]] = li_num[i]

        self.db = {
            '지역'          :  0,
            '확진자'        :  0,
            '격리자'        :  0,
            '사망'        :  0,
            '의심환자'      :  0,
            '검사중'        :  0,
            '결과음성'      :  0,
            '자가격리자'    :  0,
            '감시중'        :  0,
            '감시해제'      :  0,
            '퇴원'          :  0,
            }


        self.gangnam_gu()
        self.gangdong_gu()
        self.gangbuk_gu()
        self.gangseo_gu()
        self.gwanak_gu()
        self.gwangjin_gu()
        self.guro_gu()
        self.geumcheon_gu()
        self.nowon_gu()
        self.dobong_gu()
        self.dongdaemun_gu()
        self.dongjak_gu()
        self.mapo_gu()
        self.seodaemun_gu()
        self.seocho_gu()
        self.seongdong_gu()
        self.seongbuk_gu()
        self.songpa_gu()
        self.yangcheon_gu()
        self.yeongdeungpo_gu()
        self.yongsan_gu()
        self.eunpyeong_gu()
        self.jongno_gu()
        self.jung_gu()
        self.jungnang_gu()

        self.db['확진자'] += others # 기타

        print("# 기타 : %d"%(others))
        
        stat['지역'] = '서울'
        stat['확진자'] = format(self.db['확진자'], ',')
        # stat['사망'] = li[2].text.split(' ')[1]
        stat['퇴원'] = format(int(stat['퇴원'].replace(',','')) - 1, ',')
        stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    
        print("pass : ", stat['지역'])
        
        return stat
