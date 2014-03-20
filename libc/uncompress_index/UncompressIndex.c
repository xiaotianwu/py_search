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
        handlers[i].postingList = indexLists[i];
        handlers[i].curPos = 0;
    }
    uint32_t targetDocid = 0;
    Vector docids = CreateVector_uint32();
    while (true) {
        uint32_t nextTargetDocid = 0;
        bool found = true;
        for (uint32_t i = 0; i < listSize; ++i) {
            uint32_t docid = Next(handlers[i], targetDocid);
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
            PushBack_uint32(docids, targetDocid)
        }
        targetDocid = nextTargetDocid;
    }
quit:
    DocidSet docidSet = {
        .set = docids.array,
        .len = docis.len,
    };
    return docidSet;
}

static uint32_t Next(PostingListHandler* handler,
                     uint32_t targetDocId)
{
    DocScorePair* postingList = handler.postingList.list;
    uint32_t len = handler.postingList.len;
    while (handler.curPos < len &&
           postingList[handler.curPos].docid < targetDocId) {
        handler.curPos++;
    }
    if (handler.curPos == len) {
        return UINT32_MAX;
    }
    else {
        return handler.postingList.list[handler.curPos].docid;
    }
}
