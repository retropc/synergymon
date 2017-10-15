import os

def read_full(fn):
  with open(fn, "rb") as f:
    return f.read()

def get_tids(pid):
  try:
    for tid in os.listdir("/proc/%d/task/" % pid):
      try:
        yield int(tid)
      except ValueError:
        pass
  except OSError:
    pass
  except IOError:
    pass

def start_time(pid):
  try:
    return int(read_full("/proc/%d/stat" % pid).split(b" ")[21])
  except (ValueError, IOError, OSError):
    return None

def find_pids():
  for pid in os.listdir("/proc/"):
    try:
      pid = int(pid)
    except ValueError:
      continue
    yield pid

def find_qemu_vm(binary, uuid):
  binary_h = bytes("%s\0" % binary, "utf8")
  uuid_h = bytes("\0-uuid\0%s\0" % uuid, "utf8")
  for pid in find_pids():
    try:
      cmdline = read_full("/proc/%d/cmdline" % pid)
    except (IOError, OSError):
      continue
    if cmdline.startswith(binary_h) and uuid_h in cmdline:
      return pid

def get_thread_name(pid, tid):
  try:
    return read_full("/proc/%d/task/%d/comm" % (pid, tid))
  except (IOError, OSError):
    return None

def get_cpu_tids(pid):
  for tid in get_tids(pid):
    name = get_thread_name(pid, tid)
    if name is None:
      continue
    if name.startswith(b"CPU ") and name.endswith(b"/KVM\n"):
      yield tid

def same_pid(old_pid, old_start_time):
  return old_pid is not None and start_time(old_pid) == old_start_time

RT_SP = os.sched_param(90)
OT_SP = os.sched_param(0)
chrt_rt = lambda pid: os.sched_setscheduler(pid, os.SCHED_RR, RT_SP)
chrt_ot = lambda pid: os.sched_setscheduler(pid, os.SCHED_OTHER, OT_SP)

def set_rt(tids, rt):
  chrt = chrt_rt if rt else chrt_ot
  for tid in tids:
    chrt(tid)

if __name__ == "__main__":
  main()
