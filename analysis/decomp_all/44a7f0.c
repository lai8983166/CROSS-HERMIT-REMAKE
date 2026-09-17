
undefined4 __fastcall FUN__text__0044a7f0(int param_1)

{
  bool bVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [19];
  int local_18;
  int local_10;
  int local_c;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = 0;
  for (local_c = 0; local_c != 0x28; local_c = local_c + 1) {
    *(undefined2 *)(param_1 + 0x1be0 + local_c * 2) = 0xffff;
  }
  for (local_c = 0; local_c < 5; local_c = local_c + 1) {
    for (local_10 = 0; local_10 < 4; local_10 = local_10 + 1) {
      if (*(short *)(&DAT_007aaa22 + local_10 * 2 + local_c * 0x1c) != -1) {
        *(undefined2 *)(param_1 + 0x1be0 + local_18 * 2) =
             *(undefined2 *)(&DAT_007aaa22 + local_10 * 2 + local_c * 0x1c);
        local_18 = local_18 + 1;
      }
    }
  }
  iVar2 = (int)DAT_007a5260;
  local_c = 0;
  do {
    if (local_c == iVar2) {
      return 0;
    }
    bVar1 = false;
    for (local_10 = 0; local_10 != local_18; local_10 = local_10 + 1) {
      if (*(short *)(param_1 + 0x1be0 + local_10 * 2) == *(short *)(&DAT_007a5210 + local_c * 2)) {
        bVar1 = true;
        break;
      }
    }
    if (!bVar1) {
      *(short *)(param_1 + 0x1be0 + local_18 * 2) = *(short *)(&DAT_007a5210 + local_c * 2);
      local_18 = local_18 + 1;
    }
    local_c = local_c + 1;
  } while( true );
}

