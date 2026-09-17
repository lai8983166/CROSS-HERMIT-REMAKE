
void __thiscall FUN__text__00465040(int param_1,int param_2,int param_3,int param_4)

{
  ushort uVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  byte *local_18;
  ushort local_14;
  undefined2 uStack_12;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(short *)(param_1 + 0x48) != -1) {
    local_8 = param_1;
    if (((param_4 < 1) || (9 < param_4)) &&
       (iVar3 = FUN__text__00424f80("(1<=dir)&&(dir<=9)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitAnim.cpp",
                                    DAT_00610528 + 8,0), iVar3 != 0)) {
      pcVar2 = (code *)swi(3);
      (*pcVar2)();
      return;
    }
    *(undefined2 *)(param_2 + 0xc) = (undefined2)param_3;
    local_18 = (byte *)(*(int *)(local_8 + 0x4c) +
                       ((uint)(byte)(&DAT_00610510)[param_4] + param_3 * 8) * 2);
    uVar1 = *(ushort *)(*(int *)(local_8 + 0x50) + (uint)*local_18 * 2);
    _local_14 = CONCAT22(uStack_12,uVar1);
    local_c = (int)(uVar1 & 0xff00) >> 8;
    local_10 = uVar1 & 0xff;
    FUN__text__00409ff0(param_2,local_c,local_10,local_18[1] & 3);
  }
  local_8 = 0x465133;
  FUN__text__0056ce80();
  return;
}

