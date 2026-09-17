
void FUN__text__00472f40(short param_1,short param_2,undefined2 param_3,int param_4,int param_5,
                        int param_6,uint param_7,int param_8)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  short local_1c;
  int local_18;
  int local_14;
  byte local_10 [4];
  byte local_c;
  byte bStack_b;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((param_5 < 0) || (2 < param_5)) &&
     (iVar2 = FUN__text__00424f80("(0<=keta)&&(keta<=2)",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618c38 + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (param_8 == 0) {
    local_10[0] = (byte)((param_4 / 0xe10) % 0x3c);
    local_10[2] = (byte)((param_4 / 0x3c) % 0x3c);
    local_c = (byte)(param_4 % 0x3c);
  }
  else {
    local_10[0] = (byte)((param_4 / 6000) % 100);
    if (param_4 / 0x3c < 100) {
      local_10[2] = (byte)((param_4 / 0x3c) % 100);
    }
    else {
      local_10[2] = 99;
    }
    local_c = (byte)(param_4 % 0x3c);
  }
  local_10[1] = (byte)((ulonglong)(CONCAT12(local_10[2],(ushort)local_10[0]) & 0xff) % 10);
  local_10[3] = (byte)((ulonglong)(CONCAT12(local_c,(ushort)local_10[2]) & 0xff) % 10);
  bStack_b = local_c % 10;
  local_10[0] = (byte)((ulonglong)(CONCAT12(local_10[2],CONCAT11(local_10[1],local_10[0])) & 0xff) /
                      10);
  local_10[2] = (byte)((ulonglong)(CONCAT12(local_c,CONCAT11(local_10[3],local_10[2])) & 0xff) / 10)
  ;
  local_c = (byte)((ulonglong)(CONCAT11(bStack_b,local_c) & 0xff) / 10);
  FUN__text__004077c0(DAT_007a49fc);
  *(char *)(local_8 + 0xde797) = (char)(param_7 >> 0x18);
  if (*(char *)(local_8 + 0xde797) == -1) {
    *(undefined4 *)(local_8 + 0xde78c) = 0;
  }
  else {
    *(undefined4 *)(local_8 + 0xde78c) = 1;
  }
  *(char *)(local_8 + 0xde796) = (char)((param_7 & 0xff0000) / 0x20000);
  *(char *)(local_8 + 0xde795) = (char)((param_7 & 0xff00) / 0x200);
  *(char *)(local_8 + 0xde794) = (char)((param_7 & 0xff) / 2);
  *(undefined2 *)(local_8 + 0xde7a6) = param_3;
  FUN__text__00407870(0x5a,0x14);
  *(ushort *)(local_8 + 0xde788) = *(ushort *)(local_8 + 0xde788) | 0x40;
  *(undefined2 *)(local_8 + 0xde768) = *(undefined2 *)(&DAT_00618958 + param_6 * 0xe0);
  *(undefined2 *)(local_8 + 0xde76a) = *(undefined2 *)(&DAT_0061895c + param_6 * 0xe0);
  local_1c = 7;
  for (local_18 = param_5; local_18 != 3; local_18 = local_18 + 1) {
    for (local_14 = 0; local_14 != 2; local_14 = local_14 + 1) {
      *(undefined2 *)(local_8 + 0xde7a8) =
           *(undefined2 *)
            (&DAT_00618950 + (uint)local_10[local_14 + local_18 * 2] * 0x10 + param_6 * 0xe0);
      *(undefined2 *)(local_8 + 0xde7aa) =
           *(undefined2 *)
            (&DAT_00618954 + (uint)local_10[local_14 + local_18 * 2] * 0x10 + param_6 * 0xe0);
      *(short *)(local_8 + 0xde7ac) = *(short *)(local_8 + 0xde7a8) + *(short *)(local_8 + 0xde768);
      *(short *)(local_8 + 0xde7ae) = *(short *)(local_8 + 0xde7aa) + *(short *)(local_8 + 0xde76a);
      FUN__text__004079c0((int)param_1,(int)param_2);
      param_1 = param_1 + local_1c;
    }
    if (local_18 == 2) break;
    *(undefined2 *)(local_8 + 0xde7a8) = *(undefined2 *)(&DAT_006189f0 + param_6 * 0xe0);
    *(undefined2 *)(local_8 + 0xde7aa) = *(undefined2 *)(&DAT_006189f4 + param_6 * 0xe0);
    *(short *)(local_8 + 0xde7ac) = *(short *)(local_8 + 0xde7a8) + *(short *)(local_8 + 0xde768);
    *(short *)(local_8 + 0xde7ae) = *(short *)(local_8 + 0xde7aa) + *(short *)(local_8 + 0xde76a);
    FUN__text__004079c0((int)param_1,(int)param_2);
    param_1 = param_1 + local_1c;
  }
  local_8 = 0x47337d;
  FUN__text__0056ce80();
  return;
}

