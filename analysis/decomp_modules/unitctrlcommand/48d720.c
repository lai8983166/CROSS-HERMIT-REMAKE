
void __thiscall FUN__text__0048d720(int param_1,int param_2,undefined1 param_3)

{
  code *pcVar1;
  ushort uVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_70 [16];
  int local_30;
  undefined2 local_2c;
  undefined2 local_28;
  short local_24;
  short local_20;
  int local_1c;
  int local_18;
  uint local_14;
  undefined1 *local_10;
  int local_c;
  int local_8;
  
  puVar6 = local_70;
  for (iVar5 = 0x1b; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  if (((((*(char *)(param_1 + 0x108b35) == '\0') ||
        (local_8 = param_1, iVar5 = FUN__text__00469b90(param_2), iVar5 != 0)) ||
       (iVar5 = FUN__text__00469c60(param_2), iVar5 != 0)) ||
      ((*(char *)(local_8 + 0x3098c) == '\0' || (iVar5 = FUN__text__004690a0(param_2), iVar5 != 0)))
      ) || ((iVar5 = FUN__text__00469480(param_2), iVar5 == 0 ||
            ((iVar5 = FUN__text__0046a430(param_2), iVar5 == 0 ||
             (iVar5 = FUN__text__00469660(param_2), iVar5 == 0)))))) goto LAB__text__0048dc2d;
  if ((*(char *)(local_8 + 0x2f156) != '\0') &&
     (((*(char *)(local_8 + 0x3098d) == '\x01' && (*(short *)(local_8 + 0x30992) != -1)) &&
      (local_1c = local_8 + 0x80aec + *(short *)(local_8 + 0x30992) * 0x520,
      *(short *)(local_1c + 2) == *(short *)(param_2 + 2))))) {
    FUN__text__004812c0(param_2);
    FUN__text__004815c0();
    goto LAB__text__0048dc2d;
  }
  if (*(char *)(param_2 + 0x28c) == '\0') goto LAB__text__0048dc2d;
  uVar2 = FUN__text__0046c350(param_2,0);
  local_14 = CONCAT22(local_14._2_2_,uVar2);
  if ((uVar2 == 0xffff) || ((uVar2 & 0x8000) != 0)) goto LAB__text__0048dc2d;
  local_18 = FUN__text__0046c480(param_2,uVar2,(int)*(char *)(local_8 + 0x3098d));
  local_30 = local_18 + -1;
  switch(local_18) {
  case 1:
    break;
  case 2:
  case 4:
    iVar5 = FUN__text__0046a6a0(local_8 + 0x80aec + *(short *)(local_8 + 0x30992) * 0x520);
    if (iVar5 == 0) goto LAB__text__0048dc2d;
    iVar5 = *(int *)(local_8 + 0x80dd8 + *(short *)(local_8 + 0x30992) * 0x520);
    uVar3 = (int)((iVar5 >> 0x10) + (iVar5 >> 0x1f & 0x1fU)) >> 5;
    local_28 = (undefined2)uVar3;
    iVar5 = *(int *)(local_8 + 0x80ddc + *(short *)(local_8 + 0x30992) * 0x520);
    uVar4 = (int)((iVar5 >> 0x10) + (iVar5 >> 0x1f & 0xfU)) >> 4;
    local_2c = (undefined2)uVar4;
    iVar5 = FUN__text__0047e460(param_2,uVar3 & 0xffff,uVar4 & 0xffff);
    if (iVar5 == 0) goto switchD__text__0048d8e8_caseD_6e;
    break;
  case 3:
    break;
  default:
    goto LAB__text__0048dc2d;
  case 100:
    iVar5 = FUN__text__0046c930(param_2,local_14 & 0xffff);
    if (iVar5 != 0) {
      local_c = FUN__text__00427d60();
      if ((local_c == 0) &&
         (iVar5 = FUN__text__00424f80("lw!=0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                      DAT_00618f98 + 0x53,0), iVar5 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_10 = *(undefined1 **)(local_c + 8);
      *local_10 = 3;
      local_10[1] = param_3;
      local_10[2] = param_3;
      *(ushort *)(local_10 + 6) = (ushort)(byte)local_14;
      local_10[3] = *(undefined1 *)(local_8 + 0x3098e);
      local_10[4] = *(undefined1 *)(local_8 + 0x30990);
      FUN__text__00427e30(local_c);
      FUN__text__0048f100(param_2);
    }
    goto LAB__text__0048dc2d;
  case 0x6e:
switchD__text__0048d8e8_caseD_6e:
    local_20 = (short)((int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                            (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_24 = (short)((int)((*(int *)(param_2 + 0x2f0) >> 0x10) +
                            (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    if ((local_20 != *(short *)(local_8 + 0x3098e)) || (local_24 != *(short *)(local_8 + 0x30990)))
    {
      local_c = FUN__text__00427d60();
      if ((local_c == 0) &&
         (iVar5 = FUN__text__00424f80("lw!=0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                      DAT_00618f98 + 0x72,0), iVar5 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_10 = *(undefined1 **)(local_c + 8);
      *local_10 = 1;
      local_10[1] = param_3;
      local_10[2] = 0xff;
      local_10[3] = *(undefined1 *)(local_8 + 0x3098e);
      local_10[4] = *(undefined1 *)(local_8 + 0x30990);
      FUN__text__00427e30(local_c);
      FUN__text__0048f100(param_2);
    }
    goto LAB__text__0048dc2d;
  }
  iVar5 = FUN__text__0046c930(param_2,local_14 & 0xffff);
  if (iVar5 != 0) {
    local_c = FUN__text__00427d60();
    if ((local_c == 0) &&
       (iVar5 = FUN__text__00424f80("lw!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618f98 + 0x99,0), iVar5 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = *(undefined1 **)(local_c + 8);
    *local_10 = 3;
    local_10[1] = param_3;
    local_10[2] = *(undefined1 *)(local_8 + 0x30992);
    *(undefined2 *)(local_10 + 6) = (undefined2)local_14;
    local_10[3] = *(undefined1 *)(local_8 + 0x3098e);
    local_10[4] = *(undefined1 *)(local_8 + 0x30990);
    FUN__text__00427e30(local_c);
    FUN__text__0048f100(param_2);
  }
LAB__text__0048dc2d:
  local_8 = 0x48dc3a;
  FUN__text__0056ce80();
  return;
}

