watches synergys output, then switches keyboard layout / qemu thread priority accordingly

I run with:

```
$ synergys -f --no-tray --debug INFO --name YOURBOX -c /PATH/TO//synergy.conf --address INTERFACE:24800 |  /usr/local/bin/synergymon/capwrap /usr/bin/qemu-system-x86_64 vm_uuid
```

make sure to compile capwrap and setcap on it -- see header
