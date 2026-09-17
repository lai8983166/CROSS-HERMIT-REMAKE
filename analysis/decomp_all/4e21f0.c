
void FUN__text__004e21f0(int param_1,int param_2,uint param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  undefined *local_14;
  undefined *local_10;
  undefined *local_c;
  undefined *local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((param_2 < 0) || (3 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=type)&&(type<=3)",
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738cbc + 3
                                  ,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((param_1 == -1) || (param_1 == 0xffff)) {
    param_1 = (int)DAT_007f4488;
  }
  if (((param_2 < 0) || (400 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=type)&&(type<=400)",
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738cbc + 9
                                  ,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = &DAT_007f8020 + param_1 * 0xb0;
  local_24 = param_2;
  switch(param_2) {
  case 0:
    if ((9 < (int)param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (10)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cbc + 0xf,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = local_8 + param_3 * 4;
    break;
  case 1:
    if ((0x13 < (int)param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (10*2)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cbc + 0x14,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = local_8 + param_3 * 2 + 0x28;
    break;
  case 2:
    if ((0x27 < (int)param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (10*4)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cbc + 0x19,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_14 = local_8 + param_3 + 0x50;
    break;
  case 3:
    if ((0x13f < param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (sizeof(uint32)*8*(10))",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cbc + 0x1f,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_1c = param_3 >> 5;
    local_20 = param_3 % 0x20;
    local_18 = *(uint *)(local_8 + local_1c * 4 + 0x78) >> (0x1fU - (char)local_20 & 0x1f) & 1;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cbc + 0x29,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = (undefined *)0x4e241f;
  FUN__text__0056ce80();
  return;
}

