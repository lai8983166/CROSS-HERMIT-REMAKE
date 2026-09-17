
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__005247b0(int param_1)

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
      FUN__text__00505580((int)_DAT_00757da8,(int)_DAT_00757daa,(int)_DAT_00757dac,
                          (int)_DAT_00757dae,(int)_DAT_00757db0,(int)_DAT_00757db2,
                          (int)_DAT_00757db4,(int)_DAT_00757db6,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_DAT_00757da8,(int)_DAT_00757daa,(int)_DAT_00757dac,
                          (int)_DAT_00757dae,(int)_DAT_00757db0,(int)_DAT_00757db2,
                          (int)_DAT_00757db4,(int)_DAT_00757db6);
    }
  }
  if (*(char *)(local_8 + 0x3a) != '\0') {
    local_c = CONCAT31(local_c._1_3_,1);
    if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
      FUN__text__00505580((int)_UNK_00757db8,(int)_UNK_00757dba,(int)_UNK_00757dbc,
                          (int)_UNK_00757dbe,(int)_UNK_00757dc0,(int)_UNK_00757dc2,
                          (int)_UNK_00757dc4,(int)_UNK_00757dc6,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_UNK_00757db8,(int)_UNK_00757dba,(int)_UNK_00757dbc,
                          (int)_UNK_00757dbe,(int)_UNK_00757dc0,(int)_UNK_00757dc2,
                          (int)_UNK_00757dc4,(int)_UNK_00757dc6);
    }
  }
  if (*(char *)(local_8 + 0x3b) != '\0') {
    local_c = CONCAT31(local_c._1_3_,2);
    if ((*(char *)(local_8 + 0x3b) == '\x01') || (*(char *)(local_8 + 0x3b) == '\x03')) {
      FUN__text__00505580((int)_UNK_00757dc8,(int)_UNK_00757dca,(int)_UNK_00757dcc,
                          (int)_UNK_00757dce,(int)_UNK_00757dd0,(int)_UNK_00757dd2,
                          (int)_UNK_00757dd4,(int)_UNK_00757dd6,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_UNK_00757dc8,(int)_UNK_00757dca,(int)_UNK_00757dcc,
                          (int)_UNK_00757dce,(int)_UNK_00757dd0,(int)_UNK_00757dd2,
                          (int)_UNK_00757dd4,(int)_UNK_00757dd6);
    }
  }
  local_8 = 0x524ca7;
  FUN__text__0056ce80();
  return;
}

