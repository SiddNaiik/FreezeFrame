#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/fanotify.h>
#include <limits.h>
#include <string.h>

#define BUF_SIZE 4096

int main() {
    int fd;
    char buffer[BUF_SIZE];
    
    /* Initialize fanotify instance */
    fd = fanotify_init(FAN_CLOEXEC | FAN_CLASS_NOTIF, O_RDONLY);
    
    if (fd < 0) {
        perror("fanotify_init");
        fprintf(stderr, "Note: fanotify requires root privileges (run with sudo)\n");
        exit(EXIT_FAILURE);
    }
    
    
    /* Monitor target directory */
    int ret = fanotify_mark(
        fd,
        FAN_MARK_ADD | FAN_MARK_MOUNT,
        FAN_OPEN | FAN_ACCESS | FAN_CLOSE_WRITE | FAN_CLOSE_NOWRITE,
        AT_FDCWD,
        "/home/sidd/FreezeFrame_Data/FreezeFrame/demo/vault/.ff_honey"
    );
    
    if (ret < 0) {
        perror("fanotify_mark");
        exit(EXIT_FAILURE);
    }
    
    fprintf(stderr, "Monitor target directory\n");

    while (1) {
        ssize_t len = read(fd, buffer, sizeof(buffer));
        if (len < 0) { 
            perror("read"); 
            continue; 
        }

        struct fanotify_event_metadata *metadata;

        for (metadata = (struct fanotify_event_metadata *)buffer;
             FAN_EVENT_OK(metadata, len);
             metadata = FAN_EVENT_NEXT(metadata, len)) {

            if (metadata->vers != FANOTIFY_METADATA_VERSION) {
                fprintf(stderr, "Mismatch metadata version\n");
                exit(1);
            }

            if (metadata->mask & FAN_Q_OVERFLOW) {
                fprintf(stderr, "FAN_Q_OVERFLOW\n");
                continue;
            }

            const char *mask_type = "unknown";
            if (metadata->mask & FAN_OPEN) mask_type = "opened";
            else if (metadata->mask & FAN_ACCESS) mask_type = "accessed";
            else if (metadata->mask & FAN_CLOSE_WRITE) mask_type = "close_write";
            else if (metadata->mask & FAN_CLOSE_NOWRITE) mask_type = "close_nowrite";

            if (metadata->fd >= 0) {
                char fd_path[PATH_MAX];
                char filepath[PATH_MAX] = {0};

                snprintf(fd_path, sizeof(fd_path), "/proc/self/fd/%d", metadata->fd);
                
                ssize_t path_len = readlink(fd_path, filepath, sizeof(filepath) - 1);
                if (path_len != -1) {
                    filepath[path_len] = '\0';
                } else {
                    strcpy(filepath, "unknown");
                }

                printf("%d|%s|%s\n", metadata->pid, mask_type, filepath);
                fflush(stdout);

                close(metadata->fd);
            } else {
                printf("%d|%s|unknown\n", metadata->pid, mask_type);
                fflush(stdout);
            }
        }
    }

    close(fd);
    return 0;
}