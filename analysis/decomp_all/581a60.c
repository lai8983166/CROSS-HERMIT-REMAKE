
undefined4 FUN__text__00581a60(void)

{
  int iVar1;
  undefined4 uVar2;
  undefined2 *local_34;
  undefined1 *local_30;
  undefined2 *local_2c;
  undefined2 *local_28;
  uint local_24;
  undefined2 *local_20;
  byte *local_1c;
  uint local_18;
  byte local_12 [14];
  
  local_30 = (undefined1 *)0x0;
  local_2c = (undefined2 *)0x0;
  if (DAT_0080a62c == 0) {
    PTR_DAT_00764164 = &DAT_0076416e;
    PTR_DAT_00764168 = &DAT_0076416e;
    __free_dbg(DAT_0080a61c,2);
    __free_dbg(DAT_0080a620,2);
    DAT_0080a61c = (undefined2 *)0x0;
    DAT_0080a620 = (undefined2 *)0x0;
    uVar2 = 0;
  }
  else {
    if ((DAT_0080a63c != 0) ||
       (iVar1 = FUN__text__0058aa30(0,DAT_0080a650,0x1004,&DAT_0080a63c), iVar1 == 0)) {
      local_34 = (undefined2 *)__malloc_dbg(0x202,2,"initctyp.c",0x5c);
      local_20 = (undefined2 *)__malloc_dbg(0x202,2,"initctyp.c",0x5e);
      local_30 = (undefined1 *)__malloc_dbg(0x101,2,"initctyp.c",0x60);
      local_2c = (undefined2 *)__malloc_dbg(0x202,2,"initctyp.c",0x62);
      if ((local_34 != (undefined2 *)0x0) &&
         (((local_20 != (undefined2 *)0x0 && (local_30 != (undefined1 *)0x0)) &&
          (local_2c != (undefined2 *)0x0)))) {
        local_1c = local_30;
        for (local_24 = 0; (int)local_24 < 0x100; local_24 = local_24 + 1) {
          *local_1c = (undefined1)local_24;
          local_1c = local_1c + 1;
        }
        iVar1 = (*API_KERNEL32_DLL_GetCPInfo)(DAT_0080a63c,&local_18);
        if ((iVar1 != 0) && (local_18 < 3)) {
          DAT_00764370 = local_18 & 0xffff;
          if (1 < DAT_00764370) {
            for (local_1c = local_12; (*local_1c != 0 && (local_1c[1] != 0));
                local_1c = local_1c + 2) {
              for (local_24 = (uint)*local_1c; (int)local_24 <= (int)(uint)local_1c[1];
                  local_24 = local_24 + 1) {
                local_30[local_24] = 0;
              }
            }
          }
          iVar1 = FUN__text__00587230(1,local_30,0x100,local_34 + 1,0,0,0);
          if (iVar1 != 0) {
            *local_34 = 0;
            local_28 = local_2c;
            for (local_24 = 0; (int)local_24 < 0x100; local_24 = local_24 + 1) {
              *local_28 = (undefined2)local_24;
              local_28 = local_28 + 1;
            }
            iVar1 = FUN__text__0058acd0(1,local_2c,0x100,local_20 + 1,0,0);
            if (iVar1 != 0) {
              *local_20 = 0;
              if (1 < (int)DAT_00764370) {
                for (local_1c = local_12; (*local_1c != 0 && (local_1c[1] != 0));
                    local_1c = local_1c + 2) {
                  for (local_24 = (uint)*local_1c; (int)local_24 <= (int)(uint)local_1c[1];
                      local_24 = local_24 + 1) {
                    local_34[local_24 + 1] = 0x8000;
                  }
                }
              }
              PTR_DAT_00764164 = (undefined *)(local_34 + 1);
              PTR_DAT_00764168 = (undefined *)(local_20 + 1);
              if (DAT_0080a61c != (undefined2 *)0x0) {
                __free_dbg(DAT_0080a61c,2);
              }
              DAT_0080a61c = local_34;
              if (DAT_0080a620 != (undefined2 *)0x0) {
                __free_dbg(DAT_0080a620,2);
              }
              DAT_0080a620 = local_20;
              __free_dbg(local_30,2);
              __free_dbg(local_2c,2);
              return 0;
            }
          }
        }
      }
    }
    __free_dbg(local_34,2);
    __free_dbg(local_20,2);
    __free_dbg(local_30,2);
    __free_dbg(local_2c,2);
    uVar2 = 1;
  }
  return uVar2;
}

