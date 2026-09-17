
void __thiscall FUN__text__00442580(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  void *local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_2 + 8);
  local_8 = param_1;
  if (((*(char *)(local_c + 0x10) < '\x01') || ('\x14' < *(char *)(local_c + 0x10))) &&
     (iVar2 = FUN__text__00424f80("(0<recv->rcnt) && (recv->rcnt<=20)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffc88 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = (uint)*(byte *)(local_c + 0xc4);
  if ((3 < local_10) &&
     (iVar2 = FUN__text__00424f80("(0<=off) && (off<4)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffc88 + 9,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  *(undefined1 *)(local_8 + local_10 + 0x1a91) = 1;
  local_14 = (void *)(local_8 + 0x1c30 + local_10 * 0xdc0);
  _memset(local_14,0,0xdc0);
  FUN__text__0056d4d0(local_14,local_c + 0x20,*(char *)(local_c + 0x10) * 0xb0);
  local_8 = 0x442688;
  FUN__text__0056ce80();
  return;
}

