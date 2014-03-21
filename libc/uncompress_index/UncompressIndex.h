#ifndef UNCOMPRESS_INDEX_H
#define UNCOMPRESS_INDEX_H

#include <stdint.h>

typedef struct _DocScorePair
{
    uint32_t docid;
    // uint32_t score;
} DocScorePair;

typedef struct _PostingList
{
    uint32_t len;
    DocScorePair* list;
} PostingList;

typedef struct _PostingListHandler
{
    PostingList postingList;
    uint32_t curPos;
} PostingListHandler;

typedef struct _DocidSet
{
    uint32_t* docids;
    uint32_t len;
} DocidSet;

static uint32_t Next(PostingListHandler*, uint32_t);
DocidSet Intersect(PostingList*, uint32_t);
void PrintDocidSet(DocidSet);

#endif
