
void __fastcall FUN__text__0049bb20(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined1 *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x108b54) == 1) {
    local_8 = param_1;
    for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
      iVar2 = FUN__text__0046a840(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
      if (iVar2 != 0) {
        local_10 = FUN__text__00427d60();
        if ((local_10 == 0) &&
           (iVar2 = FUN__text__00424f80("list!=0",
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                        DAT_0061aff4 + 0x13,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        local_14 = *(undefined1 **)(local_10 + 8);
        *local_14 = 5;
        local_14[1] = *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 2);
        local_14[2] = *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 2);
        FUN__text__00427e30(local_10);
      }
    }
  }
  local_8 = 0x49bc2c;
  FUN__text__0056ce80();
  return;
}

