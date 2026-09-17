
void __thiscall FUN__text__00468690(int param_1,int param_2,short param_3,short param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_3 < 0) || (*(short *)(*(int *)(param_1 + 0x2a304) + 4) <= param_3)) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059c598,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b4c + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (((param_4 < 0) || (*(short *)(*(int *)(local_8 + 0x2a304) + 6) <= param_4)) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059c530,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b4c + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  *(int *)(param_2 + 0x2ec) = (param_3 * 0x20 + 0x10) * 0x10000;
  *(int *)(param_2 + 0x2f0) = (param_4 * 0x10 + 8) * 0x10000;
  if (*(char *)(*(int *)(param_2 + 600) + 0xf) == '\x01') {
    FUN__text__0043c470(*(undefined1 *)(param_2 + 0x4e7),*(undefined1 *)(param_2 + 0x4e8),0);
    FUN__text__0046b2c0(param_2);
    FUN__text__0043c470(*(undefined1 *)(param_2 + 0x4e7),*(undefined1 *)(param_2 + 0x4e8),1);
  }
  else {
    *(undefined1 *)(param_2 + 0x4e7) = 0xff;
    *(undefined1 *)(param_2 + 0x4e8) = 0xff;
  }
  local_8 = 0x4687ff;
  FUN__text__0056ce80();
  return;
}

