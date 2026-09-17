
int * FUN_0057ad20(uint param_1)

{
  undefined **ppuVar1;
  int *piVar2;
  int *piVar3;
  undefined *puVar4;
  undefined **local_24;
  int *local_20;
  int local_1c;
  int local_18;
  undefined **local_14;
  int local_c;
  int *local_8;
  
  local_24 = (undefined **)PTR_LOOP_00764158;
  do {
    if (local_24[4] != (undefined *)0xffffffff) {
      local_8 = (int *)local_24[2];
      local_c = (int)local_24[4] + ((int)local_8 - (int)(local_24 + 6) >> 3) * 0x1000;
      for (; local_8 < local_24 + 0x806; local_8 = local_8 + 2) {
        if (((int)param_1 <= *local_8) && (param_1 < (uint)local_8[1])) {
          piVar2 = (int *)FUN_0057b0e0(local_c,*local_8,param_1);
          if (piVar2 != (int *)0x0) {
            PTR_LOOP_00764158 = (undefined *)local_24;
            *local_8 = *local_8 - param_1;
            local_24[2] = (undefined *)local_8;
            return piVar2;
          }
          local_8[1] = param_1;
        }
        local_c = local_c + 0x1000;
      }
      piVar2 = (int *)local_24[2];
      local_c = (int)local_24[4];
      for (local_8 = (int *)(local_24 + 6); local_8 < piVar2; local_8 = local_8 + 2) {
        if (((int)param_1 <= *local_8) && (param_1 < (uint)local_8[1])) {
          piVar3 = (int *)FUN_0057b0e0(local_c,*local_8,param_1);
          if (piVar3 != (int *)0x0) {
            PTR_LOOP_00764158 = (undefined *)local_24;
            *local_8 = *local_8 - param_1;
            local_24[2] = (undefined *)local_8;
            return piVar3;
          }
          local_8[1] = param_1;
        }
        local_c = local_c + 0x1000;
      }
    }
    local_24 = (undefined **)*local_24;
  } while (local_24 != (undefined **)PTR_LOOP_00764158);
  local_24 = &PTR_LOOP_00762138;
  while ((local_24[4] == (undefined *)0xffffffff || (local_24[3] == (undefined *)0x0))) {
    local_24 = (undefined **)*local_24;
    if (local_24 == &PTR_LOOP_00762138) {
      puVar4 = (undefined *)FUN_0057a860();
      if (puVar4 == (undefined *)0x0) {
        piVar2 = (int *)0x0;
      }
      else {
        piVar2 = *(int **)(puVar4 + 0x10);
        *(undefined1 *)(piVar2 + 2) = (undefined1)param_1;
        PTR_LOOP_00764158 = puVar4;
        *piVar2 = (int)piVar2 + param_1 + 8;
        piVar2[1] = 0xf0 - param_1;
        *(uint *)(puVar4 + 0x18) = *(int *)(puVar4 + 0x18) - (param_1 & 0xff);
        piVar2 = piVar2 + 0x40;
      }
      return piVar2;
    }
  }
  ppuVar1 = (undefined **)local_24[3];
  piVar2 = (int *)(local_24[4] + ((int)ppuVar1 - (int)(local_24 + 6) >> 3) * 0x1000);
  local_14 = ppuVar1;
  for (local_18 = 0; (*local_14 == (undefined *)0xffffffff && (local_18 < 0x10));
      local_18 = local_18 + 1) {
    local_14 = local_14 + 2;
  }
  piVar3 = (int *)(*API_KERNEL32_DLL_VirtualAlloc)(piVar2,local_18 << 0xc,0x1000,4);
  if (piVar3 == piVar2) {
    _memset(piVar2,local_18 << 0xc,0);
    local_20 = piVar2;
    local_14 = ppuVar1;
    for (local_1c = 0; local_1c < local_18; local_1c = local_1c + 1) {
      *local_20 = (int)(local_20 + 2);
      local_20[1] = 0xf0;
      *(undefined1 *)(local_20 + 0x3e) = 0xff;
      *local_14 = (undefined *)0xf0;
      local_14[1] = (undefined *)0xf1;
      local_20 = local_20 + 0x400;
      local_14 = local_14 + 2;
    }
    PTR_LOOP_00764158 = (undefined *)local_24;
    for (; (local_14 < local_24 + 0x806 && (*local_14 != (undefined *)0xffffffff));
        local_14 = local_14 + 2) {
    }
    local_24[3] = (undefined *)(-(uint)(local_14 < local_24 + 0x806) & (uint)local_14);
    *(undefined1 *)(piVar2 + 2) = (undefined1)param_1;
    local_24[2] = (undefined *)ppuVar1;
    *ppuVar1 = *ppuVar1 + -param_1;
    *piVar2 = (int)piVar2 + param_1 + 8;
    piVar2[1] = piVar2[1] - param_1;
    return piVar2 + 0x40;
  }
  return (int *)0x0;
}

