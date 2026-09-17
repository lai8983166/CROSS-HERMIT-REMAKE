
int FUN__text__004c2120(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [22];
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return param_1 + (*(uint *)(param_1 + param_2 * 4 + 4) & 0xfffff);
}

