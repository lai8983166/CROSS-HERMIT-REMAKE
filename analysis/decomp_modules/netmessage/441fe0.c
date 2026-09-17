
void FUN__text__00441fe0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_90 [16];
  int local_50;
  undefined1 local_4c [13];
  undefined1 local_3f;
  undefined2 local_3c;
  int local_8;
  
  puVar3 = local_90;
  for (iVar2 = 0x23; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _memset(local_4c,0,0x44);
  local_3f = 5;
  local_3c = *(undefined2 *)(local_8 + 0x1a88);
  local_50 = FUN__text__00419fe0(local_4c,0x44);
  if ((local_50 != 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffc7c + 10,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x44208b;
  FUN__text__0056ce80();
  return;
}

