
void FUN__text__00441f40(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  undefined1 local_1c [13];
  undefined1 local_f;
  undefined1 local_c;
  undefined1 local_b;
  undefined4 local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _memset(local_1c,0,0x14);
  local_f = 3;
  local_c = 1;
  local_b = 0;
  local_20 = FUN__text__00419fe0(local_1c,0x14);
  if ((local_20 != 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffc78 + 0xb,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x441fdc;
  FUN__text__0056ce80();
  return;
}

