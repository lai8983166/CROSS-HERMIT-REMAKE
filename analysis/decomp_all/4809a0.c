
void FUN__text__004809a0(int param_1,undefined2 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined1 *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__00427d60();
  if (local_c == 0) {
    iVar2 = FUN__text__00424f80("lw!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618ea0 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = *(undefined1 **)(local_c + 8);
  *local_10 = 0xe;
  local_10[1] = *(undefined1 *)(param_1 + 2);
  local_10[2] = 0xff;
  *(undefined2 *)(local_10 + 6) = param_2;
  FUN__text__00427e30(local_c);
  FUN__text__0042b2d0(&DAT_0059d7dc);
  local_8 = 0x480a53;
  FUN__text__0056ce80();
  return;
}

