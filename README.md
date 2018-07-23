PoC of bcc uprobe that parses DWARF via pyelftools.

https://github.com/iovisor/bcc/issues/1803


```
apt-get install python-pyelftools python-jinja2
cd /tmp/
git clone x minimal
gcc -g3 -o minimal minimal.c
```


```
marek@node:/tmp/minimal$ ./minimal
0
1
2
3
4
5
6
```


```
marek@node:/tmp/minimal$ sudo python minimal_probe.py
Searching for compile unit minimal.c in file /tmp/minimal/minimal struct dupa_s variable buf
8
Searching for compile unit minimal.c in file /tmp/minimal/minimal struct dupa_s variable c
100

#include <uapi/linux/ptrace.h>

int trace_a(struct pt_regs *ctx) {
 int c=0;
  bpf_probe_read(&c, sizeof(c), (void *)PT_REGS_PARM1(ctx)+100);
   bpf_trace_printk("%s %d\n", (void *)PT_REGS_PARM1(ctx)+8, c);
    return 0;
    }
    TEST nr :  0
    TEST nr :  1
    TEST nr :  2
    TEST nr :  3
    TEST nr :  4
    TEST nr :  5
    TEST nr :  6
```
