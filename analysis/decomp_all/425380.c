
void __thiscall FUN_00425380(int param_1,uint param_2)

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
  local_8 = param_1;
  if ((param_2 & 2) == 0) {
    FUN_00409360();
    if ((param_2 & 1) != 0) {
      FUN_00428ad0(local_8);
    }
  }
  else {
    FUN_0056de40(param_1,0x8c,*(undefined4 *)(param_1 + -4),FUN_00409360);
    if ((param_2 & 1) != 0) {
      FUN_00428ad0(local_8 + -4);
    }
  }
  local_8 = 0x425410;
  __chkesp();
  return;
}

