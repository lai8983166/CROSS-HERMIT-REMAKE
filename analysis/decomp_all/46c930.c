
bool FUN__text__0046c930(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return -1 < (int)*(short *)(*(int *)(param_1 + 600) + 0x1c) -
              (int)*(short *)(&DAT_006c2dd0 + param_2 * 0x48);
}

