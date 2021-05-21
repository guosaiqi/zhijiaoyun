import requests
import urllib3
import random
import json
import time

# 解决警告
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

session = requests.Session()

session.headers = headers

def prepareWork():
    print('************************************************')
    print('                欢迎使用本脚本                   ')
    print('            author: 热狗得小舔狗                 ')
    print('            createTime:2021-1-3                 ')
    print('            updateTime:2021-4-23                ')
    print('     免责声明,仅供学习使用,任何行为与作者无关       ')
    print('************************************************')

    userName = input('请输入用户名:')
    passWord = input('请输入密  码:')

    needPinglun = int(input('是否需要评论:1.需要  2.不需要  '))

    return userName, passWord, needPinglun

def getCookie_acw_tc():
    url = 'https://zjy2.icve.com.cn/portal/login.html'
    session.get(url, verify=False)


def download_code():
    r = random.random()
    
    url = "https://zjy2.icve.com.cn/api/common/VerifyCode/index" + "?t=" + str(r)

    res = session.get(url, verify=False)
    
    img = res.content

    with open('verifycode.png', 'wb') as f:
        f.write(img)


def login(userName, passWord,  needPinglun):
    verifyCode = input("请输入验证码:")

    url = 'https://zjy2.icve.com.cn/api/common/login/login'

    data = {
        'userName': userName,
        'userPwd': passWord,
        'verifyCode': verifyCode
    }
    res = session.post(url, data=data, verify=False).json()
    
    if(res['code'] != 1):
        print('登录失败, 请检查账号 密码 验证码.')
        exit()
    else:
        print('登录成功!')

    token = res['token']

    choose_course(token, needPinglun)

# 选择需要刷的课程
def choose_course(token, needPinglun):
    url = 'https://zjy2.icve.com.cn/api/student/learning/getLearnningCourseList'

    res = session.post(url, verify=False)
    
    courseList = res.json()['courseList']

    for i in range(len(courseList)):
        course = courseList[i]
        courseName = course['courseName']

        print(str(i+1) +'   '+ courseName)

    i = int(input('请选择你要刷的课程：')) - 1
    
    course = courseList[i]

    chapterInfo(course, token, needPinglun)

def chapterInfo(course, token, needPinglun):
    
    courseOpenId = course['courseOpenId']
    openClassId = course['openClassId']

    moduleList = processList(courseOpenId, openClassId)
    listChapter = []

    for i in range(len(moduleList)):
       
        module = moduleList[i]
       
        moduleId = module['id']
      
        moduleName = module['name']
    
        dic = {
            'courseOpenId': courseOpenId,
            'openClassId': openClassId,
            'moduleId': moduleId,
            'moduleName': moduleName
        }
        
        listChapter.append(dic)
    
    topicInfo(listChapter, token,  needPinglun)
         

def topicInfo(listChapter, token,  needPinglun):
    url = 'https://zjy2.icve.com.cn/api/study/process/getTopicByModuleId'
    listChapterComment = []

    for i in range(len(listChapter)):
        courseOpenId = listChapter[i]['courseOpenId']
        openClassId = listChapter[i]['openClassId']
        moduleId = listChapter[i]['moduleId']
        moduleName = listChapter[i]['moduleName']

        print('章节:' + moduleName)

        params = {
            'courseOpenId': courseOpenId,
            'moduleId': moduleId
        }

        topicList = session.post(url, headers=headers, params=params).json()['topicList']
        listTopic = []

        for j in range(len(topicList)):
            topicId = topicList[j]['id']
            topicName = topicList[j]['name']

            dic = {
                'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'moduleId': moduleId,
                'topicId': topicId,
                'topicName': topicName
            }
           
            listTopic.append(dic)
      
        listTopicComment = cellInfo(listTopic, token)
       
        listChapterComment.append(listTopicComment)
        
        time.sleep(1)

    if needPinglun == 1:
        print('各文件评论开始, 需要一段时间')
        print('请等待..')
        doComment(listChapterComment)


