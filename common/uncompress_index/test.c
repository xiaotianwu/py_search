#include "test.h"

#include <stdint.h>
#include <malloc.h>

struct TestStruct
{
    uint32_t* data;
    uint32_t len;
};

void TestFunc(struct TestStruct* testStruct)
{
    testStruct->len = 10;
    testStruct->data = (uint32_t*)malloc(sizeof(uint32_t) * testStruct->len);
    for (uint32_t i = 0; i < testStruct->len; ++i) {
        testStruct->data[i] = i;
    }
}
