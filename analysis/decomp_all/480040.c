
void FUN__text__00480040(int param_1,int param_2,undefined1 param_3,undefined1 param_4)

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
  iVar2 = FUN__text__0046a120(param_2);
  if (((iVar2 != 0) && (iVar2 = FUN__text__00469480(param_2), iVar2 == 0)) &&
     (iVar2 = FUN__text__004695d0(param_2), iVar2 != 0)) {
    if (param_1 == 0) {
      local_c = FUN__text__00427d60();
      if ((local_c == 0) &&
         (iVar2 = FUN__text__00424f80("lw!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e94 + 0xc,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_10 = *(undefined1 **)(local_c + 8);
      *local_10 = 4;
      local_10[1] = *(undefined1 *)(param_2 + 2);
      local_10[2] = *(undefined1 *)(param_2 + 2);
      local_10[3] = param_3;
      local_10[4] = param_4;
      FUN__text__00427e30(local_c);
    }
    else {
      local_c = FUN__text__00427d60();
      if ((local_c == 0) &&
         (iVar2 = FUN__text__00424f80("lw!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e94 + 0x19,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_10 = *(undefined1 **)(local_c + 8);
      *local_10 = 4;
      local_10[1] = *(undefined1 *)(param_2 + 2);
      local_10[2] = *(undefined1 *)(param_2 + 2);
      local_10[3] = param_3;
      local_10[4] = param_4;
      FUN__text__00427e30(local_c);
    }
  }
  local_8 = 0x4801cf;
  FUN__text__0056ce80();
  return;
}

