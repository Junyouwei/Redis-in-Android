#ifndef A059A5B6_C96E_47C1_84A5_F8D7BFE7E3B8
#define A059A5B6_C96E_47C1_84A5_F8D7BFE7E3B8


#include "pcre2.h"
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

// Custom glob structure
typedef struct {
    char** gl_pathv;
    size_t gl_pathc;
} glob_t;

void initGlob(glob_t* pglob);

void addPathToGlob(glob_t* pglob, const char* path);

void clearGlob(glob_t* pglob);

int glob(const char* pattern, int flags, void* errfunc, glob_t* pglob);

void globfree(glob_t* pglob);

int my_mkostemp(char *template, int flags);

#endif /* A059A5B6_C96E_47C1_84A5_F8D7BFE7E3B8 */
