#include <assert.h>
#include <malloc.h>

#include "UncompressIndex.h"
#include "../Vector.h"

void TestCase1()
{
    DocScorePair d1 = {1};
    PostingList p1 = {1, &d1};
    DocScorePair d2 = {2};
    PostingList p2 = {1, &d2};
    PostingList plList[2] = {p1, p2};
    DocidSet dSet = Intersect(plList, 2);
    assert(dSet.len == 0);
    free(dSet.docids);
}

void TestCase2()
{
    DocScorePair d1[2];
    d1[0].docid = 1;
    d1[1].docid = 2;
    PostingList p1 = {2, d1};
    DocScorePair d2[2];
    d2[0].docid = 1;
    d2[1].docid = 3;
    PostingList p2 = {2, d2};
    PostingList plList[2] = {p1, p2};
    DocidSet dSet = Intersect(plList, 2);
    assert(dSet.len == 1);
    assert(dSet.docids[0] == 1);
    free(dSet.docids);
}

void TestCase3()
{
    DocScorePair d1[5];
    d1[0].docid = 0;
    d1[1].docid = 1;
    d1[2].docid = 2;
    d1[3].docid = 3;
    d1[4].docid = 4;
    PostingList p1 = {5, d1};
    DocScorePair d2[5];
    d2[0].docid = 1;
    d2[1].docid = 2;
    d2[2].docid = 3;
    d2[3].docid = 4;
    d2[4].docid = 5;
    PostingList p2 = {5, d2};
    DocScorePair d3[5];
    d3[0].docid = 2;
    d3[1].docid = 3;
    d3[2].docid = 4;
    d3[3].docid = 5;
    d3[4].docid = 6;
    PostingList p3 = {5, d3};
    PostingList plList[3] = {p1, p2, p3};
    DocidSet dSet = Intersect(plList, 3);
    assert(dSet.len == 3);
    assert(dSet.docids[0] == 2);
    assert(dSet.docids[1] == 3);
    assert(dSet.docids[2] == 4);
    free(dSet.docids);
}

void TestCase4()
{
    DocScorePair d1[5];
    d1[0].docid = 1;
    d1[1].docid = 3;
    d1[2].docid = 5;
    d1[3].docid = 7;
    d1[4].docid = 9;
    PostingList p1 = {5, d1};
    DocScorePair d2[5];
    d2[0].docid = 2;
    d2[1].docid = 4;
    d2[2].docid = 6;
    d2[3].docid = 8;
    d2[4].docid = 10;
    PostingList p2 = {5, d2};
    DocScorePair d3[5];
    d3[0].docid = 8;
    d3[1].docid = 11;
    d3[2].docid = 14;
    d3[3].docid = 18;
    d3[4].docid = 19;
    PostingList p3 = {5, d3};
    PostingList plList[3] = {p1, p2, p3};
    DocidSet dSet = Intersect(plList, 3);
    assert(dSet.len == 0);
    free(dSet.docids);
}

void TestCase5()
{
    DocScorePair d1[6];
    d1[0].docid = 1;
    d1[1].docid = 3;
    d1[2].docid = 5;
    d1[3].docid = 7;
    d1[4].docid = 9;
    d1[5].docid = 11;
    PostingList p1 = {6, d1};
    DocScorePair d2[4];
    d2[0].docid = 2;
    d2[1].docid = 7;
    d2[2].docid = 9;
    d2[3].docid = 11;
    PostingList p2 = {4, d2};
    DocScorePair d3[8];
    d3[0].docid = 0;
    d3[1].docid = 1;
    d3[2].docid = 2;
    d3[3].docid = 3;
    d3[4].docid = 7;
    d3[5].docid = 9;
    d3[6].docid = 11;
    d3[7].docid = 12;
    PostingList p3 = {8, d3};
    DocScorePair d4[5];
    d4[0].docid = 0;
    d4[1].docid = 2;
    d4[2].docid = 3;
    d4[3].docid = 9;
    d4[4].docid = 11;
    PostingList p4 = {5, d4};
    PostingList plList[4] = {p1, p2, p3, p4};
    DocidSet dSet = Intersect(plList, 4);
    assert(dSet.len == 2);
    assert(dSet.docids[0] == 9);
    assert(dSet.docids[1] == 11);
    free(dSet.docids);
}

int main()
{
    TestCase1();
    TestCase2();
    TestCase3();
    TestCase4();
    TestCase5();
    return 0;
}
