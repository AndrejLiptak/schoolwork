#include "cpu.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int nop(struct cpu *cpu);
static int halt(struct cpu *cpu);
static int add(struct cpu *cpu);
static int sub(struct cpu *cpu);
static int mul(struct cpu *cpu);
static int divide(struct cpu *cpu);
static int inc(struct cpu *cpu);
static int dec(struct cpu *cpu);
static int loop(struct cpu *cpu);
static int movr(struct cpu *cpu);
static int load(struct cpu *cpu);
static int store(struct cpu *cpu);
static int in(struct cpu *cpu);
static int get(struct cpu *cpu);
static int out(struct cpu *cpu);
static int put(struct cpu *cpu);
static int swap(struct cpu *cpu);
static int push(struct cpu *cpu);
static int pop(struct cpu *cpu);
#ifdef BONUS_JMP
static int cmp(struct cpu *cpu);
static int jmp(struct cpu *cpu);
static int jz(struct cpu *cpu);
static int jnz(struct cpu *cpu);
static int jgt(struct cpu *cpu);
#endif // BONUS_JMP
#ifdef BONUS_CALL
static int call(struct cpu *cpu);
static int ret(struct cpu *cpu);
#endif // BONUS_CALL

enum operation_t
{
    Nop,
    Halt,
    Add,
    Sub,
    Mul,
    Div,
    Inc,
    Dec,
    Loop,
    Movr,
    Load,
    Store,
    In,
    Get,
    Out,
    Put,
    Swap,
    Push,
    Pop,
    Cmp,
    Jmp,
    Jz,
    Jnz,
    Jgt,
    Call,
    Ret
};

int32_t *cpuCreateMemory(FILE *program, size_t stackCapacity, int32_t **stackBottom)
{
    assert(program != NULL);
    assert(stackBottom != NULL);

    int32_t *memory = malloc(4 * 1024);
    int32_t *temp;
    int32_t position = 0;
    int32_t size = 1024;
    int32_t num;

    if (memory == NULL)
        return NULL;

    while (fread(&(num), 4, 1, program) == 1) {
        if ((position) == (size)) {
            size += 1024;
            temp = realloc(memory, size * 4);
            if (temp == NULL) {
                free(memory);
                return NULL;
            }
            memory = temp;
        }
        *(memory + position) = num;
        position++;
    }
    if (!feof(program)) {
        free(memory);
        return NULL;
    }
    while (memory + position + stackCapacity > memory + size) {
        size += 1024;
        temp = realloc(memory, size * 4);
        if (temp == NULL) {
            free(memory);
            return NULL;
        }
        memory = temp;
    }

    if (memory == NULL)
        return NULL;

    *stackBottom = memory + size - 1;

    while (memory + position <= *(stackBottom) -stackCapacity) {
        *(memory + position) = 0;
        position++;
    }
    return memory;
}

void cpuCreate(struct cpu *cpu, int32_t *memory, int32_t *stackBottom, size_t stackCapacity)
{
    assert(cpu != NULL);
    assert(memory != NULL);
    assert(stackBottom != NULL);

    cpu->A = 0;
    cpu->B = 0;
    cpu->C = 0;
    cpu->D = 0;
    cpu->status = cpuOK;
    cpu->stackSize = 0;
    cpu->instructionPointer = 0;
    cpu->memory = memory;
    cpu->stackBottom = stackBottom;
    cpu->stackLimit = stackBottom - stackCapacity;
#ifdef BONUS_JMP
    cpu->result = 0;
#endif // BONUS_JMP
}

void cpuDestroy(struct cpu *cpu)
{
    assert(cpu != NULL);
    free(cpu->memory);

    cpu->A = 0;
    cpu->B = 0;
    cpu->C = 0;
    cpu->D = 0;
    cpu->status = cpuOK;
    cpu->stackSize = 0;
    cpu->instructionPointer = 0;
    cpu->memory = NULL;
    cpu->stackBottom = NULL;
    cpu->stackLimit = NULL;
#ifdef BONUS_JMP
    cpu->result = 0;
#endif // BONUS_JMP
}

void cpuReset(struct cpu *cpu)
{
    assert(cpu != NULL);

    cpu->A = 0;
    cpu->B = 0;
    cpu->C = 0;
    cpu->D = 0;
    cpu->status = cpuOK;
    cpu->stackSize = 0;
    cpu->instructionPointer = 0;
#ifdef BONUS_JMP
    cpu->result = 0;
#endif // BONUS_JMP

    if (cpu->stackBottom != NULL && cpu->stackLimit != NULL) {

        int32_t *position = cpu->stackLimit + 1;
        while (position <= cpu->stackBottom) {
            *(position) = 0;
            position++;
        }
    }
}

