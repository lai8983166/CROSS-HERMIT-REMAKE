
/* WARNING: Removing unreachable block (ram,0x0047e085) */

void FUN__text__0047dec0(int param_1)

{
  int iVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar2;
  undefined4 local_70 [16];
  int local_30;
  int local_2c;
  int local_28;
  char local_24;
  int local_20;
  int local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_70;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00470250(param_1,&local_1c,&local_20);
  if ((int)*(short *)(param_1 + 0x4ec) % 0x5a < 0x1e) {
    local_24 = (&DAT_00618da4)[(int)*(short *)(param_1 + 0x4ec) / 0xb];
  }
  else if ((int)*(short *)(param_1 + 0x4ec) % 0x5a < 0x3d) {
    local_24 = (&DAT_00618d80)[(int)*(short *)(param_1 + 0x4ec) / 0xb];
  }
  else {
    local_24 = (&DAT_00618da4)[(int)*(short *)(param_1 + 0x4ec) / 0xb];
  }
  local_c = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                         (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_10 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  local_14 = (short)((int)((int)*(short *)(param_1 + 0x4dc) +
                          ((int)*(short *)(param_1 + 0x4dc) >> 0x1f & 0x1fU)) >> 5);
  local_18 = (short)((int)((int)*(short *)(param_1 + 0x4de) +
                          ((int)*(short *)(param_1 + 0x4de) >> 0x1f & 0xfU)) >> 4);
  if ((local_c == local_14) && (local_10 == local_18)) {
    local_28 = 1;
  }
  else {
    local_28 = 0;
  }
  iVar1 = FUN__text__0043c0c0((int)local_14,(int)local_18);
  if (local_28 < iVar1) {
    local_2c = FUN__text__0047e320(CONCAT22(extraout_var_00,local_14),
                                   CONCAT22(extraout_var,local_18));
    if ((local_2c == 0) ||
       ((*(char *)(*(int *)(local_2c + 600) + 0xa4) != *(char *)(*(int *)(param_1 + 600) + 0xa4) &&
        (iVar1 = FUN__text__0046ad60(param_1,local_2c), iVar1 == 0)))) goto LAB__text__0047e21f;
    if (*(ushort *)(*(int *)(param_1 + 600) + 0x2e) <= *(ushort *)(*(int *)(local_2c + 600) + 0x2e))
    {
      local_1c = local_1c / 2;
      local_20 = local_20 / 2;
    }
  }
  iVar1 = FUN__text__004698a0(param_1);
  if ((((iVar1 == 0) || (*(char *)(*(int *)(param_1 + 600) + 0x9f) != '\x01')) ||
      (iVar1 = FUN__text__0047d010(param_1), iVar1 != 0)) ||
     (iVar1 = FUN__text__0047d0e0(param_1), iVar1 != 0)) {
    *(int *)(param_1 + 0x2ec) = *(int *)(param_1 + 0x2ec) + local_1c;
    *(int *)(param_1 + 0x2f0) = *(int *)(param_1 + 0x2f0) + local_20;
    *(short *)(param_1 + 0x4e2) = *(short *)(param_1 + 0x4e2) + 1;
    if ((*(short *)(param_1 + 0x54) != 3) || (*(char *)(param_1 + 0x28a) != local_24)) {
      *(undefined1 *)(param_1 + 0x28b) = *(undefined1 *)(param_1 + 0x28a);
      *(char *)(param_1 + 0x28a) = local_24;
      FUN__text__00465040(param_1 + 0x48,3,(int)*(char *)(param_1 + 0x28a));
      *(undefined2 *)(param_1 + 0x4e2) = 0;
    }
    iVar1 = FUN__text__004698a0(param_1);
    if (iVar1 != 0) {
      FUN__text__0047e240(param_1);
    }
  }
  else {
    local_30 = FUN__text__0047a8e0(param_1);
    FUN__text__0047d190(param_1,*(undefined1 *)(local_30 + 0x3c),*(undefined1 *)(local_30 + 0x3d));
  }
LAB__text__0047e21f:
  local_8 = 0x47e22c;
  FUN__text__0056ce80();
  return;
}

