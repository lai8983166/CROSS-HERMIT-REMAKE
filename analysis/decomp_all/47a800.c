
void FUN__text__0047a800(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__004da7f0((int)DAT_007f4488);
  if (*(char *)(*(int *)(param_1 + 600) + 0xa2) == '\0') {
    iVar2 = FUN__text__00424f80(&DAT_0059d548,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e30 + 8,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__0042b2d0(&DAT_0059d520,(int)*(short *)(param_1 + 2),
                        *(undefined2 *)(*(int *)(param_1 + 600) + 2));
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xa2) = 1;
  }
  local_8 = 0x47a8cb;
  FUN__text__0056ce80();
  return;
}

