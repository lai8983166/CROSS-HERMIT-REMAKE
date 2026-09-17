
void __thiscall FUN__text__0043c530(int param_1,int param_2,int param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x2659c) != 0) {
    local_8 = param_1;
    if (((param_4 < 0) || (0x20 < param_4)) &&
       (iVar2 = FUN__text__00424f80("(0<=view)&&(view<=32)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ffa08 + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_1c = (int)(char)(&DAT_0059558c)[param_4 * 2];
    local_20 = (int)(char)(&DAT_0059558d)[param_4 * 2];
    local_14 = param_2 - (local_1c + -1) / 2;
    local_18 = param_3 - (local_20 + -1) / 2;
    local_24 = *(int *)(local_8 + 8 + param_4 * 4);
    for (local_10 = 0; local_10 != local_20; local_10 = local_10 + 1) {
      for (local_c = 0; local_c != local_1c; local_c = local_c + 1) {
        if (((-1 < local_18 + local_10) && (-1 < local_14 + local_c)) &&
           ((local_18 + local_10 < (int)*(short *)(*(int *)(local_8 + 0x2659c) + 6) &&
            ((local_14 + local_c < (int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) &&
             (*(char *)(local_24 + local_10 * local_1c + local_c) != '\0')))))) {
          FUN__text__00410310((local_14 + local_c) * 0x20 - (int)*(short *)(local_8 + 0x265a6),
                              ((local_18 + local_10) * 0x10 - (int)*(short *)(local_8 + 0x265a8)) +
                              0x1e,0x20,0x10,0xeff,DAT_005ff9cc,1);
        }
      }
    }
  }
  local_8 = 0x43c6f2;
  FUN__text__0056ce80();
  return;
}

