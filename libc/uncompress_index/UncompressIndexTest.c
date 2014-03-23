#include <assert.h>
#include <malloc.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#include "UncompressIndex.h"
#include "../Vector.h"

void TestCase1()
{
    DocScorePair d1 = {1};
    PostingList p1 = {1, &d1};
    DocScorePair d2 = {2};
    PostingList p2 = {1, &d2};
    PostingList plList[2] = {p1, p2};
    DocidSet dSet;
    Intersect(plList, 2, &dSet);
    assert(dSet.len == 0);
    ReleaseDocidSet(dSet);
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
    DocidSet dSet;
    Intersect(plList, 2, &dSet);
    assert(dSet.len == 1);
    assert(dSet.docids[0] == 1);
    ReleaseDocidSet(dSet);
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
    DocidSet dSet;
    Intersect(plList, 3, &dSet);
    assert(dSet.len == 3);
    assert(dSet.docids[0] == 2);
    assert(dSet.docids[1] == 3);
    assert(dSet.docids[2] == 4);
    ReleaseDocidSet(dSet);
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
    DocidSet dSet;
    Intersect(plList, 3, &dSet);
    assert(dSet.len == 0);
    ReleaseDocidSet(dSet);
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
    DocidSet dSet;
    Intersect(plList, 4, &dSet);
    assert(dSet.len == 2);
    assert(dSet.docids[0] == 9);
    assert(dSet.docids[1] == 11);
    ReleaseDocidSet(dSet);
}

void TestCase6()
{
    srand(time(NULL));
    PostingList plList[8];
    for (int caseNo = 0; caseNo < 8; ++caseNo) {
        Vector pairs = CreateVector_DocScorePair();
        for (unsigned int i = 0; i < 1000000; ++i) {
            unsigned int prob = rand() % 10;
            if (prob < 4) {
                DocScorePair d = {i};
                PushBack_DocScorePair(&pairs, &d);
            }
        }
        plList[caseNo].list = pairs.array;
        plList[caseNo].len = pairs.len;
        printf("create posting list %d\n", caseNo);
    }
    DocidSet dSet;
    Intersect(plList, 8, &dSet);
    PrintDocidSet(dSet);
    for (int caseNo = 0; caseNo < 8; ++caseNo) {
        free(plList[caseNo].list);
    }
    ReleaseDocidSet(dSet);
}

int main()
{
    TestCase1();
    TestCase2();
    TestCase3();
    TestCase4();
    TestCase5();
    TestCase6();
    return 0;
}
