
void FUN__text__00442b30(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_8ec [16];
  int local_8ac;
  undefined4 local_8a8;
  int local_8a4;
  undefined1 local_8a0 [13];
  undefined1 local_893;
  undefined1 local_890;
  undefined4 auStack_88c [544];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_8ec;
  for (iVar2 = 0x23a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0041ae70();
  _memset(local_8a0,0,0x894);
  local_893 = 2;
  local_890 = FUN__text__0041aea0();
  for (local_8a4 = 0; local_8a4 != 0x10; local_8a4 = local_8a4 + 1) {
    puVar3 = (undefined4 *)(local_c + local_8a4 * 0x88);
    puVar4 = auStack_88c + local_8a4 * 0x22;
    for (iVar2 = 0x22; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
    FUN__text__0042b2d0("(%d) : %s : %08x : RD(%d) : %UD(%d)\n",local_8a4,
                        local_c + 2 + local_8a4 * 0x88,
                        *(undefined4 *)(local_c + 0x84 + local_8a4 * 0x88),
                        (int)*(char *)(local_c + 1 + local_8a4 * 0x88),
                        (int)*(char *)(local_c + local_8a4 * 0x88));
  }
  local_8a8 = 0x894;
  local_8ac = FUN__text__00419fe0(local_8a0,0x894);
  if (local_8ac != 0) {
    iVar2 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                DAT_005ffc98 + 0x11,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x442ccd;
  FUN__text__0056ce80();
  return;
}

