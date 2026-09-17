
int FUN__text1__00810e63(int param_1,uint param_2)

{
  return (*(int *)(param_1 + (param_2 >> 0x18) * 4) +
          *(int *)(param_1 + 0x400 + (param_2 >> 0x10 & 0xff) * 4) ^
         *(uint *)(param_1 + 0x800 + (param_2 >> 8 & 0xff) * 4)) +
         *(int *)(param_1 + 0xc00 + (param_2 & 0xff) * 4);
}

