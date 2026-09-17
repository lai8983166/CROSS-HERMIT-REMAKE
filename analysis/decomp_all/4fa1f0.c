
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004fa1f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x39) != '\0') {
    local_c = local_c & 0xffffff00;
    if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
      FUN__text__00505580((int)_DAT_00752724,(int)_DAT_00752726,(int)_DAT_00752728,
                          (int)_DAT_0075272a,(int)_DAT_0075272c,(int)_DAT_0075272e,
                          (int)_DAT_00752730,(int)_DAT_00752732,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_DAT_00752724,(int)_DAT_00752726,(int)_DAT_00752728,
                          (int)_DAT_0075272a,(int)_DAT_0075272c,(int)_DAT_0075272e,
                          (int)_DAT_00752730,(int)_DAT_00752732);
    }
  }
  if (*(char *)(local_8 + 0x3a) != '\0') {
    local_c = CONCAT31(local_c._1_3_,1);
    if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
      FUN__text__00505580((int)_UNK_00752734,(int)_UNK_00752736,(int)_UNK_00752738,
                          (int)_UNK_0075273a,(int)_UNK_0075273c,(int)_UNK_0075273e,
                          (int)_UNK_00752740,(int)_UNK_00752742,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_UNK_00752734,(int)_UNK_00752736,(int)_UNK_00752738,
                          (int)_UNK_0075273a,(int)_UNK_0075273c,(int)_UNK_0075273e,
                          (int)_UNK_00752740,(int)_UNK_00752742);
    }
  }
  if (*(char *)(local_8 + 0x3b) != '\0') {
    local_c = CONCAT31(local_c._1_3_,2);
    if ((*(char *)(local_8 + 0x3b) == '\x01') || (*(char *)(local_8 + 0x3b) == '\x03')) {
      FUN__text__00505580((int)_UNK_00752744,(int)_UNK_00752746,(int)_UNK_00752748,
                          (int)_UNK_0075274a,(int)_UNK_0075274c,(int)_UNK_0075274e,
                          (int)_UNK_00752750,(int)_UNK_00752752,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_UNK_00752744,(int)_UNK_00752746,(int)_UNK_00752748,
                          (int)_UNK_0075274a,(int)_UNK_0075274c,(int)_UNK_0075274e,
                          (int)_UNK_00752750,(int)_UNK_00752752);
    }
  }
  local_8 = 0x4fa6e7;
  FUN__text__0056ce80();
  return;
}

