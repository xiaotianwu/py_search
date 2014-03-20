#ifndef VECTOR_H 
#define VECTOR_H

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define CreateVector_int32() _CreateVector(sizeof(int32_t))
#define PushBack_int32(v, ptr) _PushBack(v, sizeof(int32_t), ptr)
#define PopBack_int32(v) _PopBack(v, sizeof(int32_t))
#define At_int32(v, i) ((int32_t*)_At(v, sizeof(int32_t), i))

#define CreateVector_uint32() _CreateVector(sizeof(uint32_t))
#define PushBack_uint32(v, ptr) _PushBack(v, sizeof(uint32_t), ptr)
#define PopBack_uint32(v) _PopBack(v, sizeof(uint32_t))
#define At_uint32(v, i) ((uint32_t*)_At(v, sizeof(uint32_t), i))

typedef struct _Vector
{
    uint32_t len;
    uint32_t capacity;
    void* array;
} Vector;

Vector _CreateVector(size_t);

bool _PushBack(Vector*, size_t, void*);

void _PopBack(Vector*, size_t);

void* _At(Vector*, size_t, uint32_t);

void ReleaseVector(Vector*);

bool Empty(Vector*);

#endif
