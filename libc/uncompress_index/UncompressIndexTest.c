#include <assert.h>
#include <malloc.h>

#include "UncompressIndex.h"

void TestCase1()
{
    DocScorePair d1 = {1};
    PostingList p1 = {1, &d1};
    DocScorePair d2 = {2};
    PostingList p2 = {1, &d2};
    PostingList* plList = (PostingList*)malloc(sizeof(PostingList) * 2);
    plList[0] = p1;
    plList[1] = p2;
    DocidSet dSet = Intersect(plList, 2);
    assert(dSet.len == 0);
    free(plList);
}

void TestCase2()
{
    DocScorePair* d1 = (DocScorePair*)malloc(sizeof(DocScorePair) * 2);
    d1[0].docid = 1;
    d1[1].docid = 2;
    PostingList p1 = {2, d1};
    DocScorePair* d2 = (DocScorePair*)malloc(sizeof(DocScorePair) * 2);
    d2[0].docid = 1;
    d2[1].docid = 3;
    PostingList p2 = {2, d2};
    PostingList* plList = (PostingList*)malloc(sizeof(PostingList) * 2);
    plList[0] = p1;
    plList[1] = p2;
    DocidSet dSet = Intersect(plList, 2);
    assert(dSet.len == 1);
    assert(dSet.docids[0] == 1);
    free(d1);
    free(d2);
    free(plList);
}

void TestCase3()
{
    DocScorePair* d1 = (DocScorePair*)malloc(sizeof(DocScorePair) * 5);
    d1[0].docid = 0;
    d1[1].docid = 1;
    d1[2].docid = 2;
    d1[3].docid = 3;
    d1[4].docid = 4;
    PostingList p1 = {5, d1};
    DocScorePair* d2 = (DocScorePair*)malloc(sizeof(DocScorePair) * 5);
    d2[0].docid = 1;
    d2[1].docid = 2;
    d2[2].docid = 3;
    d2[3].docid = 4;
    d2[4].docid = 5;
    PostingList p2 = {5, d2};
    DocScorePair* d3 = (DocScorePair*)malloc(sizeof(DocScorePair) * 5);
    d3[0].docid = 2;
    d3[1].docid = 3;
    d3[2].docid = 4;
    d3[3].docid = 5;
    d3[4].docid = 6;
    PostingList p3 = {5, d3};
    PostingList* plList = (PostingList*)malloc(sizeof(PostingList) * 3);
    plList[0] = p1;
    plList[1] = p2;
    plList[2] = p3;
    DocidSet dSet = Intersect(plList, 3);
    assert(dSet.len == 3);
    assert(dSet.docids[0] == 2);
    assert(dSet.docids[1] == 3);
    assert(dSet.docids[2] == 4);
    free(d1);
    free(d2);
    free(d3);
    free(plList);
}

void TestCase4()
{
    DocScorePair* d1 = (DocScorePair*)malloc(sizeof(DocScorePair) * 5);
    d1[0].docid = 1;
    d1[1].docid = 3;
    d1[2].docid = 5;
    d1[3].docid = 7;
    d1[4].docid = 9;
    PostingList p1 = {5, d1};
    DocScorePair* d2 = (DocScorePair*)malloc(sizeof(DocScorePair) * 5);
    d2[0].docid = 2;
    d2[1].docid = 4;
    d2[2].docid = 6;
    d2[3].docid = 8;
    d2[4].docid = 10;
    PostingList p2 = {5, d2};
    DocScorePair* d3 = (DocScorePair*)malloc(sizeof(DocScorePair) * 5);
    d3[0].docid = 8;
    d3[1].docid = 11;
    d3[2].docid = 14;
    d3[3].docid = 18;
    d3[4].docid = 19;
    PostingList p3 = {5, d3};
    PostingList* plList = (PostingList*)malloc(sizeof(PostingList) * 3);
    plList[0] = p1;
    plList[1] = p2;
    plList[2] = p3;
    DocidSet dSet = Intersect(plList, 3);
    assert(dSet.len == 0);
    free(d1);
    free(d2);
    free(d3);
    free(plList);
}

int main()
{
    TestCase1();
    TestCase2();
    TestCase3();
    TestCase4();
    return 0;
}
