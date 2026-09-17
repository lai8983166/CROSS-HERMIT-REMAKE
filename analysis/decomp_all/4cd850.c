
/* WARNING: Removing unreachable block (ram,0x004cd89e) */

uint FUN__text__004cd850(uint param_1,uint param_2,uint param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int)((param_3 & 0xffff) * (param_1 & 0xffff)) / (int)(param_2 & 0xffff) & 0xffff;
  if ((param_3 & 0xffff) < local_c) {
    local_c = param_3 & 0xffff;
  }
  return local_c;
}

