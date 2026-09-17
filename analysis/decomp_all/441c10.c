
void FUN__text__00441c10(int param_1,int *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  undefined4 local_24;
  undefined1 local_20 [4];
  int local_1c;
  int local_18;
  size_t local_14;
  int local_10;
  void *local_c;
  undefined4 local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0x3700;
  local_24 = (void *)FUN__text__00428a40(0x25d000);
  local_c = local_24;
  if ((local_24 == (void *)0x0) &&
     (iVar2 = FUN__text__00424f80("ud != 0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffc74 + 8,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_c != (void *)0x0) {
    _memset(local_c,0,local_14);
    local_1c = FUN__text__0044ad50();
    _memset(local_20,0,4);
    local_18 = 0;
    for (local_10 = 0; local_10 != 0x50; local_10 = local_10 + 1) {
      if (*(short *)(param_1 + local_10 * 0xb0) != 0) {
        if (((*(short *)(param_1 + local_10 * 0xb0) == 0) ||
            (4 < *(ushort *)(param_1 + local_10 * 0xb0))) &&
           (iVar2 = FUN__text__00424f80("(1<=wk[i].no) && (wk[i].no<=4)",
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                        DAT_005ffc74 + 0x12,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        if ((char)local_20[*(ushort *)(param_1 + local_10 * 0xb0) - 1] < local_1c) {
          puVar3 = (undefined4 *)(param_1 + local_10 * 0xb0);
          puVar4 = (undefined4 *)((int)local_c + local_18 * 0xb0);
          for (iVar2 = 0x2c; iVar2 != 0; iVar2 = iVar2 + -1) {
            *puVar4 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar4 = puVar4 + 1;
          }
          local_20[*(ushort *)(param_1 + local_10 * 0xb0) - 1] =
               local_20[*(ushort *)(param_1 + local_10 * 0xb0) - 1] + '\x01';
          local_18 = local_18 + 1;
        }
      }
    }
    *param_2 = local_18;
  }
  local_8 = 0x441dd6;
  FUN__text__0056ce80();
  return;
}

