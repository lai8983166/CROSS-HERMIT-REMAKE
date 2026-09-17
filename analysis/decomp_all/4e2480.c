
void FUN__text__004e2480(int param_1,int param_2,uint param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  undefined *local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((param_2 < 0) || (3 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=type)&&(type<=3)",
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738cc0 + 3
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
                                  "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",DAT_00738cc0 + 9
                                  ,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = &DAT_007f8020 + param_1 * 0xb0;
  local_1c = param_2;
  switch(param_2) {
  case 0:
    if ((9 < (int)param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (10)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cc0 + 0xe,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(int *)(local_8 + param_3 * 4) = param_4;
    break;
  case 1:
    if ((0x13 < (int)param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (10*2)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cc0 + 0x12,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined2 *)(local_8 + param_3 * 2 + 0x28) = (undefined2)param_4;
    break;
  case 2:
    if ((0x27 < (int)param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (10*4)",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cc0 + 0x16,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_8[param_3 + 0x50] = (undefined1)param_4;
    break;
  case 3:
    if ((0x13f < param_3) &&
       (iVar2 = FUN__text__00424f80("offset < (sizeof(uint32)*8*(10))",
                                    "E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                    DAT_00738cc0 + 0x1c,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_14 = param_3 >> 5;
    local_18 = param_3 % 0x20;
    local_c = 1 << (0x1fU - (char)local_18 & 0x1f);
    local_10 = local_c ^ 0xffffffff;
    *(uint *)(local_8 + local_14 * 4 + 0x78) = *(uint *)(local_8 + local_14 * 4 + 0x78) & local_10;
    if (param_4 != 0) {
      *(uint *)(local_8 + local_14 * 4 + 0x78) = *(uint *)(local_8 + local_14 * 4 + 0x78) | local_c;
    }
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                DAT_00738cc0 + 0x25,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = (undefined *)0x4e26c3;
  FUN__text__0056ce80();
  return;
}

