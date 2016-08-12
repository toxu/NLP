import string

class NaiveBaysianClassifier:
    def __init__(self, chn_trained, eng_trained):
        self.chn_freq = chn_trained
        self.eng_freq = eng_trained

    def cal_prob(self, word, t):
        if t == 'words':
            class_a, class_b = self.eng_freq, self.chn_freq
        elif t == 'pinyin':
            class_a, class_b = self.chn_freq, self.eng_freq
        else:
            raise Exception("unknown type")
        prob = 1
        for ch in class_a:
            if ch in word:
                #prob = (class_a[ch] * 0.5) / (class_a[ch] * 0.5 + class_b[ch] * 0.5)
                prob *= class_a[ch]
        return prob

    def classify(self, word):
        for ch in word:
            if ch not in list(string.ascii_lowercase):
                return None
        try:
            if self.cal_prob(word, 'words') >= self.cal_prob(word, 'pinyin'):
                return 'words'
            else:
                return 'pinyin'
        except Exception as e:
            print e
            return None

