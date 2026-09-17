
undefined4 FUN__text1__008411a4(int *param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int local_18;
  uint local_14;
  char *local_8;
  
  if ((param_1 == (int *)0x0) || (param_1[7] == 0)) {
    uVar3 = 0xfffffffe;
  }
  else {
    if (*(int *)param_1[7] != 0xd) {
      *(undefined4 *)param_1[7] = 0xd;
      *(undefined4 *)(param_1[7] + 4) = 0;
    }
    local_18 = param_1[1];
    if (local_18 == 0) {
      uVar3 = 0xfffffffb;
    }
    else {
      local_8 = (char *)*param_1;
      local_14 = *(uint *)(param_1[7] + 4);
      while ((local_18 != 0 && (local_14 < 4))) {
        if (*local_8 == (&DAT_00872ef0)[local_14]) {
          local_14 = local_14 + 1;
        }
        else if (*local_8 == '\0') {
          local_14 = 4 - local_14;
        }
        else {
          local_14 = 0;
        }
        local_8 = local_8 + 1;
        local_18 = local_18 + -1;
      }
      param_1[2] = (int)(local_8 + (param_1[2] - *param_1));
      *param_1 = (int)local_8;
      param_1[1] = local_18;
      *(uint *)(param_1[7] + 4) = local_14;
      if (local_14 == 4) {
        iVar1 = param_1[2];
        iVar2 = param_1[5];
        FUN__text1__008407c0(param_1);
        param_1[2] = iVar1;
        param_1[5] = iVar2;
        *(undefined4 *)param_1[7] = 7;
        uVar3 = 0;
      }
      else {
        uVar3 = 0xfffffffd;
      }
    }
  }
  return uVar3;
}

