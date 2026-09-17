
void __thiscall FUN__text__00403e70(int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((*(short *)(param_3 + 0x38) != 0) && (*(short *)(param_3 + 0x3a) != 0)) &&
      (*(int *)(param_3 + 0x34) != 0)) && (*(int *)(param_3 + 0x2c) != 0)) {
    *(undefined2 *)(param_1 + 0x38) = *(undefined2 *)(param_3 + 0x38);
    *(undefined2 *)(param_1 + 0x3a) = *(undefined2 *)(param_3 + 0x3a);
    *(undefined4 *)(param_1 + 0x34) = *(undefined4 *)(param_3 + 0x34);
    local_8 = param_1;
    FUN__text__00403bd0(param_2,0);
  }
  local_8 = 0x403eff;
  FUN__text__0056ce80();
  return;
}

