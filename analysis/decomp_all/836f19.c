
/* WARNING: Instruction at (ram,0x00836f9e) overlaps instruction at (ram,0x00836f9d)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x00837191) */
/* WARNING: Removing unreachable block (ram,0x00837137) */
/* WARNING: Removing unreachable block (ram,0x008370db) */
/* WARNING: Removing unreachable block (ram,0x00837015) */
/* WARNING: Removing unreachable block (ram,0x00836f6a) */
/* WARNING: Removing unreachable block (ram,0x00836fb9) */
/* WARNING: Removing unreachable block (ram,0x0083706d) */
/* WARNING: Removing unreachable block (ram,0x00837050) */
/* WARNING: Removing unreachable block (ram,0x00837086) */
/* WARNING: Removing unreachable block (ram,0x00837023) */
/* WARNING: Removing unreachable block (ram,0x00836f78) */
/* WARNING: Removing unreachable block (ram,0x00837196) */
/* WARNING: Removing unreachable block (ram,0x00837062) */
/* WARNING: Removing unreachable block (ram,0x00836f40) */
/* WARNING: Removing unreachable block (ram,0x0083718a) */
/* WARNING: Removing unreachable block (ram,0x0083717a) */
/* WARNING: Removing unreachable block (ram,0x00837060) */
/* WARNING: Removing unreachable block (ram,0x00836ff0) */
/* WARNING: Removing unreachable block (ram,0x0083706c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8
FUN__text1__00836f19(undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  void *pvVar1;
  void *pvVar2;
  int iVar3;
  int unaff_ESI;
  
  DAT_00875408 = param_2 + 0xfffU >> 0xc;
  _UNK_008753fc = param_4;
  DAT_008753f4 = param_1;
  pvVar1 = operator_new(DAT_00875408 << 2);
  DAT_00875410 = pvVar1;
  pvVar2 = operator_new(DAT_00875408 << 2);
  *(void **)(unaff_ESI + -0xc) = pvVar2;
  DAT_00875414 = *(int *)(unaff_ESI + -0xc);
  pvVar2 = operator_new(DAT_00875408 << 2);
  *(void **)(unaff_ESI + -0x10) = pvVar2;
  DAT_00875418 = *(int *)(unaff_ESI + -0x10);
  pvVar2 = operator_new(0x1000);
  *(void **)(unaff_ESI + -0x14) = pvVar2;
  DAT_0087541c = *(undefined4 *)(unaff_ESI + -0x14);
  pvVar2 = operator_new(DAT_00875408 << 2);
  *(void **)(unaff_ESI + -0x18) = pvVar2;
  iVar3 = *(int *)(unaff_ESI + -0x18);
  *(undefined4 *)(unaff_ESI + -4) = 0;
  DAT_008753e8 = iVar3;
  while (*(int *)(unaff_ESI + -4) < (int)DAT_00875408) {
    *(undefined4 *)((int)DAT_00875410 + *(int *)(unaff_ESI + -4) * 4) = 0xffffffff;
    *(undefined4 *)(DAT_00875414 + *(int *)(unaff_ESI + -4) * 4) = 0;
    *(undefined4 *)(DAT_00875418 + *(int *)(unaff_ESI + -4) * 4) = 0xffffffff;
    iVar3 = *(int *)(unaff_ESI + -4);
    *(undefined4 *)(DAT_008753e8 + iVar3 * 4) = 0;
    pvVar1 = (void *)(*(int *)(unaff_ESI + -4) + 1);
    *(void **)(unaff_ESI + -4) = pvVar1;
  }
  return CONCAT44(iVar3,pvVar1);
}

