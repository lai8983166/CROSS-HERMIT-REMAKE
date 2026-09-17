
void __fastcall FUN_0052b0c2(int param_1)

{
  int iVar1;
  
  if ((*(int *)(param_1 + 4) != 0) && (*(int *)(param_1 + 0x38) != 0)) {
    FUN_00428ad0(*(int *)(param_1 + 4));
  }
  if ((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0x3c) != 0)) {
    FUN_00428ad0(*(int *)(param_1 + 8));
  }
  iVar1 = *(int *)(param_1 + 0x4c);
  if (iVar1 != 0) {
    FUN_0052b0c2();
    FUN_00428ad0(iVar1);
  }
  iVar1 = *(int *)(param_1 + 0x50);
  if (iVar1 != 0) {
    FUN_0052b0c2();
    FUN_00428ad0(iVar1);
  }
  return;
}

