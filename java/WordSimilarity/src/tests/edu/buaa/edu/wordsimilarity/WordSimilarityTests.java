/*
 * Copyright (C) 2008 SKLSDE(State Key Laboratory of Software Development and Environment, Beihang University)., All Rights Reserved.
 */
package edu.buaa.edu.wordsimilarity;

import junit.framework.TestCase;


/**
 * DOCUMENT ME!
 *
 * @author Yingqiang Wu
 * @version 1.0
  */
public class WordSimilarityTests extends TestCase {
    public void test_loadGlossary(){
        WordSimilarity.loadGlossary();
    }
    /**
     * test the method {@link WordSimilarity#disPrimitive(String, String)}.
     */
    /* 计算两个词语的距离 */
    public void test_disPrimitive(){
    	// 这里计算的义项相似度和软件中的词语相似度一样，而不是计算概念相似度。
        int dis = WordSimilarity.disPrimitive("开心", "争斗");
        System.out.println("雇用 and 争斗 dis : "+ dis);
    }
    
    /* 计算两个词语的义项相似度。但是这个速度太慢了，需要改进 */
    public void test_simPrimitive(){
        double simP = WordSimilarity.simPrimitive("开心", "争斗");
        System.out.println("雇用 and 争斗 sim : "+ simP);
    }
    
    /*  */
    public void test_simWord(){
        String word1 = "开心";
        String word2 = "争斗";
        System.out.println("词语相似度");
        double sim = WordSimilarity.simWord(word2, word1);
        System.out.println(sim);
    }
    
}
