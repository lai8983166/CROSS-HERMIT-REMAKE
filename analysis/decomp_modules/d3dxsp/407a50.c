
void __thiscall FUN__text__00407a50(int param_1,undefined4 param_2,undefined4 param_3)

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
  if ((*(int *)(param_1 + 0x4c) != 0) &&
     (((*(ushort *)(param_1 + 0x58) & 0x80) != 0 || (*(int *)(param_1 + 0x2c) != 0)))) {
    local_8 = param_1;
    FUN__text__00407ad0(param_2,param_3);
  }
  local_8 = 0x407abd;
  FUN__text__0056ce80();
  return;
}

