import os
import json
import pandas as pd
from sudachipy import dictionary,tokenizer,config


def sudachi_tokenize(text:str):
    '''
    テキストから名詞を抽出する
    '''
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C # 形態素解析の単語分割の細かさを指定
    #words = [token.surface() for token in self.tokenizer_obj.tokenize(text,mode)]
    # 正規化することで、言葉のゆらぎを吸収できる
    words = []
    additional_words = []
    for token in tokenizer_obj.tokenize(text,mode):
        # 特定の名詞のみを取得
        part = token.part_of_speech()
        if "名詞" in part:
            words.extend([token.normalized_form()])

    return words
            
            

def normalize(text:str) -> list:
    '''
    textを単語分割の上、正規化して結果をカンマ区切りtextで返す
    '''
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C # 形態素解析の単語分割の細かさを指定
    exclude_parts = ['助詞', '補助記号', '句点']
    normalized_words = []   
    parts = []
    for token in tokenizer_obj.tokenize(text,mode):
        part = token.part_of_speech()
        # 除外する品詞が含まれていない場合は、正規化してリストに追加
        if len(set(part) & set(exclude_parts)) == 0:
            normalized_words.append(token.normalized_form())
            parts.append(token.part_of_speech())
    
    return normalized_words


def synonyms(word: str):
    '''
    wordの類義語を取得する
    '''
    dic_path = os.path.join(os.getcwd(), "word_data", "synonyms.txt") 
    df = pd.read_csv(dic_path, skip_blank_lines=True,
                    names=('group_id', 'type', 'expand', 'vocab_id',         
                    'relation', 'abbreviation', 'spelling', 'domain',  
                    'surface', 'reserve1', 'reserve2'))
        
    res = []
    for row in df[df.surface==word].itertuples():
        res.extend(list(df[df.group_id==row.group_id]["surface"]))
        
    return list(set(res))
