
void __fastcall FUN_00548ed9(int *param_1)

{
  int iVar1;
  uint uVar2;
  
  if (*param_1 != 0) {
    uVar2 = 0;
    if (param_1[1] != 0) {
      do {
        iVar1 = *(int *)(*param_1 + uVar2 * 4);
        if (iVar1 != 0) {
          FUN_00428ad0(iVar1);
        }
        uVar2 = uVar2 + 1;
      } while (uVar2 < (uint)param_1[1]);
    }
    FUN_00428ad0(*param_1);
  }
  return;
}