int cpuStatus(struct cpu *cpu)
{
    assert(cpu != NULL);

    return cpu->status;
}


int32_t cpuPeek(struct cpu *cpu, char reg)
{
    assert(cpu != NULL);

    switch (reg) {
    case 'A':
        return cpu->A;
    case 'B':
        return cpu->B;
    case 'C':
        return cpu->C;
    case 'D':
        return cpu->D;
    case 'S':
        return cpu->stackSize;
    case 'I':
        return cpu->instructionPointer;
#ifdef BONUS_JMP
    case 'R':
        return cpu->result;
#endif // BONUS_JMP
    default:
        return 0;
    }
}

static int indexCheck(struct cpu *cpu, int32_t curPointer)
{
    if (cpu->memory + curPointer > cpu->stackLimit || curPointer < 0) {
        cpu->status = cpuInvalidAddress;
        return 1;
    }
    return 0;
}

static int32_t *getReg(struct cpu *cpu, int32_t reg)
{
    switch (reg) {
    case 0:
        return &(cpu->A);
    case 1:
        return &(cpu->B);
    case 2:
        return &(cpu->C);
    case 3:
        return &(cpu->D);
#ifdef BONUS_JMP
    case 4:
        return &(cpu->result);
#endif // BONUS_JMP
    default:
        return NULL;
    }
}

static int nop(struct cpu *cpu)
{
    cpu->instructionPointer += 1;
    return 1;
}

static int halt(struct cpu *cpu)
{
    cpu->instructionPointer += 1;
    cpu->status = cpuHalted;
    return 0;
}

