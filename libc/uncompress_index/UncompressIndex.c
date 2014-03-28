#include <malloc.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "../Macro.h"
#include "../Vector.h"
#include "UncompressIndex.h"

void PrintDocidSet(DocidSet dSet)
{
    printf("DocidSet, length = %d, elements = ", dSet.len);
    for (uint32_t i = 0; i < dSet.len; ++i) {
        printf("%d ", dSet.docids[i]);
    }
    printf("\n");
}

void Intersect(PostingList* plLists, uint32_t listSize, DocidSet* ret)
{
    PostingListHandler* handlers =
        (PostingListHandler*)malloc(
            sizeof(PostingListHandler) * listSize);
    for (uint32_t i = 0; i < listSize; ++i) {
        handlers[i].postingList = plLists[i];
        handlers[i].curPos = 0;
    }
    uint32_t targetDocid = handlers[0].postingList.list[0].docid;
    uint32_t targetListNo = 0;
    Vector docids = CreateVector_uint32();
    while (true) {
        uint32_t nextTargetDocid = targetDocid;
        uint32_t nextTargetListNo = targetListNo;
        bool found = true;
        for (uint32_t i = 0; i < listSize; ++i) {
            if (i == targetListNo) {
                continue;
            }
            uint32_t docid = Next(&handlers[i], targetDocid);
            if (UNLIKELY(docid == UINT32_MAX)) {
                goto quit;
            }
            if (LIKELY(docid > targetDocid)) {
                found = false;
                if (LIKELY(docid > nextTargetDocid)) {
                    nextTargetDocid = docid;
                    nextTargetListNo = i;
                }
            }
        }
        if (UNLIKELY(found)) {
            PushBack_uint32(&docids, &targetDocid);
            uint32_t docid = Next(&handlers[targetListNo], targetDocid);
            if (docid == UINT32_MAX) {
                goto quit;
            }
            targetDocid = docid;
        }
        else {
            targetDocid = nextTargetDocid;
            targetListNo = nextTargetListNo;
        }
        // printf("targetdocid = %d, targetlistno = %d\n", targetDocid, targetListNo);
    }
quit:
    free(handlers);
    ret->docids = docids.array;
    ret->len = docids.len;
}

static uint32_t Next(PostingListHandler* handler,
                     uint32_t targetDocId)
{
    DocScorePair* postingList = handler->postingList.list;
    uint32_t len = handler->postingList.len;
    while (LIKELY(handler->curPos < len &&
           postingList[handler->curPos].docid < targetDocId)) {
        handler->curPos++;
    }
    if (UNLIKELY(handler->curPos == len)) {
        return UINT32_MAX;
    }
    else {
        return handler->postingList.list[handler->curPos++].docid;
    }
}
