import nltk
from nltk.stem.lancaster import LancasterStemmer
from bs4 import BeautifulSoup
import requests
import requests
import re
import smtplib
stemmer = LancasterStemmer()
def scrape(m_url,email):
    def retrieve_comments(url):
        main_url = "https://www.instagram.com"
        url = str(url)
        tag = str("script")
        url_str = str(url)
        req = requests.get(url_str)
        soup = BeautifulSoup(req.text, 'lxml')
        paragraph=soup.find_all(str(tag))
        print(paragraph)
        comments=re.findall(r"\"@type\":\"Comment\",\"text\":\"(.*?)\",\"author\":{\"@type\":\"Person\",\"alternateName\":\"(.*?)\"",str(paragraph))
    # {"@type":"Comment","text":"no blessing","author":{"@type":"Person","alternateName":"@rita_bhash",
        #print(comments[0][0])
        #for i in comments:
        #    print(i+"\n")
        print(comments)
        return comments
    training_data = []
    negative_words=['hate','unhygienic','Tatti','mana mariyadi','thu nin makke','Yakkkkk','Bhosdi','Useless','Huccha','die','Jaathre','Kothi','Ulti','Narak','Durankaara','Dabba','kachada','cheap minded','yuck','Thuuu','Daridra','Kantri','Dubba','Fake person','Ghamandi','Fake','deshdrohi','bhosdike','cheat','Bitch','ass','dog','bhoot','madarchod','hate','Chutiya','Ghatiua','Batmeez aadmi','GetLost','boody cheater','Fucking loser','asshole','kamina','sharam krle','pagal','Chutiyaaa','idiot','kutte','go to hell']
    positive_words=['love','cute','angel','lovely','sweety','gorgious','handsome','like']
    for words in positive_words:
        training_data.append({"class":"positive", "sentence":words})
    for words in negative_words:
        training_data.append({"class":"negative", "sentence":words})
    corpus_words = {}
    class_words = {}
    classes = list(set([a['class'] for a in training_data]))
    for c in classes:
        class_words[c] = []

    for data in training_data:
        #print(data)
        for word in nltk.word_tokenize(data['sentence']):
            if word not in ["?", "'s"]:
                stemmed_word = stemmer.stem(word.lower())
                #print(stemmed_word)
                if stemmed_word not in corpus_words:
                    corpus_words[stemmed_word] = 1
                    class_words[data['class']].extend([stemmed_word])
                else:
                    corpus_words[stemmed_word] += 1
                    class_words[data['class']].extend([stemmed_word])
    #print ("Corpus words and counts: %s \n" % corpus_words)
    #print ("Class words: %s" % class_words)
    # calculate a score for a given class


    def calculate_class_score(sentence, class_name, show_details=True):
        score = 0
        for word in nltk.word_tokenize(sentence):
            if stemmer.stem(word.lower()) in class_words[class_name]:
                score += 1
                if show_details:
                    print ("   match: %s" % stemmer.stem(word.lower() ))
        return score


    sentence = "i hate you "
    for c in class_words.keys():
        print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))


    def calculate_class_score(sentence, class_name, show_details=True):
        score = 0
        for word in nltk.word_tokenize(sentence):
            if stemmer.stem(word.lower()) in class_words[class_name]:
                score += (1 / corpus_words[stemmer.stem(word.lower())])
                if show_details:
                    print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
        return score


    def classify(sentence):
        high_class = None
        high_score = 0
        for c in class_words.keys():
            score = calculate_class_score(sentence, c, show_details=False)
            if score > high_score:
                high_class = c
                high_score = score
        return high_class, high_score

    #comments=retrieve_comments("https://www.instagram.com/p/BqHsWSslHjT/")
    comments=retrieve_comments(str(m_url))
    negative=[]
    for comm in comments:
        print(comm[0])
        print(comm[1])
        x=classify(comm[0])
        print(x)
        if(x[0] == "negative"):
            negative.append(comm[1])
        # {"@type":"Comment","text":"no blessing","author":{"@type":"Person","alternateName":"@rita_bhash",
    print(negative)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("poori21097@gmail.com", "poornimajayraman")
    #msg = "Hello!" # The /n separates the message from the headers
    server.sendmail("poori21097@gmail.com", email, str(negative)) #"vksummi@gmail.com"
    server.quit()
    return(negative)
