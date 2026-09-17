
/* WARNING: Removing unreachable block (ram,0x00541cd4) */
/* WARNING: Removing unreachable block (ram,0x00541cc6) */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

undefined8 __fastcall FUN__text__00541cb5(undefined4 param_1,undefined4 param_2)

{
  uint *puVar1;
  int iVar2;
  undefined4 local_8;
  
  local_8 = 0;
  puVar1 = (uint *)cpuid(0x80000000);
  if (0x80000000 < *puVar1) {
    iVar2 = cpuid(0x80000001);
    local_8 = (uint)((*(uint *)(iVar2 + 8) & 0x80000000) != 0);
  }
  return CONCAT44(param_2,local_8);
}

