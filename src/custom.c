#ifndef BF69CD51_7DF2_413D_81C3_A4EDD94C6583
#define BF69CD51_7DF2_413D_81C3_A4EDD94C6583

#include "pcre2.h"
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "custom.h"


void initglob(glob_t* pglob) {
    pglob->gl_pathv = NULL;
    pglob->gl_pathc = 0;
}

void addPathToGlob(glob_t* pglob, const char* path) {
    pglob->gl_pathv = realloc(pglob->gl_pathv, (pglob->gl_pathc + 1) * sizeof(char*));
    pglob->gl_pathv[pglob->gl_pathc] = strdup(path);
    pglob->gl_pathc++;
}

void clearGlob(glob_t* pglob) {
    for (size_t i = 0; i < pglob->gl_pathc; i++) {
        free(pglob->gl_pathv[i]);
    }
    free(pglob->gl_pathv);
    pglob->gl_pathv = NULL;
    pglob->gl_pathc = 0;
}

int glob(const char* pattern, int flags, void* errfunc, glob_t* pglob) {
    clearGlob(pglob);

    const char* directory = ".";
    char* regexPattern = strdup(pattern);

    // Convert glob pattern to PCRE2 pattern
    char* pos;
    while ((pos = strstr(regexPattern, "*")) != NULL) {
        *pos = '\0';
        strcat(regexPattern, ".*");
        strcat(regexPattern, pos + 1);
    }
    while ((pos = strstr(regexPattern, "?")) != NULL) {
        *pos = '\0';
        strcat(regexPattern, ".?");
        strcat(regexPattern, pos + 1);
    }

    int errorcode;
    PCRE2_SIZE erroroffset;
    pcre2_code* re = pcre2_compile((PCRE2_SPTR)regexPattern, PCRE2_ZERO_TERMINATED, 0, &errorcode, &erroroffset, NULL);
    free(regexPattern);
    if (!re) {
        printf("PCRE2 compilation failed at offset %zu: error %d\n", erroroffset, errorcode);
        return -1;
    }

    DIR* dir = opendir(directory);
    if (!dir) {
        printf("Failed to open directory: %s\n", directory);
        pcre2_code_free(re);
        return -1;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        pcre2_match_data* match_data = pcre2_match_data_create_from_pattern(re, NULL);
        int rc = pcre2_match(re, (PCRE2_SPTR)entry->d_name, strlen(entry->d_name), 0, 0, match_data, NULL);
        if (rc >= 0) {
            addPathToGlob(pglob, entry->d_name);
        }
        pcre2_match_data_free(match_data);
    }
    closedir(dir);
    pcre2_code_free(re);

    return 0;
}

void globfree(glob_t* pglob) {
    clearGlob(pglob);
}

int my_mkostemp(char *template, int flags) {
    int fd = mkstemp(template);
    if (fd == -1) {
        return -1;
    }

    // Set the specified flags
    int fd_flags = fcntl(fd, F_GETFD);
    if (fd_flags == -1) {
        close(fd);
        return -1;
    }

    if (fcntl(fd, F_SETFD, fd_flags | flags) == -1) {
        close(fd);
        return -1;
    }

    return fd;
}



#endif /* BF69CD51_7DF2_413D_81C3_A4EDD94C6583 */
