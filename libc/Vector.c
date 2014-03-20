#include <malloc.h>
#include <string.h>

#include "Vector.h"

Vector _CreateVector(size_t elemSize)
{
    Vector v = {
        .len = 0,
        .capacity = 128,
        .array = (void*)malloc(elemSize * 128),
    };
    return v;
}

bool _PushBack(Vector* v, size_t elemSize, void* newElem)
{
    memcpy(v->array + (v->len * elemSize), newElem, elemSize);
    v->len++;
    if (v->len >= v->capacity) {
        // growth factor is approximately 1.5
        v->capacity = (v->capacity * 3) >> 1;
        void* reallocArea =
            (void*)realloc(v->array, v->capacity * elemSize);
        if (reallocArea == NULL) {
            return false;
        }
        else {
            v->array = reallocArea;
        }
    }
    return true;
}

void _PopBack(Vector* v, size_t elemSize)
{
    if (v->len == 0) {
        return;
    }
    if (--v->len == 0) {
        return;
    }
    uint32_t shrinkCapacity = (v->capacity >> 3) + 1;
    if (v->len < shrinkCapacity - 1) {
        v->capacity = shrinkCapacity;
        void* reallocArea =
            (void*)realloc(v->array, v->capacity * elemSize);
        v->array = reallocArea;
    }
}

void* _At(Vector* v, size_t elemSize, uint32_t index)
{
    if (index >= v->len) {
        return NULL;
    }
    return v->array + index * elemSize;
}

void ReleaseVector(Vector* v)
{
    free(v->array);
    v->array = NULL;
    v->len = 0;
    v->capacity = 0;
}

bool Empty(Vector* v)
{
    return v->len == 0;
}

