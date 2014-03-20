#include <assert.h>
#include <stdio.h>

#include "Vector.h"

int main(int argc, char** argv)
{
    int32_t caseNum = 10;
    while (--caseNum > 0) {
        Vector vInt = CreateVector_int32();
        for (int32_t i = 0; i < 1234567; ++i) {
            PushBack_int32(&vInt, &i);
        }
        for (int32_t i = 0; i < 1234567; ++i) {
            int32_t j = *At_int32(&vInt, i);
            assert(j == i);
        }
        for (int32_t i = 0; i < 1234567; ++i) {
            PopBack_int32(&vInt);
        }
        ReleaseVector(&vInt);

        vInt = CreateVector_uint32();
        for (uint32_t i = 0; i < 1234567; ++i) {
            PushBack_uint32(&vInt, &i);
        }
        for (uint32_t i = 0; i < 1234567; ++i) {
            uint32_t j = *At_uint32(&vInt, i);
            assert(j == i);
        }
        for (uint32_t i = 0; i < 1234567; ++i) {
            PopBack_uint32(&vInt);
        }
        ReleaseVector(&vInt);
    }
    return 0;
}
