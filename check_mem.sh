watch -d -n1 "sudo nice ./ps_mem.py | tail -n $((${LINES:-16}-2))"
