from common.sudachi import *


def test_tokenize():
    res = sudachi_tokenize("React、Node.js、Typescript、AWSでの豊富な知識と経験")
    print(res)
    
    
def test_synonims():
    res = synonyms("スクレイピング")
    print(res)