'''
Created on Oct 19, 2010
@author: Peter
'''
from numpy import *

def loadDataSet(): # 실제 file을 오픈하지는 않고 입력된 list를 반환하기는 하지만, 여하튼 data(spam 여부 포함)를 불러오는 함수.
    postingList=[['I', 'got', 'free', 'two', 'movie', 'ticket', 'from', 'your', 'boy', 'friend'],
                 ['free', 'coupon', 'from', 'xx.com'],
                 ['watch', 'free', 'new', 'movie', 'from', 'freemovie.com'],
                 ['best', 'deal', 'promo', 'code', 'here'],
                 ['there', 'will', 'be', 'free', 'pizza', 'during', 'the', 'meeting'],
                 ['scheduled', 'meeting', 'tomorrow'],
                 ['can','we','have','lunch','today'],
                 ['I','miss','you'],
                 ['thanks','my','friend'],
                 ['it','was','good','to','see','you','today'],
                 ['free','coupon','last','deal'],
                 ['free','massage','coupon'],
                 ['I','sent','the','coupon','you','asked','it','is','not','free'],
                 ['coupon','promo','code','here']]
    classVec = [0,1,1,1,0,0,0,0,0,0,1,1,0,1]    #1 is spam, 0 not
    return postingList, classVec
                 
def createVocabList(dataSet): # dataset을 불러와서 단어들의 set을 만든 뒤(중복 X를 위해) list로 반환. (vocab list)
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet): # vocab list 중 어떤 단어들이 input set에 있는지에 관한 dummy vector 반환
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word # 이건 몰까..?
    return returnVec

def trainNB00(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix) # num of rows
    numWords = len(trainMatrix[0]) # num of columns = num of words
    pSpam = sum(trainCategory)/float(numTrainDocs) # spam의 도수 확률
    p0Num = zeros(numWords); p1Num = zeros(numWords)
    p0Denom = 0.0; p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom # P(X/S)
    p0Vect = p0Num/p0Denom # P(X/~S)
    return p0Vect,p1Vect,pSpam # P(S), P(X/S), P(X/~S) 각각 반환

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pSpam = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pSpam # trainNB00와 크게 다르지 않으나, laplace smoothing 적용 및 log(p) 반환

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1) # p1, p0 각각 P(X/S)*P(S)와 P(X/~S)*P(~S) 의미
    if p1 > p0:
        return 1 # SPAM으로 판단
    else: 
        return 0 # ~SPAM으로 판단
    
def bagOfWords2VecMN(vocabList, inputSet): # inputset에서 vocab list에 있는 단어들의 수를 count한 vector를 반환하는 함수
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1 # setOfWords2Vec에서는 유/무 여부만 따져서 1/0 반환했으나, 여기는 count함
    return returnVec

def testingNB():
    listOPosts,listClasses = loadDataSet() # train data 불러옴
    myVocabList = createVocabList(listOPosts) # vocab list 만든 뒤..
    trainMat=[] # 각 entity에 대한 setofwords2vec로 이뤄진 matrix 만들 것.
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc)) # 유/무만 따져서 matrix 반환 (0, 1로만 이뤄져있을 것.)
    #print(str(trainMat))
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(listClasses)) # P(X/S), P(X/~S), P(S)를 얻고
    testEntry = ['free', 'pizza', 'coupon']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry)) # test용 setofwords2vec 만듦.

    if classifyNB(thisDoc, p0V, p1V, pSpam) == 1: # 분류 해버리기~
        print testEntry, 'classified this is a spam'
    else:
        print testEntry, 'classified this is not a spam'

    testEntry = ['I', 'will', 'miss','free', 'pizza'] # 이하 동일
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    if classifyNB(thisDoc,p0V,p1V,pSpam) == 1:
        print testEntry, 'classified this is a spam'
    else:
        print testEntry, 'classified this is not a spam'


def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString) # 알파벳으로 시작하는 것들 전부 split
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] # 3글자 이상 단어에 대해서만 lower version으로 반환
    
def spamTest():
    docList=[]; classList = []; fullText =[] # data set 만들기- 각각 단어 matrix, spam 여부 vector, 모든 단어의 list
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList) #create vocabulary 만들고..
    trainingSet = range(50); testSet=[]           #create test set
    for i in range(10): # 10개의 test data 추출 - random하게
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0 - 남은 걸로 training data 만듦
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses)) # NB classifier 만듦.
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items - test data로 test 진행
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1 # class 불일치 시 error count 올림
            print "classification error",docList[docIndex]
    print 'the error rate is: ',float(errorCount)/len(testSet) # err rate 출력
    #return vocabList,fullText

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token) # full text에서 vocablist 단어들 몇 번씩 나왔는지 count
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True) # frequency 기준으로 sort된 것 반환
    return sortedFreq[:30] # 빈도 수 30위까지 출력

def localWords(feed1,feed0): # 다른 구조의 데이터를 불러와서 data set 만드는 것인 듯- 자료 구조에 대해 잘 모르겠음.
    import feedparser
    docList=[]; classList = []; fullText =[] # spamTest에서처럼 단어 matrix, class vector와 full text list를 만듦
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1) #NY is class 1
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0) 
    vocabList = createVocabList(docList)#create vocabulary
    top30Words = calcMostFreq(vocabList,fullText)   
    for pairW in top30Words: # 빈도 상위 30위에 해당하는 단어들 지움 - 왜인지 모르겠지만-
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet=[]           #spamTest()에서 했던 것과 동일한 방식으로 test 진행.
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex])) # 흥미로운 점은 누적 count로 NB 적용
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V # spamTest()에서와 같은 방식으로 test 진행 및 err rate 출력

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i])) # log p(x/s)가 -6 초과인 단어들 추출
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i])) # log p(x/~s)가 -6 초과인 단어들 추출
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True) # log p 크기로 내림차순
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0] # 상위 단어들 출력
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True) # ~s에 대해서도 동일하게 진행
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]

testingNB()
