#!/usr/bin/env python
from bcc import BPF
import ctypes as ct
import minimal_dwarf
from datetime import datetime
from jinja2 import Template



# 1. Actual probe code C , but uses {{ variable }} to be templated using jinja2
bpf_text = """
#include <uapi/linux/ptrace.h> 

int trace_a(struct pt_regs *ctx) {
 int c=0;
 bpf_probe_read(&c, sizeof(c), (void *)PT_REGS_PARM1(ctx)+{{ dupa_s_c_offset }});
 bpf_trace_printk("%s %d\\n", (void *)PT_REGS_PARM1(ctx)+{{ dupa_s_buf_offset }}, c);
 return 0;
}
"""

# jinja2 patching offsets. Actual offset calculation within the struct is done with our "minimal_dwarf" thing which uses pyelftools.
bpf_text_template = Template(bpf_text)

# Load the binary, iterate over "compile units" , find the struct and check where it is in struct.
dupa_s_buf_offset = minimal_dwarf.show_struct_offset('/tmp/minimal/minimal','minimal.c','dupa_s','buf')
print(dupa_s_buf_offset)
dupa_s_c_offset = minimal_dwarf.show_struct_offset('/tmp/minimal/minimal','minimal.c','dupa_s','c')
print(dupa_s_c_offset)

# Actual template rendering using above offsets
final_bpf = bpf_text_template.render(dupa_s_buf_offset=dupa_s_buf_offset,dupa_s_c_offset=dupa_s_c_offset)

# 2. Load the C code, and attach to particular function calls
b = BPF(text=final_bpf)
print(final_bpf)
b.attach_uprobe(name="/tmp/minimal/minimal", sym="Shee3yie", fn_name="trace_a")


while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    print("%s" % msg)
