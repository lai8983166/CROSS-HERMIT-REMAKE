
void FUN__text__004e1da0(int param_1,uint param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  uint local_1c;
  uint local_18;
  uint *local_14;
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((param_1 < 0) || (3 < param_1)) &&
     (iVar2 = FUN__text__00424f80("(0<=type)&&(type<=3)",
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738cb4 + 1
                                  ,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_20 = param_1;
  switch(param_1) {
  case 0:
    if ((0x3f < (int)param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (64)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb4 + 5,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 1:
    if ((0x7f < (int)param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (64*2)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb4 + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = &DAT_007f7d18 + param_2 * 2;
    break;
  case 2:
    if ((0xff < (int)param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (64*4)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb4 + 0xf,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = &DAT_007f7e18 + param_2;
    break;
  case 3:
    if ((0x7ff < param_2) &&
       (iVar2 = FUN__text__00424f80("offset < (sizeof(uint32)*8*(64))",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cb4 + 0x15,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_18 = param_2 >> 5;
    local_1c = param_2 % 0x20;
    local_14 = (uint *)(&DAT_007f7f18 + local_18 * 4);
    *local_14 = *local_14 >> (0x1fU - (char)local_1c & 0x1f);
    *local_14 = *local_14 & 1;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cb4 + 0x1f,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4e1f81;
  FUN__text__0056ce80();
  return;
}

