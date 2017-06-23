/*
 * Copyright (C) 2008 SKLSDE(State Key Laboratory of Software Development and Environment, Beihang University)., All Rights Reserved.
 */
package edu.buaa.edu.wordsimilarity;

import java.util.List;

import junit.framework.TestCase;


/**
 * DOCUMENT ME!
 *
 * @author Yingqiang Wu
 * @version 1.0
  */
public class PrimitiveTests extends TestCase {
    /**
     * test the method {@link Primitive#getParents(String)}.
     * @note:本用例测试寻找义原在树中的路径。
     */
    public void test_getParents(){
        String primitive = "军";
        List<Integer> list = Primitive.getParents(primitive);
        for(Integer i : list){
            System.out.println(i);
        }
    }
}
