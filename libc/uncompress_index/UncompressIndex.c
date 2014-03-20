#include <malloc.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "UncompressIndex.h"

DocidSet Intersect(UncompressIndex* indexLists, uint32_t listSize)
{
    UncompressIndexHandler* handlers =
        (UncompressIndexHandler*)malloc(
            sizeof(UncompressIndexHandler) * listSize);
    for (uint32_t i = 0; i < listSize; ++i) {
        handlers[i].index = indexLists[i];
        handlers[i].curPos = 0;
    }
    uint32_t targetDocid = 0;
    DocidSet docidSet;
    while (true) {
        uint32_t nextTargetDocid = 0;
        bool found = true;
        for (uint32_t i = 0; i < listSize; ++i) {
            uint32_t docid = MoveToNext(handlers[i], targetDocid);
            if (docid == UINT32_MAX) {
                goto quit;
            }
            if (docid > targetDocid) {
                found = false;
            }
            if (docid > nextTargetDocid) {
                nextTargetDocid = docid;
            }
        }
        if (found) {
            // PushBack(docidSet.set, targetDocid)
            // docidSet.len++;
        }
        targetDocid = nextTargetDocid;
    }
quit:
    return docidSet;
}

static uint32_t MoveToNext(UncompressIndexHandler handler,
                           uint32_t targetDocId)
{
    DocScorePair* postingList = handler.index.postingList;
    int32_t maxLen = handler.index.len;
    while (handler.curPos <= maxLen &&
           postingList[handler.curPos].docid < targetDocId) {
        handler.curPos++;
    }
    if (handler.curPos == maxLen) {
        return UINT32_MAX;
    }
    else {
        return handler.index.postingList[handler.curPos].docid;
    }
}
