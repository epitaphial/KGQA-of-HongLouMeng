# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor,Postagger

class Hlp:
    def __init__(self, ltp_path, user_path):
        cws_model_path = os.path.join(ltp_path, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        user_model_path = os.path.join(user_path, 'userdict.txt') #用户自定义字典
        pos_model_path = os.path.join(ltp_path, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`]
        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load_with_lexicon(cws_model_path,user_model_path)  # 加载模型
        self.postagger = Postagger() # 初始化实例
        self.postagger.load_with_lexicon(pos_model_path,user_model_path)  # 加载模型

    def process_ques(self,question):
        words = self.segmentor.segment(question)  # 分词
        words_list = list(words)
        postags = self.postagger.postag(words_list)  # 词性标注
        postags_list = list(postags)
        print(words_list)
        print(postags_list)
        sent_list = [[],[]]
        expect_list = ['n','nh','r']
        final_list = []
        for index,item in enumerate(postags_list):
            if item in expect_list:
                sent_list[0].append(item)
                sent_list[1].append(words_list[index])
        if sent_list[0] == ['nh','nh','r','n']:
            final_list.append(1)
            final_list.append(sent_list[1][0])
            final_list.append(sent_list[1][1])
            final_list.append('?')
        elif sent_list[0] == ['nh','nh']:
            final_list.append(1)
            final_list.append(sent_list[1][0])
            final_list.append(sent_list[1][1])
            final_list.append('?')
        elif sent_list[0] == ['nh','r','n']:
            final_list.append(2)
            final_list.append(sent_list[1][0])
            final_list.append('?')
            final_list.append(sent_list[1][2])
        elif sent_list[0] == ['r','n','nh']:
            final_list.append(2)
            final_list.append(sent_list[1][2])
            final_list.append('?')
            final_list.append(sent_list[1][1])
        elif sent_list[0] == ['nh','n','r']:
            final_list.append(3)
            final_list.append('?')
            final_list.append(sent_list[1][0])
            final_list.append(sent_list[1][1])
        elif sent_list[0] == ['r','nh','n']:
            final_list.append(3)
            final_list.append('?')
            final_list.append(sent_list[1][1])
            final_list.append(sent_list[1][2])
        elif sent_list[0] == ['nh','n']:
            final_list.append(3)
            final_list.append('?')
            final_list.append(sent_list[1][0])
            final_list.append(sent_list[1][1])
        else:
            pass
        return final_list

    def __del__(self):
        self.segmentor.release()  # 释放模型
        self.postagger.release()  # 释放模型