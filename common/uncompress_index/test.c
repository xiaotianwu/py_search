#include "test.h"

#include <malloc.h>

struct TestStruct
{
    int* data;
    int len;
};

void TestFunc(struct TestStruct* testStruct)
{
    testStruct->len = 10;
    testStruct->data = (int*)malloc(sizeof(int) * testStruct->len);
    for (int i = 0; i < testStruct->len; ++i) {
        testStruct->data[i] = i;
    }
}
