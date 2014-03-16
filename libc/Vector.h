#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct _VectorInt
{
    uint32_t len;
    uint32_t capacity;
    int32_t* array;
} VectorInt;

VectorInt CreateVectorInt();

bool PushBack(VectorInt*, int32_t);

int32_t PopBack(VectorInt*);

int32_t At(VectorInt*, uint32_t);

bool Empty(VectorInt*);