def cellInfo(listTopic, token):
    url = 'https://zjy2.icve.com.cn/api/study/process/getCellByTopicId'

    listTopicComment = []

    for i in range(len(listTopic)):
        courseOpenId = listTopic[i]['courseOpenId']
        openClassId = listTopic[i]['openClassId']
        moduleId = listTopic[i]['moduleId']
        topicId = listTopic[i]['topicId']
        topicName = listTopic[i]['topicName']

        params = {
        'courseOpenId': courseOpenId,
        'openClassId': openClassId,
        'topicId': topicId
        }

        cellList = session.post(url, params=params, verify=False).json()['cellList']
        listCell = []
        listCellComemnt = []

        print('     子目录:' + topicName)
        for j in range(len(cellList)):
            cellId = cellList[j]['Id']
            cellName = cellList[j]['cellName']
            categoryName = cellList[j]['categoryName']
            childNodeList = cellList[j]['childNodeList']
            stuCellPercent = cellList[j]['stuCellPercent']

            dicComment = {
                'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'cellId': cellId,
                'cellName': cellName
            }
            
            number = len(childNodeList)
            
            for k  in range(number):
                cellId = childNodeList[k]['Id']
                cellName = childNodeList[k]['cellName']
                stuCellPercent = childNodeList[k]['stuCellFourPercent']

                dicComment = {
                'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'cellId': cellId,
                'cellName': cellName
                }

                if k+1 == number:
                    break

                listCellComemnt.append(dicComment)

            dic = {
                'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'cellId': cellId,
                'moduleId': moduleId,
                'cellName': cellName,
                'categoryName': categoryName,
                'childNodeList': childNodeList
            }

              
            listCellComemnt.append(dicComment)

            # 
            if stuCellPercent == 100:
                print('           文件: '+ cellName[:10] + '.., 进度100%(自动跳过)')  
                continue

            listCell.append(dic) 

        listTopicComment.append(listCellComemnt)

        time.sleep(2)
        
        doIt(listCell, token)
   
    return listTopicComment
        
def doIt(listCell, token):
    for i in range(len(listCell)):
        courseOpenId = listCell[i]['courseOpenId']
        openClassId = listCell[i]['openClassId']
        cellId = listCell[i]['cellId']
        moduleId = listCell[i]['moduleId']
        cellName = listCell[i]['cellName']
        categoryName = listCell[i]['categoryName']
        childNodeList = listCell[i]['childNodeList']
        
        # 刷视频文件
        if categoryName == '视频' or categoryName == '音频':
            res = doItNeedInfo(courseOpenId, openClassId, cellId, moduleId, cellName).json()
            
            audioVideoLong = res['audioVideoLong']
            
            stuStudyNewlyTime = res['stuStudyNewlyTime']
            
            cellPercent = res['cellPercent']

            cellLogId = res['cellLogId']
            
            print('           文件：' + cellName[:10] + '.., 目前进度：' + str(cellPercent))
            print('           ' + '请等待..')

            video(courseOpenId, openClassId, cellId, cellLogId,stuStudyNewlyTime, audioVideoLong, token)


       
        elif categoryName == 'ppt文档' or  categoryName == '文档' or  categoryName == 'ppt' or categoryName == 'office文档' or categoryName == '图片':
            res = doItNeedInfo(courseOpenId, openClassId, cellId, moduleId, cellName).json()
           
            cellPercent = res['cellPercent']
            
            pageCount = res['pageCount']

            cellLogId = res['cellLogId']

            print('           文件：' + cellName[:10] +  '.., 目前进度：' + str(cellPercent))
            print('           ' + '请等待..')

            text(courseOpenId, openClassId, cellId, cellLogId, pageCount, token)
        
        
        elif categoryName == '子节点':
            listChildCell = []

            for j in range(len(childNodeList)):
                cellId = childNodeList[j]['Id']
                cellName = childNodeList[j]['cellName']
                categoryName = childNodeList[j]['categoryName']

                dic = {
                'courseOpenId': courseOpenId,
                'openClassId': openClassId,
                'cellId': cellId,
                'moduleId': moduleId,
                'cellName': cellName,
                'categoryName': categoryName,
                'childNodeList': []
                }

                listChildCell.append(dic)  
            doIt(listChildCell, token)



        elif categoryName == '压缩包':
            print('           文件：' + cellName[:10] + '.., 压缩包')
            print('           ' + '请等待..')

            doItNeedInfo(courseOpenId, openClassId, cellId, moduleId, cellName)

        else:
            print('           Warning:{}, 文件无法实现'.format(cellName[:5]))
            continue
        
        time.sleep(2)

    time.sleep(1)


