/* Runtime path compatibility for this container's PID namespace.
   The release uses /proc/<getpid()>/exe; numeric PIDs are not visible here.
   /proc/self/exe is visible and names the same running process.
   This translates only the current process's executable symlink lookup;
   no proof elaboration or kernel code is replaced and no access is broadened.
*/
#define _GNU_SOURCE
#include <unistd.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    ssize_t (*original)(const char *, char *, size_t) = dlsym(RTLD_NEXT, "readlink");
    char numeric[64];
    snprintf(numeric, sizeof(numeric), "/proc/%ld/exe", (long)getpid());
    return original(strcmp(path, numeric) == 0 ? "/proc/self/exe" : path, buf, bufsiz);
}

