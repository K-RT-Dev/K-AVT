import deepl
from googletrans import Translator

# Class for managment of translation services
# TODO: Impreove output lenguage selection
# TODO: Improve deeplKey handle
# TODO: Add input lenguage specification base on OCR config
class translatorModule():
    def __init__(self, debug=False):
        self.debug = debug
        # Load DeepL Key
        try:
            f = open("kavt_data/deeplkey.txt", "r")
            defaultKey = f.read()
            f.close()
            if len(defaultKey) == 0:
                defaultKey = "xxx"
        except:
            defaultKey = "xxx"
        self.translatorDeep = deepl.Translator(defaultKey)
        self.translatorGoogle = Translator()
        self.target_lang = "en"
        self.transType = "google"
    
    # Change output lenguage
    # Support en (English), es (Spanish)
    def setOutLan(self, outLan):
        if outLan == "en":
            self.target_lang = "en"
        elif outLan == "es":
            self.target_lang = "es"
        else:
            self.target_lang = "en"
    
    # Change DeepL Api Key
    def setDeepLKey(self):
        try:
            f = open("kavt_data/deeplkey.txt", "r")
            defaultKey = f.read()
            f.close()
            if len(defaultKey) == 0:
                defaultKey = "xxx"
        except:
            defaultKey = "xxx"
        self.translatorDeep = deepl.Translator(defaultKey)

    # Change Translator Motor
    def setTransType(self, transType):
        self.transType = transType

    def translate(self, text):
        print("Translating with")
        try:
            # DeepL
            if self.transType == "deepl":
                print("DeepL")
                if len(text) > 0:
                    if self.target_lang == "en":
                        result = self.translatorDeep.translate_text(text, source_lang="JA", target_lang="EN-US")
                    elif self.target_lang == "es":
                        result = self.translatorDeep.translate_text(text, source_lang="JA", target_lang="ES")
                    else:
                        result = self.translatorDeep.translate_text(text, source_lang="JA", target_lang="EN-US")
                else:
                    result = "<None>"
                if self.debug:
                    print(result)
                return result
            # Google Translate
            elif self.transType == "google":
                print("Google Translate")
                if len(text) > 0:
                    if self.target_lang == "en":
                        result = self.translatorGoogle.translate(text, src="ja", dest='en')
                    elif self.target_lang == "es":
                        result = self.translatorGoogle.translate(text, src="ja", dest='es')
                    else:
                        result = self.translatorGoogle.translate(text, src="ja", dest='en')
                    result= result.text
                else:
                    result = "<None>"
                if self.debug:
                    print(result)
                return result
            else:
                print("Invalid Translator")
                return ""
        except:
            print("Error in Translate")
            return "<None>"
