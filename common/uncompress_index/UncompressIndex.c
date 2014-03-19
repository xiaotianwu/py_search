#include <stdio.h>

#include "UncompressIndex.h"

struct DocScorePair
{
    uint32_t docid;
    uint32_t score;
};

struct UncompressIndex
{
    uint32_t postingListLen;
    struct DocScorePair* postingList;
};

struct UncompressIndexHandler
{
    struct UncompressIndex* index;
    uint32_t curPos;
};

void Intersect(struct UncompressIndex* indexLists, uint32_t listSize)
{
    struct UncompressIndexHandler* handlers = (struct UncompressIndexHandler*)malloc(sizeof(struct UncompressIndexHandler) * listSize);
    for (int32_t i = 0; i < listSize; ++i) {
        handlers[i].index = indexLists[i];
        handlers[i].curPos = 0;
    }
    uint32_t targetDocid = 0;
    while (true) {
        uint32_t nextTargetDocid = 0;
        bool found = true;
        for (int32_t i = 0; i < listSize; ++i) {
            uint32_t docid = MoveToNext(handler, targetDocId);
            if (docid == -1) {
                goto quit;
            }
            if (docid > targetDocid) {
                found = false;
            }
            if (docid > nextTargetDocid) {
                nextTargetDocid = docid;
            }
        }
        if (found == true) {
            // add to result
        }
        targetDocid = nextTargetDocid;
    }
quit:
    // do gc here
}

void MoveToNext(struct UncompressIndexHandler handler, uint32_t targetDocId)
{
    struct DocScorePair* postingList = handler.index->postingList;
    int32_t maxLen = handler.index->postingList;
    while (handler.curPos <= maxLen && postingList[curPos].docid < targetDocId) {
        handler.curPos++;
    }
    if (handler.curPos == maxLen) {
        return -1;
    }
    else {
        return handler.index->postingList[handler.curPos].docid;
    }
}
