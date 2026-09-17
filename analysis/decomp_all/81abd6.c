
/* WARNING: Removing unreachable block (ram,0x0081ac07) */
/* WARNING: Removing unreachable block (ram,0x0081ac09) */
/* WARNING: Removing unreachable block (ram,0x0081ac26) */
/* WARNING: Removing unreachable block (ram,0x0081ac28) */
/* WARNING: Removing unreachable block (ram,0x0081ac43) */
/* WARNING: Removing unreachable block (ram,0x0081ac45) */

void FUN__text1__0081abd6(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c60)(param_1);
  local_c = (DAT_0086e390 ^ DAT_0086e394) << 1;
  if ((uVar1 & 0xffff0001) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c10)(local_c);
  return;
}

