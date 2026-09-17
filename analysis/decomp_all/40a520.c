
void FUN__text__0040a520(int param_1)

{
  code *pcVar1;
  undefined2 uVar2;
  ushort uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_84 [16];
  uint local_44;
  int local_40;
  undefined4 *local_3c;
  int local_38;
  undefined4 local_34;
  undefined4 *local_30;
  int local_2c;
  undefined4 local_28;
  ushort local_24;
  undefined2 uStack_22;
  int local_20;
  int local_1c;
  undefined4 local_18;
  undefined4 local_14;
  byte *local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar5 = local_84;
  for (iVar4 = 0x20; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  if ((*(int *)(param_1 + 4) != 0) &&
     ((*(int *)(param_1 + 0x2c) == 0 || (*(short *)(param_1 + 0x48) < 1)))) {
    local_c = CONCAT31(local_c._1_3_,**(byte **)(param_1 + 4)) & 0xffffff03;
    local_44 = **(byte **)(param_1 + 4) & 3;
    switch(local_44) {
    case 0:
      *(undefined4 *)(param_1 + 0x28) = *(undefined4 *)(param_1 + 4);
      local_10 = *(byte **)(param_1 + 0x28);
      uVar2 = FUN__text__00415070(*(undefined2 *)(local_10 + 8));
      *(undefined2 *)(param_1 + 0xe) = uVar2;
      if ((*local_10 & 4) != 0) {
        if ((*(int *)(param_1 + 0x24) == 0) &&
           (iVar4 = FUN__text__00424f80("aw->top!=0",
                                        "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                        DAT_005ff0fc + 0x19,0), iVar4 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        local_20 = *(int *)(param_1 + 0x24);
        *(undefined1 *)(local_20 + 9) = 1;
        if (*(int *)(param_1 + 0x2c) != 0) {
          local_28 = *(undefined4 *)(param_1 + 0x2c);
          local_2c = FUN__text__0040bd10();
          local_30 = *(undefined4 **)(local_2c + 8);
          *local_30 = *(undefined4 *)(param_1 + 0x48);
          local_30[1] = *(undefined4 *)(param_1 + 0x4c);
          local_30[2] = *(undefined4 *)(param_1 + 0x50);
          FUN__text__0040bd80(local_20,local_2c);
        }
      }
      if ((*local_10 & 8) != 0) {
        if ((*(int *)(param_1 + 0x24) == 0) &&
           (iVar4 = FUN__text__00424f80("aw->top!=0",
                                        "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                        DAT_005ff0fc + 0x29,0), iVar4 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        local_20 = *(int *)(param_1 + 0x24);
        *(undefined1 *)(local_20 + 10) = 1;
        if (*(int *)(param_1 + 0x2c) != 0) {
          local_34 = *(undefined4 *)(param_1 + 0x2c);
          local_38 = FUN__text__0040bd10();
          local_3c = *(undefined4 **)(local_38 + 8);
          *local_3c = *(undefined4 *)(param_1 + 0x48);
          local_3c[1] = *(undefined4 *)(param_1 + 0x4c);
          local_3c[2] = *(undefined4 *)(param_1 + 0x50);
          FUN__text__0040bdd0(local_20,local_38);
        }
      }
      if (((*(byte *)(param_1 + 3) & 0x40) != 0) || (*(char *)(param_1 + 8) == '\0')) {
        uVar3 = (ushort)local_10[2] | (*(ushort *)(local_10 + 6) & 0xf) << 8;
        _local_24 = CONCAT22(uStack_22,uVar3);
        if (uVar3 < 0xfff) {
          local_40 = FUN__text__00409fb0(param_1,uVar3);
          *(uint *)(param_1 + 0x18) = (uint)*(byte *)(local_40 + 8);
        }
      }
      break;
    case 1:
      local_14 = *(undefined4 *)(param_1 + 4);
      break;
    case 2:
      local_18 = *(undefined4 *)(param_1 + 4);
      break;
    case 3:
      if (*(short *)(param_1 + 0x10) == 0) {
        local_1c = *(int *)(param_1 + 4);
        if (*(char *)(local_1c + 1) == '\x7f') {
          *(ushort *)(param_1 + 0x10) = (ushort)*(byte *)(local_1c + 1);
        }
        else {
          *(ushort *)(param_1 + 0x10) = *(byte *)(local_1c + 1) + 1;
        }
      }
    }
  }
  local_8 = 0x40a7e0;
  FUN__text__0056ce80();
  return;
}

