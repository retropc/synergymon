/* needs libcap-dev
gcc -o capwrap capwrap.c -DSYNERGYMON_PATH=\"/path/to/synergymon/synergymon\" -lcap
sudo setcap 'cap_sys_nice=eip' capwrap
*/
#include <sys/capability.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/prctl.h>

int main(int argc, char *argv[]) {
  cap_t caps = cap_get_proc();
  cap_value_t newcaps[1] = { CAP_SYS_NICE, };
  cap_set_flag(caps, CAP_INHERITABLE, 1, newcaps, CAP_SET);
  cap_set_proc(caps);

  if (prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_RAISE, CAP_SYS_NICE, 0, 0)) {
    perror("prctl");
    return 1;
  }

  execv(SYNERGYMON_PATH, argv);
  perror("exec");
  return 2;
}

