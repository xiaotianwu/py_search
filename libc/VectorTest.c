#include <assert.h>
#include <stdio.h>

#include "Vector.h"

int main(int argc, char** argv)
{
    Vector vInt = CreateVector_int32();
    for (int32_t i = 0; i < 8192; ++i) {
        PushBack_int32(&vInt, &i);
    }
    for (int32_t i = 0; i < 8192; ++i) {
        int32_t j = *At_int32(&vInt, i);
        assert(j == i);
    }
    return 0;
}
