
void FUN__text__00473570(short param_1,short param_2,undefined2 param_3,int param_4,int param_5,
                        uint param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004077c0(DAT_007a49fc);
  *(char *)(local_8 + 0xde797) = (char)(param_6 >> 0x18);
  if (*(char *)(local_8 + 0xde797) == -1) {
    *(undefined4 *)(local_8 + 0xde78c) = 0;
  }
  else {
    *(undefined4 *)(local_8 + 0xde78c) = 1;
  }
  *(char *)(local_8 + 0xde796) = (char)((param_6 & 0xff0000) / 0x20000);
  *(char *)(local_8 + 0xde795) = (char)((param_6 & 0xff00) / 0x200);
  *(char *)(local_8 + 0xde794) = (char)((param_6 & 0xff) / 2);
  *(undefined2 *)(local_8 + 0xde7a6) = param_3;
  FUN__text__00407870(0x5a,0x14);
  *(ushort *)(local_8 + 0xde788) = *(ushort *)(local_8 + 0xde788) | 0x40;
  *(undefined2 *)(local_8 + 0xde768) = *(undefined2 *)(&DAT_00618958 + param_5 * 0xe0);
  *(undefined2 *)(local_8 + 0xde76a) = *(undefined2 *)(&DAT_0061895c + param_5 * 0xe0);
  local_14 = 7;
  for (local_10 = param_4; local_10 != 3; local_10 = local_10 + 1) {
    for (local_c = 0; local_c != 2; local_c = local_c + 1) {
      *(undefined2 *)(local_8 + 0xde7a8) = *(undefined2 *)(&DAT_00618a20 + param_5 * 0xe0);
      *(undefined2 *)(local_8 + 0xde7aa) = *(undefined2 *)(&DAT_00618a24 + param_5 * 0xe0);
      *(short *)(local_8 + 0xde7ac) = *(short *)(local_8 + 0xde7a8) + *(short *)(local_8 + 0xde768);
      *(short *)(local_8 + 0xde7ae) = *(short *)(local_8 + 0xde7aa) + *(short *)(local_8 + 0xde76a);
      FUN__text__004079c0((int)param_1,(int)param_2);
      param_1 = param_1 + local_14;
    }
    if (local_10 == 2) break;
    *(undefined2 *)(local_8 + 0xde7a8) = *(undefined2 *)(&DAT_006189f0 + param_5 * 0xe0);
    *(undefined2 *)(local_8 + 0xde7aa) = *(undefined2 *)(&DAT_006189f4 + param_5 * 0xe0);
    *(short *)(local_8 + 0xde7ac) = *(short *)(local_8 + 0xde7a8) + *(short *)(local_8 + 0xde768);
    *(short *)(local_8 + 0xde7ae) = *(short *)(local_8 + 0xde7aa) + *(short *)(local_8 + 0xde76a);
    FUN__text__004079c0((int)param_1,(int)param_2);
    param_1 = param_1 + local_14;
  }
  local_8 = 0x47384c;
  FUN__text__0056ce80();
  return;
}

