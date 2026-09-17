
void __thiscall FUN__text__0048ff70(undefined4 param_1,int param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  uint local_1c;
  int local_18;
  int local_14;
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_4 < 1) || (0x45 < param_4)) &&
     (iVar2 = FUN__text__00424f80("(1<=cno)&&(cno<=(69))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                  DAT_006191ec + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = &DAT_006f4088 + param_4 * 0x10;
  local_20 = 0;
  local_14 = 0;
  do {
    if (local_14 == 6) {
      local_8 = 0x4900d5;
      FUN__text__0056ce80();
      return;
    }
    local_1c = (uint)(byte)local_c[local_14 + 7];
    if ((local_1c != 0) && (local_18 = FUN__text__004900e0(param_2,local_1c), local_18 != 0)) {
      local_20 = local_20 + 1;
      if ((((int)local_1c < 1) || (0x45 < (int)local_1c)) &&
         (iVar2 = FUN__text__00424f80("(1<=no)&&(no<=(69))",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                      DAT_006191ec + 0x13,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_10 = &DAT_006f4088 + local_1c * 0x10;
      local_24 = local_18 + -1;
      if (((local_24 < 0) || (2 < local_24)) &&
         (iVar2 = FUN__text__00424f80("(0<=off) && (off<3)",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                      DAT_006191ec + 0x17,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      FUN__text__004902e0(param_2,param_2 + 0x14 + local_24 * 0x10,local_24);
    }
    local_14 = local_14 + 1;
  } while( true );
}

