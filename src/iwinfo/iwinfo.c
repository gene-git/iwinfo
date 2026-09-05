/*
 * SPDX-License-Identifier: MIT
 * SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
 *
 * Wrapper to run iwinfo-app.py with the required network capabilities.
 *
 * Capabilities needed:
 *  cap_net_raw,cap_net_admin
 *
 * Install as: /usr/bin/iwinfo
 * Execs /usr/lib/iwinfo/iwinfo-app
 *
 * Uses libcap-ng.
 *
 * Once installed in /usr/bin/iwinfo then:
 * Set effective, inherited and permitted capabilities to the compiled binary
 * 
 *  sudo setcap cap_setpcap,cap_net_raw,cap_net_admin+eip ambient
 * 
 */
#include <cap-ng.h>
#include <errno.h>
#include <grp.h>
#include <linux/capability.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/types.h>
#include <unistd.h>


/*
 * We want the process that gets execv() to get these caps.
 */
static bool set_ambient_caps(size_t num_caps, const unsigned int *caps) {

    if (!caps || num_caps == 0) {
        return true;
    }

    /*
     * load (kernel) state into libcap-ng
     */
    if (capng_get_caps_process() != 0) {
        printf("Warning : failed to get capabilities\n");
        return false;
    }

    /*
     * Add the caps to the Inheritable set
     * - check current process has right to the cap
     */
    for (size_t i = 0; i < num_caps; i++) {
        if (capng_have_capability(CAPNG_PERMITTED, caps[i]) == 0) {
            printf("Error: capability %u is not in the Permitted set. Cannot make ambient.\n", caps[i]);
            return false;
        }

        if (capng_update(CAPNG_ADD, CAPNG_INHERITABLE, caps[i]) != 0) {
            printf("Error: failed to add cap %u to inheritable set\n", caps[i]);
            return false;
        }
    }

    /*
     * Apply the Inheritable set to the kernel
     */
    if (capng_apply(CAPNG_SELECT_CAPS) != 0) {
        printf("Error: failed to apply inheritable capabilities\n");
        return false;
    }

    /*
     * Raise each cap one at a time 
     * prctl only takes one cap.
     */
    for (size_t i = 0; i < num_caps; i++) {
        if (prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_RAISE, caps[i], 0, 0) != 0) {
            printf("Error: unable to set ambient cap %u: %s\n", caps[i], strerror(errno));
            return false;
        }
    }

    return true;
}


/*
 * Root and members of wheel only
 * We dont assume root is in wheel even though that is typical
 */
static bool permitted_user() {
    bool permitted = false;
    bool is_root = false;
    bool is_wheel = false;
    const char *wheel = "wheel";
    struct group *grp = nullptr;
    gid_t gid_wheel = {} ;

    /*
     * Check for root or wheel
     */
    is_root = (geteuid() == 0) ;

    grp = getgrnam(wheel);
    if (grp) {
        gid_wheel = grp->gr_gid ;
        if (group_member(gid_wheel) != 0) {
            is_wheel = true ;
        }
    }

    if (is_root || is_wheel) {
        permitted = true ;
    }

    return permitted;
}


/*
 * Only set caps for root or wheel
 */
int main([[maybe_unused]] int argc, char ** argv) {
    unsigned int caps[] = { CAP_NET_RAW, CAP_NET_ADMIN};
    size_t num_caps = sizeof(caps) / sizeof(caps[0]);
    char *prog = "/usr/lib/iwinfo/iwinfo-app";

    if (permitted_user()) {
        if (!set_ambient_caps(num_caps, caps)) {
            printf("Failed to set ambient caps\n");
        }
    }

    if (execv(prog, argv)) {
        printf("Unable to run %s : %s\n", prog, strerror(errno));
    }
    return 0;
}
