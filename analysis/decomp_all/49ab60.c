
void FUN__text__0049ab60(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 local_5c [16];
  undefined *local_1c;
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_5c;
  for (iVar3 = 0x16; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(int *)(param_1 + 0x25c) != 0) {
    iVar3 = FUN__text__0046a430(param_1);
    if ((iVar3 == 0) &&
       (iVar3 = FUN__text__00424f80("IsUwPlayer(wk)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlTalk.cpp",
                                    DAT_0061a400 + 0xb,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = *(int *)(param_1 + 0x25c);
    if ((int)*(char *)(param_1 + 0x290) == *(int *)(local_c + 0x80)) goto LAB__text__0049ac91;
    do {
      if ((*(int *)(local_8 + 0xdb80c) == 0) &&
         (iVar3 = FUN__text__00424f80("tFont!=0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlTalk.cpp",
                                      DAT_0061a400 + 0x11,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *(int *)(local_c + 0x80) = (int)*(char *)(param_1 + 0x290);
      local_1c = (&PTR_PTR_0061a2a4)[*(ushort *)(*(int *)(param_1 + 600) + 2)];
      FUN__text__00407780();
      uVar7 = 1;
      uVar6 = *(undefined4 *)(local_1c + *(int *)(local_c + 0x80) * 4);
      uVar5 = *(undefined4 *)(local_8 + 0xdb80c);
      uVar2 = FUN__text__004142b0(uVar5,uVar6,1);
      FUN__text__00408e30(uVar2,uVar5,uVar6,uVar7);
      FUN__text__0049ad90(param_1,*(undefined4 *)(local_c + 0x80));
LAB__text__0049ac91:
    } while (*(int *)(local_c + 0x2c) == 0);
    local_18 = (uint)*(byte *)(param_1 + 0x501);
    local_10 = (int)*(short *)(&DAT_00617ef0 + local_18 * 4);
    local_14 = (int)*(short *)(&DAT_00617ef2 + local_18 * 4);
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_c + 0x58) = 0;
    *(undefined4 *)(local_c + 0x5c) = 0;
    *(undefined2 *)(local_c + 0x76) = 0xd2;
    if ((int)local_18 < 10) {
      local_10 = local_10 + 0x36;
    }
    else {
      local_10 = local_10 - (*(short *)(local_c + 0x40) + 4);
    }
    local_14 = local_14 + 0x10;
  }
  local_8 = 0x49ad3b;
  FUN__text__0056ce80();
  return;
}

