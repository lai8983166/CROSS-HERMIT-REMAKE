
void __thiscall FUN__text__0046f8b0(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  short local_1c;
  short local_18;
  undefined2 local_14;
  undefined2 local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  if (param_2 == 0) {
    if ((((DAT_00617ed0 <= *(int *)(param_1 + 0x2a320)) &&
         (*(int *)(param_1 + 0x2a328) <= DAT_00617ed8)) &&
        (DAT_00617ed4 <= *(int *)(param_1 + 0x2a324))) &&
       (*(int *)(param_1 + 0x2a32c) <= DAT_00617edc)) {
      local_c = 1;
    }
    if (((DAT_00617ee0 <= *(int *)(param_1 + 0x2a320)) &&
        (*(int *)(param_1 + 0x2a328) <= DAT_00617ee8)) &&
       ((DAT_00617ee4 <= *(int *)(param_1 + 0x2a324) &&
        (*(int *)(param_1 + 0x2a32c) <= DAT_00617eec)))) {
      local_c = local_c | 2;
    }
  }
  else {
    local_18 = (short)(DAT_00617eb8 / 2);
    local_1c = (short)(DAT_00617ebc / 2);
    iVar2 = DAT_00617eb0 + local_18;
    local_10 = (undefined2)iVar2;
    iVar1 = DAT_00617eb4 + local_1c;
    local_14 = (undefined2)iVar1;
    local_8 = param_1;
    iVar1 = FUN__text__0046fff0(*(undefined2 *)(param_1 + 0x2a330),
                                *(undefined2 *)(param_1 + 0x2a334),
                                *(undefined2 *)(param_1 + 0x2a338),
                                CONCAT22((short)((uint)iVar1 >> 0x10),
                                         *(undefined2 *)(param_1 + 0x2a33c)),iVar2,iVar1,
                                CONCAT22(local_1c >> 0xf,local_18),
                                CONCAT22((short)((uint)iVar2 >> 0x10),local_1c));
    if (iVar1 != 0) {
      local_c = local_c | 1;
    }
    local_18 = (short)(DAT_00617ec8 / 2);
    local_1c = (short)(DAT_00617ecc / 2);
    iVar1 = DAT_00617ec0 + local_18;
    local_10 = (undefined2)iVar1;
    iVar2 = DAT_00617ec4 + local_1c;
    local_14 = (undefined2)iVar2;
    iVar1 = FUN__text__0046fff0(*(undefined2 *)(local_8 + 0x2a330),
                                *(undefined2 *)(local_8 + 0x2a334),
                                *(undefined2 *)(local_8 + 0x2a338),
                                CONCAT22((short)((uint)iVar2 >> 0x10),
                                         *(undefined2 *)(local_8 + 0x2a33c)),iVar1,iVar2,
                                CONCAT22(local_1c >> 0xf,local_18),
                                CONCAT22((short)((uint)iVar1 >> 0x10),local_1c));
    if (iVar1 != 0) {
      local_c = local_c | 2;
    }
  }
  local_8 = 0x46faac;
  FUN__text__0056ce80();
  return;
}

