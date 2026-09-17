
void __fastcall FUN__text__00414190(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0xb20c) != 0) {
    local_8 = param_1;
    for (local_10 = 0; *(int *)(&DAT_005ff4ac + local_10 * 4) != 0; local_10 = local_10 + 1) {
      (**(code **)(**(int **)(local_8 + 0xb20c) + 0x28))
                (*(undefined4 *)(local_8 + 0xb20c),*(undefined4 *)(local_8 + 0xb318),
                 *(undefined4 *)(local_8 + 0xb314),*(undefined4 *)(local_8 + 0xb3e8),1,1,
                 *(undefined4 *)(&DAT_005ff4ac + local_10 * 4));
      local_c = FUN__text__0056ce80();
      if (-1 < local_c) {
        *(undefined4 *)(local_8 + 0xb268) = *(undefined4 *)(&DAT_005ff4ac + local_10 * 4);
        goto LAB__text__00414267;
      }
    }
    *(undefined4 *)(local_8 + 0xb268) = 0;
  }
LAB__text__00414267:
  local_8 = 0x414274;
  FUN__text__0056ce80();
  return;
}

