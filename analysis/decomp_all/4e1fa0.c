
void FUN__text__004e1fa0(int param_1,uint param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar4 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (((param_1 < 0) || (3 < param_1)) &&
     (iVar2 = FUN__text__00424f80("(0<=type)&&(type<=3)",
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738cb8 + 1
                                  ,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_18 = param_1;
  switch(param_1) {
  case 0:
    if ((0x3f < (int)param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (64)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb8 + 4,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (&DAT_007f7c18)[param_2] = param_3;
    break;
  case 1:
    if ((0x7f < (int)param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (64*2)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb8 + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined2 *)(&DAT_007f7d18 + param_2 * 2) = (undefined2)param_3;
    break;
  case 2:
    if ((0xff < (int)param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (64*4)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb8 + 0xc,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (&DAT_007f7e18)[param_2] = (undefined1)param_3;
    break;
  case 3:
    if ((0x7ff < param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (sizeof(uint32)*8*(64))",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb8 + 0x12,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = param_2 >> 5;
    local_14 = param_2 % 0x20;
    uVar3 = 1 << (0x1fU - (char)local_14 & 0x1f);
    local_c = uVar3 ^ 0xffffffff;
    *(uint *)(&DAT_007f7f18 + local_10 * 4) = *(uint *)(&DAT_007f7f18 + local_10 * 4) & local_c;
    if (param_3 != 0) {
      *(uint *)(&DAT_007f7f18 + local_10 * 4) = *(uint *)(&DAT_007f7f18 + local_10 * 4) | uVar3;
    }
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb8 + 0x1c,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4e2192;
  FUN__text__0056ce80();
  return;
}

