
void __thiscall FUN__text__00437a70(int *param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *param_1 = param_4;
  param_1[1] = param_4;
  local_8 = param_1;
  local_c = FUN__text__00428a40(*param_1 * 0x1c);
  local_8[2] = local_c;
  if ((local_8[2] == 0) &&
     (iVar2 = FUN__text__00424f80("NodeWork!=0","E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                  DAT_005ff9ac + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_8[2] != 0) {
    _memset((void *)local_8[2],0,*local_8 * 0x1c);
    iVar2 = FUN__text__00439550(param_2,param_3,local_8[2]);
    if (iVar2 == 0) {
      local_10 = FUN__text__00428a40(*local_8 << 3);
      local_8[3] = local_10;
      if ((local_8[3] == 0) &&
         (iVar2 = FUN__text__00424f80("DebugSearch!=0",
                                      "E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                      DAT_005ff9ac + 0xf,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if (local_8[3] != 0) goto LAB__text__00437bf9;
    }
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                              DAT_005ff9ac + 0x15,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_8[2] == 0) {
    local_14 = local_8[2];
    FUN__text__00428ad0(local_14);
    local_8[2] = 0;
  }
  FUN__text__004394a0();
LAB__text__00437bf9:
  local_8 = (int *)0x437c06;
  FUN__text__0056ce80();
  return;
}

