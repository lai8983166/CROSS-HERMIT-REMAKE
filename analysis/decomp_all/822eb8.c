
/* WARNING: Removing unreachable block (ram,0x00822f1f) */
/* WARNING: Removing unreachable block (ram,0x00822eea) */
/* WARNING: Removing unreachable block (ram,0x00822eec) */
/* WARNING: Removing unreachable block (ram,0x00822f21) */

void __thiscall FUN__text1__00822eb8(undefined4 param_1,undefined4 param_2,int param_3)

{
  uint local_8;
  
  local_8 = (DAT_0086e390 ^ DAT_0086e394) << 1;
  if (param_3 == 0) {
    local_8 = local_8 | 1;
  }
  (*(code *)PTR_DAT_00872c10)(local_8,param_1);
  return;
}

