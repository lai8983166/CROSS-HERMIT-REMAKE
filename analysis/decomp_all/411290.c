
void __fastcall FUN__text__00411290(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  uint *local_c;
  int *local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (uint *)(param_1 + 0x224);
  if ((*param_1 != 0) && (param_1[1] != 0)) {
    local_8 = param_1;
    _memset(param_1 + 3,0,0x100);
    (**(code **)(*(int *)local_8[1] + 0x24))(local_8[1],0x100,local_8 + 3);
    local_10 = FUN__text__0056ce80();
    if (local_10 < 0) {
      local_24 = local_10;
      if ((local_10 == -0x7ff8fff4) || (local_10 == -0x7ff8ffe2)) {
        local_20 = 0;
        while( true ) {
          (**(code **)(*(int *)local_8[1] + 0x1c))(local_8[1]);
          local_28 = FUN__text__0056ce80();
          local_10 = local_28;
          if ((local_28 != -0x7ff8ffe2) || (local_20 = local_20 + 1, 10000 < local_20)) break;
          local_28 = -0x7ff8ffe2;
          local_10 = -0x7ff8ffe2;
        }
      }
      if (local_10 < 0) {
        _memset(local_8 + 3,0,0x100);
      }
      else {
        (**(code **)(*(int *)local_8[1] + 0x24))(local_8[1],0x100,local_8 + 3);
        local_10 = FUN__text__0056ce80();
      }
    }
    FUN__text__0056d4d0(local_8 + 0xe0,local_8 + 0x120,0x100);
    FUN__text__0056d4d0(local_8 + 0x120,local_8 + 3,0x100);
    for (local_14 = 0; local_14 != 0x100; local_14 = local_14 + 1) {
      *(byte *)((int)local_8 + local_14 + 0x480) = *(byte *)((int)local_8 + local_14 + 0x480) & 0x80
      ;
    }
    for (local_14 = 0; local_14 != 0x100; local_14 = local_14 + 1) {
      *(byte *)((int)local_8 + local_14 + 0x580) =
           (*(byte *)((int)local_8 + local_14 + 0x380) ^ *(byte *)((int)local_8 + local_14 + 0x480))
           & *(byte *)((int)local_8 + local_14 + 0x480);
      *(byte *)((int)local_8 + local_14 + 0x780) =
           (*(byte *)((int)local_8 + local_14 + 0x380) ^ *(byte *)((int)local_8 + local_14 + 0x480))
           & *(byte *)((int)local_8 + local_14 + 0x380);
    }
    FUN__text__0056d4d0(local_8 + 0x1a0,local_8 + 0x160,0x100);
    local_18 = 0;
    local_1c = 0;
    for (local_14 = 0; local_14 != 0x100; local_14 = local_14 + 1) {
      if (*(char *)((int)local_8 + local_14 + 0x380) == *(char *)((int)local_8 + local_14 + 0x480))
      {
        local_18 = local_18 + 1;
      }
      if (*(char *)((int)local_8 + local_14 + 0x480) != '\0') {
        local_1c = local_1c + 1;
      }
    }
    if ((local_18 == 0x100) && (local_1c != 0)) {
      if (local_8[0x223] == 0) {
        if (local_8[0x220] <= local_8[0x222]) {
          local_8[0x223] = 1;
          local_8[0x222] = 0;
          for (local_14 = 0; local_14 != 0x100; local_14 = local_14 + 1) {
            *(byte *)((int)local_8 + local_14 + 0x680) =
                 *(byte *)((int)local_8 + local_14 + 0x680) |
                 *(byte *)((int)local_8 + local_14 + 0x480);
          }
        }
      }
      else if (local_8[0x221] <= local_8[0x222]) {
        local_8[0x223] = 1;
        local_8[0x222] = 0;
        for (local_14 = 0; local_14 != 0x100; local_14 = local_14 + 1) {
          *(byte *)((int)local_8 + local_14 + 0x680) =
               *(byte *)((int)local_8 + local_14 + 0x680) |
               *(byte *)((int)local_8 + local_14 + 0x480);
        }
      }
      local_8[0x222] = local_8[0x222] + 1;
    }
    else {
      local_8[0x223] = 0;
      local_8[0x222] = 0;
    }
    *local_c = local_c[1];
    local_c[1] = 0;
    if ((*(byte *)(local_8 + 0x152) & 0x80) != 0) {
      local_c[1] = local_c[1] | 1;
    }
    if ((*(byte *)(local_8 + 0x154) & 0x80) != 0) {
      local_c[1] = local_c[1] | 2;
    }
    if ((*(byte *)((int)local_8 + 0x54b) & 0x80) != 0) {
      local_c[1] = local_c[1] | 4;
    }
    if ((*(byte *)((int)local_8 + 0x54d) & 0x80) != 0) {
      local_c[1] = local_c[1] | 8;
    }
    if ((*(byte *)((int)local_8 + 0x4d2) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x10;
    }
    if ((*(byte *)((int)local_8 + 0x4cf) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x20;
    }
    if ((*(byte *)(local_8 + 0x134) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x40;
    }
    if ((*(byte *)((int)local_8 + 0x4d1) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x80;
    }
    if ((*(byte *)((int)local_8 + 0x4cb) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x100;
    }
    if ((*(byte *)(local_8 + 0x133) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x200;
    }
    if ((*(byte *)((int)local_8 + 0x4cd) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x400;
    }
    if ((*(byte *)((int)local_8 + 0x4c7) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x800;
    }
    if ((*(byte *)(local_8 + 0x132) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x1000;
    }
    if ((*(byte *)((int)local_8 + 0x4c9) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x2000;
    }
    if ((*(byte *)(local_8 + 0x127) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x4000;
    }
    if ((*(byte *)((int)local_8 + 0x4b9) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x8000;
    }
    if ((*(byte *)((int)local_8 + 0x481) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x10000;
    }
    if ((*(byte *)((int)local_8 + 0x4aa) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x20000;
    }
    if ((*(byte *)((int)local_8 + 0x4b6) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x20000;
    }
    if ((*(byte *)((int)local_8 + 0x49d) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x40000;
    }
    if ((*(byte *)((int)local_8 + 0x51d) & 0x80) != 0) {
      local_c[1] = local_c[1] | 0x40000;
    }
    local_c[2] = (*local_c ^ local_c[1]) & local_c[1];
    local_c[4] = (*local_c ^ local_c[1]) & *local_c;
    local_c[3] = 0;
    if ((*(byte *)(local_8 + 0x1d2) & 0x80) != 0) {
      local_c[3] = local_c[3] | 1;
    }
    if ((*(byte *)(local_8 + 0x1d4) & 0x80) != 0) {
      local_c[3] = local_c[3] | 2;
    }
    if ((*(byte *)((int)local_8 + 0x74b) & 0x80) != 0) {
      local_c[3] = local_c[3] | 4;
    }
    if ((*(byte *)((int)local_8 + 0x74d) & 0x80) != 0) {
      local_c[3] = local_c[3] | 8;
    }
    if ((*(byte *)((int)local_8 + 0x6d2) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x10;
    }
    if ((*(byte *)((int)local_8 + 0x6cf) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x20;
    }
    if ((*(byte *)(local_8 + 0x1b4) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x40;
    }
    if ((*(byte *)((int)local_8 + 0x6d1) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x80;
    }
    if ((*(byte *)((int)local_8 + 0x6cb) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x100;
    }
    if ((*(byte *)(local_8 + 0x1b3) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x200;
    }
    if ((*(byte *)((int)local_8 + 0x6cd) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x400;
    }
    if ((*(byte *)((int)local_8 + 0x6c7) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x800;
    }
    if ((*(byte *)(local_8 + 0x1b2) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x1000;
    }
    if ((*(byte *)((int)local_8 + 0x6c9) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x2000;
    }
    if ((*(byte *)(local_8 + 0x1a7) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x4000;
    }
    if ((*(byte *)((int)local_8 + 0x6b9) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x8000;
    }
    if ((*(byte *)((int)local_8 + 0x681) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x10000;
    }
    if ((*(byte *)((int)local_8 + 0x6aa) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x20000;
    }
    if ((*(byte *)((int)local_8 + 0x6b6) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x20000;
    }
    if ((*(byte *)((int)local_8 + 0x69d) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x40000;
    }
    if ((*(byte *)((int)local_8 + 0x71d) & 0x80) != 0) {
      local_c[3] = local_c[3] | 0x40000;
    }
  }
  local_8 = (int *)0x411cef;
  FUN__text__0056ce80();
  return;
}

