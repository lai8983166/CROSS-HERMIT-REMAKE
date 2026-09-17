
/* WARNING: Removing unreachable block (ram,0x0049bd4b) */
/* WARNING: Removing unreachable block (ram,0x0049bd61) */

void __thiscall FUN__text__0049bc90(int param_1,int param_2,uint param_3)

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
  if ((*(int *)(param_1 + 0x108b50) != 0) && (param_2 == 0)) {
    local_8 = param_1;
    for (local_10 = 0; local_10 != *(int *)(local_8 + 0x108b50); local_10 = local_10 + 1) {
      local_c = *(int *)(local_8 + 0x108b60 + local_10 * 4);
      iVar1 = FUN__text__0046a430(local_c);
      if (((iVar1 != 0) && (iVar1 = FUN__text__004690a0(local_c), iVar1 == 0)) &&
         (*(byte *)(*(int *)(local_c + 600) + 0x9f) != param_3)) {
        FUN__text__0049bd90(local_c,param_3);
      }
    }
  }
  local_8 = 0x49bd86;
  FUN__text__0056ce80();
  return;
}

