
void FUN__text__0046db20(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_5c [16];
  uint local_1c;
  int local_18;
  uint local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar4 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if ((iVar2 != 0) && (iVar2 = FUN__text__0046a430(param_1), iVar2 != 0)) {
    local_18 = param_2;
    if (param_2 == 0) {
      if (*(char *)(param_1 + 0x501) == -1) goto LAB__text__0046df5c;
      if (*(char *)(local_8 + 0x108b48) == '\0') {
        FUN__text__0049ab60(param_1);
        FUN__text__0046e3d0(param_1);
      }
      local_14 = (uint)*(byte *)(param_1 + 0x501);
      local_c = *(short *)(&DAT_00617ef0 + local_14 * 4);
      local_10 = *(short *)(&DAT_00617ef2 + local_14 * 4);
      *(undefined2 *)(local_8 + 0xde5a6) = 499;
      *(undefined1 *)(local_8 + 0xde597) = 0xff;
      local_1c = (uint)*(byte *)(*(int *)(param_1 + 600) + 0xf);
      switch(local_1c) {
      case 0:
      case 2:
        if (*(char *)(param_1 + 0x28c) == '\0') {
          *(undefined1 *)(local_8 + 0xde596) = 0x40;
          *(undefined1 *)(local_8 + 0xde595) = 0x40;
          *(undefined1 *)(local_8 + 0xde594) = 0x40;
        }
        else {
          *(undefined1 *)(local_8 + 0xde596) = 0x60;
          *(undefined1 *)(local_8 + 0xde595) = 0x60;
          *(undefined1 *)(local_8 + 0xde594) = 0x60;
          FUN__text__00410680((int)local_c,(int)local_10,local_c + 0x31,local_10 + 0x2f,0x1f2,
                              0xffffff00,0);
          FUN__text__00410680(local_c + 1,local_10 + 1,local_c + 0x30,local_10 + 0x2e,0x1f2,
                              0xffffff00,0);
        }
        if (*(char *)(local_8 + 0x2f156) != '\0') {
          uVar3 = *(uint *)(DAT_007a49fc + 0xb310) & 0x8000000f;
          if ((int)uVar3 < 0) {
            uVar3 = (uVar3 - 1 | 0xfffffff0) + 1;
          }
          *(char *)(local_8 + 0xde596) = *(char *)(local_8 + 0xde596) + (char)uVar3;
          uVar3 = *(uint *)(DAT_007a49fc + 0xb310) & 0x8000000f;
          if ((int)uVar3 < 0) {
            uVar3 = (uVar3 - 1 | 0xfffffff0) + 1;
          }
          *(char *)(local_8 + 0xde595) = *(char *)(local_8 + 0xde595) + (char)uVar3;
          uVar3 = *(uint *)(DAT_007a49fc + 0xb310) & 0x8000000f;
          if ((int)uVar3 < 0) {
            uVar3 = (uVar3 - 1 | 0xfffffff0) + 1;
          }
          *(char *)(local_8 + 0xde594) = *(char *)(local_8 + 0xde594) + (char)uVar3;
        }
        break;
      case 1:
        if (*(char *)(param_1 + 0x28c) == '\0') {
          *(undefined1 *)(local_8 + 0xde596) = 0x80;
          *(undefined1 *)(local_8 + 0xde595) = 0x80;
          *(undefined1 *)(local_8 + 0xde594) = 0x80;
        }
        else {
          *(undefined1 *)(local_8 + 0xde596) = 0x90;
          *(undefined1 *)(local_8 + 0xde595) = 0x90;
          *(undefined1 *)(local_8 + 0xde594) = 0x90;
          FUN__text__00410680((int)local_c,(int)local_10,local_c + 0x31,local_10 + 0x2f,0x1f2,
                              0xff00ff00,0);
          FUN__text__00410680(local_c + 1,local_10 + 1,local_c + 0x30,local_10 + 0x2e,0x1f2,
                              0xff00ff00,0);
        }
        break;
      case 3:
        *(undefined1 *)(local_8 + 0xde596) = 0x80;
        *(undefined1 *)(local_8 + 0xde595) = 0;
        *(undefined1 *)(local_8 + 0xde594) = 0;
        break;
      case 4:
        *(undefined1 *)(local_8 + 0xde596) = 0x40;
        *(undefined1 *)(local_8 + 0xde595) = 0;
        *(undefined1 *)(local_8 + 0xde594) = 0;
        break;
      default:
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                    DAT_00618c28 + 0x4b,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
    }
    else {
      local_c = 0xd;
      local_10 = 0x272;
      *(undefined2 *)(local_8 + 0xde5a6) = 0xc3;
      *(undefined1 *)(local_8 + 0xde597) = 0xff;
      *(undefined1 *)(local_8 + 0xde596) = 0x80;
      *(undefined1 *)(local_8 + 0xde595) = 0x80;
      *(undefined1 *)(local_8 + 0xde594) = 0x80;
    }
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined4 *)(local_8 + 0xde58c) = 0;
    *(undefined2 *)(local_8 + 0xde588) = 0x80;
    FUN__text__00407870(0x5a,*(ushort *)(*(int *)(param_1 + 600) + 2) + 0x1e);
    FUN__text__004079c0((int)local_c,(int)local_10);
  }
LAB__text__0046df5c:
  local_8 = 0x46df69;
  FUN__text__0056ce80();
  return;
}

