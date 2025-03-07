#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

char volatile format[] = "Hi! Welcome to TRX's birdshop!\nWe've recently got stolen most of our birds... \nBut we've got some secured in our super secure enclave:/bin/sh";

void usefull(){
    asm volatile ("pop %rax");
    asm volatile ("pop %rdx");
    asm volatile ("ret");
    asm volatile ("pop %rdi");
    asm volatile ("pop %r13");
    asm volatile ("pop %rcx");
    asm volatile ("pop %rax");
    asm volatile ("ret");
    asm volatile ("pop %rsi");
    asm volatile ("pop %r14");
    asm volatile ("pop %r15");
    asm volatile ("ret");
    asm volatile("syscall");
}

void canary(){
    char input[0x20];
    printf("What color would you like your canary to be?\n");
    printf(">");
    read(0,input,41);
    printf("Ok so we got some %s colored canary for you, that will be 5.99$ wanna proceed?\n",input);
    printf("[yes/no]>");
    read(0,input,41);
    if(!strcmp(input,"yes")){
        printf("Ok, here is your canary, have a nice day!\n");
    }else{
        printf("Ok, come back again!\n");
    }
    return;
}

void parrot(){
    char input[0x20];
    printf("We only have orange parrots, that will be 13.99$ wanna proceed?\n");
    printf("[yes/no]>");
    read(0,input,0x100);
    if(!strcmp(input,"yes")){
        printf("Ok, here is your parrot, have a nice day!\n");
    }else{
        printf("Ok, come back again!\n");
    }
    return;
}

void penguin(){
    printf("We don't sell penguins!\nWhy the hell would you want a penguin?\nShall we call the cops?!\n");
    exit(0);
}

void raven(){
    char input[0x20];
    printf("We only have black ravens, that will be 59.99$ wanna proceed?\n");
    printf("[yes/no]>");
    read(0,input,0x10);
    if(!strcmp(input,"yes")){
        printf("Ok, here is your raven, have a nice day!\n");
    }else{
        printf("Ok, come back again!\n");
    }
    return;
}

void chicken(){
    char input[0x20];
    printf("We only have female chickens, that will be 2.99$ wanna proceed?\n");
    printf("[yes/no]>");
    read(0,input,0x10);
    if(!strcmp(input,"yes")){
        printf("Ok, here is your chicken, have a nice day!\n");
    }else{
        printf("Ok, come back again!\n");
    }
    return;
}

void birdShop(){
    int choice;
    printf("%s",format);
    while(1){
        printf("What do you want to do?\n");
        printf("1. Buy a canary\n");
        printf("2. Buy a parrot\n");
        printf("3. Buy a penguin\n");
        printf("4. Buy a raven\n");
        printf("5. Buy a chicken\n");
        printf("6. Exit\n");
        printf(">");
        scanf("%d",&choice);
        switch(choice){
            case 1:
                canary();
                break;
            case 2:
                parrot();
                break;
            case 3:
                penguin();
                break;
            case 4:
                raven();
                break;
            case 5:
                chicken();
                break;
            case 6:
                return;
                break;
            default:
                printf("Invalid choice\n");
                break;
        }
    }
}

int main(){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    birdShop();
    return 0;
}