def doComment(listChapterComment): 
    for i in range(1, 5):
        for j in range(len(listChapterComment)):
            listTopicComment = listChapterComment[j]

            for k in range(len(listTopicComment)):
                listCellComemnt = listTopicComment[k]
                
                for l in range(len(listCellComemnt)):
                    dicComment = listCellComemnt[l]

                    courseOpenId = dicComment['courseOpenId']
                    openClassId = dicComment['openClassId']
                    cellId = dicComment['cellId']
                    cellName = dicComment['cellName']

                    if(i == 1):
                        comment(courseOpenId, openClassId, cellId, cellName, 1, 5)
                    else:
                        comment(courseOpenId, openClassId, cellId, cellName, i, 0)
                
                    time.sleep(1)
        time.sleep(60)

def processList(courseOpenId, openClassId):
    url = 'https://zjy2.icve.com.cn/api/study/process/getProcessList'
    params = {
        'courseOpenId': courseOpenId,
        'openClassId': openClassId
    }
    
    res = session.post(url, params=params, verify=False).json()

    return res['progress']['moduleList']

def doItNeedInfo(courseOpenId, openClassId, cellId, moduleId, cellName):
    url = 'https://zjy2.icve.com.cn/api/common/Directory/viewDirectory'

    params = {
        'courseOpenId': courseOpenId,
        'openClassId': openClassId,
        'cellId': cellId,
        'flag': 's',
        'moduleId': moduleId
    }

    res = session.post(url, params=params, verify=False)
    
    if res.json()['code'] == -100 or res.json()['code'] == '-100':
        changeCellData(courseOpenId, openClassId, moduleId, cellId, cellName)
        res = doItNeedInfo(courseOpenId, openClassId, cellId, moduleId, cellName)
        return res
        
    return res

def changeCellData(courseOpenId, openClassId, moduleId, cellId, cellName):
    url = 'https://zjy2.icve.com.cn/api/common/Directory/changeStuStudyProcessCellData'
    
    data = {
        'courseOpenId': courseOpenId,
        'openClassId': openClassId,
        'moduleId': moduleId,
        'cellId': cellId,
        'cellName': cellName
    }
    
    session.post(url, data=data, verify=False)

# 刷视频
def video(courseOpenId, openClassId, cellId, cellLogId,stuStudyNewlyTime, audioVideoLong, token):
    url = 'https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog'

    forNum = int((audioVideoLong - stuStudyNewlyTime) / 10) + 2 

    
    for i in range(forNum):
        if stuStudyNewlyTime-1 < 0:
            stuStudyNewlyTime = 1
            
        nowTime = stuStudyNewlyTime-1 + 10.000001*i
        
        if nowTime >= audioVideoLong: 
            stutyTime = audioVideoLong
        else:
            stutyTime = nowTime

        params = {
            'courseOpenId': courseOpenId,
            'openClassId': openClassId,
            'cellId': cellId,
            'cellLogId': cellLogId,
            'picNum': 0,
            'studyNewlyTime': stutyTime,
            'studyNewlyPicNum': 0,
            'token': token
        }

        res = session.post(url, params=params, verify=False).json()
        if res['code'] != 1:
            print('Warning 视频刷课出现未知错误')
            print(res)
            exit()
            
        time.sleep(10)

def text(courseOpenId, openClassId, cellId, cellLogId, pageCount, token):
    url = 'https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog'

    for i in range(2):
        if(i == 1):
            i = pageCount

        params = {
        'courseOpenId': courseOpenId,
        'openClassId': openClassId,
        'cellId': cellId,
        'cellLogId': cellLogId,
        'picNum': i,
        'studyNewlyTime': '0',
        'studyNewlyPicNum': i,
        'token': token
        }

        res = session.post(url, params=params, verify=False).json()
        
        if res['code'] != 1:
            print('Warning ppt\文档刷课出现未知错误')
            exit()

        time.sleep(5)

def comment(courseOpenId, openClassId, cellId, cellName, chooseNum, starNum):
    url = 'https://zjy2.icve.com.cn/api/common/Directory/addCellActivity'
    params = {
        'courseOpenId': courseOpenId,
        'openClassId': openClassId,
        'cellId': cellId,
        'content': '{}'.format(random.choice(['无', '非常好', '好', '结构紧凑', '内容详细', '讲的不错，都明白了，点赞！', '此课程讲的非常好。'])),
        'docJson': '',
        'star': str(starNum),
        'activityType': str(chooseNum)
    }

    res = session.post(url, params=params, verify=False).json()
    if res['code'] != 1:
        print('评论间隔时间过快, 被发现了！')
        exit()
    time.sleep(1)


if __name__ == "__main__":
    userName, passWord, needPinglun= prepareWork()

    getCookie_acw_tc()

    download_code()

    login(userName, passWord, needPinglun)

    print('该课程以完成 谢谢使用！')
