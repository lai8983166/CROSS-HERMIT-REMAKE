
void FUN__text__0041df60(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0041d790();
  if (iVar1 != 0) {
    (**(code **)(**(int **)(local_8 + 8) + 0xc))(*(undefined4 *)(local_8 + 8),local_8 + 0x24);
    local_c = FUN__text__0056ce80();
    if (-1 < local_c) {
      if ((*(uint *)(local_8 + 0x24) & 2) != 0) {
        FUN__text__0042b2d0(&DAT_0059468c);
      }
      if ((*(uint *)(local_8 + 0x24) & 2) != 0) {
        FUN__text__0042b2d0(&DAT_00594670);
      }
      if ((*(uint *)(local_8 + 0x24) & 4) != 0) {
        FUN__text__0042b2d0(&DAT_00594654);
      }
      if ((*(uint *)(local_8 + 0x24) & 8) != 0) {
        FUN__text__0042b2d0(&DAT_00594634);
      }
      if ((*(uint *)(local_8 + 0x24) & 0x10) != 0) {
        FUN__text__0042b2d0(&DAT_00594614);
      }
      if ((*(uint *)(local_8 + 0x24) & 0x20) != 0) {
        FUN__text__0042b2d0(&DAT_005945ec);
      }
      if ((*(uint *)(local_8 + 0x24) & 0x40) != 0) {
        FUN__text__0042b2d0(&DAT_005945d0);
      }
      if ((*(uint *)(local_8 + 0x24) & 0x80) != 0) {
        FUN__text__0042b2d0(&DAT_005945a4);
      }
      if ((*(uint *)(local_8 + 0x24) & 0x100) != 0) {
        FUN__text__0042b2d0(&DAT_00594598);
      }
      (**(code **)(**(int **)(local_8 + 8) + 0x1c))(*(undefined4 *)(local_8 + 8),local_8 + 0x28);
      local_c = FUN__text__0056ce80();
      if (-1 < local_c) {
        (**(code **)(**(int **)(local_8 + 8) + 0x28))(*(undefined4 *)(local_8 + 8),local_8 + 0x38);
        local_c = FUN__text__0056ce80();
        if (-1 < local_c) goto LAB__text__0041e129;
      }
    }
    FUN__text__0041d040(local_c);
  }
LAB__text__0041e129:
  local_8 = 0x41e136;
  FUN__text__0056ce80();
  return;
}

