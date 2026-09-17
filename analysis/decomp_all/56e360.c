
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_0056e360(undefined4 param_1,undefined4 param_2,int param_3,int param_4)

{
  undefined4 uVar1;
  uint uVar2;
  int *piVar3;
  
  FUN_0056e450(param_1);
  if (DAT_0080a428 == 1) {
    uVar1 = (*API_KERNEL32_DLL_GetCurrentProcess)(param_2);
    (*DAT_0059219c)(uVar1);
  }
  _DAT_0080a424 = 1;
  DAT_0080a420 = (undefined1)param_4;
  if (param_3 == 0) {
    piVar3 = DAT_0080bb84;
    if (DAT_0080bb88 != (int *)0x0) {
      while (piVar3 = piVar3 + -1, DAT_0080bb88 <= piVar3) {
        if (*piVar3 != 0) {
          (*(code *)*piVar3)();
        }
      }
    }
    __initterm(&DAT_005ff02c,&DAT_005ff034);
  }
  __initterm(&DAT_005ff038,&DAT_005ff040);
  if ((DAT_0080a42c == 0) && (uVar2 = FUN_0056ff20(0xffffffff), (uVar2 & 0x20) != 0)) {
    DAT_0080a42c = 1;
    FUN_005709d0();
  }
  if (param_4 == 0) {
    DAT_0080a428 = 1;
    (*DAT_005921a0)(param_2);
  }
  else {
    FUN_0056e460();
  }
  return;
}

