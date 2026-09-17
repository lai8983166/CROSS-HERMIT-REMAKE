
void FUN__text__0049bd90(int param_1,byte param_2)

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
  iVar2 = FUN__text__0046a430(param_1);
  if (iVar2 != 0) {
    local_c = FUN__text__00427d60();
    if ((local_c == 0) &&
       (iVar2 = FUN__text__00424f80("list!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                    DAT_0061aff8 + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = *(undefined1 **)(local_c + 8);
    *local_10 = 0xd;
    local_10[1] = *(undefined1 *)(param_1 + 2);
    local_10[2] = 0xff;
    *(ushort *)(local_10 + 6) = (ushort)param_2;
    FUN__text__00427e30(local_c);
  }
  local_8 = 0x49be4b;
  FUN__text__0056ce80();
  return;
}

