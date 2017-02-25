#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <stdint.h>

uint8_t command;
uint64_t *exec_guy, *s_exec_guy, *m_exec_guy;

void execute_it() {
    uint32_t local_command;
    uint32_t *sth;
    uint64_t other_var;

    uint64_t buf[8]; //ish

    // rax,QWORD PTR fs:0x28
    // QWORD PTR [rbp-0x28],rax

    if (exec_guy == 0) {
        exec_guy = calloc(0x24, 0x1);
        s_exec_guy = exec_guy;
        m_exec_guy = s_exec_guy + 1;

        *(s_exec_guy+5) = 0x400d36;
        *(s_exec_guy+7) = 0x400d5b;

        local_command = command;
        other_var = m_exec_guy;
        if (local_command == 0)
            other_var = s_exec_guy;

        puts((char*) 0x401660);
        printf((char*) 0x401622);
        sth = read(0, (char*)0x602140, 0x100);

        *(sth + 0x602140) = 0;
    }

}

handle_it() {
    char buf[32]; //ish

    // Is this canary stuff?
    // mov    rax,QWORD PTR fs:0x28
    // mov    QWORD PTR [rbp-0x8],rax

    printf((char *) 0x401698);
    read(0, buf, 4);

    if (buf[0] == '1')
        sign_it();
    else if (buf[0] != '2')
        execute_it();
    else
        puts((char *) 0x4016bf);

    // checking canary now?
    // mov    rcx,QWORD PTR [rbp-0x8]
    // xor    rcx,QWORD PTR fs:0x28
    // je     40144d <handle_it+0x94> # return
    // call   400bd0 <__stack_chk_fail@plt>
}

void ALARMhandler() {
    puts((char *) 0x4016c8);
    exit(1);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    command = 1;
    if (argc == 2)
        command = 0;

    init_key();
    signal(0xe, ALARMhandler);
    alarm(0xa);
    puts((char*) 0x401700);
    while (1)
        handle_it();
}
