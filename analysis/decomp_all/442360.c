
void __fastcall FUN__text__00442360(int param_1)

{
  code *pcVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  local_c = FUN__text__00441c10(param_1 + 0x1c30,&local_14);
  if ((local_c == 0) &&
     (iVar3 = FUN__text__00424f80("ud != 0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffc84 + 7,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_c != 0) {
    _memset((void *)(local_8 + 0x5330),0,0x3720);
    *(undefined1 *)(local_8 + 0x533d) = 6;
    *(undefined1 *)(local_8 + 0x5340) = (undefined1)local_14;
    local_1c = local_14 * 0xb0 + 0x20;
    FUN__text__0056d4d0(local_8 + 0x5350,local_c,local_14 * 0xb0);
    for (local_18 = 0; local_18 != 4; local_18 = local_18 + 1) {
      *(undefined1 *)(local_8 + local_18 + 0x5341) = *(undefined1 *)(local_8 + local_18 + 0x1a8c);
    }
    iVar3 = _rand();
    iVar2 = _rand();
    *(int *)(local_8 + 0x5348) = iVar3 * iVar2;
    *(undefined2 *)(local_8 + 0x5346) = *(undefined2 *)(local_8 + 0x1aa4);
    for (local_18 = 0; local_18 != 4; local_18 = local_18 + 1) {
      *(undefined1 *)(local_8 + local_18 + 0x534c) = *(undefined1 *)(local_8 + local_18 + 0x1aac);
    }
    _memset((void *)(local_8 + 0x1c30),0,0x3700);
    FUN__text__0056d4d0(local_8 + 0x1c30,local_c,local_14 * 0xb0);
    local_10 = FUN__text__00419fe0(local_8 + 0x5330,local_1c);
    local_20 = local_c;
    FUN__text__00428ad0(local_c);
    if ((local_10 != 0) &&
       (iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                    DAT_005ffc84 + 0x33,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x44257a;
  FUN__text__0056ce80();
  return;
}

