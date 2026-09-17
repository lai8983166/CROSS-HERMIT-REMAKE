
void FUN__text__00497aa0(void)

{
  char cVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  char local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(char *)(DAT_007a49f8 + 0x2499) != '\0') {
    cVar1 = *(char *)(DAT_007a49f8 + 0x2498);
    local_8 = CONCAT31(local_8._1_3_,cVar1);
    if (cVar1 == '\0') {
      *(int *)(DAT_007a49f8 + 0x2490) =
           *(int *)(DAT_007a49f8 + 0x2490) - *(int *)(DAT_007a49f8 + 0x2494);
      if (*(int *)(DAT_007a49f8 + 0x2490) < 1) {
        *(undefined4 *)(DAT_007a49f8 + 0x2490) = 0;
      }
    }
    else if (cVar1 == '\x01') {
      *(int *)(DAT_007a49f8 + 0x2490) =
           *(int *)(DAT_007a49f8 + 0x2490) + *(int *)(DAT_007a49f8 + 0x2494);
      if (0x97ff < *(int *)(DAT_007a49f8 + 0x2490)) {
        *(undefined4 *)(DAT_007a49f8 + 0x2490) = 0x9800;
      }
    }
    else {
      iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                  DAT_00619fc8 + 0xf,0);
      if (iVar3 != 0) {
        pcVar2 = (code *)swi(3);
        (*pcVar2)();
        return;
      }
    }
    *(int *)(DAT_007a49f8 + 0x249c) = *(int *)(DAT_007a49f8 + 0x249c) + -1;
    if (*(int *)(DAT_007a49f8 + 0x249c) == 0) {
      *(undefined1 *)(DAT_007a49f8 + 0x2499) = 0;
      local_c = *(char *)(DAT_007a49f8 + 0x2498);
      if (local_c == '\0') {
        *(undefined1 *)(DAT_007a49f8 + 0x249a) = 0;
      }
      else if (local_c == '\x01') {
        *(undefined1 *)(DAT_007a49f8 + 0x249a) = 2;
      }
      FUN__text__004977a0();
    }
    else {
      *(undefined1 *)(DAT_007a49f8 + 0x249a) = 1;
    }
  }
  local_8 = 0x497c3f;
  FUN__text__0056ce80();
  return;
}

