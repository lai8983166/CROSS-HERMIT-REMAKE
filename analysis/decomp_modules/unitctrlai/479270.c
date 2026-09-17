
void FUN__text__00479270(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  char local_28;
  undefined2 local_24;
  short local_20;
  int local_1c;
  char *local_18;
  int local_14;
  undefined *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = param_1 + 0x290;
  local_18 = (char *)(param_1 + 0x293);
  local_c = 0;
  if ((((*(short *)(param_1 + 0x4f8) != -1) && (iVar1 = FUN__text__00468d10(0), iVar1 != 0)) &&
      (iVar1 = FUN__text__00469480(local_c), iVar1 != 0)) &&
     (iVar1 = FUN__text__004690a0(local_c), iVar1 == 0)) {
    local_c = local_8 + 0x80aec + *(short *)(param_1 + 0x4f8) * 0x520;
  }
  local_1c = (int)*(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40
                            );
  local_10 = &DAT_00613b78 + local_1c * 6;
  local_28 = *local_18;
  if (local_28 == '\0') {
    FUN__text__0046b0b0(param_1,1);
    if (local_c != 0) {
      local_20 = (short)((uint)*(undefined4 *)(local_c + 0x2ec) >> 0x10);
      local_24 = (undefined2)((uint)*(undefined4 *)(local_c + 0x2f0) >> 0x10);
      FUN__text__0046c120(param_1,local_20,CONCAT22(local_20 >> 0xf,local_24));
    }
    FUN__text__0046bcc0(param_1,(int)*(short *)(local_10 + 2));
    *local_18 = *local_18 + '\x01';
  }
  else if (local_28 == '\x01') {
    if (*(char *)(param_1 + 4) != '\0') {
      *local_18 = *local_18 + '\x01';
    }
  }
  else if (local_28 == '\x02') {
    *(undefined1 *)(local_14 + 0x17) = 0;
    FUN__text__00475270(param_1,0xf);
  }
  local_8 = 0x4793fb;
  FUN__text__0056ce80();
  return;
}

