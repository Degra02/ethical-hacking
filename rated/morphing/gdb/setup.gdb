# start
# info proc mappings
# readelf -S ./bin | grep mysec   # get offset
# watch *(int*)$mysec
# executed each time mysec section is altered
# commands
#     set pagination off
#     set logging file disass.txt
#     set logging overwrite on
#     set logging enabled on
#     x/300i $mysec
#     set logging enabled off
# end

file ./patched-bin

set $base = 0x0000555555554000
set $mysec = $base + 0x12a8
set $decrypt = 0x555555555189

# analyze the disassembly and get the next character
catch signal SIGSEGV SIGILL
commands
    set logging file last-char.txt
    set logging overwrite on
    set logging enabled on
    x/300i $mysec
    set logging enabled off
end
