/*
 * Set ambient capabilities for cap_net_raw,cap_net_admin
 * Install as: /usr/bin/iwinfo
 *
 * Will run /usr/lib/iwinfo/iwinfo.py
 *
 * compile using:
 *    gcc -Wl,--no-as-needed -lcap-ng -o iwinfo ambient_cap_net.c
 *
 * Once installed in /usr/bin/iwinfo then:
 * Set effective, inherited and permitted capabilities to the compiled binary
 * 
 *  sudo setcap cap_setpcap,cap_net_raw,cap_net_admin+eip ambient
 * 
 * SPDX-License-Identifier: MIT
 * SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
 */

#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <grp.h>
#include <sys/prctl.h>
#include <linux/capability.h>
#include <cap-ng.h>

// why is this not declared in unistd
extern int group_member(gid_t gid);

static void set_ambient_cap(int cap) {

    if (capng_get_caps_process() != 0) {
        printf("Warning : failed to get capabilities\n");
        return ;
    }

    if (capng_update(CAPNG_ADD, CAPNG_INHERITABLE, cap) != 0) {
        printf("Warning : failed to add inheritable capability\n");
    }

    if (capng_apply(CAPNG_SELECT_CAPS) != 0) {
        printf("Warning : failed to apply capabilities\n");
    }

    // Note the two 0s at the end. Kernel checks for these
    if (prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_RAISE, cap, 0, 0)) {
        printf("Warning cap: unable to set %d : %s\n", cap, strerror(errno));
    }
}


bool user_permitted() {
    /*
     * Root and members of wheel only
     * We dont assume root is in wheel even though that is normal
     */
    bool permitted = false;
    bool is_root = false, is_wheel = false;
    const char *wheel = "wheel";
    struct group *grp = NULL;
    gid_t gid_wheel = -1 ;

    // root?
    is_root = (geteuid() == 0) ;

    // wheel?
    grp = getgrnam(wheel);
    gid_wheel = grp->gr_gid ;
    if (group_member(gid_wheel) != 0) {
        is_wheel = true ;
    }

    if (is_root || is_wheel) {
        permitted = true ;
    }
    // printf("root: %d wheel %d -> %d\n", is_root, is_wheel, permitted);
    return(permitted);
}

int main(int argc, char ** argv) {
    int i ;
    int caplist[] = { CAP_NET_RAW, CAP_NET_ADMIN, -1 };
    char *prog = "/usr/lib/iwinfo/iwinfo.py";
    bool permitted = false;

    // limit this to root and wheel group
    permitted = user_permitted();

    if (permitted) {
        for (i = 0; caplist[i] != -1; i++) {
            set_ambient_cap(caplist[i]);
        }
    }

    if (execv(prog, argv))
        printf("Unable to run %s : %s\n", prog, strerror(errno));
    return 0;
}
