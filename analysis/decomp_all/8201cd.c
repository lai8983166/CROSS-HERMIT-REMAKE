
/* WARNING: Instruction at (ram,0x00820265) overlaps instruction at (ram,0x00820264)
    */
/* WARNING: Removing unreachable block (ram,0x00820254) */
/* WARNING: Removing unreachable block (ram,0x0082020e) */
/* WARNING: Removing unreachable block (ram,0x00820210) */
/* WARNING: Removing unreachable block (ram,0x00820256) */

void FUN__text1__008201cd(undefined4 param_1)

{
  uint uVar1;
  undefined4 local_c;
  
  uVar1 = (*(code *)PTR_DAT_00872c98)(param_1);
  local_c = (DAT_0086e3c8 ^ DAT_0086e3cc) << 1;
  if ((uVar1 & 0xffff0001) != 0) {
    local_c = local_c | 1;
  }
  (*(code *)PTR_DAT_00872c48)(local_c);
  return;
}

