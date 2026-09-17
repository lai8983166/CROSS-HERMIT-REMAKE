
void __thiscall
FUN__text__004b66f0(int param_1,undefined4 *param_2,short param_3,char param_4,char param_5)

{
  short sVar1;
  undefined2 uVar2;
  undefined4 uVar3;
  int iVar4;
  ushort uVar5;
  undefined4 *puVar6;
  undefined4 *puVar7;
  undefined4 uVar8;
  undefined *puVar9;
  undefined4 uVar10;
  undefined4 local_68 [16];
  char local_28;
  char local_24;
  ushort local_20;
  undefined2 uStack_1e;
  undefined4 *local_1c;
  uint local_18;
  short local_14;
  undefined2 uStack_12;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar6 = local_68;
  for (iVar4 = 0x19; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  for (local_c = 0; local_c < 0x28; local_c = local_c + 1) {
    *(undefined1 *)(param_1 + local_c + 0x41) = 0;
  }
  *(undefined2 *)(param_1 + 0x30) = *(undefined2 *)((int)param_2 + 6);
  for (local_c = 0; local_c < 0xf; local_c = local_c + 1) {
    *(undefined1 *)(param_1 + local_c + 0x32) = 1;
  }
  for (local_c = 0; local_c < *(short *)(param_1 + 0x594); local_c = local_c + 1) {
    *(char *)(param_1 + 0x41 +
             (int)*(short *)(&DAT_007e17ee + *(short *)(param_1 + 0x596 + local_c * 2) * 0x4a0)) =
         *(char *)(param_1 + 0x41 +
                  (int)*(short *)(&DAT_007e17ee + *(short *)(param_1 + 0x596 + local_c * 2) * 0x4a0)
                  ) + '\x01';
  }
  *(undefined1 *)(param_1 + 0x69) = *(undefined1 *)((int)param_2 + 0x72);
  if (param_3 < 1) {
    *(undefined2 *)(param_1 + 0xc84) = *(undefined2 *)((int)param_2 + 6);
    *(undefined2 *)(param_1 + 0x632) = *(undefined2 *)(param_1 + 0xc84);
    *(undefined *)(param_1 + 0x570) = (&DAT_006b2d8c)[*(short *)((int)param_2 + 6) * 0x40];
    *(undefined *)(param_1 + 0x582) = (&DAT_006b2d8b)[*(short *)((int)param_2 + 6) * 0x40];
  }
  else {
    *(short *)(param_1 + 0xc84) = param_3;
  }
  puVar6 = param_2;
  puVar7 = (undefined4 *)(param_1 + 0x634);
  for (iVar4 = 0x128; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar7 = *puVar6;
    puVar6 = puVar6 + 1;
    puVar7 = puVar7 + 1;
  }
  *(undefined2 *)(param_1 + 0x63a) = *(undefined2 *)(param_1 + 0xc84);
  local_24 = param_5;
  if (param_5 == '\x01') {
    for (local_c = 0; local_c < 8; local_c = local_c + 1) {
      if (*(short *)((int)param_2 + local_c * 2 + 0x52) != 0) {
        *(undefined1 *)(param_2 + (*(short *)((int)param_2 + local_c * 2 + 0x52) + -1) * 3 + 0x2e) =
             3;
        *(undefined2 *)((int)param_2 + local_c * 2 + 0x52) = 0;
      }
    }
    for (local_c = 0; local_c < 8; local_c = local_c + 1) {
      if (*(short *)((int)param_2 + local_c * 2 + 0x62) != 0) {
        *(ushort *)(&DAT_007aacaa + *(short *)((int)param_2 + local_c * 2 + 0x62) * 2) =
             *(ushort *)(&DAT_007aacaa + *(short *)((int)param_2 + local_c * 2 + 0x62) * 2) & 0xf0ff
             | 0x100;
        *(undefined2 *)((int)param_2 + local_c * 2 + 0x62) = 0;
      }
    }
  }
  else if (param_5 == '\x02') {
    for (local_c = 0; local_c < 8; local_c = local_c + 1) {
      *(undefined2 *)(param_1 + 0x686 + local_c * 2) = 0;
      *(undefined2 *)(param_1 + 0x696 + local_c * 2) = 0;
    }
  }
  local_8 = param_1;
  FUN__text__004b93c0(param_1 + 0x634,param_1 + 0xad4,param_1 + 0xc34);
  uVar2 = FUN__text__004d1ba0((uint)*(byte *)(local_8 + 0xad8) + (uint)*(byte *)(local_8 + 0xad9) +
                              (uint)*(byte *)(local_8 + 0xada) + (uint)*(byte *)(local_8 + 0xadb) +
                              (uint)*(byte *)(local_8 + 0xadc) + (uint)*(byte *)(local_8 + 0xadd) +
                              (uint)*(byte *)(local_8 + 0xade),0,999);
  *(undefined2 *)(local_8 + 0xc82) = uVar2;
  local_28 = param_4;
  if (param_4 == '\x01') {
    puVar6 = (undefined4 *)(local_8 + 0xad4);
    puVar7 = (undefined4 *)(local_8 + 0xb84);
    for (iVar4 = 0x2c; iVar4 != 0; iVar4 = iVar4 + -1) {
      *puVar7 = *puVar6;
      puVar6 = puVar6 + 1;
      puVar7 = puVar7 + 1;
    }
    *(undefined2 *)(local_8 + 0xc80) = *(undefined2 *)(local_8 + 0xc82);
  }
  for (local_c = 0; local_c < 0x168; local_c = local_c + 1) {
    FUN__text__004b5af0(param_2,local_c + 1);
  }
  for (local_c = 0; local_c < 0x54; local_c = local_c + 1) {
    FUN__text__004b5c90(param_2,local_c + 1);
  }
  DAT_007d7704 = 0;
  DAT_007d7706 = 0;
  local_1c = param_2;
  for (local_c = 0; local_c < 8; local_c = local_c + 1) {
    sVar1 = *(short *)((int)local_1c + local_c * 2 + 0x62);
    local_10 = CONCAT22(local_10._2_2_,sVar1);
    if (sVar1 != 0) {
      FUN__text__004077c0(DAT_007a49fc);
      uVar10 = 2;
      puVar9 = (&PTR_DAT_006e3150)[local_10 & 0xffff];
      uVar8 = *(undefined4 *)(local_8 + 0xc8c);
      uVar3 = FUN__text__004142b0(uVar8,puVar9,2);
      FUN__text__00408e30(uVar3,uVar8,puVar9,uVar10);
      local_18 = local_18 & 0xffff0000;
      while ((local_18 & 0xffff) < 3) {
        _local_14 = CONCAT22(uStack_12,
                             (short)(char)(&DAT_006d514d)
                                          [(local_18 & 0xffff) +
                                           *(short *)((int)local_1c + local_c * 2 + 0x62) * 0x38]);
        if ((char)(&DAT_006d514d)
                  [(local_18 & 0xffff) + *(short *)((int)local_1c + local_c * 2 + 0x62) * 0x38] ==
            0x19) {
          uVar5 = (ushort)(byte)(&DAT_006d5140)
                                [*(short *)((int)local_1c + local_c * 2 + 0x62) * 0x38];
          _local_20 = CONCAT22(uStack_1e,uVar5);
          if ((short)DAT_007d7706 < (short)(ushort)(byte)(&DAT_006f408b)[(uint)uVar5 * 0x10]) {
            DAT_007d7706 = (ushort)(byte)(&DAT_006f408b)[(uint)uVar5 * 0x10];
            DAT_007d7704 = uVar5;
          }
        }
        local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
      }
    }
  }
  local_8 = 0x4b6c58;
  FUN__text__0056ce80();
  return;
}

