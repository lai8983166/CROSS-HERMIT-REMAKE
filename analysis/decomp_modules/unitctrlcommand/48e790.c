
void FUN__text__0048e790(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00469480(param_1);
  if ((iVar2 == 0) && (iVar2 = FUN__text__004693b0(param_1), iVar2 == 0)) {
    if ((*(char *)(*(int *)(param_1 + 600) + 0x30) == '\x04') ||
       (iVar2 = FUN__text__0043be60(*(undefined1 *)(param_2 + 3),*(undefined1 *)(param_2 + 4),
                                    *(undefined1 *)(*(int *)(param_1 + 600) + 0x30)), iVar2 != 0)) {
      FUN__text__0046b0f0(param_1,1);
      FUN__text__0046b0b0(param_1,1);
      *(uint *)(param_1 + 0x2ec) = ((uint)*(byte *)(param_2 + 3) * 0x20 + 0x10) * 0x10000;
      *(uint *)(param_1 + 0x2f0) = ((uint)*(byte *)(param_2 + 4) * 0x10 + 8) * 0x10000;
      FUN__text__00475370(param_1,1,0xffffffff);
      *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 1;
      *(undefined1 *)(param_1 + 0x4e8) = 0xff;
      *(undefined1 *)(param_1 + 0x4e7) = 0xff;
      FUN__text__0042b2d0("ExecUnitComAppear():(wkno:%3d,(%03d,%03d),grp:%03d\n",
                          (int)*(short *)(param_1 + 2),*(undefined1 *)(param_2 + 3),
                          *(undefined1 *)(param_2 + 4),
                          *(undefined1 *)(*(int *)(param_1 + 600) + 0x98));
    }
    else {
      FUN__text__0042b2d0(&DAT_0059e418,*(undefined1 *)(param_2 + 3),*(undefined1 *)(param_2 + 4),
                          (int)*(short *)(param_1 + 2));
      local_c = FUN__text__0047fcf0((int)*(short *)(param_1 + 2),*(undefined1 *)(param_2 + 3),
                                    *(undefined1 *)(param_2 + 4),5);
      if ((local_c == 0) &&
         (iVar2 = FUN__text__00424f80(&DAT_0059e3b8,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                      DAT_00618fac + 0x10,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  local_8 = 0x48e980;
  FUN__text__0056ce80();
  return;
}

