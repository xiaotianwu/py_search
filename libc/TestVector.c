#include <stdio.h>

#include "Vector.h"

int main(int argc, char** argv)
{
    VectorInt vInt = CreateVectorInt();
    for (int32_t i = 0; i < 8192; ++i) {
        PushBack(&vInt, i);
    }
    for (int32_t i = 0; i < 1024; ++i) {
        printf("%d ", PopBack(&vInt));
    }
    for (int32_t i = 0; i < vInt.len; ++i) {
        printf("%d ", At(&vInt, i));
    }
    return 0;
}
