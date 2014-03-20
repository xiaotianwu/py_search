#ifndef MACRO_H
#define MACRO_H

#undef LIKELY
#undef UNLIKELY

#if defined(__GNUC__) && (__GNUC__ == 2 && __GNUC_MINOR__ < 96 || __GNUC__ > 2)
#define LIKELY(x) (__builtin_expect((x), 1))
#define UNLIKELY(x) (__builtin_expect((x), 0))
#else
#define LIKELY(x) (x)
#define UNLIKELY(x) (x)
#endif

#endif
