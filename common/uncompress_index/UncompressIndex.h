#include <stdint.h>

typedef struct _DocScorePair
{
    uint32_t docid;
    // uint32_t score;
} DocScorePair;

typedef struct _UncompressIndex
{
    uint32_t len;
    DocScorePair* postingList;
} UncompressIndex;

typedef struct _UncompressIndexHandler
{
    UncompressIndex index;
    uint32_t curPos;
} UncompressIndexHandler;

typedef struct _DocidSet
{
    uint32_t* set;
    uint32_t len;
} DocidSet;

static uint32_t MoveToNext(UncompressIndexHandler, uint32_t);
DocidSet Intersect(UncompressIndex*, uint32_t);
