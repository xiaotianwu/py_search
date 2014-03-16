#include <malloc.h>

#include "Vector.h"

VectorInt CreateVectorInt()
{
    VectorInt vInt = {
        .len = 0,
        .capacity = 128,
        .array = (int32_t*)malloc(sizeof(int32_t) * 128),
    };
    return vInt;
}

bool PushBack(VectorInt* vInt, int32_t newElem)
{
    vInt->array[(vInt->len)++] = newElem;
    if (vInt->len >= vInt->capacity) {
        vInt->capacity = (vInt->capacity * 3) >> 1;
        int32_t* newArea =
            (int32_t*)realloc(vInt->array, vInt->capacity);
        if (newArea == NULL) {
            return false;
        }
        else {
            vInt->array = newArea;
        }
    }
    return true;
}

int32_t PopBack(VectorInt* vInt)
{
    return vInt->array[(vInt->len)--];
}

int32_t At(VectorInt* vInt, uint32_t index)
{
    return vInt->array[index];
}

bool Empty(VectorInt* vInt)
{
    return vInt->len == 0;
}
