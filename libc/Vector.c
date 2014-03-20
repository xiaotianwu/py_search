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
        void* newArea =
            (void*)realloc(v->array, v->capacity * elemSize);
        if (newArea == NULL) {
            return false;
        }
        else {
            v->array = newArea;
        }
    }
    return true;
}

void _PopBack(Vector* v, size_t elemSize)
{
    if (--v->len < v->capacity / 8) {
        v->capacity >>= 3;
        void* newArea =
            (void*)realloc(v->array, v->capacity * elemSize);
    }
}

void* _At(Vector* v, size_t elemSize, uint32_t index)
{
    if (index >= v->len) {
        return NULL;
    }
    return v->array + index * elemSize;
}

bool Empty(Vector* v)
{
    return v->len == 0;
}
