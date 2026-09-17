
void __fastcall FUN__text__0049ba60(int param_1)

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
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x108b50) != 0) && (*(int *)(param_1 + 0x108b54) == 2)) {
    local_10 = 0;
    for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
      iVar1 = FUN__text__0046a120(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
      if (iVar1 == 0) {
        local_10 = local_10 + 1;
      }
    }
    if (*(int *)(local_8 + 0x108b50) != local_10) {
      *(undefined1 *)(local_8 + 0x2f156) = 1;
      goto LAB__text__0049bb07;
    }
  }
  *(undefined1 *)(local_8 + 0x2f156) = 0;
LAB__text__0049bb07:
  local_8 = 0x49bb1a;
  FUN__text__0056ce80();
  return;
}

