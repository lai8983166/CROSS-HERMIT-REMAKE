
void FUN__text__00496e70(undefined4 param_1,undefined4 param_2)

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
  local_8 = FUN__text__0043bb90(param_1,param_2);
  if (((local_8 < 0) || (99 < local_8)) &&
     (iVar2 = FUN__text__00424f80("(0<=eno)&&(eno<100)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                  DAT_00619f8c + 4,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x496f0b;
  FUN__text__0056ce80();
  return;
}

