
void __thiscall
FUN__text__0047fe70(int param_1,undefined4 param_2,int param_3,int param_4,undefined2 param_5,
                   undefined2 param_6,undefined4 param_7)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  short local_24 [2];
  short local_20 [2];
  uint local_1c;
  uint local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_3 < 0) || (0xf < param_3)) {
    iVar2 = FUN__text__00424f80("(0<=player)&&(player<=15)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e90 + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_4 < 0) || (0xff < param_4)) {
    iVar2 = FUN__text__00424f80("(0<=group)&&(group<=255)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e90 + 8,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_18 = CONCAT31(local_18._1_3_,(undefined1)param_3);
  local_1c = CONCAT31(local_1c._1_3_,(undefined1)param_4);
  local_14 = 0;
  local_c = (int *)(local_8 + 0xdccd8);
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    if (((local_18 & 0xff) == (uint)*(byte *)(*(int *)(local_c[local_10 + 1] + 600) + 0xa4)) &&
       ((local_1c & 0xff) == (uint)*(byte *)(*(int *)(local_c[local_10 + 1] + 600) + 0x98))) {
      iVar2 = FUN__text__00468d10(local_c[local_10 + 1]);
      if (iVar2 != 0) {
        iVar2 = FUN__text__0046a120(local_c[local_10 + 1]);
        if (iVar2 != 0) {
          iVar2 = FUN__text__0043d660(param_5,CONCAT22((short)((uint)*(int *)(local_c[local_10 + 1]
                                                                             + 600) >> 0x10),param_6
                                                      ),param_7,
                                      *(undefined1 *)(*(int *)(local_c[local_10 + 1] + 600) + 0x30),
                                      local_20,local_24);
          if (iVar2 != 0) {
            FUN__text__00480040(param_2,local_c[local_10 + 1],(int)local_20[0],(int)local_24[0]);
            local_14 = local_14 + 1;
          }
        }
      }
    }
  }
  local_8 = 0x48002c;
  FUN__text__0056ce80();
  return;
}

