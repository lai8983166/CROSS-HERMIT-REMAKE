
void FUN__text__0046e0f0(int param_1)

{
  int iVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  short local_1c;
  short local_18;
  undefined2 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0x1f1;
  iVar1 = FUN__text__0046a430(param_1);
  if ((iVar1 != 0) && (*(char *)(param_1 + 0x501) != -1)) {
    local_18 = *(short *)(&DAT_00617ef0 + (uint)*(byte *)(param_1 + 0x501) * 4);
    local_1c = *(short *)(&DAT_00617ef2 + (uint)*(byte *)(param_1 + 0x501) * 4) + 0x30;
    local_10 = 0x30;
    iVar1 = ((*(short *)(*(int *)(param_1 + 600) + 0x16) * 100) /
            (int)*(short *)(*(int *)(param_1 + 600) + 0x14)) * 0x30;
    local_c = iVar1 / 100;
    FUN__text__00410310(local_18 + 1,local_1c + 1,local_c,2,
                        CONCAT22((short)((uint)(iVar1 % 100) >> 0x10),local_14),0xffff0000,0);
    iVar1 = local_10 *
            ((*(short *)(*(int *)(param_1 + 600) + 0x1c) * 100) /
            (int)*(short *)(*(int *)(param_1 + 600) + 0x1a));
    local_c = iVar1 / 100;
    FUN__text__00410310(local_18 + 1,local_1c + 4,local_c,2,
                        CONCAT22((short)((uint)(iVar1 % 100) >> 0x10),local_14),0xff00ff00,0);
    if (*(short *)(param_1 + 0x10) < 1) {
      if (0 < *(short *)(param_1 + 0xc)) {
        if (*(short *)(param_1 + 0xe) == 0) {
          local_c = 0;
        }
        else {
          local_c = (*(short *)(param_1 + 0xc) * 100) / (int)*(short *)(param_1 + 0xe);
        }
        iVar1 = (local_10 * local_c) / 100;
        local_c = local_10 - iVar1;
        FUN__text__00410310(local_18 + 1,local_1c + 7,local_c,1,
                            CONCAT22((short)((uint)iVar1 >> 0x10),local_14),0xff00ffff,0);
      }
    }
    else {
      if (*(short *)(param_1 + 0x12) == 0) {
        local_c = 0;
      }
      else {
        local_c = (*(short *)(param_1 + 0x10) * 100) / (int)*(short *)(param_1 + 0x12);
      }
      iVar1 = local_10 * local_c;
      local_c = iVar1 / 100;
      FUN__text__00410310(local_18 + 1,local_1c + 7,local_c,1,
                          CONCAT22((short)((uint)(iVar1 % 100) >> 0x10),local_14),0xff00ffff,0);
    }
    iVar1 = FUN__text__004944a0(param_1);
    uVar2 = extraout_var;
    if (iVar1 != 0) {
      FUN__text__00472b90(local_18 + 0x28,local_1c + -0x10,local_14,
                          *(undefined1 *)(*(int *)(param_1 + 600) + 0x98),1,0xffffffff);
      uVar2 = extraout_var_00;
    }
    FUN__text__00410310((int)local_18,(int)local_1c,0x32,9,CONCAT22(uVar2,local_14),0xff202020,0);
  }
  local_8 = 0x46e3c3;
  FUN__text__0056ce80();
  return;
}

