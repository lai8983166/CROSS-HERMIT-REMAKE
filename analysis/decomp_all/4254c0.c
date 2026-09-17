
void __thiscall FUN__text__004254c0(short *param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  short *local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*param_1 == 0) {
    iVar2 = FUN__text__00424f80("rcnt!=0","e:\\crosshermit\\game\\src\\system\\syschatbox.cpp",
                                DAT_005ff618 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = (int)local_8[1] % (int)*local_8;
  if (*local_8 < local_c) {
    iVar2 = FUN__text__00424f80("rno <= rcnt","e:\\crosshermit\\game\\src\\system\\syschatbox.cpp",
                                DAT_005ff618 + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = FUN__text__00409500(param_2);
  if (local_10 != 0) {
    iVar2 = FUN__text__00424f80("ret==0","e:\\crosshermit\\game\\src\\system\\syschatbox.cpp",
                                DAT_005ff618 + 10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((*local_8 <= local_8[1]) && (local_8[2] = local_8[2] + 1, *local_8 <= local_8[2])) {
    local_8[2] = 0;
  }
  local_8[1] = local_8[1] + 1;
  if (*local_8 * 2 - (int)local_8[1] == 0 || *local_8 * 2 < (int)local_8[1]) {
    local_8[1] = *local_8;
  }
  local_8 = (short *)0x425610;
  FUN__text__0056ce80();
  return;
}