static int add(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    cpu->A += *(reg);
#ifdef BONUS_JMP
    cpu->result = cpu->A;
#endif // BONUS_JMP
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int sub(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    cpu->A -= *(reg);
#ifdef BONUS_JMP
    cpu->result = cpu->A;
#endif // BONUS_JMP
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int mul(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    cpu->A *= *(reg);
#ifdef BONUS_JMP
    cpu->result = cpu->A;
#endif // BONUS_JMP
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int divide(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    if (*(reg) == 0) {
        cpu->status = cpuDivByZero;
        return 0;
    }
    cpu->A /= *(reg);
#ifdef BONUS_JMP
    cpu->result = cpu->A;
#endif // BONUS_JMP
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int inc(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    *(reg) += 1;
#ifdef BONUS_JMP
    cpu->result = *(reg);
#endif // BONUS_JMP
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int dec(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    *(reg) -= 1;
#ifdef BONUS_JMP
    cpu->result = *(reg);
#endif // BONUS_JMP
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int loop(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->C != 0) {
        cpu->instructionPointer = *(cpu->memory + curPointer);
    } else
        cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int movr(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    curPointer++;
    *(reg) = *(cpu->memory + curPointer);
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int load(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->D + *(cpu->memory + curPointer) >= cpu->stackSize || cpu->D + *(cpu->memory + curPointer) < 0) {
        cpu->status = cpuInvalidStackOperation;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    *(reg) = *(cpu->stackBottom - cpu->stackSize + 1 + cpu->D + *(cpu->memory + curPointer));
    cpu->instructionPointer = curPointer + 1;
    return 1;
}

static int store(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->D + *(cpu->memory + curPointer) >= cpu->stackSize || cpu->D + *(cpu->memory + curPointer) < 0) {
        cpu->status = cpuInvalidStackOperation;
        return 0;
    }
    *(cpu->stackBottom - cpu->stackSize + 1 + cpu->D + *(cpu->memory + curPointer)) = *(reg);
    cpu->instructionPointer = curPointer + 1;
    return 1;
}

static int in(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;
    int32_t loadInt = 0;

    if (scanf("%d", &loadInt) == 0) {
        cpu->status = cpuIOError;
        return 0;
    }
    if (feof(stdin)) {
        cpu->C = 0;
        loadInt = -1;
    }
    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    *(reg) = loadInt;
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int get(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;
    int32_t loadInt = 0;

    loadInt = getchar();
    if (loadInt == EOF) {
        cpu->C = 0;
    }
    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    *(reg) = loadInt;
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int out(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    printf("%d", *(reg));
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int put(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    if (*(reg) >= 256 || *(reg) < 0) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    printf("%c", *(reg));
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int swap(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;
    int32_t *reg2;
    int32_t temp = 0;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg2 = getReg(cpu, *(cpu->memory + curPointer));
    if (reg2 == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result) || reg2 == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    temp = *(reg);
    *(reg) = *(reg2);
    *(reg2) = temp;
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int push(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    if (cpu->stackBottom - cpu->stackSize <= cpu->stackLimit) {
        cpu->status = cpuInvalidStackOperation;
        return 0;
    }
    *(cpu->stackBottom - cpu->stackSize) = *(reg);
    cpu->stackSize++;
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int pop(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    if (cpu->stackSize == 0) {
        cpu->status = cpuInvalidStackOperation;
        return 0;
    }
#ifdef BONUS_JMP
    if (reg == &(cpu->result)) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
#endif // BONUS_JMP
    *(reg) = *(cpu->stackBottom - cpu->stackSize + 1);
    cpu->stackSize--;
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

#ifdef BONUS_JMP
static int cmp(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;
    int32_t *reg;
    int32_t *reg2;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg = getReg(cpu, *(cpu->memory + curPointer));
    if (reg == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    reg2 = getReg(cpu, *(cpu->memory + curPointer));
    if (reg2 == NULL) {
        cpu->status = cpuIllegalOperand;
        return 0;
    }
    cpu->result = *(reg) - *(reg2);
    cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int jmp(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    cpu->instructionPointer = *(cpu->memory + curPointer);
    return 1;
}

static int jz(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->result == 0)
        cpu->instructionPointer = *(cpu->memory + curPointer);
    else
        cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int jnz(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->result != 0)
        cpu->instructionPointer = *(cpu->memory + curPointer);
    else
        cpu->instructionPointer = (curPointer + 1);
    return 1;
}

static int jgt(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->result > 0)
        cpu->instructionPointer = *(cpu->memory + curPointer);
    else
        cpu->instructionPointer = (curPointer + 1);
    return 1;
}
#endif // BONUS_JMP

#ifdef BONUS_CALL
static int call(struct cpu *cpu)
{
    int32_t curPointer = cpu->instructionPointer;

    curPointer++;
    if (indexCheck(cpu, curPointer))
        return 0;
    if (cpu->stackBottom - cpu->stackSize == cpu->stackLimit) {
        cpu->status = cpuInvalidStackOperation;
        return 0;
    }
    *(cpu->stackBottom - cpu->stackSize) = (curPointer + 1);
    cpu->instructionPointer = *(cpu->memory + curPointer);
    cpu->stackSize++;
    return 1;
}

static int ret(struct cpu *cpu)
{
    if (cpu->stackSize == 0) {
        cpu->status = cpuInvalidStackOperation;
        return 0;
    }
    cpu->stackSize -= 1;
    cpu->instructionPointer = *(cpu->stackBottom - cpu->stackSize);
    return 1;
}
#endif // BONUS_CALL

int cpuStep(struct cpu *cpu)
{
    assert(cpu != NULL);
    if (cpu->status != cpuOK)
        return 0;

    if (indexCheck(cpu, cpu->instructionPointer))
        return 0;

    enum operation_t operation = *(cpu->memory + cpu->instructionPointer);

    switch (operation) {
    case Nop:
        return nop(cpu);
    case Halt:
        return halt(cpu);
    case Add:
        return add(cpu);
    case Sub:
        return sub(cpu);
    case Mul:
        return mul(cpu);
    case Div:
        return divide(cpu);
    case Inc:
        return inc(cpu);
    case Dec:
        return dec(cpu);
    case Loop:
        return loop(cpu);
    case Movr:
        return movr(cpu);
    case Load:
        return load(cpu);
    case Store:
        return store(cpu);
    case In:
        return in(cpu);
    case Get:
        return get(cpu);
    case Out:
        return out(cpu);
    case Put:
        return put(cpu);
    case Swap:
        return swap(cpu);
    case Push:
        return push(cpu);
    case Pop:
        return pop(cpu);
#ifdef BONUS_JMP
    case Cmp:
        return cmp(cpu);
    case Jmp:
        return jmp(cpu);
    case Jz:
        return jz(cpu);
    case Jnz:
        return jnz(cpu);
    case Jgt:
        return jgt(cpu);
#endif // BONUS_JMP

#ifdef BONUS_CALL
    case Call:
        return call(cpu);
    case Ret:
        return ret(cpu);
#endif // BONUS_CALL
    default:
        cpu->status = cpuIllegalInstruction;
        return 0;
    }
}

int cpuRun(struct cpu *cpu, size_t steps)
{
    assert(cpu != NULL);
    if (cpu->status != cpuOK)
        return 0;

    size_t count = 0;
    while (count < steps && cpu->status == cpuOK) {
        cpuStep(cpu);
        count++;
    }
    if (cpu->status != cpuOK && cpu->status != cpuHalted) {
        return -count;
    }
    return count;
}
