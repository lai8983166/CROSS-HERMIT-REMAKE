
void FUN__text__0057d5b0(void)

{
  int iVar1;
  uint uVar2;
  undefined4 *puVar3;
  int *piVar4;
  int local_70;
  int local_6c;
  int local_68;
  byte *local_64;
  int local_60;
  uint local_5c;
  undefined4 *local_54;
  undefined1 local_4c [50];
  short local_1a;
  undefined2 uStack_18;
  undefined2 uStack_16;
  byte *local_8;
  
  local_54 = (undefined4 *)__malloc_dbg(0x480,2,"ioinit.c",0x81);
  if (local_54 == (undefined4 *)0x0) {
    __amsg_exit(0x1b);
  }
  DAT_0080a900 = 0x20;
  DAT_0080a800 = local_54;
  for (; local_54 < DAT_0080a800 + 0x120; local_54 = local_54 + 9) {
    *(undefined1 *)(local_54 + 1) = 0;
    *local_54 = 0xffffffff;
    *(undefined1 *)((int)local_54 + 5) = 10;
    local_54[2] = 0;
  }
  (*DAT_00592180)(local_4c);
  if ((local_1a != 0) && (CONCAT22(uStack_16,uStack_18) != 0)) {
    local_6c = *(int *)CONCAT22(uStack_16,uStack_18);
    local_8 = (byte *)(CONCAT22(uStack_16,uStack_18) + 4);
    local_64 = local_8 + local_6c;
    if (0x7ff < local_6c) {
      local_6c = 0x800;
    }
    local_68 = local_6c;
    local_60 = 1;
    while (DAT_0080a900 < local_6c) {
      local_54 = (undefined4 *)__malloc_dbg(0x480,2,"ioinit.c",0xb6);
      if (local_54 == (undefined4 *)0x0) {
        local_68 = DAT_0080a900;
        break;
      }
      (&DAT_0080a800)[local_60] = local_54;
      DAT_0080a900 = DAT_0080a900 + 0x20;
      for (; local_54 < (undefined4 *)((int)(&DAT_0080a800)[local_60] + 0x480);
          local_54 = local_54 + 9) {
        *(undefined1 *)(local_54 + 1) = 0;
        *local_54 = 0xffffffff;
        *(undefined1 *)((int)local_54 + 5) = 10;
        local_54[2] = 0;
      }
      local_60 = local_60 + 1;
    }
    for (local_5c = 0; (int)local_5c < local_68; local_5c = local_5c + 1) {
      if (((*(int *)local_64 != -1) && ((*local_8 & 1) != 0)) &&
         (((*local_8 & 8) != 0 || (iVar1 = (*DAT_00592104)(*(undefined4 *)local_64), iVar1 != 0))))
      {
        puVar3 = (undefined4 *)((int)(&DAT_0080a800)[(int)local_5c >> 5] + (local_5c & 0x1f) * 0x24)
        ;
        *puVar3 = *(undefined4 *)local_64;
        *(byte *)(puVar3 + 1) = *local_8;
      }
      local_8 = local_8 + 1;
      local_64 = local_64 + 4;
    }
  }
  for (local_5c = 0; (int)local_5c < 3; local_5c = local_5c + 1) {
    piVar4 = DAT_0080a800 + local_5c * 9;
    if (*piVar4 == -1) {
      *(undefined1 *)(piVar4 + 1) = 0x81;
      if (local_5c == 0) {
        local_70 = -10;
      }
      else {
        local_70 = -0xb - (uint)(local_5c != 1);
      }
      iVar1 = (*API_KERNEL32_DLL_GetStdHandle)(local_70);
      if ((iVar1 == -1) || (uVar2 = (*DAT_00592104)(iVar1), uVar2 == 0)) {
        *(byte *)(piVar4 + 1) = *(byte *)(piVar4 + 1) | 0x40;
      }
      else {
        *piVar4 = iVar1;
        if ((uVar2 & 0xff) == 2) {
          *(byte *)(piVar4 + 1) = *(byte *)(piVar4 + 1) | 0x40;
        }
        else if ((uVar2 & 0xff) == 3) {
          *(byte *)(piVar4 + 1) = *(byte *)(piVar4 + 1) | 8;
        }
      }
    }
    else {
      *(byte *)(piVar4 + 1) = *(byte *)(piVar4 + 1) | 0x80;
    }
  }
  (*DAT_00592118)(DAT_0080a900);
  return;
}

