
void FUN__text__00492c20(int param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_b8 [16];
  byte local_78;
  undefined *local_74;
  undefined1 local_70 [4];
  undefined2 local_6c;
  int local_68;
  undefined2 local_62;
  undefined1 local_60 [44];
  undefined1 local_34 [44];
  undefined4 local_8;
  
  puVar3 = local_b8;
  for (iVar2 = 0x2d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),1);
  local_78 = *(byte *)(param_3 + 6);
  if (local_78 != 0) {
    if (local_78 < 4) {
      local_74 = &DAT_006c2dc8 + *(short *)(param_3 + 4) * 0x48;
      FUN__text__004deaa0(param_1,local_34);
      FUN__text__0046b3e0(param_1,local_34);
      FUN__text__004deaa0(param_2,local_60);
      FUN__text__0046b3e0(param_2,local_60);
      _memset(local_70,0,0x10);
      local_6c = *(undefined2 *)(param_3 + 4);
      local_68 = (uint)*(ushort *)(local_74 + 0x1c) +
                 ((uint)*(byte *)(*(int *)(param_1 + 600) + 6) * (uint)*(ushort *)(local_74 + 0x1e))
                 / 100;
      local_62 = 0;
      FUN__text__0048c850(0x41,7,0,local_70,param_1,param_2,local_34,local_60);
    }
    else if ((local_78 == 4) &&
            (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                         "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                         DAT_00619260 + 0x24,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x492d87;
  FUN__text__0056ce80();
  return;
}

